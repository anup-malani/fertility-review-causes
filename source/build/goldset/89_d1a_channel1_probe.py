#!/usr/bin/env python3
"""
89_d1a_channel1_probe.py — D.1.a (postmaterialism / individualism / secularization), stage A3.

COLD-START CHANNEL 1 PROBE, run per PAIR rather than per hypothesis.

The scope doc (`{slug}-search-scope.md`, Ruling 1) defines this chapter as FIVE treatment x outcome
pairs sharing one chapter, and predicts channel 1 will be pair-asymmetric: reviews and meta-analyses
of religion -> fertility plausibly exist and would be the privileged S3 seed, while a systematic
review of postmaterialism -> fertility very likely does not. That prediction is testable before any
anchor is committed, and this script tests it.

Discipline carried from 72 (D.3.b) and 64 (B.1):
  * NOTHING here asserts a DOI, a title, or an author from memory. Every record printed is whatever
    the live OpenAlex API returned today. Verification against Crossref/doi.org is a SEPARATE later
    step; a hit here is a CANDIDATE, never an anchor.
  * Channel 1 is declared EMPTY for a pair only after multiple probe forms fail, following the C.2.c
    precedent (four probe forms were run before concluding channel 1 was empty there). A single failed
    lookup is not evidence of non-existence -- that lesson cost a false ghost call on the C.2.c run.
  * Probe forms are recorded verbatim in the output so the negative result is reproducible and
    auditable. An empty channel 1 is a REPORTABLE FINDING, not a search failure.

LEAKAGE WALL (GACS A3, channel 1): a review found here may feed its INCLUDED STUDIES as anchors, or
its SEARCH STRING as query terms, but never both from the same review.

Output: temp/d1a/channel1-probe.json   (raw, every hit)
        temp/d1a/channel1-probe.md     (readable summary for RA assessment)
"""
import json, os, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTDIR = os.path.join(ROOT, "temp", "d1a")
os.makedirs(OUTDIR, exist_ok=True)
OUT_JSON = os.path.join(OUTDIR, "channel1-probe.json")
OUT_MD = os.path.join(OUTDIR, "channel1-probe.md")

API = "https://api.openalex.org/works"
PER_PAGE = 25

# The fertility outcome axis, held constant across every probe. Half of the treatment x outcome pair.
#
# RUN-1 FINDING (2026-08-03), and it is a production-query problem, not a screening problem. The first
# pass of this probe used a bare `fertility OR births OR ... OR "birth rate"` outcome axis with no field
# restriction, and every one of the five pairs came back swamped by clinical and perinatal medicine:
# "fertility" reads as IVF and infertility treatment, "birth" reads as birth weight and birth cohort,
# and OpenAlex's stemming matched "individualism" to "individualiSED dosing of follitropin delta" and
# "consumer" to "direct-to-consumer telemedicine". The top-cited hit across three separate pairs was a
# systematic review of antenatal care utilisation. This is the same class of collision the C.2.c run
# found for `housing AND fertility` (livestock housing, soil fertility) and it has to be handled in the
# query, or it is paid for in screening cost. Two fixes applied below: demographic-specific outcome
# vocabulary, and a field restriction.
OUTCOME = ("fertility OR childbearing OR \"family size\" OR parity OR childlessness "
           "OR \"fertility intentions\" OR \"fertility behavior\" OR \"fertility decline\" "
           "OR \"total fertility rate\" OR \"number of children\" OR \"completed fertility\" "
           "OR \"fertility differentials\"")

# Field restriction: the four OpenAlex fields this literature actually lives in (Social Sciences,
# Economics/Econometrics/Finance, Psychology, Arts and Humanities). Comma-separated values inside one
# filter key are OR'd. This is a deliberate recall/precision trade recorded rather than hidden: a
# genuinely relevant paper indexed under Medicine will be missed here, which is acceptable for a
# CHANNEL-1 REVIEW PROBE and would NOT be acceptable for the production query.
FIELDS = ("primary_topic.field.id:fields/33|fields/20|fields/32|fields/12")

# Treatment axis, one entry per pair (scope doc, Ruling 1). These are the CAUSE-side vocabularies.
PAIRS = {
    "S1_POSTMATERIALISM": 'postmaterialism OR postmaterialist OR "post-materialist" OR "value change" '
                          'OR "self-expression values" OR Inglehart OR "ideational change" '
                          'OR "second demographic transition"',
    "S2_INDIVIDUALISM": 'individualism OR individualisation OR individualization OR autonomy '
                        'OR "kinship intensity" OR collectivism OR "cultural values"',
    "S3_SECULARIZATION": 'religiosity OR religion OR secularization OR secularisation '
                         'OR "religious affiliation" OR "church attendance" OR "religious participation"',
    "S4_CHILDLESSNESS_NORM": '"voluntary childlessness" OR childfree OR "childless by choice" '
                             'OR "attitudes toward childlessness"',
    "S5_CONSUMERISM": 'consumerism OR materialism OR "material values" OR "consumption aspirations" '
                      'OR "lifestyle aspirations"',
}

