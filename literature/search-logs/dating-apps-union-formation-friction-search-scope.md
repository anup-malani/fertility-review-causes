# Search scope — dating apps and union-formation friction

**Hypothesis:** A.24 (`dating-apps-union-formation-friction`), HYPOTHESES-v5.md §A.24
**Ticket:** TICK-071 · **Stage:** PROTOCOL §5 stage 2
**Status:** **FROZEN 2026-08-24.** All five PI calls ruled (§PI calls). Everything below that
carries a count was measured live on 2026-08-24 by `source/build/goldset/170_a24_recon_probe.py`
(65 requests, 0 failed) and `171_a24_named_recheck.py` (17 requests, 0 failed). Reports:
`dating-apps-union-formation-friction-recon-probe.md`, `-named-recheck.md`. Stages A3, A4, D1, D2 and
5 ran against the drafted scope and are unaffected by the rulings — see *What changed at freeze*.

---

## Causal claim

As registered in v5: online dating platforms raise the volume of potential contacts but *lower*
conversion to committed partnership — through match abundance, strategic delay, and the
commodification of potential partners — reducing pair-bond formation and, downstream, fertility.
Phenomenon: SDT only.

## A.24 is a three-link chain, and the link the registry entry names is the one nobody has estimated

The claim decomposes into three links, and they are in very different empirical states:

| Link | Statement | State of the evidence |
|---|---|---|
| 1 | app adoption → partnering behaviour (matches, standards, rejection) | **measured, mostly in the lab and on platform data** |
| 2 | partnering behaviour → union formation and stability | **measured, and the field estimates run the OPPOSITE way to v5** |
| 3 | union formation → births | **owned by A.7 / C.7.a. A.24 imports it; it does not estimate it** |

The registry entry asserts the composition of all three. No study measured here estimates it. This is
B.7's shape — a chain whose weakest link carries the whole claim — and the scope states it in its
first paragraph rather than discovering it at extraction.

## The primary cell is empty, and that is a measurement rather than an expectation

| Probe | n | What sits at the citation-ranked head |
|---|---|---|
| dating apps **AND** a population fertility quantity | **11** | a JOLE marriage-market paper; *Stories of Love from Vikings to Tinder*; two survey data-resource profiles |
| dating apps **AND** any fertility outcome | 64 | COVID sexual-and-reproductive-health; egg freezing; **pet dogs and cats in human courtship**; one maize *nitrogen fertility* paper |
| dating apps **AND** childbearing / parenthood / childlessness | 42 | Tinder-use longitudinal study; *Online Dating in Singapore: The Desire to Have Children* |
| dating apps named as a **cause of** a fertility quantity | 21 | same records; no estimate among them |

Eleven records, and reading their heads, not one estimates the effect of app exposure on a fertility
quantity. The nearest thing in the whole probe is a 2026 SSRN working paper, *The Effect of Cellular
Data on Fertility* — whose exposure is cellular data, not dating apps, and which therefore belongs to
C.2.h's treatment (see Call 2).

**Consequence for the chapter's design.** A.24 cannot produce a pooled fertility effect. What it can
produce is (a) a graded synthesis of link 2, where estimates exist; (b) an explicit statement of the
link-3 elasticity it would have to import from A.7 to reach a fertility number; and (c) a bound from
timing (below). The scope commits to that structure now so the chapter is not written as if a
fertility estimate were expected to appear.

## Where field evidence exists, it runs against the hypothesis

This is the finding that most shapes the walls. Four identified or longitudinal studies reach a
partnering or fertility outcome, and every one of them points the other way:

| Study | Design | Direction |
|---|---|---|
| Rosenfeld 2017, *Sociological Science* | HCMST longitudinal; explicitly tests the choice-overload critique | meeting online does **not** predict breakup; predicts **faster** transitions to marriage |
| Bellou 2014, *J. Population Economics* | broadband-market variation, US | internet diffusion → marriage rates (sign to be extracted; the paper is framed as an increase) |
| Billari Giuntella & Stella 2019, *Population Studies* | German panel, Falck et al. IV | **positive** effect of broadband availability on fertility of highly educated women 25–45 |
| Kalabikhina et al. 2020, *Lomonosov Economics J.* | RLMS-HSE panel, IV | **positive** effect on fertility of women 25–49; strongest at second and higher parities |
| Erevik et al. 2020, *Frontiers in Psychology* | 5,253 students, two waves, Norway | Tinder use predicts romantic **relationship formation** one year later |

