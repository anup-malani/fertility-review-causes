# Search scope — cultural westernization and developmental idealism

**Hypothesis:** D.1.b (HYPOTHESES-v5.md)
**Hypothesis slug:** `caldwell-wealth-flows-westernization`
**Target phenomena:** FDT and SDT. No pre-modern cell, and the FDT cell is restricted to the *diffused*
transition — see "Phenomenon scope" below.
**Ticket:** TICK-063
**Status:** boundary walls **FROZEN** (Shravan, 2026-08-07) — hard lines on all six. Both scope calls
approved as recommended: (i) the FDT cell is restricted to the diffused transition, so the historical
Western transition enters only as the source of the package; (ii) reduced-form schooling estimates
that decompose no mechanism take `MECHANISM_UNRESOLVED_SCHOOLING` and stay out of the pool, reported
as a count. Anchors sourced and existence-verified. Ready for A4.

## A note on the slug

The slug says `caldwell-wealth-flows-westernization` and the file names built from it will too. It is
kept for continuity with the ticket and the branch, but it names the wrong half of Caldwell. Under v5,
**the wealth-flows mechanism is C.3.f and this chapter is the cultural channel only.** Everywhere the
two are in tension, v5 §D.1.b's claim text governs and the slug is treated as an inherited label.

## Causal claim

A package of beliefs about what modernity is — that a modern family is nuclear and conjugal rather than
extended and kin-embedded, marries late by choice rather than early by arrangement, treats spouses as
equals, invests heavily in few children, and is therefore small — has diffused globally from Western
societies through mass schooling, mass media, development institutions, and direct contact. Where the
package is absorbed, family aspirations and then fertility move toward it. The distinguishing feature is
that this happens **independently of structural economic change**: the belief that small families are
what modern people have arrives before, and can act without, the income growth, urbanization, mortality
decline, or child-cost inflation that the belief describes.

Caldwell's version routes the mechanism through mass schooling, which he argued restructures authority
and obligation inside the family before it changes any wage or price. Thornton's developmental idealism
is the general form: a causal *belief* about development, held by ordinary people and propagated by
states and international organizations, that is itself a cause of the change it forecasts.

## Phenomenon scope, and the FDT restriction

**PM: no cell.** The mechanism requires an external society already identified with modernity. There is
none before the transition begins.

**FDT: the diffused transition only.** This is a substantive restriction, not a technicality. For the
historical Western transition of roughly 1870–1930 the westernization claim is degenerate — there was
no external West to import a family model from, and the within-Europe spread of small-family practice
along linguistic and religious lines is the Princeton finding, which v5 files at A.3 and A.20. So the
FDT cell here covers **societies entering fertility transition after roughly 1945 under exposure to an
external modern model**: post-colonial Asia, Africa, Latin America, and the Middle East. The historical
Western FDT enters only as the *source* of the diffused package, never as a case of it.

**SDT: in scope,** where the claim is that late-transition and post-transition societies continue to
converge on a Western family model — East Asian and Southern European marriage postponement, the
spread of the conjugal-nuclear ideal in the Gulf and South Asia, immigrant fertility convergence toward
host-country norms.

*Call 1 — APPROVED (2026-08-07).* The FDT restriction above is frozen. The alternative considered and
declined was to carry the historical Western FDT and treat "westernization" as within-Europe diffusion,
which would make this chapter and A.3 near-duplicates and would hand it the entire Princeton corpus.

## The six boundary walls

D.1.b sits at the intersection of the most heavily populated literatures in the review. Almost every
candidate paper will belong to a neighbour. Routing is the central screening task, and the walls below
are load-bearing in the same way B.1's sex-drive wall and D.3.b's three walls were.

