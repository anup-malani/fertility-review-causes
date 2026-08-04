# D.1.a — cold-start channel-1 probe, per pair

**Hypothesis:** D.1.a, slug `postmaterialism-individualism-secularization`
**Stage:** GACS Phase A3, cold-start bootstrap channel 1 (prior meta-analyses and systematic-review
included-study lists — the privileged seed, requiring no search and no screening)
**Run:** 2026-08-03 (Shravan/Claude), live OpenAlex
**Script:** `source/build/goldset/89_d1a_channel1_probe.py`
**Raw output:** `temp/d1a/channel1-probe.json`, `temp/d1a/channel1-probe.md`

Everything below is live API output assessed by hand. Nothing here is an anchor yet: a candidate
becomes an anchor only after the Crossref and doi.org existence gate.

---

## Result

**Channel 1 is effectively empty for four of the five pairs, and the one pair with a real channel 1
is the pair whose estimates Ruling 2 mostly bars.** No systematic review or meta-analysis exists of
postmaterialism, individualism, or consumerism against fertility. For secularization the only
syntheses found are regional and both cover sub-Saharan Africa. For voluntary childlessness there
are several reviews, and that is the degenerate pair.

| Pair | Channel 1 | What was found |
|---|---|---|
| `S1_POSTMATERIALISM` | **Empty** | No review, no meta-analysis, at any field restriction |
| `S2_INDIVIDUALISM` | **Empty** | No review of the pair; probes return clinical "individualised treatment" noise |
| `S3_SECULARIZATION` | **Thin, regional only** | Two sub-Saharan Africa syntheses. No global or Western review; `title.search:religion AND fertility, type:review` returns **zero across all fields** |
| `S4_CHILDLESSNESS_NORM` | **Present** | Several reviews of voluntary childlessness, 1982 to 2026 |
| `S5_CONSUMERISM` | **Empty** | No review of the pair |

**This inverts the scope doc's prediction and the inversion is the finding.** The scope
("Expected shape of the evidence," item 2) predicted reviews would exist for S3 and not for S1, S2,
and S5. The negative half is confirmed. The positive half is not: religion and fertility has been
studied for a century and never systematically synthesised outside one region. Two consequences:

1. **S3 cannot be bootstrapped from an external authority** and its anchors must come from channels
   2 and 3, which raises the cost of the one pair expected to carry the chapter.
2. **The absence is itself a chapter result.** A literature this large with no synthesis is worth
   one line in §10, and it is part of the case for the review's existence.

**Third chapter running to find channel 1 thin or empty.** D.3.b found it near-empty because the
literature is too new; C.2.c found it empty because housing and fertility has never been synthesised;
D.1.a finds it empty for four pairs and regional for the fifth. GACS §7 move 5 should now be reported
as **tested and failing on this leg** rather than left open. Three chapters, three different causes,
one outcome: the privileged seed channel is usually not available, and the bootstrap in practice runs
on channels 2 and 3.

---

## Channel-1 candidates found (S3 and S4 only)

**S3 — secularization.** Both are regional and neither is a meta-analysis.

- `10.29063/ajrh2023/v27i1.11` — "Human fertility and religions in sub-Saharan Africa: A
  comprehensive review of publications," 2023, *African Journal of Reproductive Health*, 9 citations.
- `10.31237/osf.io/sezdq` — "Influence of Religion and Religiosity on Fertility and Contraceptive Use
  in Continental Sub-Saharan Africa," 2021, OSF preprint, 12 citations. Preprint status noted; needs
  a published-version check under the source-procurement rule.

**S4 — childlessness norm.** Listed for completeness. Under Ruling 2 most S4 estimates are degenerate
pairs, so these reviews seed context rather than the empirical core.

- `10.1007/bf00140093` — "Voluntary childlessness: A review of the evidence and implications," 1982,
  *Population Research and Policy Review*, 106 citations.
- `10.2307/j.ctv1fkgcjd.5` — "A Critical Review of the Interdisciplinary Literature on Voluntary
  Childlessness," 2021, Demeter Press.
- `10.1177/10664807221104795` — "A Systematic Review of Life Satisfaction Experiences Among Childfree
  Adults," 2022, *The Family Journal*. Outcome is life satisfaction, not fertility, so it is
  `OFF_OUTCOME` for this chapter and useful only as a bibliography.

**Leakage wall, standing.** Any of these may feed its included studies as anchors *or* its search
string as query terms. Never both from the same review.

---

## Positive controls (run before declaring any pair empty)

The C.2.c run recorded that a single failed lookup is not evidence of non-existence, because its own
first Crossref probe for a real paper returned nothing on a malformed query string. Four positive
controls were therefore run to confirm the probe can find things it should find:

| Control | Expected | Returned |
|---|---|---|
| Zaidi and Morgan SDT review | Should exist | `10.1146/annurev-soc-060116-053442`, *Annual Review of Sociology* 2017, 301c ✅ |
| Lesthaeghe and Wilson, Princeton EFP secularization chapter | Should exist | "Modes of production, secularization and the pace of the fertility decline in Western Europe" 1986, 160c ✅ |
| Religion and fertility empirical core | Should be large | 313 title hits, led by "When Does Religion Influence Fertility?" *PDR* 2004, 435c ✅ |
| Religion and fertility, `type:review`, all fields | Unknown | **0** ✅ (the negative result, confirmed unrestricted) |

