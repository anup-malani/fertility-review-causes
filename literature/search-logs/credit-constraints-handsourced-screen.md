# The hand-sourced stratum was never screened — C.3.e

**TICK-077 · 2026-09-01 · Shravan**

## The gap

The screening sheets covered `both_channels`, `snowball_r2_only` and `frame_only`. They did **not**
cover `hand_sourced` — the 130 records injected into the universe precisely because a snowball pool
holds what its seeds *reached* and never the seeds themselves.

So the anchors, decoys, boundary-hunt finds and hand-picked arm seeds sat in the universe with **no
cell assignment**, and the primary pool of 48 excluded them. Among the excluded:

- **Desai and Tarozzi 2011** — the chapter's only randomised estimate, with a separately randomised
  credit-only arm. Retrieved, scanned and reasoned about all day; never in the screen table.
- Steele et al. 1998, Küchler 2012, Lan et al. 2023, **Islam et al. 2026** — the composite studies the
  boundary hunt found.
- The inherited C.2.c Arm B anchors: Cumming and Dettling, Hacamo, the **2026 PNAS provident-fund
  study that C.2.c explicitly routed to this chapter**.
- The Arm S anchors: Cain 1981 and 1983, Pörtner, Pitt et al., Delavallade, the AGEP cluster-RCT.

**This is the third time in this chapter that hand-sourced studies fell out of an accounting.** They
were missing from the universe (fixed in `291`), then reported absent-by-id when present as version
twins (fixed in `292`), and now missing from the screen. Each fix addressed the symptom at one stage.
The rule that would have caught all three: **at every stage, reconcile against the hand-sourced list
explicitly, and make the reconciliation a check that fails loudly.**

## What screening it produced

**Primary pool 48 → 69** (Arm B 10 → 17, composite 32 → 40, Arm S 6 → 12). Total screened **2,750**.

Two records are genuinely new to the chapter and both are **identified**, which is what the next search
phase was going to look for:

**How Does the Million Baht Village Fund Impact Fertility in Thailand (2017)** — quasi-experimental,
instrumental-variable model with fixed effects on a pre/post panel, finding a **negative** relationship
between microloan receipt and the number of babies. **Identified, middle-income, negative** — the half
of the sign flip the chapter had no identified support for. *Caveat: published in* The Mathematics
Enthusiast *with zero citations; the venue does not match the design and the paper needs a hard read.*

**Financing Fertility through Bank Competition? China (2023)** — bank deregulation as an exogenous
shock to bank competition; city-level birth rates **increase**, more so where employment, savings and
housing affordability are higher. **Identified, middle-income, positive.** *Caveat: Research Square
preprint, unrefereed, zero citations.*

## The sign picture, now that the identified estimates are assembled

| Setting | Design | Sign |
|---|---|---|
| Thailand, village fund | IV + FE panel | **negative** |
| China, bank competition | deregulation shock | **positive** |
| China, household credit | FE-Poisson + IV | **inverted U** |
| US, banking deregulation and Bartik credit shock | quasi-experiment | **positive** |
| US, mortgage-market deregulation | regulator ruling | **positive** |
| Taiwan, mortgage interest subsidy | DiD + matching | **null** (first stage verified) |
| Ethiopia, credit-only RCT arm | randomised | **null on births; desires up** |

Seven identified or quasi-identified estimates and they do not agree. Two structures are on the table
for the synthesis rather than one: the **cross-setting sign flip** (poor settings negative, rich
positive) and the **within-setting inverted U** (expansion raises fertility to a point, then lowers
it). They are not the same claim and the chapter should not blur them.

## The Orton review, mined

Five of its 56 references carry a fertility term; **three were already in the pool**, one is Desai and
Tarozzi (now added), one is a BMJ Open empowerment study. An independent systematic review of
group-microfinance health impacts contains almost nothing on fertility that this chapter does not have
— **a corroboration that the composite cell is saturated**, from a channel that owes nothing to our
query.

## The Benin RCT, resolved

The r1 probe flagged *Credit with Health Education in Benin* as uncertain. Its abstract carries **no
fertility term at all**, and the 2×2 design varies the *features* of a credit product — gender
composition and health-education bundling — not access to credit versus none. Outcomes are health
knowledge and self-reported behaviour. **Not a C.3.e estimate; the uncertainty resolves negative.**
