#!/usr/bin/env python3
r"""
105_d1a_stem_audit.py — D.1.a. Does OpenAlex actually execute the query we validated?

WHY THIS EXISTS. A6b cross-validated the production query offline, matching compiled terms against
stored titles, and reported Recall(B-only) 92.1%. The live C1 pull returned 80.8%. The pull script
anticipated a gap and called it "a finding about the index rather than about the query". It is
neither: it is a finding that THE VALIDATED QUERY AND THE EXECUTED QUERY ARE DIFFERENT QUERIES.

The production query carries wildcard stems (`secular*`, `religio*`, `procreat*`). OpenAlex rejects
a query containing a star outright, so `103_d1a_live_search.oa_term()` STRIPS the star and sends the
bare stem. That is only safe if the stem is itself a word that stems to the same root as its
inflections. This script measures, for every wildcard term in the frozen query, what the stripped
stem actually retrieves.

TWO DISTINCT FAILURE MODES, AND THE SECOND IS INVISIBLE TO A COUNT.

  (a) DEAD STEM -- the stripped stem is not a word and retrieves ~nothing.
      `procreat` = 0, `nuptialit` = 0, `postmaterialis` = 0, `childbear` = 0, `fertilit` = 63.

  (b) LIVE BUT WRONG -- the stem is a word, returns a healthy count, and still does not match the
      inflection it was meant to cover. `secular` returns 34,326 records and does NOT match
      "Secularization"; `religio` returns 2,041 and does NOT match "Religiously". A count-only audit
      passes both of these. Only a membership test against a known paper catches them.

So the script does both: a count for every wildcard stem, and a conjunctive membership test
(`filter=doi:<doi>,title.search:<term>`) against named papers that the live pull missed.

THIS CORRECTS THE CORRECTION AT `654a491`. That commit retracted A6c's "no prefix matching" reading
on the evidence that `childless` and `childlessness` both return 2,586 -- one postings list -- and
concluded no wildcard expansion was needed. The generalisation was drawn from a single pair. It
holds for inflection (childless/childlessness) and fails for derivation (secular/secularization,
religious/religiously), which is most of this query's vocabulary.

Entity lookup by DOI is free under OpenAlex's pricing; only the `title.search` counts are billed, at
$0.001 each. The whole audit is well under a dime.

Usage:
  python3 105_d1a_stem_audit.py            # cached; re-run is free
  python3 105_d1a_stem_audit.py --refresh  # ignore cache

Output: literature/search-logs/{slug}-stem-audit.{json,md}
"""
import json, os, re, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
PQ = os.path.join(LOGS, f"{SLUG}-production-query.json")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-stem-audit.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-stem-audit.md")
CACHE = os.path.join(HERE, "d1a_stem_audit_cache.json")

KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
UA = "fertility-review/1.0 (mailto:shravanh@uchicago.edu)"
DEAD_BELOW = 200          # a stem retrieving under this is not doing the job its wildcard promised

# Papers the live pull missed, with the DOI that proves they ARE in OpenAlex. Two of the chapter's
# three Tier-1 natural experiments -- the entire stratum is three studies, so this is not a rounding
# error in a recall percentage.
MEMBERSHIP_TESTS = [
    ("10.1016/j.ssresearch.2026.103371",
     "Secularization and low fertility: how declining church membership changes childbearing",
     ["secular", "secularization", "secularisation", "church", "church attendance",
      "fertility", "childbearing", "childbear"]),
    ("10.1007/s00148-025-01092-5",
     "Religiously inspired baby boom: evidence from Georgia",
     ["religio", "religious", "religiously", "religiosity", "baby boom", "fertility"]),
    ("10.1086/696193",
     "Political Islam, Marriage and Fertility (retrieved -- negative control)",
     ["islam", "marriage", "fertility"]),
]


def load_cache():
    if os.path.exists(CACHE) and "--refresh" not in sys.argv:
        with open(CACHE) as fh:
            return json.load(fh)
    return {}


def oa(params, cache, ck):
    if ck in cache:
        return cache[ck]
    if KEY:
        params = {**params, "api_key": KEY}
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    p = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
        n = (d.get("meta") or {}).get("count")
    except Exception:
        n = None
    if n is not None:
        cache[ck] = n
        with open(CACHE, "w") as fh:
            json.dump(cache, fh)
    time.sleep(0.15)
    return n