The controls pass, so the empty cells above are read as empty rather than as probe failure.

---

## Two hazards found, both belonging in the production query rather than at screening

**1. The outcome axis collides head-on with clinical and perinatal medicine.** The first pass used a
bare `fertility OR births OR childbearing OR "birth rate"` outcome axis with no field restriction.
All five pairs came back swamped: *fertility* reads as IVF and infertility treatment, *birth* reads
as birth weight and birth cohort, and the top-cited hit across three separate pairs was a systematic
review of antenatal care utilisation. OpenAlex's stemming made it worse, matching *individualism* to
"individualised dosing of follitropin delta" and *consumerism* to "direct-to-consumer telemedicine."

Fixed here with demography-specific outcome vocabulary plus a four-field restriction (Social
Sciences, Economics, Psychology, Arts and Humanities). **The field restriction is acceptable for a
review probe and is not acceptable for the production query**, since it would drop genuinely relevant
work indexed under Medicine. The production query needs the vocabulary fix, not the field fix. Same
class of collision as C.2.c's `housing AND fertility` against livestock housing and soil fertility,
which suggests a standing pre-query check: run the bare axis once and read what it pulls before
building on it.

**2. OpenAlex throttles boolean searches above five operators.** Two probes returned
`{"error":"Rate limit exceeded", "message":"Your query uses 6 boolean operators ... queries with more
than 5 operators are limited"}`. This is a live constraint on the GACS clustered-query design for
every chapter, not only this one: a cause axis with eight OR'd vocabulary terms exceeds it on its
own. The workaround is to issue few-operator sub-queries and union the results client-side rather
than sending one wide boolean. Worth confirming against the production-query builders already written
for B.1, D.3.b, and C.2.c, since a throttled query that still returns a plausible count is the
failure mode that does not announce itself — the same shape as the C.2.c relevance-filter bug, where
counts stayed plausible and monotone while being wrong.

---

## Empirical anchor candidates surfaced incidentally (S3), not yet verified

The channel-1 probes returned these while looking for reviews. They are recorded here so the channel-2
and channel-3 pass does not have to rediscover them, and they carry **no verified status**: each must
clear the existence gate before entering any recall denominator.

- `10.1111/j.1728-4457.2004.00002.x` — "When Does Religion Influence Fertility?" *PDR* 2004, 435c.
- `10.1353/sof.0.0000` — "Religiosity and Fertility in the United States: The Role of Fertility
  Intentions," *Social Forces* 2008, 328c.
- `10.2307/2061727` — "Religion and fertility in the United States: New patterns," *Demography* 1992,
  197c.
- `10.1007/s10680-007-9121-y` — "Religion, Religiousness and Fertility in the US and in Europe," *EJP*
  2007, 185c.
- `10.4054/demres.2008.18.8` — "Religious affiliation, religiosity, and male and female fertility,"
  *Demographic Research* 2008, 133c.
- `10.1007/s001480050013` — "Religion as a determinant of marital fertility," *J. Population
  Economics* 1996, 137c.
- `10.1007/s00148-011-0401-9` — "The evolution of secularization: cultural transmission, religion and
  fertility," *J. Population Economics* 2012, 39c.
- `10.1515/9781400886692-011` — Lesthaeghe and Wilson, "Modes of Production, Secularization, and the
  Pace of the Fertility Decline in Western Europe," Princeton UP reissue of the 1986 EFP chapter.
  **The FDT-era anchor Ruling 4 was written to admit.**
- `10.1007/s11150-007-9011-4` — "Parental religiosity and daughters' fertility: the case of Catholics
  in southern Europe," *Review of Economics of the Household* 2007, 41c.
- `10.1007/s11113-021-09685-0` — "Disentangling the Roles of Modernization and Secularization on
  Fertility: The Case of Turkey," *PRPR* 2021.
- `10.1146/annurev-soc-060116-053442` — Zaidi and Morgan, "The Second Demographic Transition Theory: A
  Review and Appraisal," *ARS* 2017, 301c. **Theory stream**, does not count toward empirical recall.
- `10.1186/s41118-020-00077-4` — Lesthaeghe, "The second demographic transition, 1986–2020," *Genus*
  2020, 299c. **Theory stream.**
- `10.1007/s11205-010-9665-9` — "The Incompatibility of Materialism and the Desire for Children,"
  *Social Indicators Research* 2010, 38c. The only S5 candidate found so far, and note it uses
  *materialism* in the consumer-psychology sense, which is the polysemy the scope flagged.

**Note the tier composition.** Every empirical candidate above is Tier 3 or Tier 4 under Ruling 3 on
the face of its title. Not one is a natural experiment. The Tier 1 material the chapter needs — church
tax reform, blue-law repeal, state secularization campaigns, clergy-scandal shocks — did not surface
from a topical probe and will have to be sought by design vocabulary rather than by topic. That is the
next probe's job.