The theory does not give the sign, and the best-identified evidence currently available gives the
opposite one. That is the same problem D.3.c had, and it has two consequences the scope must carry:
the screen may not use directional language that presumes friction, and the chapter's headline may
well be a **bounded refutation** rather than a small positive effect. A bounded refutation reached by
not reading is not a finding, so the both-axes population is read in full at stage 4 (B.6's rule).

## The mechanism is real, measured, and never once attached to a demographic outcome

Choice overload in dating is not folk theory — it has been tested experimentally:

- Pronk & Denissen 2019, *SPPS* — a "rejection mind-set": three studies, participants reject more
  over time, cumulating in a **27% decrease** in acceptance.
- D'Angelo & Toma 2016, *Media Psychology* — 24-option choosers were less satisfied a week on.
- Jung Lim Lee & Kim 2021, *Information Systems Research* — a **randomized field experiment** varying
  choice capacity on a live platform, with **matching outcomes**. This is the one mechanism study
  whose outcome is not purely psychological, and it is the reason Wall 4 is cut on outcome.
- Sharabi & Timmermans 2020; "the agony of partner choice" 2021 — commitment intentions, fear of
  being single.

Their outcomes are satisfaction, rejection rates, regret, and fear of being single. **The friction
literature crossed into a demographic outcome in 34 records, and the head of that probe is economic
search-friction theory** (Shimer & Smith, *Econometrica*; *The Marriage Model with Search Frictions*,
*JPE*) — a different sense of the word "friction" entirely: structural search cost, not choice
overload. The lexical collision is real and the screen must separate the two senses.

So the chapter's mechanism section and its effect section are drawn from disjoint literatures. Stated
plainly at freeze, this is what a Very Low or Low GRADE for indirectness will rest on.

## The identified variation for this chapter is C.2.h's variation

Every quasi-experiment that reaches this exposure runs on technology diffusion — broadband, 3G,
cellular data, smartphone adoption — not on dating apps:

| Probe | n |
|---|---|
| dating apps **AND** identification vocabulary | **33** (heads are sociosexuality correlates and an HIV paper; no design among them) |
| technology rollout **AND** union formation **AND** identification | **4** |
| technology rollout **AND** fertility **AND** identification | 31 |

**This forces the single most consequential wall in the scope.** A wall requiring dating-app
vocabulary at title/abstract deletes Billari et al., Bellou, and Kalabikhina et al. — the only
identified estimates this chapter can reach — because none of them says "dating app" in a title or
abstract. That is A.12's Wall 8 exactly, and A.12 also established the trap: gating the recovery on
the vocabulary the wall declares invisible recovered 4 records where a provenance-gated bypass
recovered 212. Wall 9 below is therefore **declared unenforceable** and bypassed on seed provenance
plus an outcome term, with **no dating-vocabulary requirement**.

## Most of the phenomenon predates the exposure — a bound to compute, not to assume

Swipe-based apps date from Tinder's 2012 launch and diffuse over roughly 2013–2016; the pre-app
online-dating era runs from the mid-1990s. The US TFR turn is dated to 2007. So a substantial share
of the SDT decline being explained closed before the exposure existed at all, and A.24's maximum
possible contribution is bounded by the post-exposure remainder before any effect estimate is
considered.

**This is pre-registered as a computation, not stated as a number.** `data/raw/` is empty in this
working tree, so stage 10 sources a national TFR series (HFD for cross-national, CDC NVSS for the US)
and reports the peak-to-trough decline split at 2012 and at 2016. Recorded here so that an
apparently large A.24 effect gets audited against the timing rather than believed. B.7's version of
this bound — 67.6% of the SDT decline predating the exposure — is the precedent.

## Decoy clouds, counted

| Family | What the shared word means there | n | Separable? |
|---|---|---|---|
| **Geochronology** | radiocarbon / luminescence / U-series *dating* | **64,276** on the explicit vocabulary; **102,438** for bare "dating" with archaeology or sediment terms | **Yes** — pure homonym, distinct vocabulary. The SHELX pattern |
| **Dating violence and IPV** | courtship — the *same* word sense, a different outcome | **43,963**; 11,282 with adolescents; **66** inside the app cloud | **Yes, but only on OUTCOME.** No vocabulary test on "dating" can do it |
| **Sexual health on platforms** | HIV/STI risk, MSM geosocial apps | **1,244** inside the app cloud; 415 on casual sex | Yes on outcome — but casual-sex *frequency* records route to A.14, not to the bin |
| **Platform engineering / recommender systems** | matching as an algorithms problem | **421** | **Partly.** Cut on outcome: a match/partnership outcome is an include (Jung et al. 2021) |
| **Soil and agronomic fertility** | nitrogen, biofertilizers, "mineral fertility" of magmas | 181 at the geochronology×fertility intersection alone | Yes |
| **Marriage-market economics (C.7.a)** | structural matching, sex ratios, assortative mating | 382 with apps; 4,246 with fertility | Partly — route, never exclude |

The geochronology cloud is carved out from the forward-seed-everything rule. Per the standing
decoy-cloud guidance, that carve-out must rest on an exact on-topic rate rather than a sample:
**A4 issues count-only queries for each homonym seed** and the scope records the measured rate before
the exclusion is treated as settled.

## Walls

| # | Wall | Enforceable at title/abstract | Treatment |
|---|---|---|---|
| 1 | Geochronological "dating" | **Yes** | hard exclude → `OFF_HOMONYM_GEOCHRON` |
| 2 | Non-human and soil fertility | **Yes** | hard exclude → `OFF_NONHUMAN` |
| 3 | Dating violence / IPV / online abuse | **Yes, on outcome** | exclude → `OFF_VIOLENCE` |
| 4 | Platform engineering — **cut on OUTCOME, not on venue** | **Yes** | partnership or matching outcome → include; engagement/CTR/algorithm-quality only → `OFF_PLATFORM_ENG` |
| 5 | Sexual health and STI risk | **Yes, on outcome** | exclude → `OFF_SEXHEALTH`; **coital-frequency outcomes route to A.14** |
| 6 | Structural marriage-market imbalance (C.7.a) | Partly | route → C.7.a; A.24 keeps only technology-created friction |
| 7 | Link 3 alone — union formation → births with no technology exposure | **Yes** | route → A.7 / C.7.a; imported at synthesis, not graded here |
| 8 | Technology diffusion with no partnering channel (C.2.h) | Partly | route → C.2.h; shared records tagged, see Call 2 |
| 9 | **Identified estimates published under technology-diffusion vocabulary** | **NO — declared unenforceable** | provenance bypass: seed from the tech-diffusion canon, admit on exposure + outcome terms, **no dating-vocabulary requirement** |

Wall 9's cost gets reported the way A.12 reported Wall 8's: recall is stated twice, once against all
empirical anchors and once against the screenable subset, and the gap is the price of the
unenforceable wall.

## Estimand cells

| Cell | Contents | Extractable |
|---|---|---|
| `PRIMARY_APP_UNION` | app or online-dating exposure → union formation / marriage / partnering | yes — the chapter's spine |
| `PRIMARY_APP_FERTILITY` | app exposure → a fertility quantity | **expected empty; kept so the absence is reported as a count** |
| `SECONDARY_TECH_UNION` | broadband / 3G / cellular diffusion → union formation | yes — reached only through Wall 9's bypass |
| `SECONDARY_TECH_FERTILITY` | the same exposures → fertility | yes; **overlaps C.2.h — Call 2 governs who may claim the magnitude** |
| `MECHANISM_CHOICE_FRICTION` | choice-overload and rejection-mindset studies | yes, but psychological outcomes; supports mechanism, not magnitude |
| `EXPOSURE_SERIES` | HCMST, Pew adoption, platform user counts | not an effect; feeds stage 10 |
| `LINK3_IMPORTED` | union formation → births | **not estimated here**; imported from A.7 with its own uncertainty |
| `OFF_*` | the six decoy families above | — |
| `INSUFFICIENT_INFO` / `OFF_OTHER` | | — |

## What demographic significance runs on

Two series, both to be confirmed live at A3 rather than remembered:

- **HCMST** (How Couples Meet and Stay Together) — 32 records cite it; Rosenfeld & Thomas 2012 *ASR*
  (538 cites) and Rosenfeld Thomas & Hausen 2019 *PNAS* (425 cites) are built on it. It is the only
  series that gives the share of couples meeting online over time, which is this chapter's exposure.
  **US-only**, which bounds every demographic-significance statement to the US unless a second
  national series is found.
- A national TFR series for the timing bound (see above).

## Citation hygiene — v5's seminal list resolves, and two of the three do not carry the claim

All three of v5's cites exist. That is not the problem.

- **Rosenfeld Thomas & Hausen 2019** (*PNAS*, 425 cites) — resolves cleanly, authors as written.
- **Tyson et al. 2016** — resolves, but it is a **62-cite CS conference paper measuring Tinder user
  activity**. It carries no partnership outcome and no fertility outcome.
- **Bruch & Newman 2018** (*Science Advances*, 126 cites) — resolves; it estimates desirability
  hierarchies, not conversion to partnership.

So v5 supports a demographic claim with two platform-measurement papers. The chapter says so.

Three further hygiene findings:

1. **OpenAlex indexes the author of *Marriage, Choice, and Couplehood in the Age of the Internet*
   (2017) as "Michael Rosenfield"** — misspelled. An author gate keyed on surname agreement will
   refuse this anchor, and it is one of the most important INCLUDE-side records in the chapter.
   Carried to A3 as a known-good exception rather than met as a failure.
2. **`Love Unshackled` exists twice** — MIS Quarterly 2019 (127 cites) and a DOI-less 2018 SSRN
   preprint (0 cites). The version-of-record gate applies. Same for Ortega & Hergovich, which
   resolved **only** as a preprint (12 cites).
3. **Finkel et al.'s online-dating review did not resolve on either endpoint** and is NOT recorded as
   absent. A3 resolves it by DOI. See the workflow finding below for why the query failed.

## Workflow finding — author-name retries are dead code in both endpoints

170_'s pass-2 returned **zero for all fifteen** alternate wordings. That density is a property of the
query, not of the literature: `filter=title.search:` matches the **title field only**, so any retry
query carrying an author surname is unsatisfiable by construction. 171_ re-ran seven of them through
`search=` and they still miss the target work — relevance search does not match author names either.

**Every prior chapter's recon script carries this same pass-2 pattern**, inherited from B.5. On this
chapter it produced fifteen fake zeros. The fix is to retry through `filter=raw_author_name.search:`
combined with a title term, or by DOI; it belongs in the shared probe scaffold rather than in a
per-chapter fix. Recorded here, not edited across branches from this one.

## PI calls — RULED 2026-08-24

All five were ruled by the PI on 2026-08-24, after D2 and stage 5 had reported. The rulings are
recorded with the evidence each rested on at the time, because three of the five moved from
hypothetical to costed between the draft and the ruling.

**Call 1 — RULED: grade link 2 only.** A.24 grades the technology-exposure → union-formation link and
**imports** the union → births link from A.7 with its uncertainty stated. It does not grade the
composition, because nobody has estimated it. *Evidence at ruling:* the screen counted 140 records
with a partnership outcome, 56 with a fertility quantity and **two with both** — and the two are one
German cohort study plus its own working paper.
*Consequence:* the GRADE table's rows are technology→union. Any fertility number the chapter reports
is a composition of a graded link and an imported one, and must be labelled as such wherever it
appears.

**Call 2 — RULED: share the technology-diffusion records with C.2.h.** The broadband, 3G and cellular
rollout studies enter BOTH chapters' evidence bases rather than being routed away from one.
*Evidence at ruling:* 27 records reached `SECONDARY_TECH_*`, and ten of the 33 readable causal
records are of this kind — routing them out would have left A.24 with almost no readable
identification.
*One sub-question the ruling does not settle, and the reading adopted:* whether BOTH chapters may
report the same magnitude. Double-counting one coefficient across two chapters is a real defect in a
review that sums contributions, so the working rule is **shared evidence base, single claimant on
magnitude**: both chapters extract and grade the record, and the synthesis stage names which chapter
carries its contribution to the aggregate. Flagged here rather than assumed — if the PI intended both
chapters to claim it, this line is what needs changing.
*Consequence:* extraction is unblocked, and every shared record carries a `shared_with: C.2.h` tag so
the synthesis can find them without re-searching.

**Call 3 — RULED: pre-app online dating (1995–2012) is in scope.** *Consequence:* Rosenfeld & Thomas
2012, Hitsch Hortaçsu & Ariely 2010 and Bellou 2014 stay in. But v5's own framing — swiping,
commodification, match abundance — is app-specific, so **extraction carries an `era` field keyed on
the study's EXPOSURE period rather than its publication year** (`pre_app` ≤2012, `app_era` ≥2013,
`spans` for panels crossing the discontinuity), and the synthesis reports the app-era subset
separately rather than pooling across a technological break.

