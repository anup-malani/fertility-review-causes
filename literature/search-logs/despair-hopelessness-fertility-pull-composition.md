# What the 390,983-record pull actually contains

**Measured live, 2026-08-18.** Written to answer a question worth asking plainly: if every other
chapter in this review is evidence-poor — B.1 pooled 5 studies, D.3.b got 0 poolable rows from 11,
B.7's middle link had a single record, B.6's microplastics primary cell was empty — how does D.3.c
end up with a 390,983-record search?

**It doesn't. The pull is large because the query was deliberately made unselective, not because the
literature is.**

B1 established that the outcome-AND-treatment conjunction was *strictly dominated* on this chapter:
it lost 85% of the gold **and** had lower precision, because decline and uncertainty vocabulary
saturates the decoy clouds. The production query is therefore the outcome block alone — in effect
"every paper with a fertility-outcome term in its title." That is a retrieval universe, not an
evidence base, and the distance between the two is this chapter's whole problem.

## Composition

| | records | share of pull |
|---|---|---|
| **The pull** — production query, title | **390,983** | 100% |
| + any mechanism vocabulary, title or abstract | 3,768 | 0.96% |
| + chronic-decline treatment (chapter 1) | 474 | 0.12% |
| + opportunity / inequality treatment (chapter 2) | 4,800 | 1.23% |
| **+ mechanism AND treatment — the claim itself** | **65** | **0.017%** |

**Sixty-five records in the entire index carry a fertility outcome, a despair-type construct, and an
economic-decline or opportunity treatment together** — and that is an *upper bound* on the primary
cell, not an estimate of it. Co-occurrence in an abstract is not estimation: some of those 65 will be
reverse-causation (infertility distress), some mortality, some theory, some passing mention. The
screen exists to find out which.

This is the fourth independent route to the same fact. The reconnaissance found the
treatment-mechanism-outcome intersection empty (n=12, none on topic). A4 mined **zero** terms in
`MECHANISM_AND_OUTCOME` and found `despair` *negatively* discriminative. The A4 citation frame put the
joint density at 0.28% of a one-hop neighbourhood. Now the open-database count puts the claim's own
vocabulary at 0.017% of the pull.

## Chapter 2 has roughly ten times chapter 1's literature

474 records for chronic decline against 4,800 for opportunity and inequality. That asymmetry has been
visible since the reconnaissance — Kearney and Levine, Edin and Kefalas, and the teen-childbearing
literature are a real, developed body, while the deferral mechanism's American evidence never
materialised — and it should shape expectations for the two chapters' GRADE ratings before extraction
begins, not after.

## A query-parser hazard found while measuring this

A first pass reported 136,417 records (35% of the pull) carrying mechanism vocabulary. That was
false, and the cause is worth recording.

**OpenAlex drops stopwords inside quoted phrases.** `"no future"`, `"the future"` and bare `"future"`
all return exactly **36,540** when ANDed with `"fertility"`; `"of despair"` and `"despair"` both
return **156**. The phrase is not matched as a phrase — the stopword is discarded and the remaining
content word is searched.

Usually harmless: `"number of children"` returns 884 while `"number children"` returns 1, because the
content words still carry the meaning. **The dangerous class is a phrase where the stopword is doing
the semantic work** — above all negation. `"no future"` means the opposite of `"future"`, and
searching for it silently searches for the latter, inflating by a factor of 234.

Checked: every stopword-bearing phrase in this chapter's production query holds as a phrase, so the
390,983 figure is unaffected. No previously reported count in this chapter used a negation-bearing
phrase against the API — the `no future` string appears only in local Python substring matching
(`150_`, `151_`, `152_`), which does not go through the query parser.
