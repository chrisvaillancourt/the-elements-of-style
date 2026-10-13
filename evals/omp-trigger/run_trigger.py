"""Trigger test for writing-clearly-and-concisely in omp.

Usage: run_trigger.py <trigger-dir> <reps> <workers> [variants, default old,new]
Runs every case x variant (old/new) x effort (low/medium) x rep through
`omp -p --mode json` with HOME pointed at an isolated home holding that
variant, and records whether the agent read the skill. Results append to
<trigger-dir>/results.jsonl; finished runs are skipped on rerun.
"""

import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

root = Path(sys.argv[1])
reps, workers = int(sys.argv[2]), int(sys.argv[3])
variants = (sys.argv[4] if len(sys.argv) > 4 else "old,new").split(",")
cases = json.loads((root / "cases.json").read_text())
model = "openai-codex/gpt-6.1-sol"
skill = "writing-clearly-and-concisely"
results_path = root / "results.jsonl"
done = set()
if results_path.exists():
    for line in results_path.read_text().splitlines():
        r = json.loads(line)
        if r.get("exit") == 0:
            done.add(r["run_id"])

jobs = [
    (variant, effort, case, rep)
    for rep in range(1, reps + 1)
    for effort in ("low", "medium")
    for variant in variants
    for case in cases
]


def run(variant, effort, case, rep):
    run_id = f"{variant}-{effort}-{case['id']}-r{rep}"
    if run_id in done:
        return None
    rdir = root / "runs" / run_id
    if rdir.exists():
        shutil.rmtree(rdir)
    ws = rdir / "ws"
    shutil.copytree(root / "fixture", ws)
    (rdir / "prompt.md").write_text(case["prompt"])
    cmd = [
        "omp", "-p", "--mode", "json", "--no-session",
        "--cwd", str(ws), "--model", model, "--thinking", effort,
        "--max-time", "4m", f"@{rdir / 'prompt.md'}",
    ]
    env = {**__import__("os").environ, "HOME": str(root / f"home-{variant}")}
    start = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ws, env=env, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=330)
        code, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = "timeout", (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    elapsed = round(time.time() - start, 1)
    (rdir / "events.jsonl").write_text(out)
    (rdir / "stderr.txt").write_text(err)

    tools, skill_reads, ref_reads, inp, cached, outp, cost = [], [], [], 0, 0, 0, 0.0
    final = ""
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "tool_execution_start":
            args = json.dumps(ev.get("args", {}))
            tools.append(ev.get("toolName"))
            if skill in args:
                skill_reads.append(args[:200])
                if "references/" in args or "elements-of-style.md" in args:
                    ref_reads.append(args[:200])
        if ev.get("type") == "message_end":
            msg = ev.get("message") or {}
            u = msg.get("usage") or {}
            inp += u.get("input", 0); cached += u.get("cacheRead", 0); outp += u.get("output", 0)
            cost += (u.get("cost") or {}).get("total", 0)
            if msg.get("role") == "assistant":
                text = [c.get("text", "") for c in msg.get("content", []) if isinstance(c, dict) and c.get("type") == "text"]
                if any(text):
                    final = "\n".join(text)
    return {
        "run_id": run_id, "variant": variant, "effort": effort, "case": case["id"],
        "rep": rep, "expect": case["expect"], "activated": bool(skill_reads),
        "ref_reads": len(ref_reads), "tools": tools, "exit": code, "seconds": elapsed,
        "input": inp, "cache_read": cached, "output": outp, "cost": round(cost, 5),
        "final": final[:600],
    }


with ThreadPoolExecutor(max_workers=workers) as pool, results_path.open("a") as fh:
    futures = [pool.submit(run, *j) for j in jobs]
    n = 0
    for fut in as_completed(futures):
        r = fut.result()
        if r is None:
            continue
        fh.write(json.dumps(r) + "\n"); fh.flush()
        n += 1
        print(f"{n}/{len(jobs)} {r['run_id']} activated={r['activated']} exit={r['exit']} {r['seconds']}s", flush=True)
