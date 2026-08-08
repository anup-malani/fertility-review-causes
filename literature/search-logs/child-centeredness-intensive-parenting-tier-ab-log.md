# A4 Tier-A / Tier-B frame — child-centeredness-intensive-parenting (D.2.d)

Candidate frame, **not** screened or frozen. Two-tier GACS: Tier A = direct-empirical seeds; Tier B = orthogonal backward+forward citation frame.

OpenAlex auth: api_key present.

## Tier A (empirical seeds, enriched)

- resolved empirical seeds: **7**

| cell | n |
|---|---|
| COST_INDEPENDENCE | 1 |
| PRIMARY_NORM_EXPOSURE | 2 |
| PRIMARY_PERCEIVED_STANDARD | 2 |
| PRIMARY_TIME_INTENSITY | 2 |

## Anchor resolution

- input anchors: 23
- OpenAlex-resolved: 20
- unresolved (below sim 0.5, or book with no book-shaped record): 3
- deferred (network, resume on re-run): 0

## Tier B (citation frame)

- deduplicated candidates: **2,677**
- found by both channels: 20
- with usable abstracts: 1,881
- duplicates merged: 10
- forward pages requested/cached: 23
- seeds hitting the 12-page cap: 0

### Forward-seed policy (transparency)

Forward-cited anchors (19):
- OK On the Interaction between the Quantity and Quality of Child (cb=506)
- OK Parenting With Style: Altruism and Paternalism in Intergener (cb=347)
- OK Social Class, Gender, and Contemporary Parenting Standards i (cb=288)
- OK Trade-offs in modern parenting: a longitudinal study of sibl (cb=198)
- OK The Rug Rat Race (cb=188)
- OK Why did rich families increase their fertility? Inequality a (cb=178)
- OK Love, Money, and Parenting (cb=64)
- OK Costly children: the motivations for parental investment in  (cb=45)
- OK The Time Cost of Raising Children in Different Fertility Con (cb=43)
- OK “If I’m Going to Do It, I’m Going to Do It Right”: Intensive (cb=40)
- OK Women’s housework decreases fertility (cb=40)
- OK Do Socioeconomic Differences in Family Size Reflect Cultural (cb=17)
- OK Completed Fertility and its Timing: An Economic Analysis of  (cb=13)
- OK Intensive Parenting: Fertility and Breastfeeding Duration in (cb=11)
- OK Ready for Parenthood? On Intensive Parenting Ideals and Fert (cb=5)
- OK How much do norms matter for quantity and quality of childre (cb=4)
- OK Home Alone: Exploring Childcare Options to Remove Barriers t (cb=3)
- OK Parenting on a budget (cb=2)
- OK The good parent: Emerging themes and gender convergence in n (cb=1)

Forward-EXCLUDED anchors (1) — backward refs still used:
- XX Unequal Childhoods (cb=2172, cloud 2172 > cap 1000)

## Unresolved anchors

Book anchors below are refused deliberately: the title path returns only reviews of the work, and a review's reference list and citation cloud are not the book's. The loss is real and is recorded here rather than absorbed silently.

- The Cultural Contradictions of Motherhood (sim 0.0, book_no_openalex_record, book) — PARENTING_NORM_THEORY
- Pricing the Priceless Child: The Changing Social Value of  (sim 0.0, book_no_openalex_record, book) — FDT_SENTIMENTALIZATION_CONTEXT
- Centuries of Childhood: A Social History of Family Life (sim 0.0, book_no_openalex_record, book) — FDT_SENTIMENTALIZATION_CONTEXT

## Next gate

Screen the whole Tier-B frame with the D.2.d rubric, routing on the six boundary walls (vs C.3.d quantity-quality, C.2.f inequality/status, C.2.b direct costs, C.2.e female wage, C.2.a childcare, D.2.a gender equity). Four of the six are NOT enforceable at title/abstract — see the enforceability table in the scope doc — so the screen assigns a provisional cell and records `ROUTING_DEFERRED_TO_FULLTEXT` rather than guessing an `OFF_*` label. Do NOT prune the frame by vocabulary distance from the future production query; that would bias Recall(B). The seven routing decoys (Becker-Lewis C.3.d, Hazan-Zoabi C.2.f, OECD C.2.b, Butz-Ward C.2.e, Ishchanova C.2.a, Miettinen D.2.a, and the Lawson-Mace REVERSE decoy) must surface as route-away at screen.
