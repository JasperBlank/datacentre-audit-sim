"""Model calls with a disk cache. Providers: anthropic (API key), openrouter, claude-cli (Claude subscription),
codex-cli (ChatGPT subscription, through OpenAI's `codex exec`)."""
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time


def subscription_env():
    """Environment for `claude -p` without API keys, so it uses the subscription login, never API billing."""
    env = dict(os.environ)
    for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL",
              "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY"):
        env.pop(k, None)
    return env


def check_claude_cli():
    exe = shutil.which("claude")
    if not exe:
        sys.exit("`claude` not found. Install Claude Code and log in with your Claude account first.")
    run_ = lambda *a: subprocess.run([exe] + list(a), capture_output=True, text=True, encoding="utf-8",
                                     env=subscription_env(), timeout=60)
    version = (run_("--version").stdout.split() or ["?"])[0]
    if "--safe-mode" not in run_("--help").stdout:
        sys.exit("Claude Code %s is too old for this script (no --safe-mode). Run `claude update`." % version)
    try:
        status = json.loads(run_("auth", "status").stdout)
    except ValueError:
        sys.exit("Couldn't read `claude auth status`. Run `claude update`, then try again.")
    method = status.get("authMethod")
    if method not in ("claude.ai", "oauth_token"):
        sys.exit("Claude Code isn't logged in with a Claude subscription (authMethod=%s). Run `claude`, "
                 "then /login and choose your Claude account." % method)
    print("Claude Code %s, logged in with a Claude subscription. API keys are removed for these calls." % version)


def chatgpt_env():
    """Environment for `codex exec` without API keys, so it uses the ChatGPT login, never API billing."""
    env = dict(os.environ)
    for k in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "CODEX_API_KEY"):
        env.pop(k, None)
    return env


def check_codex_cli():
    exe = shutil.which("codex")
    if not exe:
        sys.exit("`codex` not found. Install it with `npm install -g @openai/codex` and log in with your ChatGPT account.")
    run_ = lambda *a: subprocess.run([exe] + list(a), capture_output=True, text=True, encoding="utf-8",
                                     env=chatgpt_env(), timeout=60)
    version = (run_("--version").stdout.split() or ["?"])[-1]
    status = run_("login", "status")
    if "ChatGPT" not in status.stdout + status.stderr:
        sys.exit("Codex isn't logged in with a ChatGPT account. Run `codex login`.")
    print("Codex CLI %s, logged in with ChatGPT. API keys are removed for these calls." % version)


# Codex is a coding agent with a shell. The detective must answer from its prompt alone: a call in which the
# model ran a command, read a file or searched the web is thrown away, because the truth is in world.py on this disk.
CODEX_NO_TOOLS = ("\n\nAnswer from the text of this message only. Do not run commands, read or write files, "
                  "search the web or use any other tool.")
CODEX_TOOL_ITEMS = ("command_execution", "file_change", "mcp_tool_call", "web_search", "patch_apply", "exec_command")


class Blocked(RuntimeError):
    """The provider's safety filter rejected the message. Not retried: the same message is rejected again."""


