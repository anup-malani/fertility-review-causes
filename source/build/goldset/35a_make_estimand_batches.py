#!/usr/bin/env python3
"""
Step 35a - Build the BLIND estimand-classification input for calibrating the automated gate.

Point 1's gate (step 34) ran on the RA's human adjudication. For a NEW hypothesis there is no RA
pass: the gate must run on Sonnet's extracted fields (GACS §D2b). This step sets up the calibration
that measures how well an automated Sonnet estimand-classification agrees with the RA ground truth on
the pilot's 40 reviewed studies -- so the production gate inherits a MEASURED precision, not an
assumed one.

The classifier is kept blind: it sees only {title, abstract, year, authors} -- the inputs D2b has --
and NOT the RA decision, and NOT the pilot's earlier relevance `scoreRationale`/`mechanism` (which
would leak the answer). The RA ground truth is written to a SEPARATE key file the classifier never
sees; only the scorer (35b) reads it.

Inputs
  {slug}-metaanalysis-studies.json     the 40 DOI-trusted reviewed studies (paperId, title, doi...)
  {slug}-oa-enrichment.json            abstracts, keyed by paperId
  output/{slug}-estimand-adjudication.csv   RA ground truth (from step 34)
Outputs (temp/estimand-calib/)
  input.json    blind classifier input (NO labels)
  PROMPT.md     the estimand-cell rubric handed to the classifier
  key.json      RA ground truth, held out of the classifier
"""
import json, csv
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SL = REPO / "literature" / "search-logs" / f"{SLUG}-"
ADJ = REPO / "output" / f"{SLUG}-estimand-adjudication.csv"
OUT = REPO / "temp" / "estimand-calib"
OUT.mkdir(parents=True, exist_ok=True)


def norm_doi(v):
    v = (v or "").strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi:"):
        if v.startswith(p):
            v = v[len(p):]
    return v


PROMPT = """# Estimand-and-mechanism classification (old-age-security -> fertility chapter)

You are the precision judge (GACS Phase D2b) deciding, for each paper, whether it identifies THIS
chapter's effect. The corpus is already screened as topically about pensions/old-age security and
fertility -- your job is NARROWER: does the paper estimate the chapter's **primary estimand cell**?

**Primary cell** = the causal effect of the **old-age-security motive** (pensions / social security /
children-as-old-age-support) **ON fertility** -- i.e. fertility is the OUTCOME, the direction is
forward (cause -> fertility), and the mechanism is old-age-security crowd-out of the demand for
children (a pension makes children less needed as old-age support, so fertility falls).

For each paper, first extract three things from the title/abstract, then assign ONE cell.

Extract:
- `outcome`: the study's dependent variable (what it estimates the effect ON).
- `direction`: "forward" if cause->fertility; "reverse" if fertility->something; "fertility-as-cause"
  if fertility is a right-hand-side treatment/instrument.
- `mechanism`: the channel (old-age-security crowd-out; grandparental childcare; income; etc.).

Assign exactly one `cell`:
- `PRIMARY` -- OAS motive -> fertility, forward, fertility is the outcome.
- `OFF:outcome-not-fertility` -- fertility is NOT the outcome (outcome is schooling, parental
  survival, labor supply, savings, migration, health, birth weight, coresidence, etc.).
- `OFF:different-channel` -- pension/retirement DOES affect fertility, but through a channel OTHER
  than OAS crowd-out -- classically grandparental childcare (retired grandparents supply childcare,
  which RAISES daughters' fertility: opposite sign).
- `OFF:fertility-as-cause` -- fertility is the treatment / right-hand-side variable, not the outcome.
- `OFF:reverse-direction` -- the study estimates the effect of children/fertility ON old-age support,
  pension take-up, or savings (the reverse chain).
- `OFF:different-cause` -- the treatment is NOT old-age security/pensions (e.g. child-grant subsidy,
  lottery income, female employment, kindergarten supply, welfare family cap, minimum-marriage-age).
- `OFF:off-topic` -- not about old-age security at all.

Judge each paper independently on ITS OWN title/abstract. If the abstract is missing, judge on the
title and be conservative. Return a JSON array, one object per input id, preserving every id:
[{"id":"<id>","outcome":"<...>","direction":"forward|reverse|fertility-as-cause",
  "mechanism":"<short>","cell":"PRIMARY|OFF:...","reason":"<=160 chars"}]
Output ONLY the JSON array.
"""


def main():
    studies = json.load(open(f"{SL}metaanalysis-studies.json"))
    enrich = json.load(open(f"{SL}oa-enrichment.json"))
    # ground-truth cell/decision from step 34's adjudication, keyed by normalized DOI
    truth = {}
    for r in csv.DictReader(open(ADJ)):
        truth[norm_doi(r["doi"])] = {
            "ra_decision": r["ra_decision"], "estimand_cell": r["estimand_cell"],
            "off_cell_reason": r["off_cell_reason"], "is_gold_anchor": r["is_gold_anchor"],
            "gold_id": r["gold_id"], "title": r["title"],
        }

    trusted = [s for s in studies
               if (s.get("doi_final") or s.get("doi")) and s.get("doi_trust") != "UNRESOLVED"]

    blind, key = [], {}
    for s in trusted:
        pid = s.get("paperId")
        doi = norm_doi(s.get("doi_final") or s.get("doi"))
        e = enrich.get(pid, {}) if pid else {}
        abstract = e.get("abstract") or s.get("abstract")
        authors = s.get("authors")
        if isinstance(authors, list):
            authors = "; ".join(str(a) for a in authors if a)
        rec_id = doi or pid
        blind.append({
            "id": rec_id, "title": s.get("title"), "year": s.get("year"),
            "authors": authors, "abstract": abstract,
            "has_abstract": bool(abstract),
        })
        key[rec_id] = {**truth.get(doi, {"estimand_cell": "?", "ra_decision": "?"}), "doi": doi, "paperId": pid}

    json.dump(blind, open(OUT / "input.json", "w"), indent=2)
    json.dump(key, open(OUT / "key.json", "w"), indent=2)
    (OUT / "PROMPT.md").write_text(PROMPT)

    tl = sum(1 for b in blind if not b["has_abstract"])
    print(f"{len(blind)} studies -> blind input.json ({tl} title-only), key.json (ground truth held out)")
    print(f"calib dir: {OUT}")
    print("next: classify input.json with Sonnet (blind), freeze to estimand_calib_sonnet.json, run 35b")


if __name__ == "__main__":
    main()