**Wall 1 — D.1.b vs C.3.f (Intergenerational Wealth Flows Reversal, `wealth-flows-reversal`).** The
sharpest wall, because both are Caldwell and share his vocabulary wholesale.
- **C.3.f asks:** does the net direction of transfers between generations reverse, and does that reversal
  reduce fertility? Its operative variable is a *flow* — child labour contributions, remittances to
  parents, old-age support, the National Transfer Accounts lifecycle deficit.
- **D.1.b asks:** does exposure to a normative model of the modern family reduce fertility, whether or
  not any flow has reversed?
- **Discriminator:** what does the estimate actually vary? A study measuring transfers, their direction,
  or their magnitude routes to `OFF_WEALTH_FLOWS_C3f` **even when it cites Caldwell's cultural
  argument in its framing.** A study measuring beliefs, ideals, or exposure to an external family model
  is D.1.b. Caldwell's own joint claim — that schooling reverses the flows *by* restructuring family
  morality — belongs here only when the estimate isolates the ideational side of the joint claim.

**Wall 2 — D.1.b vs D.1.a (Postmaterialism, `postmaterialism-individualism-secularization`).** v5 draws
this line as internal versus external, and that is the right line.
- **D.1.a asks:** why do people in already-modernized, affluent, secure societies come to value
  self-actualization and autonomy over family formation? The value change is endogenous to affluence.
- **D.1.b asks:** why do people in societies that have *not yet* undergone the structural change adopt
  the family model of societies that have? The value change is imported.
- **Discriminator, two-part.** *Content:* D.1.a's content is the self — autonomy, self-realization,
  freedom from obligation, non-child consumption. D.1.b's content is a *family form* — nuclear
  residence, conjugal primacy, self-chosen spouse, late marriage, gender equality, intensive investment
  in few children. *Direction:* D.1.a's values arise from within a rich society; D.1.b's arrive from an
  identified external reference point. A paper on individualism and childlessness in Northern Europe is
  D.1.a. A paper on the spread of the conjugal-nuclear ideal in rural Nepal is D.1.b.
- **Immigrant-fertility seam.** Studies of migrants converging on host-country fertility are D.1.b when
  the estimand is *convergence with exposure* (duration, generation, host-language acquisition,
  enclave density). They are A.19 when the estimand is *persistence of origin norms* net of
  environment — the Fernández–Fogli epidemiological design. Same data, different estimand, different
  chapter.

**Wall 3 — D.1.b vs A.20 (Cultural Diffusion Mechanisms) and A.3 (Diffusion of Fertility Control).**
Content versus channel versus contraceptive information. This wall decides the disposition of the
strongest quasi-experiments in the whole cultural literature, so it is written tightly.
- **A.20 is the channel:** how any norm spreads — network position, media reach, distance, linguistic
  and religious community boundaries. Content-agnostic by construction.
- **A.3 is a specific content:** that birth control exists, works, and is permissible.
- **D.1.b is a different specific content:** that the modern family is small, nuclear, late-marrying,
  and egalitarian, and that this is what development looks like.
- **Discriminator:** ask what the treatment delivers. Contraceptive knowledge or legitimation → A.3.
  A channel whose content is unspecified, or an estimand about the geometry of spread → A.20. Depiction
  of or instruction in a modern family model, with the paper attributing its effect to that aspirational
  content → D.1.b.
- **Dual-home rule.** The television quasi-experiments (Brazilian novelas, Indian cable) are *both* the
  cleanest identification of a diffusion channel and the cleanest identification of family-model content.
  They are claimed here when the paper's own mechanism evidence is about the depicted family — the
  small, wealthy, autonomous television family — and by A.20 when the estimand is the channel. Where
  both readings are live, the paper is tagged `PRIMARY_MEDIA_WESTERN_MODEL` **and** carries
  `shared_with: A.20`, so the same study can be cited in both chapters against different estimands
  without being pooled twice. This is a deliberate departure from D.3.b's exclusive routing, and it is
  confined to Wall 3.

