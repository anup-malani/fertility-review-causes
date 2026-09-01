#!/usr/bin/env python3
"""279 — C.3.e query repair, one candidate term at a time. TICK-077.

278 recalled 6 of 23 gold. Reading the missed records (rather than widening on a hunch)
separated two very different causes:

  (a) REAL QUERY FAILURES. The record is on-estimand and the query's vocabulary misses it.
      Pitt 1999 calls the exposure a "credit program" and the outcome "reproductive
      behavior"; Cain 1981 calls the outcome "derived demand for children"; the Baby Boom
      paper's abstract never says fertility at all, only "baby boom". A sub-literature
      renaming the outcome is the A.18 failure exactly, and it is repairable.

  (b) NOT FAILURES AT ALL. The microcredit RCTs, the branch-expansion studies and the
      savings-access experiments do not mention fertility in their abstracts because they
      do not measure it. That is the composite stratum's answer, not the query's fault,
      and widening the query cannot fix it -- it can only hide it.

So every candidate term below is scored on GOLD RECOVERED, not on frame growth. A term
that adds records and no gold is refused: frame growth is not frame gain.

Usage: python3 279_c3e_query_repair.py
"""
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")


def q(params):
    args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works"]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}",
             "--data-urlencode", "mailto=shravanh@uchicago.edu"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, "non-JSON body"
    if "meta" not in d or d["meta"].get("count") is None:
        return None, (d.get("message") or "refused")[:100]
    return d, None


def phrase(p):
    assert not p.lower().startswith("not "), p
    assert "?" not in p and "!" not in p and "," not in p, p
    return f'"{p}"'


def blk(t):
    return "(" + " OR ".join(phrase(x) for x in t) + ")"


base = json.loads((LOGS / "credit-constraints-production-query.json").read_text())
OUTCOME = base["outcome_axis"]
EXPOSURE = base["exposure_axes"]
anchors = json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())
ids = {a["key"]: a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
role = {a["key"]: a.get("role", "anchor") for a in anchors}
gold = {k: v for k, v in ids.items() if role[k] != "decoy"}

OUTCOME_ADD = ["demand for children", "reproductive behavior", "reproductive behaviour",
               "baby boom", "total fertility rate", "number of births", "fertility decline"]
EXPO_ADD = {
    "S": ["old age support", "children as security", "insurance mechanism",
          "security motive", "risk coping"],
    "B": ["housing loan", "housing finance", "provident fund", "uninsurable",
          "mortgage", "credit rationing"],
    "composite": ["credit program", "credit programme", "group lending",
                  "group-based lending", "joint liability", "rural bank",
                  "branch expansion", "bank expansion"],
}


def recalled(filter_str, want):
    hit = set()
    keys = list(want)
    for i in range(0, len(keys), 40):
        b = keys[i:i + 40]
        d, err = q([("filter", "openalex_id:" + "|".join(want[k] for k in b) + "," + filter_str),
                    ("per-page", "40"), ("select", "id")])
        if err:
            raise SystemExit(err)
        got = {w["id"].rsplit("/", 1)[-1] for w in d["results"]}
        hit |= {k for k in b if want[k] in got}
    return hit


def count(filter_str):
    d, err = q([("filter", filter_str), ("per-page", "1"), ("select", "id")])
    return None if err else d["meta"]["count"]


def frame(expo, out):
    return f"title_and_abstract.search:{blk(expo)} AND {blk(out)}"


out = {"outcome_additions": [], "exposure_additions": {}}
allexpo = [t for v in EXPOSURE.values() for t in v]
base_f = frame(allexpo, OUTCOME)
base_hit = recalled(base_f, gold)
base_n = count(base_f)
print(f"BASELINE union query: frame {base_n}, gold {len(base_hit)}/{len(gold)}")
print(f"  missing: {', '.join(sorted(set(gold) - base_hit))}\n")

print("OUTCOME AXIS candidates (gold recovered / frame added):")
keep_out = list(OUTCOME)
cur_hit, cur_n = base_hit, base_n          # MUST advance with each acceptance: comparing
                                           # a growing kept-set against a frozen baseline
                                           # credits later terms with earlier terms' gold.
for t in OUTCOME_ADD:
    f2 = frame(allexpo, keep_out + [t])
    h2 = recalled(f2, gold)
    n2 = count(f2)
    rec = sorted(h2 - cur_hit)
    out["outcome_additions"].append({"term": t, "frame_added": n2 - cur_n,
                                     "gold_recovered": rec})
    verdict = "KEEP" if rec else "refuse"
    print(f"  {t:26s} +{n2-cur_n:6d}  {verdict:7s} {','.join(rec) or '-'}")
    if rec:
        keep_out.append(t)
        cur_hit, cur_n = h2, n2

f_out = frame(allexpo, keep_out)
h_out = recalled(f_out, gold)
n_out = count(f_out)
cur_hit, cur_n = h_out, n_out
print(f"\nafter outcome repair: frame {n_out}, gold {len(h_out)}/{len(gold)}")
print(f"  still missing: {', '.join(sorted(set(gold) - h_out))}\n")

print("EXPOSURE AXIS candidates (gold recovered / frame added):")
keep_expo = dict(EXPOSURE)
for arm, cands in EXPO_ADD.items():
    for t in cands:
        trial = {k: (v + [t] if k == arm else v) for k, v in keep_expo.items()}
        fa = [x for v in trial.values() for x in v]
        f2 = frame(fa, keep_out)
        h2 = recalled(f2, gold)
        n2 = count(f2)
        rec = sorted(h2 - cur_hit)
        out["exposure_additions"].setdefault(arm, []).append(
            {"term": t, "frame_added": n2 - cur_n, "gold_recovered": rec})
        print(f"  {arm:9s} {t:22s} +{n2-cur_n:6d}  {'KEEP' if rec else 'refuse':7s} "
              f"{','.join(rec) or '-'}")
        if rec:
            keep_expo[arm] = keep_expo[arm] + [t]
            cur_hit, cur_n = h2, n2

fa = [x for v in keep_expo.values() for x in v]
f_fin = frame(fa, keep_out)
h_fin = recalled(f_fin, gold)
n_fin = count(f_fin)
print(f"\nFINAL: frame {n_fin}, gold {len(h_fin)}/{len(gold)}")
unreach = sorted(set(gold) - h_fin)
print(f"  UNREACHED: {', '.join(unreach) or 'none'}")
out.update({"final": {"outcome_axis": keep_out, "exposure_axes": keep_expo,
                      "frame": n_fin, "gold_recalled": len(h_fin),
                      "gold_total": len(gold), "unreached": unreach}})
(LOGS / "credit-constraints-query-repair.json").write_text(json.dumps(out, indent=2))
print("\nwritten: credit-constraints-query-repair.json")
