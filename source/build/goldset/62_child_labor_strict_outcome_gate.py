#!/usr/bin/env python3
"""Apply the evidence-grounded second-pass gate requested after RA spot review.

This never overwrites the edited 42-row sheet. It emits (1) a 42-row audit explaining
every keep/exclude/quarantine decision and (2) a smaller strict RA/retrieval-candidate
sheet. Existing RA annotations are copied verbatim and RA EXCLUDE decisions govern.
"""

import csv
from pathlib import Path

SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUTPUT = REPO / "output"
SOURCE = OUTPUT / f"{SLUG}-focused-ra-review.csv"

# Manual evidence-grounded audit of the 42-row focused set. Each decision was made from
# the committed title/abstract, requiring an explicit covered treatment + fertility
# outcome for empirical rows and a direct child-labor/schooling–fertility link for theory.
DECISIONS = {
    "W4396938006": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Studies employment and school attendance, not fertility."),
    "W2073343854": ("KEEP_RA_CORRECTED_THEORY", "Preserve RA correction to THEORY; no empirical policy estimate."),
    "W4409029977": ("KEEP", "Compulsory-schooling discontinuities identify marital fertility, including a zero estimate."),
    "W4405602751": ("KEEP_RA_CORRECTED_THEORY", "Preserve RA correction to THEORY; not an empirical policy-fertility estimate."),
    "W2979888791": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Health outcomes only; RA confirmed exclusion."),
    "W2185731654": ("KEEP", "UK reform study explicitly reports teen and completed fertility."),
    "W2752104534": ("KEEP", "Taiwan law study explicitly estimates fertility, including a null effect."),
    "W2411634914": ("KEEP", "Compulsory-schooling reforms explicitly estimate fertility."),
    "W2122096529": ("KEEP", "Compulsory-schooling reforms explicitly estimate fertility."),
    "W2188242424": ("KEEP", "Compulsory-schooling reforms explicitly estimate fertility."),
    "W2318594386": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Schooling and earnings outcomes only; RA confirmed exclusion."),
    "W1555027305": ("QUARANTINE_IDENTITY", "RA identified metadata mismatch; re-resolve DOI/title/authors before retrieval."),
    "W2617310741": ("EXCLUDE_IDENTITY_OR_OUTCOME", "Birth-order/education record is not a policy-fertility study; RA reports missing paper."),
    "W1576507153": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Instrument-validity comment concerns wages and schooling, not fertility."),
    "W2015046142": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Age-at-entry study estimates educational attainment, not fertility."),
    "W4415043415": ("KEEP_UNCERTAIN_FULLTEXT", "Title explicitly names fertility and China's compulsory-schooling law; abstract missing."),
    "W4224284165": ("KEEP_UNCERTAIN_FULLTEXT", "Title explicitly names fertility and China's compulsory-schooling reform; abstract missing."),
    "W3124938256": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Turn-of-century natural experiment estimates attendance only."),
    "W4412362654": ("KEEP", "India compulsory-schooling reform explicitly estimates fertility behavior and timing."),
    "W4392812928": ("EXCLUDE_OFF_EXPOSURE", "Full-time-school program is not a child-labor or compulsory-schooling legal mandate."),
    "W3212471012": ("KEEP", "Compulsory-schooling reform explicitly estimates age at first birth."),
    "W3006219298": ("KEEP", "School-leaving-age reform explicitly estimates pregnancy timing."),
    "W2108204833": ("KEEP", "Compulsory-schooling extension explicitly estimates teenage first births."),
    "W2186769068": ("KEEP", "Mandatory-schooling reform explicitly estimates fertility timing."),
    "W3024321219": ("KEEP", "Compulsory-schooling laws explicitly identify teen fertility."),
    "W2169373049": ("KEEP", "Compulsory-schooling laws explicitly identify teenage births."),
    "W4385628385": ("KEEP_UNCERTAIN_FULLTEXT", "Title explicitly names fertility and Thailand's compulsory-schooling law; abstract missing."),
    "W4206743955": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Title identifies marriage outcomes only; no fertility outcome supplied."),
    "W2154210580": ("KEEP_UNCERTAIN_FULLTEXT", "Title explicitly names teen fertility and compulsory-schooling laws; abstract missing."),
    "W3138623659": ("EXCLUDE_OFF_EXPOSURE", "School-entry rule is adjacent education exposure, not the covered legal mechanism."),
    "W2028140859": ("KEEP_UNCERTAIN_FULLTEXT", "Title explicitly names teenage childbearing and compulsory-education laws; abstract missing."),
    "W4405603403": ("KEEP", "Direct child-labor/fertility theoretical synthesis."),
    "W2924921004": ("ROUTE_MODE_PRODUCTION", "Agricultural earnings and structural change belong to TICK-030, not this legal-policy hypothesis."),
    "W2753276478": ("KEEP", "Model explicitly links education, child labor, and fertility."),
    "W2157906659": ("EXCLUDE_NO_FERTILITY_OUTCOME", "Empirical child-labor determinants paper; fertility is not an outcome."),
    "W2117090144": ("KEEP", "Model jointly determines fertility, child labor, and education."),
    "W2257784394": ("EXCLUDE_OFF_MECHANISM", "General endogenous-fertility/sibship-transfer model lacks the covered child-policy mechanism."),
    "W1961684553": ("KEEP", "Theory/evidence book directly covers the child-labor–education–fertility nexus."),
    "W3125141375": ("KEEP", "Economic-transformation theory jointly treats fertility decline, schooling, and the demise of child labor."),
    "W2152406420": ("KEEP", "Theory explicitly analyzes implications of child labor for fertility."),
    "W3093523732": ("KEEP_UNCERTAIN_FULLTEXT", "Title directly links child labor and fertility; abstract missing."),
    "W1525462723": ("KEEP_UNCERTAIN_FULLTEXT", "Canonical title directly links child labor, fertility, and growth; abstract missing."),
}