**Wall 4 — D.1.b vs D.2.a (Female Empowerment and Gender Equity) and C.2.e (Female Wage).** Gender
equality is *inside* the developmental-idealism package, so without this wall D.1.b swallows the entire
female-education literature.
- **D.2.a's operative variable** is a woman's own autonomy, bargaining position, or aspiration.
- **C.2.e's** is the price of her time.
- **D.1.b's** is a society-level normative model of the modern family, of which gender equality is one
  element, propagated to men and women alike from an external reference point.
- **Discriminator:** whose belief is doing the work, and about what? Women's own autonomy → D.2.a.
  A shared belief about what modern families look like, held by husbands, mothers-in-law, and community
  alike → D.1.b. Developmental-idealism instruments that ask respondents what *developed countries*
  do about marriage age and women's work are D.1.b even when every item concerns gender.

**Wall 5 — D.1.b vs C.3.b (Child Labour Restrictions and Compulsory Schooling) and the human-capital
reading of education.** Same treatment, different mechanism, and the hardest wall to enforce.
- **C.3.b's mechanism** is cost and return: schooling removes child labour income and converts children
  into expenses.
- **D.1.b's mechanism** is what schooling *teaches and legitimizes* — a curriculum and an institutional
  form that carry a model of the modern family, and that relocate authority from elders to the school
  and the state.
- **Discriminator:** does the design isolate ideational content — curriculum variation, exposure to
  mission or colonial schooling, effects surviving adjustment for literacy and wage returns, effects on
  people whose own schooling did not change but whose community's did — or does it rest on cost and
  return?
- **The unresolved majority.** Most schooling → fertility estimates decompose no mechanism at all. They
  are neither D.1.b nor C.3.b on their own evidence. They take `MECHANISM_UNRESOLVED_SCHOOLING`, verdict
  `UNCERTAIN`, and are counted as the coverage denominator for this wall. **They never enter a pooled
  estimate here.** Reporting how large that class is relative to the class that does decompose is itself
  a finding about the field, and is expected to be the chapter's central honest number.

*Call 2 — APPROVED (2026-08-07).* `MECHANISM_UNRESOLVED_SCHOOLING` stays out of the pool and is
reported as a count. The alternative considered and declined was to admit reduced-form schooling
estimates to a primary cell and downgrade for indirectness at GRADE; that would let the
best-identified literature in the review answer a question it was not designed to answer, which is
exactly the failure the estimand gate exists to prevent.

**Wall 6 — D.1.b vs D.1.c (Cultural Evolution and Maladaptive Low Fertility).** Both say low fertility
spreads by imitation.
- **D.1.c's model** is prestige-biased transmission: people copy high-status individuals, and content
  is incidental to the mechanism. Typically within-society.
- **D.1.b's model** is the diffusion of a specific package identified with the West and with modernity,
  from outside.
