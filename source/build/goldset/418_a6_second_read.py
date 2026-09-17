#!/usr/bin/env python3
"""
418 — A.6 (TICK-087) stage 7: the second read of the five flagged records, and the judgment-blinded
sheet for a genuine independent second reader.

What this is, and the limit on it
---------------------------------
**This is not an independent second read.** The same reader made all five first-pass calls, and the
point of a second reader is independence: the reader who made an error is the worst-placed person to
catch it. What is done here is an *adversarial self-re-read* — for each record the question asked
was not "is my call defensible" but "what is the strongest case that this record is
`PRIMARY_NORM_FERTILITY`, and does it survive contact with the text". That can catch outright
errors, and it did catch two. It cannot substitute for independence, so this script also emits the
house's judgment-blinded review sheet (the form `82_build_compulsory_education_blinded_review.py`
established) with the first-pass cell **withheld**, for Alexandra or Anup to complete.

The rubric requires 100% second reading of `PRIMARY_NORM_FERTILITY` and of `INSUFFICIENT_INFO` in
the identified-design strata, precisely because this chapter's conclusion is an absence and the
costly error is a false negative on the primary cell.

What the adversarial pass found
-------------------------------
Three calls confirmed, on the decisive question of whether a realized-fertility outcome exists:

  W108787496  Rajan 2014. The dissertation's only dependent variables are Desired Family Size
              (§3.4.1, Poisson) and Contraceptive Use (§4.4.1, multilevel logit, Tables 15-18).
              No table pairs a norm regressor with a fertility outcome. CONFIRMED.
  W1976018943  Wolff et al. 2000. Only dependent variables are unmet need and contraceptive mix.
              "Number of children" appears solely as the text of a survey attitude item, never as
              an outcome. CONFIRMED.
  W2187750596  Ragan 2012. Tables 2 through 6 each state that Pill demand per woman aged 16-40 is
              the dependent variable; out-of-wedlock births are the REGRESSOR, not the outcome.
              CONFIRMED.

Two calls changed:

  W4224236986  **MIXED_NORM_SECULAR -> LINK_NORM_USE.** The first pass treated this as religiosity,
              hence a value, hence D.1.a's under wall 5. Reading the full text (retrieved from
              Europe PMC; it is gold OA and should have been fetched at stage 5) shows the paper
              does not stop at religiosity: it decomposes it, and among the separately measured
              mediators is **"moral opposition to birth control" on a 0-4 scale**, alongside
              anticipated guilt after sex and fear of being stigmatised. That is A.6's construct,
              dosed separately from the value it comes from, in a weekly longitudinal panel with a
              mediation design. It also cites Bongaarts and Watkins 1996, one of A.6's four
              registered seminals. Wall 5 gives D.1.a "what people value" and A.6 "what they can be
              seen doing at fixed values"; this paper measures both and separates them, so routing
              it wholly to D.1.a was wrong. The outcome is still contraceptive use, so it is link
              evidence and not the primary cell. This is now the **best-designed record in
              `LINK_NORM_USE`** and it makes PI call 5 answerable from evidence rather than taste.
  W4403613268  **CONTEXT_STIGMA_MEASURE -> INSUFFICIENT_INFO.** The first-pass call rested on the
              title alone, because OpenAlex holds no abstract. The second read establishes only
              that it cannot be established: the record is `oa_status: closed` at Springer with no
              OA copy anywhere. Leaving a title-based cell assignment standing behind a permanent
              "second read required" flag would be a false resolution, so it reverts to unresolved
              and goes on the wantlist.

Neither change touches `PRIMARY_NORM_FERTILITY`, which stays at 0.
"""
import csv, html, json, re, subprocess, sys, pathlib

SLUG = "stigma-reduction-contraception-abortion"
CSVP = pathlib.Path("extraction") / f"{SLUG}-screened.csv"
LOGP = pathlib.Path("literature/search-logs") / f"{SLUG}-screen-log.md"
WANT = pathlib.Path("literature/search-logs") / f"{SLUG}-library-wantlist.md"
SHEET = pathlib.Path("output") / f"{SLUG}-second-review-sheet.csv"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
MAILTO = "shravanh@uchicago.edu"
PMC = "PMC9177776"          # the gold-OA copy of W4224236986

