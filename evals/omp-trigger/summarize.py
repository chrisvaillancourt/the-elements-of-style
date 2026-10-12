"""Summarize results.jsonl from run_trigger.py. Usage: summarize.py <trigger-dir>"""

import json
import sys
from collections import defaultdict
from pathlib import Path

rows = [json.loads(l) for l in (Path(sys.argv[1]) / "results.jsonl").read_text().splitlines()]
rows = [r for r in rows if r["exit"] == 0]
by_cond = defaultdict(list)
for r in rows:
    by_cond[(r["variant"], r["effort"])].append(r)

print("variant effort  n  TPR    TNR    bal.acc  refs/activation  mean_input  mean_cost  mean_s")
for (v, e), rs in sorted(by_cond.items()):
    pos = [r for r in rs if r["expect"]]
    neg = [r for r in rs if not r["expect"]]
    tpr = sum(r["activated"] for r in pos) / len(pos)
    tnr = sum(not r["activated"] for r in neg) / len(neg)
    act = [r for r in rs if r["activated"]]
    refs = sum(r["ref_reads"] > 0 for r in act) / len(act) if act else 0
    mi = sum(r["input"] + r["cache_read"] for r in rs) / len(rs)
    mc = sum(r["cost"] for r in rs) / len(rs)
    ms = sum(r["seconds"] for r in rs) / len(rs)
    print(f"{v:7} {e:6} {len(rs):3}  {tpr:.2f}   {tnr:.2f}   {(tpr + tnr) / 2:.2f}     {refs:.2f}             {mi:8.0f}    {mc:.4f}    {ms:.1f}")

print("\nActivated runs, input+cached tokens (mean) by variant:")
for v in ("old", "new"):
    act = [r for r in rows if r["variant"] == v and r["activated"]]
    if act:
        print(f"  {v}: {sum(r['input'] + r['cache_read'] for r in act) / len(act):.0f} tokens, "
              f"{sum(r['seconds'] for r in act) / len(act):.1f}s over {len(act)} runs")

print("\nPer case: activations / runs  (old-low old-med new-low new-med)")
cases = sorted({r["case"] for r in rows})
for c in cases:
    cells = []
    for v in ("old", "new"):
        for e in ("low", "medium"):
            rs = [r for r in rows if r["case"] == c and r["variant"] == v and r["effort"] == e]
            cells.append(f"{sum(r['activated'] for r in rs)}/{len(rs)}")
    print(f"  {c:20} " + "  ".join(f"{x:>4}" for x in cells))

failed = [json.loads(l) for l in (Path(sys.argv[1]) / "results.jsonl").read_text().splitlines()]
failed = [r["run_id"] for r in failed if r["exit"] != 0]
print(f"\nNon-zero exits: {len(failed)} {failed[:10]}")
