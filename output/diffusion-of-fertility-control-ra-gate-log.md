# RA title/abstract gate — diffusion-of-fertility-control

1,148 rows to review (RELEVANT + UNCERTAIN; NOT_RELEVANT excluded). Exception-based: leave `ra_decision` blank to approve the screen routing, or write **RETRIEVE**, **EXCLUDE**, **UNSURE**, or **REROUTE:<hypothesis>** (e.g. `REROUTE:A.20`). The screen is an automated Haiku recall filter, not a verdict; this gate is the human verdict.

## Review order (priority buckets)

- **1. identified-core primary**: 44
- **2. descriptive primary**: 215
- **3. theory/Princeton**: 71
- **4. UNCERTAIN w/ cell**: 144
- **5. UNCERTAIN / title-only**: 674

## Load-bearing guidance

- **Priority 1 (identified core) is the retrieval list.** These are the designs that claim to separate social diffusion from a common economic/cultural shock; the chapter's synthesis rests on them. Confirm each really identifies (not a descriptive residual mislabelled).
- **Sample Wall 1 first.** Any row with `diffusion_channel=MASS_MEDIA` that was kept in A.3, or any A.20 borderline, is the highest-cost misroute — reroute to A.20 if it is a channel effect.
- **Priority 5 is the title-only queue**, not evidence; RETRIEVE only if the title alone names a diffusion→fertility estimand.
- Output: `output/diffusion-of-fertility-control-ra-review.csv`.
