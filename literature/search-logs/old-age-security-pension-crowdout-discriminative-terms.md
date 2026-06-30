# Discriminative terms (Part 3b) · 2026-06-29

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over TITLES: gold-positive (303) vs on-disk NOT_RELEVANT (4537). Higher z = more gold-discriminative. Negatives already passed the PI keyword filter → contrast is relevant-vs-near-miss. In Part-4 CV this is recomputed fold-locally.

Candidates (gold count ≥ 3): **193** terms.


## FERTILITY block — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| fertility | 18.26 | 1.41 | 200 | 763 |
| endogenous fertility | 11.19 | 4.61 | 46 | 6 |
| children | 7.2 | 1.34 | 34 | 135 |
| child care | 5.8 | 2.78 | 9 | 8 |
| fertility social | 5.53 | 5.18 | 15 | 1 |
| value children | 4.4 | 3.16 | 5 | 3 |
| child | 3.98 | 0.85 | 23 | 155 |
| child allowances | 3.92 | 3.34 | 4 | 2 |
| family fertility | 3.7 | 2.45 | 4 | 5 |
| reform fertility | 3.68 | 4.0 | 4 | 1 |
| fertility germany | 3.68 | 4.0 | 4 | 1 |
| fertility related | 3.4 | 3.06 | 3 | 2 |
| fertility theory | 3.4 | 3.06 | 3 | 2 |
| children old | 3.3 | 3.73 | 3 | 1 |
| growth fertility | 3.3 | 3.73 | 3 | 1 |
| fertility education | 3.17 | 2.38 | 3 | 4 |
| fertility human | 3.17 | 2.38 | 3 | 4 |
| fertility child | 3.02 | 2.17 | 3 | 5 |
| fertility behaviour | 2.87 | 1.99 | 3 | 6 |
| fertility rural | 2.87 | 1.99 | 3 | 6 |
| fertility decisions | 2.84 | 1.6 | 4 | 12 |
| childcare | 2.64 | 1.46 | 4 | 14 |
| fertility behavior | 2.46 | 1.6 | 3 | 9 |
| fertility endogenous | 1.85 | 6.92 | 5 | 0 |
| children philippines | 1.43 | 6.92 | 3 | 0 |

## PENSION / OLD-AGE-SECURITY block — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| security | 15.12 | 1.56 | 117 | 374 |
| old age | 12.24 | 2.26 | 47 | 72 |
| age security | 11.31 | 3.26 | 33 | 18 |
| social security | 11.23 | 1.35 | 82 | 327 |
| pensions | 10.2 | 1.52 | 56 | 186 |
| intergenerational | 7.36 | 1.97 | 20 | 41 |
| payg | 6.27 | 2.58 | 11 | 12 |
| you pension | 5.73 | 2.34 | 10 | 14 |
| pensions endogenous | 5.72 | 3.73 | 9 | 3 |
| intergenerational transfers | 5.45 | 3.61 | 8 | 3 |
| payg pensions | 5.45 | 3.61 | 8 | 3 |
| transfers | 5.31 | 1.68 | 13 | 36 |
| security endogenous | 5.21 | 4.0 | 8 | 2 |
| security hypothesis | 4.44 | 4.52 | 7 | 1 |
| pension | 4.43 | 0.52 | 71 | 697 |
| security family | 3.98 | 4.21 | 5 | 1 |
| age pensions | 3.82 | 2.66 | 4 | 4 |
| savings | 3.5 | 1.26 | 9 | 39 |
| security rural | 3.4 | 3.06 | 3 | 2 |
| insurance | 3.37 | 0.89 | 15 | 96 |
| security saving | 3.3 | 3.73 | 3 | 1 |
| security reform | 3.28 | 1.67 | 5 | 14 |
| pension system | 3.11 | 0.79 | 16 | 115 |
| public pensions | 3.11 | 1.27 | 7 | 30 |
| payg pension | 3.02 | 2.17 | 3 | 5 |

## BOTH-block (fertility×pension bigrams) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| security fertility | 5.91 | 5.37 | 19 | 1 |
| pensions fertility | 3.69 | 6.92 | 20 | 0 |
| saving fertility | 3.68 | 4.0 | 4 | 1 |
| savings fertility | 3.3 | 3.73 | 3 | 1 |
| fertility retirement | 3.3 | 3.73 | 3 | 1 |
| pension fertility | 2.02 | 6.92 | 6 | 0 |
| fertility pension | 2.02 | 6.92 | 6 | 0 |
| pensions child | 1.43 | 6.92 | 3 | 0 |
| pension child | 1.43 | 6.92 | 3 | 0 |

## OTHER (context terms) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| endogenous | 15.08 | 3.98 | 66 | 17 |
| old | 11.56 | 2.01 | 48 | 95 |
| age | 8.85 | 1.35 | 51 | 202 |
| growth | 8.21 | 1.58 | 34 | 105 |
| pay you | 8.17 | 2.26 | 21 | 32 |
| social | 7.86 | 0.86 | 88 | 594 |
| you | 7.33 | 1.89 | 21 | 47 |
| pay | 7.22 | 1.85 | 21 | 49 |
| generations | 6.12 | 2.43 | 11 | 14 |
| overlapping | 5.63 | 4.21 | 10 | 2 |
| overlapping generations | 5.63 | 4.21 | 10 | 2 |
| theory | 5.6 | 1.92 | 12 | 26 |
| hypothesis | 5.15 | 3.49 | 7 | 3 |
| allowances | 5.15 | 3.49 | 7 | 3 |
| endogenous growth | 5.07 | 4.92 | 11 | 1 |
| economic growth | 4.52 | 1.44 | 12 | 43 |
| support | 4.41 | 1.39 | 12 | 45 |
| care policies | 4.36 | 2.88 | 5 | 4 |
| rural india | 4.23 | 4.38 | 6 | 1 |
| capital | 4.2 | 1.31 | 12 | 49 |
| motives | 4.17 | 2.49 | 5 | 6 |
| optimal | 4.13 | 1.54 | 9 | 29 |
| human capital | 4.02 | 1.6 | 8 | 24 |
| you social | 3.98 | 4.21 | 5 | 1 |
| altruism | 3.92 | 3.34 | 4 | 2 |
