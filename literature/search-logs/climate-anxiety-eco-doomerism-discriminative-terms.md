# Discriminative terms (A6a) - climate-anxiety-eco-doomerism

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over TITLES: RELEVANT+seeds (234) vs screen NOT_RELEVANT (819). Higher z = more discriminative of the on-topic class. Negatives passed the citation-frame + screen, so the contrast is relevant-vs-near-miss (precision at recall). In A6b this is recomputed fold-locally for the CV.

**Leakage wall honoured:** every term below is mined from our own screen verdicts over our own citation frame. No term is taken from the PLOS Climate review's published search string.

Candidate terms (gold count >= 3): **197**. By block: effect 15, cause 42, both 3, other 137


## EFFECT block (fertility core + intention extension) - top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| reproductive | 5.04 | 1.38 | 30 | 19 |
| procreation | 3.08 | 2.15 | 8 | 2 |
| reproductive intentions | 2.17 | 2.15 | 4 | 1 |
| intentions | 2.03 | 0.54 | 20 | 33 |
| reproductive justice | 1.89 | 3.72 | 4 | 0 |
| having children | 1.86 | 1.17 | 5 | 4 |
| pregnancy intentions | 1.64 | 3.71 | 3 | 0 |
| change reproductive | 1.64 | 3.71 | 3 | 0 |
| intentions insights | 1.64 | 3.71 | 3 | 0 |
| procreative | 1.64 | 3.71 | 3 | 0 |
| childbearing | 1.34 | 0.53 | 9 | 15 |
| reproduction | 0.56 | 0.37 | 3 | 6 |
| childfree | 0.53 | 0.24 | 6 | 14 |
| fertility intentions | 0.37 | 0.14 | 8 | 21 |
| fertility | -1.81 | -0.32 | 30 | 139 |

## CAUSE block (anxiety construct / habitability fear / carbon ethics / eco-doom / reproductive decision) - top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| climate | 8.05 | 0.93 | 127 | 136 |
| anxiety | 6.7 | 2.36 | 37 | 7 |
| climate change | 5.31 | 0.74 | 80 | 106 |
| eco | 4.66 | 2.45 | 18 | 3 |
| concerns | 3.94 | 1.58 | 16 | 8 |
| ethics | 3.82 | 1.71 | 14 | 6 |
| eco anxiety | 3.81 | 2.45 | 12 | 2 |
| climate anxiety | 3.41 | 3.72 | 13 | 0 |
| emotions | 3.18 | 1.92 | 9 | 3 |
| ecological | 3.12 | 1.33 | 12 | 8 |
| crisis | 3.12 | 1.33 | 12 | 8 |
| climate crisis | 3.04 | 1.68 | 9 | 4 |
| emotional | 2.95 | 1.82 | 8 | 3 |
| worries | 2.9 | 2.56 | 7 | 1 |
| change anxiety | 2.7 | 1.71 | 7 | 3 |
| environmental | 2.53 | 0.48 | 37 | 65 |
| climate mitigation | 2.31 | 1.77 | 5 | 2 |
| change concern | 2.17 | 2.15 | 4 | 1 |
| population ethics | 2.11 | 3.72 | 5 | 0 |
| responses climate | 2.11 | 3.72 | 5 | 0 |
| grief | 2.11 | 3.72 | 5 | 0 |
| decision making | 2.0 | 1.13 | 6 | 5 |
| environmentally | 1.97 | 1.58 | 4 | 2 |
| era climate | 1.89 | 3.72 | 4 | 0 |
| overpopulation | 1.89 | 3.72 | 4 | 0 |

## BOTH-block (effect x cause bigrams) - top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| reproductive decision | 2.32 | 3.72 | 6 | 0 |
| reproductive concerns | 1.64 | 3.71 | 3 | 0 |
| eco reproductive | 1.64 | 3.71 | 3 | 0 |

## OTHER (context terms) - top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| change | 4.47 | 0.6 | 80 | 124 |
| young | 3.69 | 1.39 | 16 | 10 |
| people | 3.39 | 1.15 | 17 | 14 |
| young people | 3.27 | 1.77 | 10 | 4 |
| students | 3.27 | 1.77 | 10 | 4 |
| university | 2.95 | 1.82 | 8 | 3 |
| coping | 2.9 | 2.56 | 7 | 1 |
| mitigation | 2.6 | 1.92 | 6 | 2 |
| responses | 2.6 | 1.92 | 6 | 2 |
| era | 2.45 | 2.32 | 5 | 1 |
| development validation | 2.45 | 2.32 | 5 | 1 |
| children | 2.38 | 0.67 | 19 | 27 |
| justice | 2.37 | 1.08 | 9 | 8 |
| validation | 2.31 | 1.77 | 5 | 2 |
| population | 2.22 | 0.52 | 25 | 42 |
| associated | 2.21 | 1.33 | 6 | 4 |
| psychological | 2.2 | 0.97 | 9 | 9 |
| making | 2.13 | 1.11 | 7 | 6 |
| planning | 2.11 | 3.72 | 5 | 0 |
| university students | 2.09 | 1.42 | 5 | 3 |
| desire | 1.97 | 1.58 | 4 | 2 |
| government | 1.97 | 1.58 | 4 | 2 |
| responsibility | 1.97 | 1.58 | 4 | 2 |
| scp | 1.89 | 3.72 | 4 | 0 |
| natalism | 1.89 | 3.72 | 4 | 0 |