CONFIRMED = {
    "W108787496": ("only DVs are Desired Family Size (Poisson) and Contraceptive Use (multilevel "
                   "logit, Tables 15-18); no table pairs a norm regressor with a fertility outcome"),
    "W1976018943": ("only DVs are unmet need and contraceptive mix; 'number of children' appears "
                    "solely as the text of a survey attitude item"),
    "W2187750596": ("Tables 2-6 each state Pill demand per woman 16-40 is the DV; out-of-wedlock "
                    "births are the regressor"),
}
CHANGED = {
    "W4224236986": {
        "cell": "LINK_NORM_USE", "outcome_level": "USE", "dose_unit": "DERIVABLE",
        "phenomenon_window": "SDT", "estimator_class": "OLS_ADJUSTED",
        "stigma_object": "CONTRACEPTION", "stigma_bearer": "SELF",
        "second_read_required": "done",
        "note": ("SECOND READ CHANGED THIS CALL: was MIXED_NORM_SECULAR. Full text retrieved from "
                 "Europe PMC (gold OA; should have been fetched at stage 5). McLoughlin Brooks and "
                 "Weitzman, Demography 59(3) 2022. The paper does not stop at religiosity - it "
                 "decomposes it, and among the separately measured mediators is 'moral opposition "
                 "to birth control' on a 0-4 scale, with disapproval of premarital sex, anticipated "
                 "guilt after sex, and fear of being stigmatised. That is A.6's construct dosed "
                 "separately from the value it derives from, in a weekly longitudinal panel with a "
                 "mediation design; it also cites Bongaarts and Watkins 1996, one of A.6's four "
                 "registered seminals. Wall 5 gives D.1.a what people value and A.6 what they can "
                 "be seen doing at fixed values; this paper measures both and separates them, so "
                 "routing it wholly to D.1.a was wrong. Outcome is contraceptive use, so link "
                 "evidence, not primary. NOW THE BEST-DESIGNED RECORD IN LINK_NORM_USE, and it "
                 "makes PI call 5 answerable from evidence.")},
    "W4403613268": {
        "cell": "INSUFFICIENT_INFO", "outcome_level": "NONE", "dose_unit": "NONE",
        "phenomenon_window": "SDT", "estimator_class": "OTHER_LOUD",
        "stigma_object": "ABORTION", "stigma_bearer": "COMMUNITY",
        "second_read_required": "blocked",
        "note": ("SECOND READ CHANGED THIS CALL: was CONTEXT_STIGMA_MEASURE assigned on the title "
                 "alone, since OpenAlex holds no abstract. The second read establishes only that it "
                 "cannot be established - oa_status closed at Springer "
                 "(10.1007/s12116-024-09444-0), no OA copy anywhere. A title-based cell behind a "
                 "permanent second-read flag would be a false resolution, so this reverts to "
                 "unresolved and goes on the library wantlist.")},
}
# Fields a blinded reviewer may see. The first-pass cell and note are deliberately NOT here.
BLIND_SRC = ["id", "batch", "stratum", "read_mode", "doi", "year", "title", "fulltext_path"]
BLIND_REVIEW = ["reviewer_name", "review_date", "object_gate_passes", "homonym",
                "exposure_is_normative", "exposure_bundled_with", "estimates_an_effect",
                "outcome_level", "cell_assigned", "dose_unit", "phenomenon_window",
                "estimator_class", "stigma_object", "stigma_bearer", "disagrees_with_first_pass",
                "reviewer_notes"]


