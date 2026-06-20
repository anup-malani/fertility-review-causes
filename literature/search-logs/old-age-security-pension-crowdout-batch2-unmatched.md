# Batch-2 Unmatched PaperId Investigation

**Date:** 2026-06-20
**Context:** 1,000 papers fetched from OpenAlex; 930 matched between Haiku and Sonnet screening agents; 70 unmatched and excluded from the divergence analysis.

---

## PaperId Profile

| Category | Count |
|---|---|
| Total papers | 1,000 |
| DOI-based paperIds | 801 |
| Title-based paperIds | 199 |
| Title-based IDs hard-truncated at 60 chars | 104 |
| Title-based IDs containing colons (`:`) | 76 |
| Title-based IDs containing periods (`.`) | 18 |
| Title-based IDs containing hyphens (`-`) | 26 |
| Title-based IDs with any fragility (truncated or non-alphanum char) | 152 of 199 |
| DOI-based IDs with unusual chars (parens, semicolons, `<>`) | 17 |
| Title-based IDs with no abstract | 6 |
| Duplicate paperIds (two distinct works sharing one ID) | 1 (`10.3726/b13605`) |
| Total plausible mismatch candidates | ~154 |

---

## Most Likely Cause(s)

**1. Hard truncation at 60 chars combined with embedded punctuation (highest probability, explains ~60–80 of the 70 mismatches)**

104 title-based IDs are exactly 60 characters — the truncation boundary. Of these, many end mid-word or mid-phrase (e.g., `'lowfertilityandfamilypolicyinjapan:inaninternationalcomparat'`). LLMs are statistically unlikely to reproduce a string that cuts off in an arbitrary place while also preserving an embedded colon, comma, or period at a precise character position. The prompt instructs agents to return the paperId "exactly as in the batch file," but even small tokenization differences mean that a string like `'children'inneedofcare'orinneedofcash?questioningsocialsecuri'` — which contains a right-quotation mark (`'`) and a question mark — is extremely likely to be re-rendered differently by each model. 76 of the 199 title-based IDs contain colons; 18 contain periods; at least some contain Unicode characters (the Polish paper `'makroekonomiczneuwarunkowaniapłodnościwpolsce...'` contains `ł` and `ś`). Any one of these is enough to cause a mismatch.

**2. Special chars in DOI-based IDs (moderate probability, explains several of the remaining mismatches)**

17 DOI-based IDs contain unusual characters beyond `a-z0-9./\-_`: parentheses, angle brackets, semicolons, and colons embedded in the suffix (e.g., `'10.1002/(sici)1099-0747(199609)12:3<119::aid-asm279>3.0.co;2-g'`). These 43-character strings are difficult for a model to echo verbatim — brackets and semicolons are tokenized as control characters in many contexts, and the angle-bracket sequences in particular may be collapsed or escaped.

**3. One duplicate paperId (low probability; affects at most 1–2 papers)**

Two distinct works both map to `10.3726/b13605` ("German Pension Reform" vs. "German Pension Reform: On Road Towards a Sustainable Multi-Pillar System"). If one agent resolves the ambiguity differently, both rows become unmatched.

**4. Title-based IDs with no abstract (minimal probability, ~6 papers)**

Six title-based IDs have no abstract. Agents with nothing to read may skip these or hallucinate a verdict with an inconsistent ID.

---

## Recommended Fix

Replace the 60-char truncated-title fallback with the OpenAlex `work_id` (the integer after `https://openalex.org/W`) as the canonical paperId — it is short, opaque, and contains only digits, eliminating all punctuation and truncation fragility. As a defense-in-depth measure, add a post-processing normalization step in `calibrate-screen.mjs` that strips whitespace and lowercases both agent response IDs before matching, which will recover any case-flip or stray-space mismatches without requiring a re-run.
