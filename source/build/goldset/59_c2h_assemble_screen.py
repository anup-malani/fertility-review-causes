#!/usr/bin/env python3
"""
59_c2h_assemble_screen.py — C.2.h (digital leisure substitution), assemble the blinded screen.

Mirror of A.3 step 94. Reads every verdict file, rejoins the blinded metadata (title/doi/year/
source_channels) from the screen frame by id, and produces:
  - tiers (T1 RELEVANT / T2 UNCERTAIN / T3 NOT_RELEVANT),
  - the POOLING SET = verdict RELEVANT AND cell in PRIMARY AND evidence not review/theory,
    split by identification (EXOGENOUS_LEISURE_VARIATION = identified core vs ASSOCIATIONAL_ONLY),
  - the theory/mechanism stream,
  - a cell tally and a routing read (how many records each OFF_* wall absorbed),
and a human-readable report. Fail-closed: refuses to assemble if any manifest batch lacks a valid
verdict file (run 57 --audit first).

Outputs: literature/search-logs/{slug}-screen-tiers.json
         literature/search-logs/{slug}-estimand-ready.json
         literature/search-logs/{slug}-theory-stream.json
         literature/search-logs/{slug}-screen-report.md
"""
import importlib.util, json
from collections import Counter
from pathlib import Path

SLUG = "digital-leisure-substitution"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

PRIMARY = {"PRIMARY_LEISURE_PRICE", "PRIMARY_PORN_SUBSTITUTION", "PRIMARY_SOCIAL_DISPLACEMENT"}
OFF = {"OFF_WAGE_C2E", "OFF_DATINGAPP_A24", "OFF_COITAL_A14", "OFF_VALUES_D1A",
       "OFF_MENTALHEALTH_D3A", "OFF_OUTCOME", "OFF_OTHER", "REVERSE"}


def load_validator():
    path = HERE / "57_c2h_validate_screen.py"
    spec = importlib.util.spec_from_file_location("c2h_screen_validator", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    validator = load_validator()
    frame = {r["id"]: r for r in json.loads((LOGS / f"{SLUG}-screen-frame.json").read_text())}

    verdicts = []
    for m in manifest["manifest"]:
        out = REPO / m["output"]
        inp = json.loads((REPO / m["input"]).read_text())
        if not out.exists():
            raise SystemExit(f"batch {m['batch']:03d} not screened yet — run 58 first")
        arr = json.loads(out.read_text())
        errs = []
        for i, (rec, paper) in enumerate(zip(arr, inp), 1):
            errs += validator.validate_record(rec, paper["id"], f"batch {m['batch']:03d} row {i}")
        if errs:
            raise SystemExit(f"batch {m['batch']:03d} invalid: {errs[:3]}")
        verdicts.extend(arr)

    for v in verdicts:
        meta = frame.get(v["id"], {})
        v["title"] = meta.get("title")
        v["doi"] = meta.get("doi")
        v["year"] = meta.get("year")
        v["source_channels"] = meta.get("source_channels")
        v["cited_by_count"] = meta.get("cited_by_count")

    def V(x):
        return str(x.get("verdict", "")).upper()

    def C(x):
        return str(x.get("estimand_cell", "")).upper()

    def E(x):
        return str(x.get("evidence_type", "")).lower()

    def I(x):
        return str(x.get("identification", "")).upper()

    t1 = [v for v in verdicts if V(v) == "RELEVANT"]
    t2 = [v for v in verdicts if V(v) == "UNCERTAIN"]
    t3 = [v for v in verdicts if V(v) == "NOT_RELEVANT"]

    pooling = [v for v in t1 if C(v) in PRIMARY and "review" not in E(v) and "theor" not in E(v)]
    identified = [v for v in pooling if I(v) == "EXOGENOUS_LEISURE_VARIATION"]
    associational = [v for v in pooling if I(v) != "EXOGENOUS_LEISURE_VARIATION"]
    theory = [v for v in verdicts if C(v) in {"THEORY", "MECHANISM_TIMEUSE"}]

    json.dump({"tier1_relevant": t1, "tier2_uncertain": t2, "tier3_not_relevant": t3},
              open(LOGS / f"{SLUG}-screen-tiers.json", "w"), indent=1)
    json.dump(pooling, open(LOGS / f"{SLUG}-estimand-ready.json", "w"), indent=2)
    json.dump(theory, open(LOGS / f"{SLUG}-theory-stream.json", "w"), indent=2)

    cell_tally = Counter(C(v) for v in verdicts if V(v) != "NOT_RELEVANT")
    off_tally = Counter(C(v) for v in verdicts if C(v) in OFF)
    prim_tally = Counter(C(v) for v in pooling)
    sub_tally = Counter(str(v.get("sub_mechanism", "")).upper() for v in pooling)

    R = [f"# C.2.h blinded screen — assembly report", "",
         f"Frame {len(verdicts)} records ({manifest['records_with_abstract']} with abstracts), "
         f"{len(manifest['manifest'])} batches. Assembled by `59_c2h_assemble_screen.py`.", "",
         "## Verdict tiers", "",
         f"- RELEVANT (T1): **{len(t1)}**",
         f"- UNCERTAIN (T2): **{len(t2)}**",
         f"- NOT_RELEVANT (T3): **{len(t3)}**", "",
         "## Pooling set (RELEVANT ∩ PRIMARY ∩ non-review/theory)", "",
         f"- Pooling set: **{len(pooling)}**",
         f"  - identified core (EXOGENOUS_LEISURE_VARIATION): **{len(identified)}**",
         f"  - associational only: **{len(associational)}**",
         f"- by primary cell: {dict(prim_tally)}",
         f"- by sub-mechanism: {dict(sub_tally)}", "",
         "## Routing (wall absorption)", "",
         f"- OFF cell tally: {dict(off_tally)}",
         f"- theory/mechanism stream: **{len(theory)}**", "",
         "## Full non-NOT_RELEVANT cell tally", "",
         f"{dict(cell_tally.most_common())}", "",
         "## Identified core (the studies to read first)", ""]
    for v in sorted(identified, key=lambda x: -(x.get("cited_by_count") or 0)):
        R.append(f"- [{C(v)}] {(v.get('title') or '')[:90]} — {v.get('outcome')}; {v.get('evidence_type')}")
    (LOGS / f"{SLUG}-screen-report.md").write_text("\n".join(R) + "\n")

    print(f"T1 {len(t1)} / T2 {len(t2)} / T3 {len(t3)}")
    print(f"pooling {len(pooling)} (identified {len(identified)} / assoc {len(associational)})")
    print(f"primary cells {dict(prim_tally)}")
    print(f"OFF routing {dict(off_tally)}; theory/mech {len(theory)}")
    print(f"wrote screen-tiers, estimand-ready, theory-stream, screen-report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