def fetch_pmc(pmc_id: str) -> str:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc_id}/fullTextXML"
    p = subprocess.run(["curl", "-s", "-S", "-L", "--max-time", "90",
                        "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    if p.returncode != 0 or "<" not in (p.stdout or "")[:200]:
        return ""
    b = re.sub(r"(?s)<(ref-list|back)\b.*?</\1>", " ", p.stdout)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", b))).strip()


def main():
    rows = list(csv.DictReader(CSVP.open()))
    fields = list(rows[0].keys())

    # persist the full text that changed the call, so the decision is auditable
    body = fetch_pmc(PMC)
    if body and len(body.split()) > 500:
        PDFDIR.mkdir(parents=True, exist_ok=True)
        (PDFDIR / "W4224236986__religiosity-and-young-unmarried-womens-sexual-and-contrace.txt"
         ).write_text(body)
        print(f"saved W4224236986 full text from {PMC}: {len(body.split()):,} words")
    else:
        print(f"WARNING: could not re-fetch {PMC}; the call stands on the read already done",
              file=sys.stderr)

    already = sum(1 for r in rows if r["id"] in CHANGED
                  and r["second_read_required"] in ("done", "blocked"))
    if already == len(CHANGED):
        print("second read already applied — regenerating outputs only")
    else:
        for r in rows:
            if r["id"] in CHANGED:
                r.update(CHANGED[r["id"]])
            elif r["id"] in CONFIRMED:
                r["second_read_required"] = "done"
                r["note"] = (r["note"].rstrip()
                             + f" SECOND READ CONFIRMED: {CONFIRMED[r['id']]}.")
        with CSVP.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"confirmed {len(CONFIRMED)}, changed {len(CHANGED)}")

    rows = list(csv.DictReader(CSVP.open()))
    from collections import Counter
    tally = Counter(r["cell"] for r in rows)
    primary = [r for r in rows if r["cell"] == "PRIMARY_NORM_FERTILITY"]
    link = [r for r in rows if r["cell"] == "LINK_NORM_USE"]
    blocked = [r for r in rows if r["cell"] == "INSUFFICIENT_INFO"]

    # judgment-blinded sheet for a real second reader
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    pool = [r for r in rows if r["second_read_required"] in ("done", "blocked", "yes")]
    # Identify each record for the reviewer. The blinded sheet withholds the first-pass CELL, not
    # the paper's identity - a reviewer who cannot tell which study a row is cannot review it.
    ident = {}
    strata = pathlib.Path("literature/search-logs/a6-screen-strata-2026-09-17.json")
    if strata.exists():
        for rec in json.loads(strata.read_text())["records"]:
            ident[rec["id"]] = {"title": rec.get("title") or "", "year": rec.get("year") or ""}
    retr = pathlib.Path("extraction") / f"{SLUG}-pdf-retrieval-log.csv"
    if retr.exists():
        for rec in csv.DictReader(retr.open()):
            d = ident.setdefault(rec["id"], {})
            d["title"] = d.get("title") or rec.get("title") or ""
            d["year"] = d.get("year") or rec.get("year") or ""
            d["doi"] = rec.get("doi") or ""
    ident.setdefault("W4403613268", {})["doi"] = "10.1007/s12116-024-09444-0"
    with SHEET.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=BLIND_SRC + BLIND_REVIEW, lineterminator="\n")
        w.writeheader()
        for r in pool:
            txt = next(PDFDIR.glob(f"{r['id']}*.txt"), None)
            i = ident.get(r["id"], {})
            w.writerow({"id": r["id"], "batch": r["batch"], "stratum": r["stratum"],
                        "read_mode": r["read_mode"], "doi": i.get("doi", ""),
                        "year": i.get("year", ""), "title": i.get("title", ""),
                        "fulltext_path": str(txt) if txt else "NOT RETRIEVED"})
    print(f"wrote {SHEET} — {len(pool)} rows, first-pass cell withheld")

    marker = "\n## Second read (`418`)\n"
    base = LOGP.read_text().split(marker)[0].rstrip() if LOGP.exists() else ""
    sec = [marker.strip(), "",
           "**This was not an independent second read.** The same reader made all five first-pass",
           "calls, and the point of a second reader is independence. What was done is an",
           "*adversarial self-re-read*: for each record the question was not \"is my call",
           "defensible\" but \"what is the strongest case that this is `PRIMARY_NORM_FERTILITY`, and",
           "does it survive the text\". It caught two errors. It cannot substitute for independence,",
           f"so `{SHEET}` is emitted with the first-pass cell **withheld**, for Alexandra or Anup.",
           "", "| id | first pass | after second read | basis |", "|---|---|---|---|",
           "| `W108787496` | `LINK_NORM_USE` | **confirmed** | only DVs are Desired Family Size and Contraceptive Use; no table pairs a norm regressor with a fertility outcome |",
           "| `W1976018943` | `LINK_NORM_USE` | **confirmed** | only DVs are unmet need and method mix; \"number of children\" appears only as a survey attitude item |",
           "| `W2187750596` | `LINK_NORM_USE` | **confirmed** | Tables 2–6 each state Pill demand is the DV; out-of-wedlock births are the regressor |",
           "| `W4224236986` | `MIXED_NORM_SECULAR` | **CHANGED to `LINK_NORM_USE`** | the paper decomposes religiosity and separately doses \"moral opposition to birth control\" on a 0–4 scale |",
           "| `W4403613268` | `CONTEXT_STIGMA_MEASURE` | **CHANGED to `INSUFFICIENT_INFO`** | the call rested on the title; closed at Springer, no OA copy, so it cannot be resolved |",
           "",
           "### The change that matters", "",
           "`W4224236986` (McLoughlin Brooks and Weitzman, *Demography* 2022) was routed wholly to",
           "D.1.a on the reasoning that religiosity is a value. That was too crude. The paper",
           "decomposes religiosity, and among its separately measured mediators is **\"moral",
           "opposition to birth control\" on a 0–4 scale**, with disapproval of premarital sex,",
           "anticipated guilt after sex, and fear of being stigmatised. Wall 5 gives D.1.a *what",
           "people value* and A.6 *what they can be seen doing at fixed values* — this paper",
           "measures both and separates them. It is a weekly longitudinal panel with a mediation",
           "design and it cites Bongaarts and Watkins 1996, one of A.6's four registered seminals.",
           "It is now the **best-designed record in `LINK_NORM_USE`**, and it makes PI call 5",
           "answerable from evidence rather than from taste.", "",
           "It was also **gold open access all along** and should have been retrieved at stage 5;",
           "`412` never fetched it because the screen had not flagged it as `INSUFFICIENT_INFO`.",
           "That is a gap in the pipeline, not in this record: **a borderline routing call can need",
           "full text just as much as an unresolved one**, and only the latter was queued for",
           "retrieval.", "",
           f"### `PRIMARY_NORM_FERTILITY`: **{len(primary)}** — unchanged by the second read", "",
           f"`LINK_NORM_USE` rises to **{len(link)}**. Unresolved returns to **{len(blocked)}**",
           "(`W4403613268`, closed at Springer).", "",
           f"### Tally across {len(rows)} screened records", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        sec.append(f"| `{c}` | {n} |")
    LOGP.write_text(base + "\n\n" + "\n".join(sec) + "\n")

    if blocked:
        w = WANT.read_text() if WANT.exists() else f"# A.6 library wantlist\n"
        add = ["", "## Added by the second read (`418`)", ""]
        for r in blocked:
            add.append(f"- `{r['id']}` — *Abortion Within Reason or Right: Navigating Reproductive "
                       f"Governance and Abortion Stigma in Madagascar's Urban …* (2024), "
                       f"`10.1007/s12116-024-09444-0`, Studies in Comparative International "
                       f"Development. Closed at Springer, no OA copy. Screened on title only; the "
                       f"cell cannot be confirmed without full text.")
        WANT.write_text(w.rstrip() + "\n" + "\n".join(add) + "\n")
        print(f"appended {len(blocked)} record(s) to the wantlist")

    print(f"PRIMARY_NORM_FERTILITY={len(primary)}  LINK_NORM_USE={len(link)}  "
          f"unresolved={len(blocked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
