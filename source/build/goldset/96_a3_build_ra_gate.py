#!/usr/bin/env python3
"""
96_a3_build_ra_gate.py — A.3, build the RA title/abstract gate hand-off sheet (PROTOCOL stage 4).

Exception-based review CSV over the screen's RELEVANT + UNCERTAIN records (NOT_RELEVANT is excluded —
those routed away or carry no cell). The RA marks each row: leave `ra_decision` blank to approve the
screen's routing, or write RETRIEVE / EXCLUDE / UNSURE / REROUTE:<hypothesis>. Rows are ordered by a
retrieval priority so the RA sees the load-bearing papers first:

  1  identified-core primary (RELEVANT, a PRIMARY cell, design separates diffusion from a common shock)
  2  descriptive primary   (RELEVANT, a PRIMARY cell, descriptive residual only)
  3  theory / Princeton canon (RELEVANT)
  4  UNCERTAIN with a substantive cell
  5  UNCERTAIN / INSUFFICIENT_INFO (title-only queue)

Within a priority, both-channel (backward+forward corroborated) rows sort first, then by year desc.

Input : output/diffusion-of-fertility-control-screen-tiers.json
Output: output/diffusion-of-fertility-control-ra-review.csv
        output/diffusion-of-fertility-control-ra-gate-log.md
"""
import csv, json, os

SLUG = "diffusion-of-fertility-control"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "output")
TIERS = os.path.join(OUT, f"{SLUG}-screen-tiers.json")
CSV_OUT = os.path.join(OUT, f"{SLUG}-ra-review.csv")
LOG_OUT = os.path.join(OUT, f"{SLUG}-ra-gate-log.md")

PRIMARY = {"PRIMARY_SOCIAL_EXPOSURE", "PRIMARY_SPATIAL_DIFFUSION",
           "PRIMARY_CULTURAL_BOUNDARY_CONTENT", "PRIMARY_LEGITIMATION_SPREAD"}
THEORY = {"DIFFUSION_THEORY", "PRINCETON_CANON"}


def priority(r):
    v, c = r["verdict"], r["cell"]
    ident = (r.get("identification_of_diffusion") or "").upper()
    if v == "RELEVANT" and c in PRIMARY:
        return 1 if ident == "SEPARATES_FROM_COMMON_SHOCK" else 2
    if v == "RELEVANT" and c in THEORY:
        return 3
    if v == "UNCERTAIN" and c not in ("INSUFFICIENT_INFO", "NA"):
        return 4
    return 5


def main():
    rows = json.load(open(TIERS))
    review = [r for r in rows if r["verdict"] in ("RELEVANT", "UNCERTAIN")]
    review.sort(key=lambda r: (priority(r), 0 if r.get("both_channel") else 1, -(r.get("year") or 0)))
    fields = ["priority", "paperId", "doi", "title", "year", "venue", "verdict", "cell",
              "diffusion_channel", "identification_of_diffusion", "evidence_type", "both_channel",
              "reason", "ra_decision", "ra_note"]
    with open(CSV_OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in review:
            w.writerow({
                "priority": priority(r), "paperId": r["paperId"], "doi": r.get("doi") or "",
                "title": r.get("title") or "", "year": r.get("year") or "", "venue": r.get("venue") or "",
                "verdict": r["verdict"], "cell": r["cell"],
                "diffusion_channel": r.get("diffusion_channel") or "",
                "identification_of_diffusion": r.get("identification_of_diffusion") or "",
                "evidence_type": r.get("evidence_type") or "",
                "both_channel": "yes" if r.get("both_channel") else "",
                "reason": (r.get("reason") or "").replace("\n", " "),
                "ra_decision": "", "ra_note": ""})
    pc = {}
    for r in review:
        pc[priority(r)] = pc.get(priority(r), 0) + 1
    labels = {1: "identified-core primary", 2: "descriptive primary", 3: "theory/Princeton",
              4: "UNCERTAIN w/ cell", 5: "UNCERTAIN / title-only"}
    L = [f"# RA title/abstract gate — {SLUG}", "",
         f"{len(review):,} rows to review (RELEVANT + UNCERTAIN; NOT_RELEVANT excluded). Exception-based: "
         "leave `ra_decision` blank to approve the screen routing, or write **RETRIEVE**, **EXCLUDE**, "
         "**UNSURE**, or **REROUTE:<hypothesis>** (e.g. `REROUTE:A.20`). The screen is an automated Haiku "
         "recall filter, not a verdict; this gate is the human verdict.", "",
         "## Review order (priority buckets)", ""]
    for p in sorted(pc):
        L.append(f"- **{p}. {labels[p]}**: {pc[p]:,}")
    L += ["", "## Load-bearing guidance", "",
          "- **Priority 1 (identified core) is the retrieval list.** These are the designs that claim to "
          "separate social diffusion from a common economic/cultural shock; the chapter's synthesis rests "
          "on them. Confirm each really identifies (not a descriptive residual mislabelled).",
          "- **Sample Wall 1 first.** Any row with `diffusion_channel=MASS_MEDIA` that was kept in A.3, or "
          "any A.20 borderline, is the highest-cost misroute — reroute to A.20 if it is a channel effect.",
          "- **Priority 5 is the title-only queue**, not evidence; RETRIEVE only if the title alone names "
          "a diffusion→fertility estimand.",
          f"- Output: `output/{SLUG}-ra-review.csv`."]
    open(LOG_OUT, "w").write("\n".join(L) + "\n")
    print(f"RA review rows {len(review)} | by priority {dict(sorted(pc.items()))}")
    print(f"-> {os.path.relpath(CSV_OUT, ROOT)}")


if __name__ == "__main__":
    main()
