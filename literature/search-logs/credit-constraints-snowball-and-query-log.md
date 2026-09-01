# Snowball round 1 and the production query — C.3.e

**TICK-077 · 2026-09-01 · Shravan**
Scripts: `277_c3e_snowball.py`, `278_c3e_production_query.py`, `279_c3e_query_repair.py`
Outputs: `credit-constraints-snowball-{pool,round1}.json`, `credit-constraints-production-query.json`,
`credit-constraints-query-repair.json`

---

## 1. Snowball round 1 — pool 3,810, zero errors

26 seeds, all resolved. Backward 1,840 reference edges → 1,062 new records; forward 3,493 (capped
at 200 per seed, 10 seeds capped) → 3,100 new. 352 duplicates collapsed. Reach by seed arm:
**S 2,080 · composite 1,163 · B 745** — Arm B is the thinnest cloud, which is what a small
household-finance literature on fertility looks like.

**Decoys were seeded deliberately and paid.** Nugent (C.3.c's) reached 270 records, 197 of them
reached by no other seed; Lovenheim (C.2.c's) 205 and 140. A boundary case is the nearest neighbour
of the thing you want, so never-seed-a-decoy would have discarded ~340 uniquely-reached records here.

### The seeds that reached nothing were a resolver defect, not a quiet literature

Four seeds returned 0 or 1 records on the first run — including Burgess and Pande's *Do Rural Banks
Matter?*, which has hundreds of citations. That is not a plausible absence, and reading it as one
would have been the whole error.

**Cause: the anchor resolver had matched "Replication data for: <title>" deposits** — four of the 26.
These are `dataset` records carrying the article's exact title, **the same authors and the same year**,
with no references and no citations. They contribute nothing to a snowball and nothing downstream.

They were admitted by the bidirectional `is_stem` fix made earlier the same day to catch book chapters
indexed as "Chapter 8 <title>". The justification written into that fix — *"safe because the author and
year gates still apply"* — was wrong: a replication package shares both. Suffix containment is unsound,
and the standing rule is **named qualifiers only**. `275` now allows the suffix direction solely for an
allowlisted structural prefix (`chapter|part|section|volume`), refuses non-study record types outright
with a `NON_STUDY_RECORD` verdict, and breaks score ties on citation count so an article beats its own
data deposit. After the fix: **0 shadow records, and the four seeds reach 211–346 records each.**

### Version twins: 617 records, 16% of the pool, reachable no other way

OpenAlex splits a study across its working-paper and published records, and **the citations do not
follow the version of record.** Dettling and Kearney's *Journal of Public Economics* article carries
**0** citations; its NBER twin carries **67**. Seeding only the version of record returns a hollow
forward cloud that reads as a quiet literature.

`277` therefore discovers twins by title for every seed (excluding non-study types), and takes backward
references and forward citations over the union. Twins were found for **12 of 26 seeds**, and **617
pool records — 16% — were reached only through a twin.** The channel is measured, not assumed.

---

## 2. The production query, per arm

Ruling 1 made this one chapter with two arms that do not share a vocabulary, so every number below is
per arm. A pooled recall figure would hide a dead arm.

### Recall against the anchor set

| Role | Recalled | Note |
|---|---|---|
| **anchor** | **8 / 11** | the number that matters |
| theory | 1 / 2 | Schultz's Handbook chapter has no credit vocabulary; reached by snowball |
| **probe** | **0 / 9** | see §3 — this is a finding, not a failure |

Anchors by arm: **S 3/4 · B 5/6 · composite 0/1.**

### What the repair actually bought, and one term that bought nothing

Every candidate term was scored on **gold recovered**, never on frame growth. Of 26 candidates, four
were kept:

| Axis | Term | Frame added | Gold recovered |
|---|---|---|---|
| outcome | `baby boom` | +167 | the Baby Boom paper, whose abstract never says "fertility" |
| S | `insurance mechanism` | +39 | Cain 1981 |
| B | `uninsurable` | +18 | Sommer 2016 |
| composite | `credit program` | +53 | Pitt 1999 |

Refused, among others: `mortgage` (+622 records, no gold), `old age support` (+213, no gold),
`demand for children`, `reproductive behavior`, `total fertility rate`, `group lending`, `rural bank`,
`branch expansion` (each ≤10 records and no gold). **Frame growth is not frame gain.**

**A measurement bug in the repair loop, caught and fixed.** The first run accepted 17 of 26 terms and
produced a 7,758-record frame. It compared each candidate's recall against a **frozen** baseline while
the kept set kept growing, so every later term inherited credit for every earlier term's recovery —
`housing loan` appeared to recover an Arm S record. With the baseline advancing correctly, 4 terms are
kept and the frame is **7,021**. The bug was buying 737 records of frame for zero gold.

### Frozen production query

- **Outcome axis (12):** fertility · birth rate · birth rates · childbearing · births · number of
  children · family size · parity · birth spacing · completed fertility · fertility intentions ·
  baby boom
- **Exposure S (13):** children as insurance · insurance motive · old age security · old-age security ·
  precautionary saving · consumption smoothing · informal insurance · risk sharing · crop insurance ·
  income risk · savings account · commitment savings · insurance mechanism
- **Exposure B (14):** credit constraint(s) · liquidity constraint · borrowing constraint · down
  payment · loan-to-value · mortgage credit · credit supply · credit expansion · interest rate ·
  mortgage rate · loan ceiling · collateral constraint · uninsurable
- **Exposure composite (11):** financial inclusion · bank branch · microfinance · microcredit · access
  to credit · credit access · financial development · access to finance · banking access · financial
  access · credit program

Frame **7,021** records. `health insurance` stays banned (276: a 9-to-1 contaminant colliding with
A.17). Single-term dominance to watch at screen: `interest rate` carries 70% of Arm B's block and
`access to credit` + `credit access` 79% of composite's.

---

## 3. The 0/9 on probes is the composite stratum's answer

The nine probes were chosen as designs that would be ideal **if** they measured fertility: the
microcredit RCTs (Banerjee, Crépon, Angelucci, Attanasio), the savings-access experiments (Dupas,
Prina), the branch-expansion studies (Burgess and Pande, Bruhn and Love), and the historical credit
cooperatives (Guinnane). **Not one is reachable by any exposure × fertility query, because not one
mentions fertility, births or family size in its abstract at all.** Their measured outcomes are
business investment, profits, consumption, poverty, food consumption and entrepreneurship.

This is not a vocabulary failure and widening the query cannot repair it — widening can only hide it.
It is the direct empirical form of the risk §3 of the scope memo named: the composite designs are the
best-identified variation available to this chapter, and they do not appear to estimate a fertility
outcome. Two consequences, both for the screen rather than for the query:

1. **`PRIMARY_COMPOSITE_ACCESS` may be empty**, and if it is, the sign-flip question — the one that
   made this one chapter rather than two — has no direct evidence. Say UNEVALUATED if so; an empty
   cell is a result, and GRADE takes **No evidence**, not VERY LOW.
2. **The full-text channel is the only way to test it.** A fertility outcome can sit in a table of an
   RCT whose abstract never mentions it. Before declaring the cell empty, the nine probes get a
   full-text check for a fertility or birth outcome — a search null is worth something only when the
   channels fail for unrelated reasons, and abstract indexing and full-text tables fail differently.

---

## 4. Next

1. Pull the 7,021-record frame; dedup against the 3,810-record snowball pool and report the overlap
   (a rung that only finds what another already had is REDUNDANT, which is not EMPTY).
2. Two-stage screen, per arm, with the `MIXED_*` classes live from the start.
3. The nine-probe full-text check above, before any statement about the composite cell.
