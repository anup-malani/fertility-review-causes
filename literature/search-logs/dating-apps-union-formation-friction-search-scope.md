# Search scope — dating apps and union-formation friction

**Hypothesis:** A.24 (`dating-apps-union-formation-friction`), HYPOTHESES-v5.md §A.24
**Ticket:** TICK-071 · **Stage:** PROTOCOL §5 stage 2
**Status:** **DRAFT — not frozen.** Five PI calls open (§PI calls). Everything below that carries a
count was measured live on 2026-08-24 by `source/build/goldset/170_a24_recon_probe.py` (65 requests,
0 failed) and `171_a24_named_recheck.py` (17 requests, 0 failed). Reports:
`dating-apps-union-formation-friction-recon-probe.md`, `-named-recheck.md`.

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

## PI calls — status

**Call 1 — does A.24 grade the composition, or only link 2?** *Recommended:* grade link 2 (technology
exposure → union formation) and import link 3 from A.7 with its uncertainty stated, rather than
grading a composite nobody has estimated. RA-provisional; the chapter can be written either way, but
the GRADE table's row labels depend on it.

**Call 2 — A.24 vs C.2.h, when the identified variation is the same variation.** Broadband/3G/cellular
rollout instruments both chapters. *Recommended:* split on **outcome**, not on treatment — A.24 owns
partnering and union formation, C.2.h owns time and attention allocation (and A.14 owns coital
frequency). A study estimating tech diffusion → fertility with no partnering channel is C.2.h's; one
that runs through partnering is shared, tagged `SECONDARY_TECH_FERTILITY`, and **only one chapter may
claim the magnitude in synthesis**. Without this rule the two chapters double-count the same
coefficient. This is A.12's Call 3 in a new setting.

**Call 3 — is pre-app online dating (1995–2012) in scope?** *Recommended:* **yes.** Excluding it
deletes Rosenfeld & Thomas 2012, Hitsch Hortaçsu & Ariely 2010, Bellou 2014 and the entire identified
literature, leaving a chapter about a decade-old technology with no estimates. v5's own framing
("swiping", "commodification") is app-specific, so the chapter must then report the app-era subset
separately rather than pooling across a technological discontinuity.

**Call 4 — what verdict does an empty primary cell earn?** `PRIMARY_APP_FERTILITY` is expected to be
empty. PROTOCOL §6 needs to say whether that is *Insufficient Evidence* or a graded *no demonstrated
effect*. The distinction matters because A.24 is a live public claim, and "no evidence" and "evidence
of no effect" are read very differently by the audience for the living resource.

**Call 5 — how is contrary evidence graded?** Rosenfeld 2017 and Billari et al. 2019 estimate the
right relationships with the wrong sign for v5. *Recommended:* grade them as evidence on the
registered estimand — i.e. the chapter can return a negative verdict with a non-trivial GRADE rating
rather than an empty one. Flagged because it determines whether the chapter has a GRADE table at all.

## Next

A3 cold-start anchor resolution (script 172), on 25 anchors spanning: `PRIMARY_APP_UNION` (Rosenfeld
2017, Erevik 2020, Potarca 2020), `SECONDARY_TECH_*` (Bellou 2014, Billari et al. 2019, Kalabikhina
et al. 2020), `MECHANISM_CHOICE_FRICTION` (Pronk & Denissen 2019, D'Angelo & Toma 2016, Jung et al.
2021), `EXPOSURE_SERIES` (Rosenfeld & Thomas 2012, Rosenfeld Thomas & Hausen 2019), and one routing
decoy per enforceable wall. Carry the Rosenfield misspelling and the two preprint-only records into
A3 as known exceptions.
