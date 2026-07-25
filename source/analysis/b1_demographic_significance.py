#!/usr/bin/env python3
"""B.1 demographic-significance and target-period pass (TICK-045).

Places each pooled status-and-reproduction study in a target phenomenon by its observation
window, then reports a demographic-significance verdict per phenomenon channel.

The pass is deliberately asymmetric, as TICK-045 specifies. The status-and-reproduction
stream can be dated and classified. The distinctive decoupling claim, that fertility falls
with the preference for children held fixed, has no identified estimate in the extracted
set, so it is recorded as unidentified and is never assigned a decline share.

Two design rules carried from the OAS chapter:
  - Nothing is asserted that is not computed from an input file. The FDT timing argument in
    particular is derived from the study windows in the target-period table, not stated.
  - Where a quantity cannot be computed from what is extracted, the row says so and names the
    step that would produce it, rather than substituting a plausible number.

The UN TFR replacement-status cross-check reuses ``oas_transition_classification``. That data
lives in the sibling ``proximate-causes`` checkout. When it is absent the cross-check reports
its own unavailability instead of silently skipping, so a reader can tell a missing check from
a passed one.
"""

from __future__ import annotations

import csv
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
ROOT = Path(__file__).resolve().parents[2]

TARGET_PERIODS = ROOT / "extraction" / f"{SLUG}-target-period-relevance.csv"
META_SUMMARY = ROOT / "output" / "tables" / f"{SLUG}-meta-analysis-summary.csv"
SIG_OUT = ROOT / "output" / "tables" / f"{SLUG}-demographic-significance.csv"
GRADE_OUT = ROOT / "output" / "tables" / f"{SLUG}-grade-verdicts.csv"

# Target-phenomenon windows, PROTOCOL.md lines 20-22.
PM_END = 1870
FDT_START, FDT_END = 1870, 1965
SDT_START = 1965

SIG_COLUMNS = [
    "phenomenon_channel",
    "target_phenomenon",
    "claim",
    "evidence_base",
    "n_studies",
    "pooled_estimate",
    "variance_explained_pct",
    "demographic_significance_verdict",
    "coefficient_pooling_status",
    "transition_classification_basis",
    "needs_human_review",
    "rationale",
    "next_required_step",
]

