#!/usr/bin/env python3
"""359 — audit the C.3.d screen verdicts for internal consistency.

WHY THIS EXISTS. 3,254 verdicts were entered by hand (see TICK-083's log for why, and for the
limitation that creates). A hand-entered table has a failure mode a scripted one does not: a slip
in one field that no downstream step notices, because every field is individually well-formed.
`safeguards-must-be-measured-not-trusted` and A.17's hand-typed demsig table -- right offsets,
wrong baselines, nothing complained.

These are INVARIANTS, not judgement calls. Each one holds by definition of the rubric, so a
violation is a data error rather than a debatable routing:

  * `QQ_SUBSTITUTION` is the BACKWARD arm by construction (scope §2), so its direction cannot be
    FORWARD.
  * A `MIXED_*` cell asserts that two primitives move together. The corresponding wall flag is what
    makes that assertion auditable, so a `MIXED_CHILD_PARENT_RETURN` row without `W2_PARENT_RETURN`
    has an unauditable claim in it -- and Wall 2's count is the chapter's deciding number.
  * `OFF_TOPIC` means "not about this at all"; it cannot carry a direction, a design, or an outcome.
  * Enumerations must be closed. An unlisted value falls through every count silently
    (`estimator-class-list-is-a-gate`).

Reported, never auto-fixed: the fix for a wrong verdict is to re-read the record, and a script that
rewrites judgements would destroy the thing being audited.

Output: literature/search-logs/quantity-quality-tradeoff-verdict-audit.{json,md}
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
VERD = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"

CELLS = {"RETURN_FERTILITY", "SHOCK_FERTILITY", "QQ_SUBSTITUTION", "MIXED_RETURN_POSITION",
         "MIXED_CHILD_PARENT_RETURN", "MIXED_RETURN_INCOME", "RETURN_ASSOCIATION",
         "PERCEIVED_RETURN", "THEORY", "OFF_TOPIC", "OFF_OTHER", "UNCLEAR"}
DIRECTIONS = {"FORWARD", "BACKWARD", "BOTH", "NA"}
DESIGNS = {"RCT", "IV", "DID", "RDD", "EVENT_STUDY", "NATURAL_EXPERIMENT", "PANEL_FE",
           "CROSS_SECTION", "CALIBRATION", "DESCRIPTIVE", "REVIEW", "THEORY", "UNCLEAR", "NA"}
OUTCOMES = {"FERTILITY", "INVESTMENT_PER_CHILD", "CHILD_ATTAINMENT", "OTHER", "NA"}
WALLS = {"W1_POSITION", "W2_PARENT_RETURN", "W4_INCOME", "W5_A12_TWINNING", "W6_MORTALITY",
         "W7_SCHOOLING_LAW"}
CONF = {"HIGH", "MED", "LOW"}
EXCLUDED = {"OFF_TOPIC"}
MIXED_REQUIRES = {"MIXED_CHILD_PARENT_RETURN": "W2_PARENT_RETURN",
                  "MIXED_RETURN_POSITION": "W1_POSITION",
                  "MIXED_RETURN_INCOME": "W4_INCOME"}


def main():
    rows = list(csv.DictReader(VERD.open()))
    findings = []

    def flag(rule, r, detail):
        findings.append({"rule": rule, "screen_id": r["screen_id"], "cell": r["cell"],
                         "direction": r["direction"], "detail": detail,
                         "note": (r.get("note") or "")[:80]})

    seen = set()
    for r in rows:
        sid = r["screen_id"]
        if sid in seen:
            flag("duplicate_id", r, "this screen_id appears more than once")
        seen.add(sid)
        walls = {w for w in (r["wall_risk"] or "").split(";") if w}

        # closed enumerations
        for field, allowed in (("cell", CELLS), ("direction", DIRECTIONS),
                               ("design", DESIGNS), ("outcome_object", OUTCOMES),
                               ("confidence", CONF)):
            if r[field] not in allowed:
                flag(f"bad_{field}", r, f"{field}={r[field]!r} is not in the rubric's list")
        for w in walls - WALLS:
            flag("bad_wall", r, f"wall_risk contains {w!r}, not in the rubric's list")
        if r["title_only"] not in ("true", "false"):
            flag("bad_title_only", r, f"title_only={r['title_only']!r}")

        # the backward arm is backward by construction (scope §2)
        if r["cell"] == "QQ_SUBSTITUTION" and r["direction"] == "FORWARD":
            flag("backward_cell_forward_direction", r,
                 "QQ_SUBSTITUTION is the BACKWARD arm; direction cannot be FORWARD")
        # the forward primary cells cannot be backward-only
        if r["cell"] in ("RETURN_FERTILITY", "SHOCK_FERTILITY") and r["direction"] == "BACKWARD":
            flag("forward_cell_backward_direction", r,
                 "a primary forward cell cannot have direction BACKWARD")
        # a MIXED cell's claim must be auditable through its wall flag
        req = MIXED_REQUIRES.get(r["cell"])
        if req and req not in walls:
            flag("mixed_without_wall", r,
                 f"{r['cell']} asserts two primitives move together but lacks {req}; "
                 "the wall count is built from this flag")
        # OFF_TOPIC carries no analytic fields
        if r["cell"] in EXCLUDED:
            if r["direction"] != "NA":
                flag("offtopic_with_direction", r, f"direction={r['direction']}")
            if r["design"] != "NA":
                flag("offtopic_with_design", r, f"design={r['design']}")
            if r["outcome_object"] != "NA":
                flag("offtopic_with_outcome", r, f"outcome_object={r['outcome_object']}")
        # a primary forward cell should have a fertility outcome -- that is what makes it primary
        if r["cell"] in ("RETURN_FERTILITY", "SHOCK_FERTILITY") and r["outcome_object"] != "FERTILITY":
            flag("primary_without_fertility_outcome", r,
                 f"outcome_object={r['outcome_object']}; a primary cell's outcome is fertility, "
                 "and a demsig share needs a fertility numerator")
        # the backward arm's outcome is a child outcome, never fertility
        if r["cell"] == "QQ_SUBSTITUTION" and r["outcome_object"] == "FERTILITY":
            flag("backward_with_fertility_outcome", r,
                 "QQ_SUBSTITUTION's dependent variable is a CHILD outcome, not fertility")
        # the rubric says prefer UNCLEAR over a confident cell on a title-only row
        if r["title_only"] == "true" and r["confidence"] == "HIGH" and r["cell"] not in EXCLUDED:
            flag("title_only_high_confidence", r,
                 "title-only row given HIGH confidence in an in-scope cell; the rubric asks for "
                 "caution here (advisory, not an error)")

    by_rule = Counter(f["rule"] for f in findings)
    hard = {k: v for k, v in by_rule.items() if k != "title_only_high_confidence"}
    blob = {"n_rows": len(rows), "n_findings": len(findings), "by_rule": dict(by_rule),
            "hard_findings": sum(hard.values()), "findings": findings}
    (LOGS / "quantity-quality-tradeoff-verdict-audit.json").write_text(json.dumps(blob, indent=2) + "\n")

    print(f"audited {len(rows)} verdicts against {len(set(by_rule) | set())} triggered rules\n")
    if not by_rule:
        print("  no violations")
    for k, v in by_rule.most_common():
        tag = "  (advisory)" if k == "title_only_high_confidence" else ""
        print(f"  {k:36} {v:>5}{tag}")
    print(f"\nhard violations (excluding the advisory rule): {sum(hard.values())}")
    for k in hard:
        print(f"\n--- {k} ---")
        for f in [x for x in findings if x["rule"] == k][:12]:
            print(f"  {f['screen_id']}  {f['cell']:26} {f['detail'][:80]}")
        n = by_rule[k]
        if n > 12:
            print(f"  ... and {n - 12} more")

    L = [f"# C.3.d verdict audit — {len(rows)} rows", "",
         "Generated by `source/build/goldset/359_c3d_verdict_audit.py`. Do not edit by hand.", "",
         "These are INVARIANTS of the rubric, not routing judgements: a violation is a data error. "
         "3,254 verdicts were hand-entered, and a hand-entered table fails by a slip in one field "
         "that nothing downstream notices. Reported, never auto-fixed — the fix for a wrong verdict "
         "is to re-read the record.", "",
         f"**{sum(hard.values())} hard violations**, "
         f"{by_rule.get('title_only_high_confidence', 0)} advisory.", "",
         "| rule | n |", "|---|---|"]
    L += [f"| `{k}` | {v} |" for k, v in by_rule.most_common()]
    if findings:
        L += ["", "## Every finding", "", "| screen id | rule | cell | detail |", "|---|---|---|---|"]
        L += [f"| `{f['screen_id']}` | `{f['rule']}` | `{f['cell']}` | {f['detail'][:110]} |"
              for f in findings if f["rule"] != "title_only_high_confidence"]
    L.append("")
    (LOGS / "quantity-quality-tradeoff-verdict-audit.md").write_text("\n".join(L))
    print(f"\nwrote quantity-quality-tradeoff-verdict-audit.{{json,md}}")
    return 1 if sum(hard.values()) else 0


main()