**Call 4 — RULED: an empty primary cell earns *Insufficient Evidence*, not a graded no-effect.**
*Consequence:* `PRIMARY_APP_FERTILITY` is reported as **Insufficient Evidence** for the SDT, with the
denominator shown — a rule-selected candidate pool that was read, not a cell nobody looked at. The
chapter must not phrase this as evidence of no effect anywhere in its text, and the distinction gets
a sentence in the verdict rather than a footnote, because the living resource's audience reads the
two very differently.

**Call 5 — RULED: contrary evidence is graded on the registered estimand.** Studies estimating the
right relationship with the wrong sign for v5 are evidence about the hypothesis, not evidence about a
different question. *Consequence:* A.24 can return a **negative verdict carrying a non-trivial GRADE
rating** rather than an empty one — and it now has evidence pointing both ways to weigh (Rosenfeld
2017 and the broadband-fertility estimates against v5; the 50-country relationship-satisfaction study
and the rejection-mindset line for it).

## What changed at freeze, and what it cost

Nothing in the walls or the estimand cells changed, so **A3, A4, D1, D2 and stage 5 all stand and
none needs re-running.** That is the payoff for having drafted the walls tightly enough to survive
the calls, and it is worth contrasting with A.12, where Call 3 forced a Wall 6 re-cut after the
scope was drafted.

Three things the rulings ADD, all downstream of work already done:

1. **An `era` field at extraction** (Call 3). Cheap — it is a coding decision per study, not a
   re-search.
2. **A `shared_with: C.2.h` tag** on the 27 technology-diffusion records (Call 2), and a note to the
   synthesis stage that the single-claimant rule applies.
3. **A verdict label change** for `PRIMARY_APP_FERTILITY` from the drafted "expected empty" to
   **Insufficient Evidence** (Call 4), which is a stronger claim than "empty" and requires the
   candidate-pool denominator to be reported alongside it.

## Next

A3 cold-start anchor resolution (script 172), on 25 anchors spanning: `PRIMARY_APP_UNION` (Rosenfeld
2017, Erevik 2020, Potarca 2020), `SECONDARY_TECH_*` (Bellou 2014, Billari et al. 2019, Kalabikhina
et al. 2020), `MECHANISM_CHOICE_FRICTION` (Pronk & Denissen 2019, D'Angelo & Toma 2016, Jung et al.
2021), `EXPOSURE_SERIES` (Rosenfeld & Thomas 2012, Rosenfeld Thomas & Hausen 2019), and one routing
decoy per enforceable wall. Carry the Rosenfield misspelling and the two preprint-only records into
A3 as known exceptions.