class Client:
    def __init__(self, provider, results_dir, dry_run=False, max_cost=None, fake=None):
        self.provider, self.dry_run, self.max_cost, self.fake = provider, dry_run, max_cost, fake
        self.cost, self.calls, self.models_seen = 0.0, 0, set()
        self.usage = {"input": 0, "output": 0}
        self.lock = threading.Lock()
        self.tl = threading.local()   # per-thread count of safety-filter rejections
        os.makedirs(results_dir, exist_ok=True)
        self.cache_path = os.path.join(results_dir, "cache.jsonl")
        self.cache = {}
        if os.path.exists(self.cache_path):
            for line in open(self.cache_path, encoding="utf-8"):
                try:
                    row = json.loads(line)
                    self.cache[row["key"]] = row["text"]
                except Exception:
                    pass
        if provider == "claude-cli" and not dry_run:
            self.claude = shutil.which("claude")
            self.workdir = tempfile.mkdtemp(prefix="dc-sim-")   # empty folder: no project settings picked up
            self.prompt_files = {}
        if provider == "codex-cli" and not dry_run:
            self.codex = shutil.which("codex")
            self.workdir = tempfile.mkdtemp(prefix="dc-sim-")   # empty folder: nothing for the agent to find
            self.tool_use = 0                                    # calls thrown away because the model used a tool

    def complete(self, model, system, user, rep=0, max_tokens=1500):
        key = hashlib.sha256(json.dumps([self.provider, self.dry_run, model, system, user, rep]).encode()).hexdigest()
        if key in self.cache:
            return self.cache[key]
        text = self.fake(system, user, rep) if self.dry_run else self._call(model, system, user, max_tokens)
        with self.lock:
            self.cache[key] = text
            with open(self.cache_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"key": key, "text": text}) + "\n")
            self.calls += 1
        return text

    def _system_file(self, system):
        with self.lock:
            if system not in self.prompt_files:
                path = os.path.join(self.workdir, "system_%d.txt" % len(self.prompt_files))
                with open(path, "w", encoding="utf-8") as f:
                    f.write(system)
                self.prompt_files[system] = path
            return self.prompt_files[system]

    def _call_cli(self, model, system, user):
        cmd = [self.claude, "-p", "--safe-mode", "--model", model, "--system-prompt-file", self._system_file(system),
               "--tools", "", "--no-session-persistence", "--output-format", "json"]
        last, rejected_here = "", 0
        for attempt in range(8):
            if self.max_cost and self.cost >= self.max_cost:
                raise RuntimeError("Stopped: estimated cost reached --max-cost %.2f USD. Rerun with a higher "
                                   "--max-cost to continue; finished calls are cached." % self.max_cost)
            try:
                p = subprocess.run(cmd, input=user, capture_output=True, text=True, encoding="utf-8",
                                   cwd=self.workdir, env=subscription_env(), timeout=600)
            except subprocess.TimeoutExpired:
                last = "timeout"
                time.sleep(2 ** attempt + random.random())
                continue
            try:
                body = json.loads(p.stdout)
            except ValueError:
                body = {}
            if p.returncode == 0 and body.get("type") == "result" and not body.get("is_error"):
                u = body.get("usage", {}) or {}
                with self.lock:
                    self.usage["input"] += (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                                            + u.get("cache_creation_input_tokens", 0))
                    self.usage["output"] += u.get("output_tokens", 0)
                    self.cost += body.get("total_cost_usd", 0) or 0
                    self.models_seen.update((body.get("modelUsage") or {}).keys())
                return body.get("result", "")
            last = (body.get("result") or p.stderr or p.stdout or "")[:300]
            if re.search(r"rate.?limit|overloaded|429|529|5\d\d|timeout|ECONN", last, re.I):
                time.sleep(2 ** attempt * 3 + random.random())
                continue
            if "safeguards flagged" in last:
                # The filter is random on a fixed message (2 of 10 in test_filter.py), so try up to 3 times.
                self.tl.rejections = getattr(self.tl, "rejections", 0) + 1
                rejected_here += 1
                if rejected_here < 3:
                    continue
                raise Blocked(last)
            raise RuntimeError("claude -p failed (exit %s): %s" % (p.returncode, last))
        raise RuntimeError("claude -p failed after retries: %s" % last)

    def _call_codex(self, model, system, user):
        """One reply from `codex exec`. Codex has no system-prompt flag, so the system text leads the message."""
        last = ""
        for attempt in range(6):
            if self.max_cost and self.calls >= self.max_cost * 20:     # no USD figure on a subscription: cap the calls
                raise RuntimeError("Stopped: %d calls, the limit --max-cost %.0f allows (20 calls per unit)."
                                   % (self.calls, self.max_cost))
            out = os.path.join(self.workdir, "reply_%d_%d.txt" % (threading.get_ident(), random.randrange(10 ** 9)))
            cmd = [self.codex, "exec", "--skip-git-repo-check", "--ephemeral", "--disable", "memories",
                   "-s", "read-only", "-m", model, "--json", "-o", out, "-"]
            try:
                p = subprocess.run(cmd, input=system + CODEX_NO_TOOLS + "\n\n-----\n\n" + user, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", cwd=self.workdir, env=chatgpt_env(),
                                   timeout=900)
            except subprocess.TimeoutExpired:
                last = "timeout"
                time.sleep(2 ** attempt + random.random())
                continue
            events = []
            for line in p.stdout.splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
            items = [e.get("item", {}).get("type") for e in events if e.get("type", "").startswith("item.")]
            failed = [json.dumps(e)[:400] for e in events if e.get("type") in ("error", "turn.failed")]
            reply = open(out, encoding="utf-8").read().strip() if os.path.exists(out) else ""
            if any(t in CODEX_TOOL_ITEMS for t in items):
                with self.lock:
                    self.tool_use += 1
                last = "the model used a tool (%s); reply thrown away" % ", ".join(sorted({t for t in items if t in CODEX_TOOL_ITEMS}))
                continue
            if reply and not failed:
                for e in events:
                    u = e.get("usage") if e.get("type") == "turn.completed" else None
                    if u:
                        with self.lock:
                            self.usage["input"] += u.get("input_tokens", 0)
                            self.usage["output"] += u.get("output_tokens", 0)
                self.models_seen.add(model)
                return reply
            last = (failed[-1] if failed else p.stderr or p.stdout or "")[:400]
            if re.search(r"newer version|not supported|model_not_found|not logged in", last, re.I):
                raise RuntimeError("codex exec refused: %s" % last)
            if re.search(r"usage limit|quota", last, re.I):
                raise RuntimeError("ChatGPT usage limit reached: %s" % last)
            if re.search(r"policy|safety|flagged|cyber", last, re.I):
                self.tl.rejections = getattr(self.tl, "rejections", 0) + 1
                raise Blocked(last)
            time.sleep(2 ** attempt * 2 + random.random())
        raise RuntimeError("codex exec failed after retries: %s" % last)

    def _call(self, model, system, user, max_tokens):
        if self.provider == "claude-cli":
            return self._call_cli(model, system, user)
        if self.provider == "codex-cli":
            return self._call_codex(model, system, user)
        import requests
        for attempt in range(6):
            try:
                if self.provider == "anthropic":
                    r = requests.post("https://api.anthropic.com/v1/messages",
                                      headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                                               "anthropic-version": "2023-06-01", "content-type": "application/json"},
                                      json={"model": model, "max_tokens": max_tokens, "system": system,
                                            "messages": [{"role": "user", "content": user}]}, timeout=300)
                    if r.status_code == 200:
                        body = r.json()
                        u = body.get("usage", {})
                        with self.lock:
                            self.usage["input"] += u.get("input_tokens", 0)
                            self.usage["output"] += u.get("output_tokens", 0)
                        return "".join(b.get("text", "") for b in body["content"] if b.get("type") == "text")
                else:
                    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                      headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]},
                                      json={"model": model, "max_tokens": max_tokens,
                                            "messages": [{"role": "system", "content": system},
                                                         {"role": "user", "content": user}]}, timeout=300)
                    if r.status_code == 200:
                        body = r.json()
                        u = body.get("usage", {}) or {}
                        with self.lock:
                            self.usage["input"] += u.get("prompt_tokens", 0)
                            self.usage["output"] += u.get("completion_tokens", 0)
                        return body["choices"][0]["message"]["content"]
                if r.status_code in (429, 500, 502, 503, 529):
                    time.sleep(2 ** attempt + random.random())
                    continue
                raise RuntimeError("API error %s: %s" % (r.status_code, r.text[:300]))
            except requests.RequestException:
                time.sleep(2 ** attempt + random.random())
        raise RuntimeError("API failed after retries")
