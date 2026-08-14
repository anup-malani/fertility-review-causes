# D1 deterministic rank and screening cutoff — microplastics-pfas-reproductive (B.6)

Frame in: **14,561** Tier B records. After collapsing **265** version duplicates on normalized title: **14,296** distinct works.

**Screened: 920** — the top **700** by D1 score, plus **0** orthogonal-channel bypasses, plus **220** both-axes completeness bypasses. **Left unscreened: 13,376.**

**Score at the margin: 60.**

## Chemical family — the split the chapter runs on

Assigned deterministically from the named compound, which is the one routing call reliably visible in a title. `both` is Wall 1's mixture case and is never collapsed to one side.

| family | whole frame | carrying both axes | in the worklist |
|---|---|---|---|
| `pfas` | 3,550 | 331 | 525 |
| `plastic` | 5,865 | 168 | 298 |
| `both` | 50 | 4 | 10 |
| `none` | 4,831 | 0 | 87 |

**Every record carrying both axes is screened, whatever its family and whatever its rank** — 220 were admitted that way, below the budget cutoff. The rule began as a microplastics-only precaution, so that half's expected finding of 'no human study estimates this quantity' could be distinguished from never having looked; it was made family-blind after the first run left 135 both-axes PFAS records unscreened while giving the plastic side complete coverage. The cross-axis AND is this ranker's precision engine, so a record satisfying it is what the screen exists to read.

## What the cutoff drops, stated rather than implied

Of the 13,376 unscreened records, 0 carry terms from both axes and 0 were reached from an empirical primary anchor (those without a fertility-axis term, which the bypass requires). The unscreened set is characterized by:

- 12,045 — no fertility-axis term at all
- 4,744 — no exposure-axis term at all
- 3,059 — environmental-fate vocabulary
- 2,593 — non-human vocabulary (Wall 5)
- 1,242 — non-reproductive PFAS outcome
- 843 — pregnancy-safety vocabulary (Wall 2)
- 795 — in-vitro vocabulary (Wall 6)
- 194 — soil-fertility homonym (Wall 8)

This is a **budget-bounded screen, not an exhaustive one**, and the number above is the honest size of the residual. Two things bound the risk. The cross-axis AND is the precision engine, so a record with no exposure term and no fertility term is very unlikely to bear on B.7's estimand; and the bypass means a paper reached from a primary anchor is read even when its keyword signal is weak, which is where the quirky-titled canon lives. Extending the screen deeper is the obvious next increment if the yield at the margin is still non-trivial.

## Ranking design

The score is the two-axis term match (title hits counted twice, since a title states the subject and an abstract merely mentions it), plus a cross-axis bonus, plus channel features (multi-seed corroboration, reached-from-a-primary-anchor, present in an anchor's own reference list), minus demotions for non-human and clinical-management vocabulary.

**The demotions are ranking signals and remove nothing.** B.7's two largest expected off-cells are the pregnancy-safety literature (Wall 4) and the aquatic-ecotoxicology literature (Wall 7), and a filter deleting them would delete the boundary cases sitting alongside them — an antidepressant-and-miscarriage study is one word away from a pregnancy-safety study and belongs to B.5. The fertility-clinic penalty is deliberately near-zero because the chapter's ART decoy returned the highest on-topic fraction of any seed cloud in the A4 frame.

## Top 25 by D1 score

| rank | score | axes | seeds | year | title |
|---|---|---|---|---|---|
| 1 | 232 | both | 13 | 2014 | Perfluoroalkyl substances and time to pregnancy in couples from Greenland, Pol |
| 2 | 150 | both | 7 | 2017 | Plasma Perfluoroalkyl and Polyfluoroalkyl Substances Concentration and Menstru |
| 3 | 150 | both | 6 | 2021 | Perfluoroalkyl Chemicals and Male Reproductive Health: Do PFOA and PFOS Increa |
| 4 | 144 | both | 15 | 2015 | Serum perfluoroalkyl acids and time to pregnancy in nulliparous women |
| 5 | 144 | both | 3 | 2022 | Preconception exposure to perfluoroalkyl and polyfluoroalkyl substances and co |
| 6 | 137 | both | 10 | 2018 | Conditioning on Parity in Studies of Perfluoroalkyl Acids and Time to Pregnanc |
| 7 | 136 | both | 5 | 2020 | Maternal Plasma Perfluoroalkyl Substances and Miscarriage: A Nested Case–Contr |
| 8 | 131 | both | 5 | 2012 | Commentary |
| 9 | 128 | both | 3 | 2023 | Adverse effects of microplastics and nanoplastics on the reproductive system:  |
| 10 | 127 | both | 9 | 2016 | Perfluoroalkyl Chemicals, Menstrual Cycle Length, and Fecundity |
| 11 | 125 | both | 11 | 2024 | Effects of Per- and Polyfluoroalkylated Substances on Female Reproduction |
| 12 | 124 | both | 8 | 2017 | Perfluoroalkyl substances and endometriosis-related infertility in Chinese wom |
| 13 | 124 | both | 2 | 2023 | Associations between lifestyle factors and levels of per- and polyfluoroalkyl  |
| 14 | 120 | both | 8 | 2023 | Exposure to perfluoroalkyl substances and women's fertility outcomes in a Sing |
| 15 | 119 | both | 4 | 2023 | Toxic effects of per- and polyfluoroalkyl substances on sperm: Epidemiological |
| 16 | 119 | both | 1 | 2025 | Per- and PolyfluoroalkylSubstances in Semen Associatedwith Repeated Measures o |
| 17 | 118 | both | 3 | 2022 | Association between Perfluoroalkyl and Polyfluoroalkyl Substances and Women’s  |
| 18 | 117 | both | 8 | 2012 | Persistent Environmental Pollutants and Couple Fecundity: The LIFE Study |
| 19 | 116 | both | 9 | 2017 | Effects of perfluorinated chemicals on thyroid function, markers of ovarian re |
| 20 | 115 | both | 4 | 2023 | Toxicity of microplastics and nanoplastics: invisible killers of female fertil |
| 21 | 115 | both | 3 | 2025 | Maternal exposure to polystyrene nanoplastics during gestation and lactation c |
| 22 | 113 | both | 4 | 2015 | Sociodemographic and Perinatal Predictors of Early Pregnancy Per- and Polyfluo |
| 23 | 113 | both | 2 | 2025 | Per- and polyfluoroalkyl substances in dog blood serum levels and semen qualit |
| 24 | 112 | both | 6 | 2019 | Perfluoroalkyl substances exposure and risk of polycystic ovarian syndrome rel |
| 25 | 112 | both | 1 | 2022 | Clinical study on the treatment of male infertility with Wuwei Fuzheng Yijing  |
