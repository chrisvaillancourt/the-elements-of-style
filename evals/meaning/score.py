"""Score meaning-run outputs against cases.json checks. Usage: score.py <meaning-dir> [results file, default results.jsonl]"""
import json, sys
from collections import defaultdict
root = sys.argv[1]
norm = lambda s: s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
cases = {c["id"]: c for c in json.load(open(f"{root}/cases.json"))}
rows = [json.loads(l) for l in open(sys.argv[2] if len(sys.argv) > 2 else f"{root}/results.jsonl")]
fails = defaultdict(list); totals = defaultdict(lambda: [0, 0])
for r in rows:
    t = norm(r["final"])
    for chk in cases[r["case"]]["checks"]:
        ok = True
        if "any" in chk: ok &= any(s in t for s in chk["any"])
        if "all" in chk: ok &= all(s in t for s in chk["all"])
        if "none" in chk: ok &= not any(s in t for s in chk["none"])
        k = (r["harness"], r["cond"]); totals[k][1] += 1; totals[k][0] += ok
        if not ok: fails[k].append(f'{r["case"]}-r{r["rep"]}: {chk["name"]}')
for k in sorted(totals):
    print(f"{k[0]:6} {k[1]:4} {totals[k][0]}/{totals[k][1]} checks passed")
    for f in fails[k]: print("     FAIL", f)
