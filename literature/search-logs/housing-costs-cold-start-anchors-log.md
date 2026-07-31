# Cold-start anchor log — housing costs (C.2.c)

**Hypothesis:** C.2.c, slug `housing-costs`
**Run:** 2026-07-31, Shravan (TICK-055)
**Artifact:** `housing-costs-cold-start-anchors.json` — 25 records, **all 25 existence-verified**
**Scope doc:** `housing-costs-search-scope.md` (identifying variation ruled 2026-07-31: housing prices)

---

## 1. Headline: channel 1 is empty, and that is a finding

**No systematic review or meta-analysis of housing costs → fertility exists.** The cold-start
bootstrap's privileged seed — prior review included-study lists, which give empirical anchors by
external authority at no search cost — returns nothing for this hypothesis.

What was run before concluding that:

| Probe | Result |
|---|---|
| OpenAlex `housing fertility`, `type:review` | 7 works, **none** on housing and fertility (a nursing childbearing-intentions review, an Amish settlement review, radiofrequency and sperm, etc.) |
| OpenAlex `housing fertility systematic review` (title/abstract) | 50 works, none on topic |
| OpenAlex `housing fertility literature review` | 90 works, none on topic |
| WebSearch, review-and-meta-analysis phrasing | surfaced primary studies plus one adjacent review (below) |

**The one near miss, run down and excluded:** *The impact of housing prices on residents' health: a
systematic review* (Grewal et al. 2024, BMC Public Health, `10.1186/s12889-024-18360-w`). SCOPUS +
PubMed to June 2022, 23 studies, outcomes split mental (7) / physical (9) / combined (7). Its only
contact with this literature is Daysal et al. 2021 — included for that paper's **birth-weight and
prematurity** outcomes, not its fertility estimate. It contributes **zero** new empirical fertility
anchors. Retained in the JSON as `channel1_SR_nearmiss` so the audit trail shows the channel was
worked, not skipped.

**Consequence for the GACS replication test.** C.2.c was picked partly because a well-studied
hypothesis should exercise cold-start channel 1 and satisfy §7 move 5. It does not. Two hypotheses in
a row (D.3.b, C.2.c) have now found channel 1 empty or near-empty from opposite directions — D.3.b
because its literature is too new, C.2.c because a large literature has never been formally
synthesised. **The bootstrap's "privileged seed" may be the exception rather than the default**, and
§7 move 5 should be reported as tested-and-failed on this leg rather than left open. Channels 2 and 3
carry the load.

## 2. Provenance and the Tier-B integrity constraint

Marked honestly in the JSON, because it binds what comes next:

- **`channel2_canon_v5seminal` (4 records).** The HYPOTHESES-v5 `seminal` field, existence-verified.
- **`channel4_keyword_scout` (20 records).** Found by my OpenAlex title/abstract sweep. This is a
  keyword search, so under GACS it is **channel 4**, not channel 2.
- **`channel1_SR_nearmiss` (1 record).** The excluded health review.

**These 20 keyword-scouted anchors must not enter Tier B.** GACS A3 is explicit: Tier B is drawn from
channels 1–3 only, or Recall(B) is measured against papers the query itself produced and the number is
circular. That is precisely how the OAS pilot's recall got inflated. They are eligible for **Tier A**
(the keyword-reachable empirical core, which Recall(A) is defined over) — but **Tier B still has to be
built, and the only clean route left is channel 3, a citation snowball off the four canon seeds.**
That snowball has not been run and is the next executable step.

Current state against the CV floor: **~20 empirical anchors, below the ≥ 30 floor** for fold-local
term mining. The snowball needs to close that gap as well as build Tier B.

## 3. Existence gate: clean, and one v5 metadata correction

All 25 records resolve to live DOIs via OpenAlex lookup. **No ghosts** — unlike the OAS Tier B, whose
frozen set was ~40% fabricated. The four v5 `seminal` names all verify:

| v5 seminal entry | Status | Resolved |
|---|---|---|
| Mulder and Billari 2010 | ✅ | `10.1080/02673031003711469`, Housing Studies |
| Dettling and Kearney 2014 | ✅ | `10.1016/j.jpubeco.2013.09.009`, J. Public Economics |
| Lovenheim and Mumford 2013 | ✅ | `10.1162/rest_a_00266`, REStat (OpenAlex dates it 2012) |
| Daysal Lovenheim and Wasser 2021 | ✅ *(author list incomplete)* | `10.1016/j.jpubeco.2021.104366` |