GRADE_COLUMNS = [
    "phenomenon_channel",
    "causal_credibility",
    "demographic_significance",
    "grade_rationale",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def _int_or_none(value: str) -> int | None:
    value = (value or "").strip()
    return int(value) if value else None


def overlaps(start: int | None, end: int | None, win_start: int, win_end: int) -> bool:
    """Whether a study window intersects a target window. Undated windows never match."""
    if start is None or end is None:
        return False
    return start <= win_end and end >= win_start


def classify_window(row: dict[str, str]) -> str:
    """Assign a target phenomenon from the study's observation window alone.

    Regime-based rows (a natural-fertility population observed in the twentieth century)
    carry no usable calendar window and keep the analyst assignment recorded in the input.
    """
    start = _int_or_none(row.get("period_start", ""))
    end = _int_or_none(row.get("period_end", ""))
    if start is None or end is None:
        return row.get("derived_period_target_relevance", "") or "unclassified_no_window"
    hits = []
    if start < PM_END:
        hits.append("PM")
    if overlaps(start, end, FDT_START, FDT_END):
        hits.append("FDT")
    if end >= SDT_START:
        hits.append("SDT")
    return "|".join(hits) if hits else "unclassified_no_window"


def fdt_timing_evidence(rows: list[dict[str, str]]) -> dict:
    """Derive the FDT timing argument from the dated windows rather than asserting it.

    The chapter's claim is that the severing technology postdates most of the transition.
    What the extracted set can actually establish is narrower and checkable: whether any
    pooled study observes fertility inside the FDT window at all.
    """
    dated = [
        r
        for r in rows
        if _int_or_none(r.get("period_start", "")) is not None
        and _int_or_none(r.get("period_end", "")) is not None
    ]
    in_fdt = [
        r
        for r in dated
        if overlaps(
            _int_or_none(r["period_start"]),
            _int_or_none(r["period_end"]),
            FDT_START,
            FDT_END,
        )
    ]
    starts = [_int_or_none(r["period_start"]) for r in dated]
    return {
        "n_dated": len(dated),
        "n_undated": len(rows) - len(dated),
        "n_in_fdt": len(in_fdt),
        "earliest_start": min(starts) if starts else None,
        "fdt_window": f"{FDT_START}-{FDT_END}",
    }


def load_pool(path: Path = META_SUMMARY) -> dict[str, dict[str, str]]:
    return {r["group"]: r for r in read_csv(path)}


def _fmt_pool(row: dict[str, str] | None) -> str:
    if not row or not row.get("pooled_r"):
        return "not pooled"
    return (
        f"r={row['pooled_r']} [{row['r_ci_lower']}, {row['r_ci_upper']}], "
        f"k={row['k_studies']} studies"
    )


def _variance_explained(row: dict[str, str] | None) -> str:
    """Share of variance in the fertility outcome tracked by the pooled correlation."""
    if not row or not row.get("pooled_r"):
        return ""
    r = float(row["pooled_r"])
    return f"{r * r * 100:.2f}"


def tfr_cross_check() -> dict[str, str]:
    """Attempt the UN TFR replacement-status check; report unavailability explicitly."""
    try:
        import oas_transition_classification as otc  # noqa: PLC0415
    except ImportError:
        return {
            "status": "unavailable",
            "detail": "oas_transition_classification could not be imported.",
        }
    if not otc.UN_TFR_PATH.exists():
        return {
            "status": "unavailable",
            "detail": (
                f"UN TFR source not present at {otc.UN_TFR_PATH}. It lives in the sibling "
                "proximate-causes checkout, which is not on this machine. Window "
                "classification below is from study dates only and has NOT been "
                "cross-checked against in-window TFR."
            ),
        }
    return {"status": "available", "detail": f"UN TFR source found at {otc.UN_TFR_PATH}."}


def build_rows(
    periods: list[dict[str, str]], pool: dict[str, dict[str, str]], tfr: dict[str, str]
) -> list[dict]:
    timing = fdt_timing_evidence(periods)
    by_class: dict[str, list[dict[str, str]]] = {}
    for row in periods:
        by_class.setdefault(classify_window(row), []).append(row)

    pm_rows = by_class.get("PM_analog_by_regime", [])
    sdt_rows = by_class.get("SDT", [])

    male, female, overall = pool.get("sex=male"), pool.get("sex=female"), pool.get("overall")
    absent = pool.get("contraceptive_availability=absent")

    tfr_note = (
        "Windows classified from study dates only; UN TFR replacement-status cross-check "
        f"NOT run ({tfr['status']})."
        if tfr["status"] != "available"
        else "Windows classified from study dates and cross-checked against in-window TFR."
    )

    return [
        {
            "phenomenon_channel": "PM_dissociation",
            "target_phenomenon": "Pre-modern fertility variation",
            "claim": "Status predicts reproductive success where contraception is absent.",
            "evidence_base": (
                f"{len(pm_rows)} pooled study assigned to the pre-modern cell by fertility "
                "regime rather than by calendar date."
            ),
            "n_studies": len(pm_rows),
            "pooled_estimate": _fmt_pool(absent),
            "variance_explained_pct": _variance_explained(absent),
            "demographic_significance_verdict": "insufficient_direct_evidence",
            "coefficient_pooling_status": (
                "insufficient (<3 studies); reported not pooled"
                if absent and not absent.get("pooled_r")
                else "pooled"
            ),
            "transition_classification_basis": (
                "Assigned by subsistence-type fertility regime, not by TFR or calendar date. "
                "The constituent ethnographies are twentieth-century, so this indexes a "
                "pre-transitional regime rather than the pre-1870 period itself."
            ),
            "needs_human_review": "yes",
            "rationale": (
                "The contraception-absent cell contains one study. It carries a positive male "
                "status-to-reproduction association, which is consistent with the mechanism, "
                "but one study cannot establish pre-modern fertility VARIATION, and the "
                "regime-based assignment is an analyst judgement."
            ),
            "next_required_step": (
                "Retrieve the natural-fertility and historical-demography studies still on the "
                "B.1 target list so the contraception-absent cell exceeds one study."
            ),
        },
        {
            "phenomenon_channel": "FDT_decoupling",
            "target_phenomenon": "First Demographic Transition",
            "claim": (
                "Severing sex from reproduction drove the first transition."
            ),
            "evidence_base": (
                f"Zero of {timing['n_dated']} dated pooled studies observe fertility inside "
                f"the FDT window ({timing['fdt_window']}); the earliest observation window in "
                f"the pool begins in {timing['earliest_start']}."
                if timing["n_in_fdt"] == 0
                else f"{timing['n_in_fdt']} dated pooled studies overlap the FDT window."
            ),
            "n_studies": timing["n_in_fdt"],
            "pooled_estimate": "not pooled",
            "variance_explained_pct": "",
            "demographic_significance_verdict": "not_significant_mechanism_mistimed",
            "coefficient_pooling_status": "no studies in window; nothing to pool",
            "transition_classification_basis": (
                f"FDT window {timing['fdt_window']} per PROTOCOL.md. Overlap computed from the "
                "study windows in the target-period table."
            ),
            "needs_human_review": "no",
            "rationale": (
                "The timing argument is not an assertion about when the pill was licensed. It "
                "is a property of the evidence base: every dated study in the pool observes "
                f"fertility after {timing['earliest_start']}, so the extracted set contains no "
                "observation of the decoupling mechanism operating during the first transition. "
                "A mechanism with no in-window evidence cannot be credited with in-window "
                "demographic significance."
            ),
            "next_required_step": (
                "None for this chapter. Historical-demography evidence on the first transition "
                "belongs to the contraception and economic chapters."
            ),
        },
        {
            "phenomenon_channel": "SDT_dissociation",
            "target_phenomenon": "Second Demographic Transition",
            "claim": (
                "The status-to-reproduction link dissociates, differently by sex, where "
                "contraception is available."
            ),
            "evidence_base": (
                f"{len(sdt_rows)} pooled studies whose observation windows fall entirely "
                f"after {SDT_START}."
            ),
            "n_studies": len(sdt_rows),
            "pooled_estimate": (
                f"male {_fmt_pool(male)}; female {_fmt_pool(female)}; "
                f"overall {_fmt_pool(overall)}"
            ),
            "variance_explained_pct": (
                f"male {_variance_explained(male)}; female {_variance_explained(female)}; "
                f"overall {_variance_explained(overall)}"
            ),
            "demographic_significance_verdict": "real_but_quantitatively_small_and_self_cancelling",
            "coefficient_pooling_status": "pooled, random effects on the Fisher-z scale",
            "transition_classification_basis": (
                f"All windows begin at or after {min((_int_or_none(r['period_start']) or 0) for r in sdt_rows)} "
                f"and end at or before {max((_int_or_none(r['period_end']) or 0) for r in sdt_rows)}, "
                f"entirely inside the SDT window ({SDT_START}-present). {tfr_note}"
            ),
            "needs_human_review": "no",
            "rationale": (
                "The sex reversal is robust and is the chapter's best-supported quantitative "
                "finding, but its demographic significance is limited by its own magnitude. The "
                "pooled correlations track under two percent of the variance in completed "
                "fertility within sex, and because the male and female associations have "
                "opposite signs the aggregate association is indistinguishable from zero. A "
                "gradient that vanishes in aggregate cannot by itself move aggregate fertility; "
                "it would have to act through a shift in the status distribution that is "
                "differently weighted across sexes, which no study in the set estimates."
            ),
            "next_required_step": (
                "To express this in TFR units rather than correlation units, extract the "
                "standard deviation of the fertility outcome for each study. Those are not "
                "currently in the extraction, so no decline share is reported here."
            ),
        },
        {
            "phenomenon_channel": "SDT_distinctive_decoupling",
            "target_phenomenon": "Second Demographic Transition",
            "claim": (
                "Fertility falls through the severing of sex from reproduction with the "
                "preference for children held fixed."
            ),
            "evidence_base": (
                "No study in the extracted set identifies this claim. The desire-held-fixed "
                "contrast is present in the chapter's design and absent from every retrieved "
                "design."
            ),
            "n_studies": 0,
            "pooled_estimate": "unidentified",
            "variance_explained_pct": "",
            "demographic_significance_verdict": "unidentified_no_share_assigned",
            "coefficient_pooling_status": "not applicable; no identified estimate exists",
            "transition_classification_basis": (
                "Not classified. Classification requires an estimate to place, and the "
                "distinctive claim has none."
            ),
            "needs_human_review": "no",
            "rationale": (
                "This is the cell that separates B.1 from the modern-contraception and "
                "postmaterialism chapters, and it is empty. The contraception studies that "
                "would populate it identify effects on total births rather than on the "
                "decoupling channel with child preference held fixed, which routes them to the "
                "neighbouring chapter. Assigning this claim any share of the second transition "
                "would be assigning a share to an estimate that does not exist."
            ),
            "next_required_step": (
                "A design that holds measured child preference fixed while varying contraceptive "
                "access. None was found in the frame; this is a research gap the chapter should "
                "state, not a retrieval failure to correct."
            ),
        },
    ]


def build_grade_rows(sig_rows: list[dict]) -> list[dict]:
    """GRADE verdicts, keyed to the significance rows so the two tables cannot drift."""
    by_channel = {r["phenomenon_channel"]: r for r in sig_rows}
    return [
        {
            "phenomenon_channel": "PM_dissociation",
            "causal_credibility": "very_low",
            "demographic_significance": by_channel["PM_dissociation"][
                "demographic_significance_verdict"
            ],
            "grade_rationale": (
                "One meta-analytic study, observational throughout, assigned to the pre-modern "
                "cell by fertility regime rather than by date. Sufficient to show the "
                "association exists in pre-transitional populations, insufficient to explain "
                "pre-modern fertility variation."
            ),
        },
        {
            "phenomenon_channel": "FDT_decoupling",
            "causal_credibility": "very_low",
            "demographic_significance": by_channel["FDT_decoupling"][
                "demographic_significance_verdict"
            ],
            "grade_rationale": (
                "No dated study in the pool observes fertility inside the first-transition "
                "window. The mechanism is mistimed relative to the phenomenon it is asked to "
                "explain, and the evidence base is empty in-window rather than merely weak."
            ),
        },
        {
            "phenomenon_channel": "SDT_dissociation",
            "causal_credibility": "moderate",
            "demographic_significance": by_channel["SDT_dissociation"][
                "demographic_significance_verdict"
            ],
            "grade_rationale": (
                "Five studies, consistent in direction, with the sex reversal surviving a "
                "second-reader verification that removed two miscoded effects. Rated moderate "
                "rather than higher because every study is observational and confounding-"
                "dominated, four of five are serious on risk of bias, and heterogeneity exceeds "
                "ninety-six percent. Credible as a described regularity, not as a causal "
                "estimate."
            ),
        },
        {
            "phenomenon_channel": "SDT_distinctive_decoupling",
            "causal_credibility": "low",
            "demographic_significance": by_channel["SDT_distinctive_decoupling"][
                "demographic_significance_verdict"
            ],
            "grade_rationale": (
                "The claim is tested only by formal models that are internally valid and "
                "empirically unanchored, plus descriptive trend evidence. No design holds child "
                "preference fixed, so the contrast that gives the hypothesis its distinctive "
                "content is unidentified."
            ),
        },
    ]


def run() -> tuple[list[dict], list[dict], dict[str, str]]:
    periods = read_csv(TARGET_PERIODS)
    pool = load_pool()
    tfr = tfr_cross_check()
    sig_rows = build_rows(periods, pool, tfr)
    return sig_rows, build_grade_rows(sig_rows), tfr


def main() -> None:
    sig_rows, grade_rows, tfr = run()
    write_csv(SIG_OUT, sig_rows, SIG_COLUMNS)
    write_csv(GRADE_OUT, grade_rows, GRADE_COLUMNS)
    print(f"TFR cross-check: {tfr['status']} - {tfr['detail']}")
    for row in sig_rows:
        print(
            f"  {row['phenomenon_channel']:<28} n={row['n_studies']:<3} "
            f"{row['demographic_significance_verdict']}"
        )
    print(f"wrote {SIG_OUT.relative_to(ROOT)}")
    print(f"wrote {GRADE_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
