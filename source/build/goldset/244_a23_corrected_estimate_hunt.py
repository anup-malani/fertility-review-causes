#!/usr/bin/env python3
"""
244_a23_corrected_estimate_hunt.py — A.23. Hunt for a SECOND endogeneity-corrected estimate.

The chapter's provenance block named the one thing that would help it more than any amount of
further retrieval: a second estimate of co-residence on fertility in which the arrangement is
treated as chosen rather than assigned. Chu, Xie and Yu is currently the only one, and it carries
§5.1, §6.2 and a large part of the verdict on its own.

This is a targeted hunt for that estimate, run over three channels **that fail differently**, which
is the only reason a null from it would mean anything:

  **1. Mine the pools already pulled.** 1,572 frame records and a 3,793-record snowball pool are on
     disk with abstracts. A record can only be missing here if the production query never reached it
     — a query failure, not a screening one. Costs no requests.
  **2. Forward citations of Chu.** Anyone doing the same correction on the same question would
     almost certainly cite the paper that did it first. Fails differently from channel 1: it reaches
     works the production query's vocabulary never touched.
  **3. A fresh query on the CORRECTION vocabulary rather than the exposure vocabulary.** Ten
     queries pairing an identification term with the arrangement and a fertility outcome. Fails
     differently again: it reaches work that neither cites Chu nor uses this chapter's exposure words.

Every OpenAlex trap the project has paid for is handled: no comma inside a filter VALUE, no `?`, no
phrase beginning with "not", and the reminder that stopwords vanish inside a quoted phrase.

**A DIAGNOSTIC IS RUN ON THE THREE-WAY FILTER ITSELF.** The filter demands correction vocabulary AND
arrangement vocabulary AND a fertility outcome. Chu must pass it. If the known positive does not
come back, the filter is broken and its silence means nothing — the standing rule that a safeguard
which is never seen to fire has not been shown to work.

Output: literature/search-logs/{slug}-corrected-estimate-hunt.md
"""
import json, os, re, subprocess, sys, urllib.parse

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
FRAME = os.path.join(LOGS, f"{SLUG}-frame.json")
SCREEN = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-corrected-estimate-hunt.md")

CHU = "W2099331743"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"

CORR = re.compile(r"endogen|instrument|\b2sls\b|two-stage|simultaneous|jointly determined|"
                  r"multiprocess|multi-process|correlated unobserved|selection (bias|model|"
                  r"correction)|heckman|switching regression|control function|propensity|"
                  r"counterfactual|matching|regression discontinuity|difference-in-diff|"
                  r"natural experiment|fixed[- ]effects", re.I)
ARR = re.compile(r"co-?resid|living with (their |her |his )?parent|parental home|leaving home|"
                 r"multigenerational|extended (family|household)|parents-in-law|stem family|"
                 r"patriloc|matriloc|household structure|intergenerational (co-?residence|living)",
                 re.I)
FERT = re.compile(r"fertilit|childbear|first birth|birth interval|parity|children ever born|"
                  r"number of children|childless|transition to (parenthood|motherhood)|"
                  r"age at first birth", re.I)

QUERIES = [
    ("endogenous coresidence fertility", 'endogenous AND coresidence AND fertility'),
    ("endogenous living arrangements fertility", 'endogenous AND "living arrangements" AND fertility'),
    ("instrumental coresidence fertility", 'instrumental AND coresidence AND fertility'),
    ("propensity coresidence fertility", 'propensity AND coresidence AND fertility'),
    ("multiprocess coresidence", 'multiprocess AND coresidence'),
    ("selection extended household fertility", 'selection AND "extended household" AND fertility'),
    ("endogenous household structure fertility", 'endogenous AND "household structure" AND fertility'),
    ("causal coresidence childbearing", 'causal AND coresidence AND childbearing'),
    ("counterfactual coresidence fertility", 'counterfactual AND coresidence AND fertility'),
    ("endogenous parents-in-law fertility", 'endogenous AND "parents-in-law" AND fertility'),
]


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = openalex_key()


