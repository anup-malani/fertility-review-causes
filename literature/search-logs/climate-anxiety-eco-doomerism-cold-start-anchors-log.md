# A3 cold-start anchors — climate-anxiety-eco-doomerism

Sourced (live web pass 2026-07-23, incl. PLOS Climate SR channel-1 seed) + existence-verified 17 candidate anchors. Every DOI pulled from a live Crossref match (Jaccard >= 0.72, year +/-1) then re-affirmed at doi.org; no DOI hand-asserted. Three-state gate: network failure = UNCONFIRMED, never ABSENT.

**Verified (live DOI): 15**  ·  **Year-drift keep (real, RA-confirm): 2**  ·  **Flagged for RA: 0**  ·  **Books (expected miss): 0**

## Coverage by query-cluster family (verified / total)

- ROUTING_DECOY: 4/4
- carbon-ethics: 2/2
- climate-anxiety-construct: 2/2
- eco-doom-pessimism: 3/3
- habitability-fear: 3/3
- reproductive-decision-climate: 3/3

## Per-candidate disposition

- **Eco-reproductive concerns in the age of climate change** (2020, habitability-fear) -> VERIFIED  doi=10.1007/s10584-020-02923-y  J=1.0  (Climatic Change)
- **Climate change worries and fertility intentions: Insights from three E** (2025, habitability-fear) -> VERIFIED  doi=10.31235/osf.io/pv7mz  J=1.0  ()
- **Climate change concerns and fertility intentions: first evidence from ** (2025, eco-doom-pessimism) -> VERIFIED  doi=10.1186/s41118-025-00244-5  J=1.0  (Genus)
- **Environmental concern and fertility intentions among Canadian universi** (2012, habitability-fear) -> VERIFIED  doi=10.1007/s11111-011-0164-y  J=1.0  (Population and Environment)
- **The impact of climate change anxiety on the willingness to have childr** (2024, climate-anxiety-construct) -> VERIFIED  doi=10.1007/s10389-024-02390-0  J=1.0  (Journal of Public Health)
- **Reproduction and the carbon legacies of individuals** (2009, carbon-ethics) -> VERIFIED  doi=10.1016/j.gloenvcha.2008.10.007  J=1.0  (Global Environmental Change)
- **One Child: Do We Have a Right to More?** (2016, carbon-ethics) -> VERIFIED  doi=10.1093/acprof:oso/9780190203436.001.0001  J=0.222  ()
- **Are environmental concerns deterring people from having children? Long** (2024, eco-doom-pessimism) -> VERIFIED  doi=10.2139/ssrn.4542920  J=1.0  ()
- **Too worried about the environment to have children? Or more worried ab** (2025, reproductive-decision-climate) -> VERIFIED  doi=10.1007/s11111-025-00501-x  J=1.0  (Population and Environment)
- **No future, no kids, no kids, no future? An exploration of motivations ** (2021, reproductive-decision-climate) -> VERIFIED  doi=10.1007/s11111-021-00379-5  J=0.214  (Population and Environment)
- **Reproductive choices and climate change in a pronatalist context** (2024, reproductive-decision-climate) -> VERIFIED  doi=10.1177/08883254241229728  J=1.0  (East European Politics and Societies)
- **Climate Change and Reproductive Intentions in Europe** (2015, eco-doom-pessimism) -> YEAR-DRIFT-KEEP  doi=10.1553/0x003d06d6  J=1.0  cand=2015 cr=2021
- **The dynamics of fertility under environmental concerns** (2025, climate-anxiety-construct) -> VERIFIED  doi=10.2139/ssrn.4744985  J=1.0  ()
- **The unfolding story of the second demographic transition** (2010, ROUTING_DECOY) -> VERIFIED  doi=10.1111/j.1728-4457.2010.00328.x  J=1.0  (Population and Development Review)
- **Where are the babies? Labor market conditions and fertility in Europe** (2011, ROUTING_DECOY) -> YEAR-DRIFT-KEEP  doi=10.2139/ssrn.530242  J=1.0  cand=2011 cr=2005
- **Climate shocks and fertility intentions: Evidence from extreme tempera** (2025, ROUTING_DECOY) -> VERIFIED  doi=10.1016/j.econmod.2025.107223  J=1.0  (Economic Modelling)
- **Systematic review of climate change effects on reproductive health** (2022, ROUTING_DECOY) -> VERIFIED  doi=10.1016/j.fertnstert.2022.06.005  J=1.0  (Fertility and Sterility)

## Soft-caveat resolution (2026-07-24, pre-freeze)

The five soft caveats flagged at A3 are now resolved via Crossref existence checks (single-DOI + bibliographic query; no OpenAlex budget touched):

- **Bastianelli** — VoR found: OSF preprint `10.31235/osf.io/pv7mz` -> **`10.1111/jomf.13048`** (*Journal of Marriage and Family*, online 2024-11-15). Swapped in JSON; preprint DOI retained as `preprint_doi`.
- **"Are environmental concerns deterring…UK births"** — VoR found: SSRN `10.2139/ssrn.4542920` -> **`10.1016/j.ecolecon.2024.108184`** (*Ecological Economics*). Swapped; SSRN retained.
- **"The dynamics of fertility under environmental concerns"** — VoR found: SSRN `10.2139/ssrn.4744985` -> **`10.1007/s10640-025-00994-y`** (*Environmental and Resource Economics*). Swapped; SSRN retained.
- **Helm 2021** — identity CONFIRMED (Crossref: "No future, no kids–no kids, no future?", *Population and Environment*, 2021, Helm/Kemper/White). The J=0.214 was a subtitle-truncation artifact, not a weak match. No change.
- **Conly "One Child"** — identity CONFIRMED (Crossref: monograph, 2016, Conly). The J=0.222 was a book-title-vs-subtitle artifact. No change.

All 17 anchors remain `candidate_not_ra_frozen` — the freeze itself (flip to RA-frozen) is Shravan's sign-off. A4 (step 73, Tier A/B frame) is BUDGET-GATED and not yet run.

## Notes

- D.3.b is a 2020s literature: anchors were WEB-SOURCED first, then verified, because discovery (not recall) is the binding problem. 'Britt et al. 2025 (Genus)' from the v5 seminal list did not resolve to a real paper and is NOT carried; the real Genus 2025 paper is Puglisi/Muttarak/Vignoli.
- Two v5 seminal-list metadata fixes surfaced: Schneider-Mayerson & Leong 2020 is in *Climatic Change*, not *Feminist Studies*; 'Britt 2025' -> Puglisi/Muttarak/Vignoli 2025. Flag for HYPOTHESES-v5.
- The realized-fertility (UK longitudinal births) and the REVERSE-causality ('worried before vs after') anchors are deliberately included: they are the scarce identification-relevant designs in an otherwise intention-heavy, cross-sectional literature.
- Routing decoys (D.1.a postmaterialism, C.5.a economic uncertainty, physical climate-shock, biological reproductive-health review) test that the search + screen route them away; they are NOT part of the D.3.b recall denominator.
- LEAKAGE WALL: the PLOS Climate SR feeds included studies as anchors here; its search string must not be mined for A6 query terms.
- Some anchors carry authors=['Anonymous'] as a placeholder where the web pass returned title+venue but not a clean author list; the Crossref match resolves the real authorship. This does not affect the existence gate, which keys on title+year+DOI.
