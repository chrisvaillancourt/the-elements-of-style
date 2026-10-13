"""Meaning-preservation runs: 3 drafts x {none, old, new} x {claude, omp} x reps.

Usage: meaning_run.py <meaning-dir> <omp-homes-dir> <reps>
Writes <meaning-dir>/results.jsonl with the output text, which skill (if any)
the agent loaded, and reference reads.
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root, homes, reps = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
cases = json.loads((root / "cases.json").read_text())
SKILL = "writing-clearly-and-concisely"


def prompt_for(case, harness, cond):
    if harness == "claude" and cond in ("old", "new"):
        hint = f"Use the wcc-{cond}:{SKILL} skill."
    else:
        hint = f"Use your {SKILL} skill if you have one."
    return f'{case["task"]} {hint}\n\n"{case["draft"]}"'


def run(case, harness, cond, rep):
    run_id = f"{harness}-{cond}-{case['id']}-r{rep}"
    rdir = root / "runs" / run_id
    ws = rdir / "ws"
    ws.mkdir(parents=True, exist_ok=True)
    (rdir / "prompt.md").write_text(prompt_for(case, harness, cond))
    env = dict(os.environ)
    if harness == "claude":
        cmd = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--no-session-persistence"]
        cmd += ["--disable-slash-commands"] if cond == "none" else ["--plugin-dir", str(root / f"plug-{cond}")]
        cmd += [(rdir / "prompt.md").read_text()]
    else:
        env["HOME"] = str(root / "home-none" if cond == "none" else homes / f"home-{cond}")
        cmd = ["omp", "-p", "--mode", "json", "--no-session", "--cwd", str(ws),
               "--model", "openai-codex/gpt-6.1-sol", "--thinking", "medium",
               "--max-time", "4m", f"@{rdir / 'prompt.md'}"]
    proc = subprocess.run(cmd, cwd=ws, env=env, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=330)
    (rdir / "events.jsonl").write_text(proc.stdout)
    (rdir / "stderr.txt").write_text(proc.stderr)
    skills, refs, final, model = [], 0, "", None
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if harness == "claude":
            if ev.get("type") == "system" and ev.get("subtype") == "init":
                model = ev.get("model")
            if ev.get("type") == "assistant":
                for c in ev["message"].get("content", []):
                    if c.get("type") == "tool_use":
                        args = json.dumps(c.get("input", {}))
                        if c.get("name") == "Skill":
                            skills.append(c["input"].get("skill"))
                        if "references/" in args or "elements-of-style.md" in args:
                            refs += 1
            if ev.get("type") == "result":
                final = ev.get("result") or ""
        else:
            if ev.get("type") == "tool_execution_start":
                args = json.dumps(ev.get("args", {}))
                if SKILL in args and "skill://" in args and "references" not in args and "elements-of-style.md" not in args:
                    skills.append("skill://" + SKILL)
                if "references/" in args or "elements-of-style.md" in args:
                    refs += 1
            if ev.get("type") == "message_end":
                msg = ev.get("message") or {}
                if msg.get("role") == "assistant":
                    text = [c.get("text", "") for c in msg.get("content", []) if isinstance(c, dict) and c.get("type") == "text"]
                    if any(text):
                        final = "\n".join(text)
                model = model or msg.get("model")
    return {"run_id": run_id, "case": case["id"], "harness": harness, "cond": cond, "rep": rep,
            "exit": proc.returncode, "skills": skills, "ref_reads": refs, "model": model, "final": final.strip()}


jobs = [(c, h, cond, r) for r in range(1, reps + 1) for h in ("claude", "omp")
        for cond in ("none", "old", "new") for c in cases]
with ThreadPoolExecutor(max_workers=6) as pool, (root / "results.jsonl").open("w") as fh:
    for res in pool.map(lambda j: run(*j), jobs):
        fh.write(json.dumps(res) + "\n"); fh.flush()
        print(res["run_id"], res["exit"], res["skills"], res["ref_reads"], flush=True)