# Probe forms. Each is (name, builder). Multiple forms per pair is the C.2.c requirement: a pair is
# declared channel-1 empty only when EVERY form comes back empty.
def forms(treatment):
    q_both = f"({treatment}) AND ({OUTCOME})"
    return [
        ("F1_review_type",
         {"filter": f"title_and_abstract.search:{q_both},type:review,{FIELDS}", "per-page": PER_PAGE,
          "sort": "cited_by_count:desc"}),
        ("F2_title_synthesis_language",
         {"filter": f"title.search:({treatment}) AND ({OUTCOME}) AND "
                    f"(\"systematic review\" OR \"meta-analysis\" OR \"meta analysis\" "
                    f"OR \"review\" OR \"synthesis\"),{FIELDS}",
          "per-page": PER_PAGE, "sort": "cited_by_count:desc"}),
        ("F3_abstract_synthesis_language",
         {"filter": f"title_and_abstract.search:{q_both} AND "
                    f"(\"systematic review\" OR \"meta-analysis\" OR \"scoping review\" "
                    f"OR \"literature review\" OR \"research synthesis\"),{FIELDS}",
          "per-page": PER_PAGE, "sort": "cited_by_count:desc"}),
        ("F4_topical_top_cited",
         {"filter": f"title_and_abstract.search:{q_both},{FIELDS}", "per-page": PER_PAGE,
          "sort": "cited_by_count:desc"}),
    ]


def fetch(params, tries=4):
    """GET with retry. A network failure is UNCONFIRMED, never ABSENT -- the three-state rule.

    Uses curl rather than urllib, matching 72/64: this machine's Python has no usable CA bundle and
    urllib fails every request with CERTIFICATE_VERIFY_FAILED. That failure mode is exactly why the
    three-state rule exists -- read as ABSENT it would have reported channel 1 empty for all five
    pairs, which is the finding the scope predicted for three of them and would have looked plausible.
    """
    params = dict(params)
    params["mailto"] = MAILTO
    url = API + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(tries):
        try:
            out = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url],
                                 capture_output=True, text=True)
            if out.returncode != 0:
                last = f"curl exit {out.returncode}: {out.stderr[:200]}"
            else:
                data = json.loads(out.stdout)
                if "results" in data:
                    return url, data, None
                last = f"unexpected payload: {out.stdout[:200]}"
        except Exception as e:  # noqa: BLE001 -- any failure here is a retryable transport failure
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 * (attempt + 1))
    return url, None, last


def invert_abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def slim(w):
    pl = w.get("primary_location") or {}
    src = pl.get("source") or {}
    return {
        "work_id": (w.get("id") or "").rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": w.get("title") or "",
        "year": w.get("publication_year"),
        "type": w.get("type"),
        "venue": src.get("display_name") or "",
        "cited_by": w.get("cited_by_count"),
        "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])[:6]],
        "abstract_head": invert_abstract(w.get("abstract_inverted_index"))[:300],
    }


def main():
    out = {"slug": SLUG, "probe": "cold-start channel 1, per pair", "outcome_axis": OUTCOME,
           "pairs": {}}
    for pair, treatment in PAIRS.items():
        print(f"\n=== {pair} ===", file=sys.stderr)
        rec = {"treatment_axis": treatment, "forms": {}}
        for name, params in forms(treatment):
            url, data, err = fetch(params)
            if data is None:
                rec["forms"][name] = {"url": url, "status": "UNCONFIRMED", "error": err}
                print(f"  {name}: UNCONFIRMED ({err})", file=sys.stderr)
                continue
            hits = [slim(w) for w in data.get("results", [])]
            rec["forms"][name] = {
                "url": url,
                "status": "OK",
                "total_count": data.get("meta", {}).get("count"),
                "returned": len(hits),
                "hits": hits,
            }
            print(f"  {name}: count={data['meta']['count']} returned={len(hits)}", file=sys.stderr)
            time.sleep(0.4)
        out["pairs"][pair] = rec

    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)

    lines = [f"# D.1.a cold-start channel-1 probe — raw results",
             "",
             "Live OpenAlex, run by `89_d1a_channel1_probe.py`. Every line below is API output.",
             "Nothing here is verified yet: these are CANDIDATES, and a candidate becomes an anchor",
             "only after the Crossref + doi.org existence gate.",
             ""]
    for pair, rec in out["pairs"].items():
        lines += [f"## {pair}", ""]
        for name, fr in rec["forms"].items():
            if fr["status"] != "OK":
                lines += [f"### {name} — **{fr['status']}** ({fr.get('error')})", ""]
                continue
            lines += [f"### {name} — total {fr['total_count']}, showing {fr['returned']}", ""]
            if not fr["hits"]:
                lines += ["*(no hits)*", ""]
            for h in fr["hits"]:
                lines.append(f"- [{h['cited_by']}c, {h['year']}, {h['type']}] {h['title']}  "
                             f"— *{h['venue']}* — `{h['doi'] or 'NO-DOI'}`")
            lines.append("")
    with open(OUT_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"\nwrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