**Correction for TICK-001:** the fourth is **Daysal, Lovenheim, Siersbæk, and Wasser** — v5 drops
Siersbæk. Minor, but the gate exists to catch exactly this class of drift, and a wrong author list
propagates into the bibliography.

*Process note:* my first Crossref probe for the Daysal paper returned nothing and it looked like a
ghost. It is not — the query string was wrong. **A single failed lookup is not evidence of
non-existence**; the gate needs a second query form before anything is called fabricated.

## 4. Two findings that change the search design

**(a) `housing` AND `fertility` is a booby-trapped phrase.** Both words are core vocabulary in animal
science, where *housing* means livestock housing and *fertility* means breeding performance — and in
agronomy, where *fertility* means soil fertility. Unfiltered queries returned dairy-cattle conception
rates, biochar in animal feeding, ruminant adaptation strategies, deer mice as laboratory animals, and
agroforestry productivity, frequently **out-ranking** the on-topic economics papers by citation count.
A second polluting class is epidemiological **"Cohort Profile"** papers, which enumerate every variable
a survey collects and therefore match almost any two-term query.

Neither is solved by better ranking; both need to be handled in the production query — domain or
concept filters, or negative terms. Recorded here because it will otherwise be rediscovered at the
screening stage, at LLM cost.

**(b) The two vocabulary families predicted in the scope are real, and they barely overlap.**

- **`econ-price`** — house prices, housing wealth, home equity, real estate, price shock. Venues:
  J. Public Economics, REStat, Economic Inquiry, J. Housing Economics, J. Health Economics, China
  Economic Review, Labour Economics.
- **`demog-tenure`** — homeownership, housing tenure, housing type, housing context, housing career,
  housing regime. Venues: Housing Studies (clearly the hub), Demography, Demographic Research,
  European J. Population.

They surface **different papers**, not the same papers under different names. Under the GACS
granularity rule they should be separate cause-axis clusters and separately budgeted. A third,
smaller family — `macro-comparative` (housing regimes, institutional/cross-national) — sits mostly in
Housing Studies and may merge into `demog-tenure` once the overlap test can be run on a real gold.

## 5. Preprint twins are pervasive — a dedup hazard to handle before it bites

**Four of the five strongest anchors have preprint or working-paper twins carrying separate DOIs:**

| Published | Twin(s) |
|---|---|
| Dettling and Kearney, JPubE | NBER `10.3386/w17485` |
| Lovenheim and Mumford, REStat | SSRN `10.2139/ssrn.1544607` |
| Daysal et al., JPubE | NBER `10.3386/w27469`, SSRN `10.2139/ssrn.3636646`, SSRN `10.2139/ssrn.3644070` |
| Li, Labour Economics | SSRN `10.2139/ssrn.4424655` |

DOI-keyed dedup will **not** catch these — the DOIs genuinely differ — and the citation counts split
across versions, which also corrupts any citation-based ranking. The Dettling and Kearney JPubE record
shows `c=0` in OpenAlex while its NBER twin shows `c=67`, so a citation-ranked cutoff would discard the
published version and keep the working paper. Normalized-title dedup (GACS C3's second key) is
load-bearing here, and the surviving record should be the **published** one.

## 6. The phenomena scope is challenged by the evidence

HYPOTHESES-v5 scopes C.2.c to **SDT only**. But Li (2024, Labour Economics,
`10.1016/j.labeco.2024.102572`) runs a global house-price panel **1870–2012** and frames its result
against the fertility transition — i.e. squarely FDT. A secondary summary reports −0.01 to −0.03 births
per woman per 10% real price rise (**not verified at source**; confirm at extraction).

So the SDT-only scoping would exclude the single most historically comprehensive study in the pool.
This is a scope question for the PI, not an RA call, and it is **not** the same question as A.10's
war-shock gap: here the routing target exists and the only issue is the period restriction. Raised in
the ticket; does not block the snowball.

## 7. Next executable step

**Citation snowball (channel 3) off the four `channel2_canon_v5seminal` seeds** — backward references
at ≤ 1 hop, forward citations capped and restricted to the topic-specific seeds per the §7.2 defaults.
Two jobs at once: build a **clean, non-circular Tier B**, and lift the empirical anchor count from ~20
over the ≥ 30 CV floor. The keyword-scouted 20 stay in Tier A and must be excluded from the Tier-B
frame.
