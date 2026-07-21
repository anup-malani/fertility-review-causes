# Tier-B frame eyeball audit + disposition — evolutionary-sex-drive-contraceptive-decoupling

**Stage:** A4 audit (post-frame, pre-screen) · 2026-07-21
**Input:** `...-tier-b-frame.json` (4,900 dedup candidates) from `65_b1_tier_ab_frame.py`
**Decision:** **KEEP-AND-ROUTE** — the frame is screened as-is; no pre-screen pruning by seed
provenance, vocabulary, or fragment hygiene. Recall is protected at the frame; precision is resolved at
the screen by the frozen B.1/A.2 boundary rubric and the two routing decoys.

---

## What the audit checked

A structured, non-LLM eyeball pass: seed contribution, year spread, crude topical keyword coverage, and
direct title inspection of (a) the both-channel core, (b) the Goldin-Katz-only cloud, (c) the "pension/
off" hits, (d) candidates reachable only via the contraception-tech seeds.

## Findings

### 1. The both-channel core (99) is gold-rich and clean
Titles are squarely on the B.1 estimand: cultural-evolution-of-fertility, biosocial fertility-transition
models, wealth/status/fertility, the quantity–quality trade-off, human behavioral ecology, and
contraceptive adoption × parental investment. This is the highest-signal stratum.

### 2. Topical coverage is healthy; off-target contamination is negligible
Crude title+abstract keyword coverage (overlapping): fertility/reproduction 36.9%, evolution/selection
23.3%, sex/mating 17.0%, status/wealth 16.0%, contraception 11.0%, desire/motivation 11.4%. The
off-target **pension/old-age bucket is 1.0% (49)** — the forward-seed exclusions and backward-only
theory clouds kept the frame from drifting into adjacent hypotheses. 36.5% are title-only (the screening
ceiling, to be noted in the screen report).

### 3. The forward-seed exclusions held
The excluded mega-clouds contribute only their backward refs: The Selfish Gene 37 candidates, Trivers 1,
Buss-37-cultures 209, Kaplan 149 — none floods the frame. Confirms the `theory_cloud>cap` rule.

### 4. The contraception-tech forward cloud is the low-precision stratum (expected B.1/A.2 leakage)

| Stratum | n | on-topic (keyword) |
|---|---|---|
| Reachable via non-contraception seeds | 3,389 | **55%** |
| Reachable ONLY via contraception-tech seeds (Goldin-Katz + Bailey) | 1,511 | **32%** |

Papers cite "The Power of the Pill" as a *pill-as-instrument* for downstream labor / gender / abortion
outcomes, not for decoupling — so its forward cloud is structurally A.2. This is exactly the leakage the
A1 scope predicted, concentrated in one seed (Goldin-Katz alone = 1,431 candidates, 29% of the frame).

### Why the low-precision stratum is NOT pruned
Making the contraception-tech seeds backward-only would shrink the frame by 1,435 **and lose 456
on-topic candidates that only their forward cloud reaches** — including genuine B.1-boundary work
(evolutionary mismatch, "when contraception fails: unintended parenthood," "toward individualistic
reproduction," son-preference measures). Pruning trades real recall for precision, and the GACS
principle (child-labor template, step 57) is explicit that selecting the frame by vocabulary/provenance
distance biases Recall(B). The ~1,000 off-topic contraception-tech items are a **screening precision
tax**, not a recall risk; the frozen boundary + decoys route them away at screen.

### 5. Data-hygiene fragments (2.0%) are also kept, not pre-stripped
An automated fragment filter flagged 98 records (2.0%) — but it false-positived on real works:
"Introduction to Quantitative Genetics" (Falconer's textbook), "Consilience" (E.O. Wilson), "Nisa"
(Shostak's !Kung ethnography). Because an automated filter cannot separate genuine junk ("References",
"Book Reviews", empty titles) from real single-word/`Introduction`-prefixed titles without nicking
recall, and the fragments are only 2% (dropped for free by the LLM screen), **no hygiene pre-strip is
applied.** 6 pre-1900 backward refs (e.g. Darwin) are likewise retained.

## Disposition

The 4,900-candidate Tier-B frame is **final for screening as-is.** The screen report must log:
1. the contraception-tech cloud (~1,511, 32% on-topic) as the known low-precision stratum and expected
   A.2 route-away volume;
2. the 36.5% title-only ceiling;
3. the routing-decoy outcomes (Pritchett → A.2, Wilcox → A.4) as the routing-validity check.
