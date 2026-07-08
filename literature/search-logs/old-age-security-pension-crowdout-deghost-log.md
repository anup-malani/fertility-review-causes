# De-ghosting the frozen gold — old-age-security-pension-crowdout

Existence-verify every no-DOI Tier-B anchor against **both** OpenAlex and Crossref; quarantine as ghost only if **both** return no confident title match (Jaccard ≥ 0.72 + author/year gate) — the conservative 'confirmed-absent' rule. DOI-bearing anchors are kept as real.

- Tier B before: **257**  (114 had DOIs, 143 no-DOI to verify)
- no-DOI anchors **resolved** (real, DOI backfilled): **17**
- no-DOI anchors **quarantined as ghosts**: **126**
- Tier B after de-ghosting: **131**

## By estimand cell (before → after; ghosts removed)

| Cell | before | ghosts quarantined | after |
|---|---|---|---|
| PRIMARY | 57 | 40 | 17 |
| THEORY | 169 | 76 | 93 |
| OFF | 31 | 10 | 21 |

**PRIMARY-cell ghost rate: 40/57 (70%)** — the snowball's forward-citation hallucination, concentrated in the primary pooling cell. The quarantine list (`old-age-security-pension-crowdout-gold-ghost-quarantine.json`) is for RA sign-off; nothing is silently dropped.

*Next: re-freeze on the survivors and re-run the recall re-grade (45) against the de-ghosted denominator vs the pre-registered 0.80 bar — the honest number.*
