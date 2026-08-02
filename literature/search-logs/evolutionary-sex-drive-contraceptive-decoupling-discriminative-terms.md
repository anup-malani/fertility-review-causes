# Discriminative terms (A6a) — evolutionary-sex-drive-contraceptive-decoupling

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over TITLES: RELEVANT+seeds (162) vs screen NOT_RELEVANT (4435). Higher z = more discriminative of the on-topic class. Negatives passed the citation-frame + screen → contrast is relevant-vs-near-miss (precision at recall). In A6b this is recomputed fold-locally for the CV.

Candidate terms (gold count ≥ 3): **127**. By block: effect 11, cause 20, both 7, other 89


## EFFECT block (fertility / reproductive outcome) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| reproductive success | 7.56 | 2.1 | 18 | 40 |
| reproductive | 7.41 | 1.31 | 35 | 181 |
| childbearing | 5.85 | 1.43 | 19 | 86 |
| reproduction | 5.47 | 1.87 | 11 | 31 |
| cultural reproductive | 3.49 | 3.91 | 3 | 1 |
| fertility behavior | 3.17 | 2.19 | 3 | 6 |
| reproductive behavior | 3.17 | 2.19 | 3 | 6 |
| fertility | 2.23 | 0.31 | 42 | 692 |
| low fertility | 2.04 | 1.03 | 4 | 28 |
| fertility desires | 1.19 | 0.66 | 3 | 32 |
| birth | -0.55 | -0.25 | 3 | 110 |

## CAUSE block (evolutionary / sex-drive / decoupling / motivation / contraception) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| motivation | 6.69 | 2.42 | 12 | 19 |
| status | 5.23 | 1.28 | 18 | 95 |
| social status | 4.58 | 2.28 | 6 | 11 |
| motivations | 4.48 | 2.19 | 6 | 12 |
| mating | 4.2 | 1.26 | 12 | 65 |
| evolutionary | 3.81 | 0.81 | 21 | 188 |
| motivational | 3.49 | 3.91 | 3 | 1 |
| problem sociobiology | 3.49 | 3.91 | 3 | 1 |
| evolutionary demography | 2.91 | 1.92 | 3 | 8 |
| evolutionary perspective | 2.61 | 1.38 | 4 | 19 |
| sexual selection | 2.2 | 1.33 | 3 | 15 |
| fitness | 2.18 | 0.98 | 5 | 37 |
| pill | 2.13 | 0.86 | 6 | 51 |
| sexual | 1.93 | 0.66 | 8 | 86 |
| contraception | 1.81 | 0.72 | 6 | 60 |
| sociobiology | 1.78 | 0.88 | 4 | 33 |
| contraceptive | 1.36 | 0.48 | 7 | 93 |
| wealth | 0.92 | 0.5 | 3 | 39 |
| selection | 0.51 | 0.17 | 7 | 138 |
| evolution | -0.03 | -0.01 | 9 | 228 |

## BOTH-block (effect×cause bigrams) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| childbearing motivations | 5.04 | 2.86 | 6 | 6 |
| childbearing motivation | 4.66 | 4.69 | 7 | 1 |
| status reproductive | 4.18 | 3.14 | 4 | 3 |
| fertility evolutionary | 3.49 | 3.91 | 3 | 1 |
| status fertility | 3.31 | 2.37 | 3 | 5 |
| fertility motivation | 3.31 | 2.37 | 3 | 5 |
| mating reproductive | 1.58 | 6.91 | 3 | 0 |

## OTHER (context terms) — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| success | 7.17 | 1.8 | 20 | 61 |
| contemporary | 6.43 | 2.44 | 11 | 17 |
| modern | 5.03 | 1.78 | 10 | 31 |
| problem | 4.2 | 2.29 | 5 | 9 |
| variables | 4.16 | 3.53 | 4 | 2 |
| societies | 4.11 | 1.72 | 7 | 23 |
| theoretical | 3.89 | 2.02 | 5 | 12 |
| bateman | 3.88 | 4.18 | 4 | 1 |
| desires | 3.88 | 1.28 | 10 | 53 |
| contemporary united | 3.63 | 3.25 | 3 | 2 |
| wife | 3.63 | 3.25 | 3 | 2 |
| industrial societies | 3.63 | 3.25 | 3 | 2 |
| number | 3.6 | 1.81 | 5 | 15 |
| dimorphism | 3.56 | 2.86 | 3 | 3 |
| theoretical problem | 3.49 | 3.91 | 3 | 1 |
| central theoretical | 3.49 | 3.91 | 3 | 1 |
| meta | 3.44 | 2.58 | 3 | 4 |
| principles | 3.32 | 1.89 | 4 | 11 |
| need | 3.31 | 2.37 | 3 | 5 |
| correlation | 3.17 | 2.19 | 3 | 6 |
| finland | 3.03 | 2.04 | 3 | 7 |
| central | 3.03 | 2.04 | 3 | 7 |
| industrial | 2.85 | 1.54 | 4 | 16 |
| 2010 | 2.79 | 1.81 | 3 | 9 |
| desires intentions | 2.69 | 1.43 | 4 | 18 |