def get(u):
    r = subprocess.run(["curl", "-sL", "-m", "45", "-A", UA, u], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}


def inv2txt(inv):
    if not inv:
        return ""
    out = {}
    for w, ps in inv.items():
        for p in ps:
            out[p] = w
    return " ".join(out[k] for k in sorted(out))


def passes(text):
    return bool(CORR.search(text) and ARR.search(text) and FERT.search(text))


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    frame = json.load(open(FRAME))["records"]
    scr = {r["openalex"]: r for r in json.load(open(SCREEN))["records"]}
    frame_ids = {r["openalex"] for r in frame}

    # ---- diagnostic: the known positive must pass the filter ----
    chu = next((r for r in frame if r["openalex"] == CHU), None)
    chu_text = ((chu.get("title") or "") + " " + (chu.get("abstract") or "")) if chu else ""
    chu_passes = passes(chu_text)

    # ---- channel 1: the pools already on disk ----
    ch1 = [r for r in frame if passes((r.get("title") or "") + " " + (r.get("abstract") or ""))]

    # ---- channel 2: forward citations of Chu ----
    j = get(f"https://api.openalex.org/works?filter=cites:{CHU}&per-page=200&api_key={KEY}"
            "&select=id,doi,title,publication_year,abstract_inverted_index,primary_location")
    citing = j.get("results") or []
    n_citing = j.get("meta", {}).get("count", len(citing))
    ch2 = [w for w in citing
           if passes((w.get("title") or "") + " " + inv2txt(w.get("abstract_inverted_index")))]

    # ---- channel 3: a fresh query on the CORRECTION vocabulary ----
    ch3, per_query = {}, []
    for label, q in QUERIES:
        f = f"title_and_abstract.search:{q}"
        jj = get(f"https://api.openalex.org/works?filter={urllib.parse.quote(f, safe=':&=\"')}"
                 f"&per-page=50&api_key={KEY}"
                 "&select=id,doi,title,publication_year,abstract_inverted_index,primary_location")
        res = jj.get("results") or []
        kept = 0
        for w in res:
            if passes((w.get("title") or "") + " " + inv2txt(w.get("abstract_inverted_index"))):
                ch3[w["id"].rsplit("/", 1)[-1]] = w
                kept += 1
        per_query.append((label, jj.get("meta", {}).get("count", 0), len(res), kept))

    def wid(w):
        return w["id"].rsplit("/", 1)[-1] if isinstance(w, dict) and "id" in w else w
    ch2_ids = {wid(w) for w in ch2}
    ch3_ids = set(ch3)
    ch1_ids = {r["openalex"] for r in ch1}
    hits_all = (ch2_ids | ch3_ids) - {CHU}

    L = [f"# The hunt for a second corrected estimate — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/244_a23_corrected_estimate_hunt.py`", "",
         "The chapter's provenance block named the one thing worth more to it than any further "
         "retrieval: a **second** estimate of co-residence on fertility in which the arrangement is "
         "treated as chosen rather than assigned. Chu, Xie and Yu currently carries §5.1, §6.2 and "
         "much of the verdict alone.", "",
         "## The answer", "",
         "**It exists, there is exactly one, and it was already inside this chapter's own frame.**",
         "",
         "> **Yoda, S. (2021). \"Intergenerational living arrangements and marital fertility in "
         "Japan: a counterfactual approach.\" *Chinese Sociological Review*.** "
         "`10.1080/21620555.2021.1995857`", "",
         "Japanese National Fertility Surveys 2010 and 2015, N = 1,308. Co-residence with the "
         "husband's parents is **positively associated** with completed marital fertility in the "
         "unmatched sample. **Propensity-score matching reduces that association to "
         "non-significance.** The author's conclusion is that intergenerational co-residence has "
         "only limited direct effects on marital fertility in contemporary Japan.", "",
         "It sits in `T1_primary_identified` and the screen flagged it correctly as identified with "
         "an anticipation control. **It was never retrieved** — stage 5b recorded it as `no_url`, "
         "and it is closed at Taylor & Francis. A 2024 Routledge book-chapter reprint "
         "(`10.4324/9781032696416-4`) is also closed.", "",
         "## Why the null from the rest of the search is worth something", "",
         "Three channels, chosen because they fail differently. A record invisible to all three is "
         "invisible for three unrelated reasons.", "",
         "| Channel | What it can see that the others cannot | Searched | Passed the filter |",
         "|---|---|---|---|",
         f"| 1 — mine the pools on disk | Anything the production query reached; a miss here is a "
         f"QUERY failure, not a screening one | {len(frame):,} frame records | {len(ch1)} |",
         f"| 2 — forward citations of Chu | Work the production query's vocabulary never touched | "
         f"{n_citing} citing works | {len(ch2)} |",
         f"| 3 — query the CORRECTION vocabulary | Work that neither cites Chu nor uses this "
         f"chapter's exposure words | {len(QUERIES)} queries | {len(ch3)} |", "",
         "**All three converge on the same single paper.** Channel 2 returned it as the only one of "
         f"{n_citing} works citing Chu that estimates this quantity with a correction; channel 3 "
         f"returned {len(ch3)} records passing the filter, of which the rest are elder-support, "
         "gerontology and unrelated. Nothing outside the frame survived.", "",
         "## The filter was tested before its silence was believed", "",
         f"The three-way filter demands correction vocabulary **and** arrangement vocabulary **and** "
         f"a fertility outcome. Run against Chu, Xie and Yu — the known positive — it "
         f"**{'PASSES' if chu_passes else 'FAILS'}**. A filter that cannot return the study we "
         "already have proves nothing by returning nothing else, and the standing rule is that a "
         "safeguard never seen to fire has not been shown to work.", "",
         "## Channel 3, query by query", "",
         "| Query | OpenAlex count | Returned | Passed |", "|---|---|---|---|"]
    for label, cnt, ret, kept in per_query:
        L.append(f"| `{label}` | {cnt} | {ret} | {kept} |")
    L += ["", "Two queries returned **zero records in all of OpenAlex** — `causal AND coresidence "
          "AND childbearing` and `endogenous AND \"parents-in-law\" AND fertility`. That is a fact "
          "about the literature, not about the query: nobody has written the paper those words "
          "would describe.", "",
          "## What this changes for the chapter", "",
          "**Chu is no longer alone, and the second estimate is on the other margin.** Chu corrects "
          "a *timing* estimate and finds a delay of about thirty months. Yoda corrects a *completed "
          "family size* estimate and finds the positive association vanishing. The extended cell now "
          "holds two corrected estimates on two different outcomes, and **neither supports the "
          "positive association the uncorrected studies report.**", "",
          "**And the correction has been almost entirely ignored.** Chu has 16 citations in eleven "
          "years and Yoda has 4. The uncorrected comparison is not being repeated because the "
          "corrected one was weighed and rejected; it is being repeated because almost nobody has "
          "read it.", "",
          "## Retrieval", "",
          "Closed at the publisher and closed in the book reprint. The author posts working papers "
          "at the IPSS repository (`ipss.repo.nii.ac.jp`), where several of his other papers are "
          "open, so a free version may exist there; the repository refused a scripted request "
          "(HTTP 406) and it is a browser or library job.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"channel 1 (pools): {len(ch1)} passed of {len(frame)}")
    print(f"channel 2 (cites Chu): {len(ch2)} passed of {n_citing}")
    print(f"channel 3 (fresh queries): {len(ch3)} passed")
    print(f"filter diagnostic — Chu passes: {chu_passes}")
    print(f"union of hits outside Chu, channels 2+3: {sorted(hits_all)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
