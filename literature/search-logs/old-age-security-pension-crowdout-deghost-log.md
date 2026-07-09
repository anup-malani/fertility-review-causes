# De-ghosting via local corpus + Crossref (zero OpenAlex budget) — old-age-security-pension-crowdout

Existence oracle = the already-pulled 11,463-record live corpus (the OpenAlex universe for the query) + free Crossref. Quarantine only if BOTH miss and Crossref actually responded.

- Tier B before: **257** (114 had DOIs, 143 no-DOI verified)
- kept (in corpus or Crossref): **38** no-DOI + 114 DOI = 152
- **ghosts (confirmed-absent): 105**
- hold (Crossref unconfirmed, NOT quarantined): 0
- Tier B after: **152**

## By cell (before → ghosts → after)

| Cell | before | ghosts | after |
|---|---|---|---|
| PRIMARY | 57 | 36 | 21 |
| THEORY | 169 | 62 | 107 |
| OFF | 31 | 7 | 24 |

**PRIMARY ghost rate: 36/57 (63%)**.

Caveat: a real OFF-query paper with no Crossref DOI would be in 'hold', not quarantined (conservative). That thin gray-lit tail is the only thing live OpenAlex would add.