def main():
    if not KEY:
        print("OPENALEX_API_KEY not set -- unauthenticated requests will be refused on budget.",
              file=sys.stderr)
    cache = load_cache()
    pq = json.load(open(PQ))
    groups = {"OUTCOME": pq["outcome_terms"], **pq["treatment_clusters"]}

    rows, dead = [], []
    for g, terms in groups.items():
        for t in sorted({x for x in terms if "*" in x}):
            stem = re.sub(r"[*?]", "", t).strip()
            n = oa({"filter": f"title.search:{stem}", "per-page": 1, "select": "id"},
                   cache, f"count::{stem}")
            row = {"cluster": g, "query_term": t, "sent_as": stem, "count": n,
                   "dead": n is not None and n < DEAD_BELOW}
            rows.append(row)
            if row["dead"]:
                dead.append(row)

    member = []
    for doi, label, terms in MEMBERSHIP_TESTS:
        for t in terms:
            n = oa({"filter": f"doi:https://doi.org/{doi},title.search:{t}",
                    "per-page": 1, "select": "id"}, cache, f"member::{doi}::{t}")
            member.append({"doi": doi, "paper": label, "term": t,
                           "matches": (n == 1), "count": n})

    out = {"slug": SLUG, "stage": "C1-diagnostic", "dead_below": DEAD_BELOW,
           "n_wildcard_terms": len(rows), "n_dead": len(dead),
           "terms": rows, "membership_tests": member}
    json.dump(out, open(OUT_JSON, "w"), indent=1)

    L = ["# D.1.a — does OpenAlex execute the query we validated?", "",
         "A6b cross-validated the production query **offline**, matching compiled terms against "
         "stored titles, and reported Recall(B-only) **92.1%**. The live C1 pull returned "
         "**80.8%**. `103_d1a_live_search.py` anticipated a gap and called it *\"a finding about the "
         "index rather than about the query\"*. It is neither. **The validated query and the "
         "executed query are different queries.**", "",
         "The frozen query carries wildcard stems. OpenAlex rejects a star outright, so the pull "
         "strips it and sends the bare stem. That is safe only when the stem is itself a word that "
         "stems to the same root as its inflections.", "",
         f"- wildcard terms in the frozen query: **{len(rows)}**",
         f"- **dead stems** (retrieve under {DEAD_BELOW} records): **{len(dead)}**", "",
         "## Failure mode (a) — dead stems", "",
         "| cluster | query term | sent as | live count |", "|---|---|---|---|"]
    L += [f"| `{r['cluster']}` | `{r['query_term']}` | `{r['sent_as']}` | **{r['count']}** |"
          for r in dead]
    L += ["", "## Failure mode (b) — live but wrong, and invisible to a count", "",
          "A healthy count does not mean the stem covers the inflection it was written for. "
          "**`secular` returns 34,326 records and does not match \"Secularization\"; `religio` "
          "returns 2,041 and does not match \"Religiously\".** A count-only audit passes both. Only "
          "a membership test against a known paper catches it.", "",
          "Conjunctive test: `filter=doi:<doi>,title.search:<term>` — count 1 means the term "
          "retrieves that paper.", ""]
    for doi, label, _ in MEMBERSHIP_TESTS:
        L += [f"**{label}**  ", f"`{doi}`", "", "| term | retrieves it? |", "|---|---|"]
        for m in [x for x in member if x["doi"] == doi]:
            L.append(f"| `{m['term']}` | {'**yes**' if m['matches'] else 'no'} |")
        L.append("")
    L += ["## What this costs the chapter", "",
          "1. **Two of the three Tier-1 natural experiments are missing from the live corpus.** The "
          "entire Tier-1 stratum is three studies, so this is not a rounding error in a recall "
          "percentage — it is most of the chapter's only high-credibility evidence.",
          "2. **`postmaterialis*` retrieves zero.** S1 is a named stratum of this hypothesis and its "
          "central term is dead.",
          "3. **S4 is dead almost end to end** — 8 of its 9 wildcard terms. A6b recorded that S4 "
          "earns zero sole credit and asked whether it is 'buying coverage of a literature that does "
          "not exist'. **That question now has a different answer: the terms retrieve nothing "
          "because they are broken, not because the literature is absent.** A methods artifact was "
          "one step from being written into the chapter as a substantive claim about the field.", "",
          "## This corrects the correction at `654a491`", "",
          "That commit retracted A6c's *\"no prefix matching\"* reading on the evidence that "
          "`childless` and `childlessness` both return 2,586 — one postings list — and concluded no "
          "wildcard expansion was needed. **The generalisation was drawn from a single pair.** It "
          "holds for inflection (childless/childlessness) and fails for derivation "
          "(secular/secularization, religious/religiously), which is most of this query's "
          "vocabulary. Sixth instance of this chapter's signature failure, and the first inside the "
          "frozen artifact that everything downstream consumes.", "",
          "## The repair", "",
          "Expand every wildcard into its explicit morphological variants before the query is "
          "frozen, and **verify each expansion against a live count rather than assuming the "
          "index stems it**. The compiled query must not leave a star for a consumer to strip: A6c "
          "already recorded that requirement — *\"the compiled query must be emitted with wildcards "
          "expanded before C1 consumes it\"* — and it was not enforced.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"wildcard terms {len(rows)} | dead {len(dead)}", file=sys.stderr)
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