def main():
    with SOURCE.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
        source_fields = list(rows[0])
    ids = {row["paperId"] for row in rows}
    if ids != set(DECISIONS):
        raise SystemExit(f"decision-map mismatch: missing={sorted(ids-set(DECISIONS))}, extra={sorted(set(DECISIONS)-ids)}")

    audit_fields = source_fields + ["strict_gate_status", "strict_gate_reason", "retrieval_candidate"]
    audit_path = OUTPUT / f"{SLUG}-strict-outcome-audit.csv"
    strict_path = OUTPUT / f"{SLUG}-strict-focused-ra-review.csv"
    strict_rows = []
    with audit_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit_fields)
        writer.writeheader()
        for row in rows:
            status, reason = DECISIONS[row["paperId"]]
            # Existing human exclusions always govern. FIX corrections are preserved in
            # the row and explicitly labeled KEEP_RA_CORRECTED_THEORY or QUARANTINE.
            if (row.get("ra_decision") or "").strip().upper() == "EXCLUDE":
                status = "EXCLUDE_RA"
                reason = row.get("ra_note") or reason
            eligible = status.startswith("KEEP")
            augmented = {**row, "strict_gate_status": status,
                         "strict_gate_reason": reason,
                         "retrieval_candidate": "YES" if eligible else "NO"}
            writer.writerow(augmented)
            if eligible:
                strict_rows.append(augmented)

    with strict_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit_fields)
        writer.writeheader()
        writer.writerows(strict_rows)
    print(f"audit: {len(rows)} -> {audit_path.relative_to(REPO)}")
    print(f"strict focused: {len(strict_rows)} -> {strict_path.relative_to(REPO)}")
    print("quarantined:", sum(status.startswith("QUARANTINE") for status, _ in DECISIONS.values()))


if __name__ == "__main__":
    main()