- **Discriminator:** a paper that formally models status- or prestige-biased copying is D.1.c, even when
  the copied behaviour is Western. A paper whose exposure variable is contact with, or belief about,
  an external modern society is D.1.b.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_DI_BELIEF` | Measured developmental-idealism beliefs — that development brings or requires small families, late marriage, nuclear residence, gender equality (Thornton-style DI instruments) | Fertility, intentions, or ideal family size | Primary synthesis |
| `PRIMARY_SCHOOLING_IDEATIONAL` | Schooling exposure where the design isolates ideational content from wage and child-cost returns | Fertility or family-formation | Primary synthesis |
| `PRIMARY_MEDIA_WESTERN_MODEL` | Exposure to media carrying modern-family depictions (television, radio serials, film, internet) | Fertility or family-formation aspirations | Primary synthesis; may carry `shared_with: A.20` |
| `PRIMARY_WESTERN_CONTACT` | Direct contact with Western institutions — missions, colonial administration, development programmes, return migration, tourism, foreign employment | Fertility | Primary synthesis |
| `DIFFUSION_INDEPENDENT_OF_STRUCTURE` | Any of the above, where the design shows the ideational effect **net of, or in the absence of,** structural economic change | Fertility | Primary / bridge — the value-added cell |
| `DI_THEORY` | Caldwell's and Thornton's theoretical statements; developmental-idealism conceptual work; world-society and world-polity theory; modernization-theory critique | No empirical fertility estimate | Theory stream |
| `MECHANISM_UNRESOLVED_SCHOOLING` | Schooling or education → fertility with no mechanism decomposition | Fertility | Wall-5 denominator; never pooled |
| `OFF_WEALTH_FLOWS_C3f` | Net intergenerational transfers, child labour contribution, old-age support, NTA lifecycle deficit | Fertility | Route to C.3.f |
| `OFF_POSTMATERIALIST_D1a` | Internal value change in an already-modernized society; self-actualization and autonomy content | Fertility | Route to D.1.a |
| `OFF_DIFFUSION_CHANNEL_A20` | The geometry of the diffusion channel, content unspecified | Fertility | Route to A.20 |
| `OFF_FERTILITY_CONTROL_A3` | Diffusion of contraceptive knowledge or legitimation | Fertility | Route to A.3 |
| `OFF_FEMALE_AUTONOMY_D2a` | Women's own autonomy, bargaining power, or aspiration as the operative variable | Fertility | Route to D.2.a |
| `OFF_SCHOOLING_ECONOMIC` | Schooling or female wage acting through cost, return, or opportunity cost, with the mechanism identified | Fertility | Route to C.3.b / C.2.e |
| `OFF_CULTURAL_EVOLUTION_D1c` | Formally modelled prestige- or status-biased transmission | Fertility | Route to D.1.c |
| `OFF_OTHER` | A non-D.1.b determinant with no sibling home | Fertility | Route out |
| `OFF_OUTCOME` | Developmental-idealism beliefs or Western exposure → a non-family outcome (politics, consumption, health, migration) | No family outcome | Mechanism or context only |
| `REVERSE` | Fertility or family status → developmental-idealism beliefs | Belief outcome | Context |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

## Two mandatory tags on every included empirical paper

**Outcome level.** `REALIZED_FERTILITY` (births, parity, completed family size); `STATED_INTENTION_OR_IDEAL`
(intentions, desired or ideal family size); `FAMILY_FORMATION_BEHAVIOUR` (age at marriage, spouse choice,
nuclear residence, marriage arrangement). The third is in scope because the developmental-idealism package
is a claim about the whole family form, and because its earliest observable effects appear there rather
than in births. **The three levels are never pooled together.** A family-formation result is evidence for
the mechanism and is not evidence about fertility until a birth is measured.

**Structural controls actually adjusted for.** Which of household income or wealth, urbanization, child
mortality, women's employment, schooling-as-human-capital, and contraceptive access the design holds
fixed. This is not descriptive metadata: Wall 1 and the whole content of the hypothesis turn on whether
the ideational effect survives structural adjustment, so the identification value of an estimate is set
by this field. A DI-belief association adjusting for none of them documents a correlation and must not be
described as evidence that belief moved fertility independently of structure.

## Eligibility rules

- Include an empirical study only when the estimate bears on **exposure to, or absorption of, an
  external model of the modern family → fertility, fertility intentions, or family-formation behaviour.**
- The Caldwell and Thornton theoretical canon, world-society theory, and modernization-theory critique
  seed the **theory stream** and do **not** count toward empirical recall.
- A study whose operative variable is a transfer, a price, a wage, a woman's own autonomy, or
  contraceptive knowledge routes to its sibling hypothesis even when it invokes westernization in its
  framing. **Judge the estimand, not the framing sentence.**
- Reduced-form schooling → fertility estimates with no mechanism decomposition are recorded under
  `MECHANISM_UNRESOLVED_SCHOOLING` and excluded from the pool. They are reported as a count.
- Family-formation outcomes are in scope, tagged, and never pooled with births.
- Historical Western FDT evidence is carried only as the source of the diffused package, not as a case
  of diffusion.

## When to adjudicate mechanisms

The title/abstract screen decides only stream membership: empirical D.1.b, theory, unresolved schooling,
or a sibling chapter. It does **not** ask the screener to determine which of the four primary channels a
paper identifies, and it cannot enforce Wall 5 — whether a schooling estimate decomposes its mechanism
lives in the results tables, invisible to an abstract. **This is the same limit the D.3.b screen hit on
its Wall 1, and it is recorded here in advance rather than discovered in an audit.** Wall 5 and the
structural-controls field are therefore enforced at extraction.

Full-text extraction must record, for every included empirical paper: the primary channel; the outcome
level; the structural controls adjusted for; whether the design establishes independence from structural
change; and, for schooling papers, whether and how the mechanism was decomposed.

## Expected shape of the evidence

Three things to expect, and to report honestly rather than paper over.

1. **The exposure is measured well in one literature and not at all in the others.** Thornton's DI
   surveys (Nepal, Argentina, Egypt, China, Vietnam, Malawi, and others) are purpose-built instruments
   that ask people directly what they believe about development and family. Almost everything else
   proxies exposure with schooling years, media access, or distance to a mission. Expect the
   best-measured exposure to sit in the smallest and least well-identified stratum, and the
   best-identified designs to have the crudest exposure measure. That trade-off is the chapter's
   organizing tension.

2. **The value-added cell is likely to be nearly empty.** Showing an ideational effect *net of*
   structural change requires either a setting where structure did not move or a design that holds it
   fixed convincingly. Few studies attempt it. As with D.3.b's `DESIRE_INDEPENDENCE`, expect a handful
   at most, and do not manufacture a pooled estimate for the distinctive claim if the literature does
   not support one.

3. **The central identification threat is that the package is the same bundle as development itself.**
   Western contact, schooling, media access, urbanization, income, and mortality decline all arrive
   together. A raw association between exposure to modern ideals and low fertility is exactly what
   every structural theory also predicts. The `DIFFUSION_INDEPENDENT_OF_STRUCTURE` cell and the
   structural-controls field exist to separate them; expect few designs to manage it.

## Cold-start channels and leakage wall

1. Prior systematic reviews and meta-analyses of ideational or diffusion effects on fertility, and the
   included-study lists of the developmental-idealism programme, seed the empirical Tier-A candidates by
   external authority. This is the privileged channel.
2. Caldwell's and Thornton's theoretical canon, and world-society theory, seed the theory set and do not
   count toward empirical recall.
3. References and citations of the channel-1 and channel-2 seeds create the orthogonal Tier-B frame.
4. Query terms mined from a source may not be evaluated on that same source; learned extensions are
   fold-local only, after the gold frame exists.

## Pre-query anchor audit (not yet built)

Anchors will be stored at `caldwell-wealth-flows-westernization-cold-start-anchors.json`. Every anchor
clears the **mandatory existence-verification gate** — a live DOI or a Crossref record confirming the
title — before entering any recall denominator. No anchor is asserted from memory. This literature has
two specific ghost risks worth naming in advance: Caldwell's and Thornton's canon is old enough that
book chapters and monographs will legitimately miss Crossref's article index and must be carried rather
than dropped, and the v5 seminal list for this entry ("Caldwell 1980, Caldwell 1982, Thornton 2001,
Thornton 2005") is exactly the kind of short-form citation that resolved to a non-existent paper for
D.3.b. Each is verified independently before use.

The anchor set will deliberately include decoys for all six walls — a wealth-flows study, a
postmaterialism study, a channel-only diffusion study, a contraceptive-diffusion study, a female-autonomy
study, and a reduced-form schooling study — so the eventual search is tested on routing as well as on
topical retrieval.
