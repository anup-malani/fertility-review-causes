#!/usr/bin/env python3
"""
Part 2 (Tier B) — build the frame. Tier B = an UNBIASED sample of relevant papers w.r.t.
keyword-findability. Decision (Shravan, 2026-06-29): definition (1) — the orthogonally-SOURCED
relevant set, taken WHOLE; we do NOT filter for keyword-absence/vocabulary-disconnection
(filtering on findability would re-introduce the selection bias we're correcting for). The
snowball's citation-graph sourcing is what delivers the unbiasedness; orthogonality is a
property of the source, not a filter we apply.

Frame = snowball llm_verdict==RELEVANT, minus papers already claimed by Tier A (gold draft +
the 15 hard residuals / dev pool), deduped by normalized title. Keyword-universe membership is
IGNORED (that was the rejected definition 2).

NOTE: snowball records carry no DOI/year/abstract — only (paperId W-ID, title, phase, verdict).
DOI resolution + abstracts come later via the OpenAlex citation graph (the orthogonal channel;
the agent/web resolver is BANNED for Tier B, spec §3/§8).

Inputs : *-snowball.json, *-tier-a-draft.json, retry_verified_final.json (residual titles)
Output : old-age-security-pension-crowdout-tier-b-frame.json + stderr stats
"""
import json,re,sys
import unicodedata
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
# --- canonical fold, TICK-074. Keep in sync with source/lib/textnorm.py; enforced by
# scripts/verify_norm.py. An unfolded accent SHATTERS a surname and an ASCII apostrophe
# becomes a SPACE while a curly one is DELETED — both silent, both producing a confident
# wrong answer rather than an error.
_TRANSLIT = {
    ord("ø"): "o", ord("Ø"): "O", ord("đ"): "d", ord("Đ"): "D",
    ord("ð"): "d", ord("Ð"): "D", ord("þ"): "th", ord("Þ"): "Th",
    ord("ı"): "i", ord("İ"): "I", ord("ł"): "l", ord("Ł"): "L",
    ord("æ"): "ae", ord("Æ"): "Ae", ord("œ"): "oe", ord("Œ"): "Oe",
    ord("ß"): "ss", ord("ħ"): "h", ord("Ħ"): "H", ord("ŋ"): "n", ord("Ŋ"): "N",
}

# U+0027 apostrophe, U+2018/U+2019 curly quotes, U+02BC modifier letter, U+00B4 acute used as an
# apostrophe, U+0060 backtick. All six occur in indexed titles.
_APOSTROPHE_CLASS = re.compile("['‘’ʼ´`]")
# U+002D hyphen-minus, U+2010-U+2015 the dash block, U+2212 minus, U+00AD soft hyphen.
_DASH_CLASS = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    """Fold to a comparable ASCII token string. Order is load-bearing: translit, then punctuation
    classes, then NFKD, then the strip."""
    s = (s or "").translate(_TRANSLIT)
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()
def ndoi(d): return (d or "").replace("https://doi.org/","").strip().lower() or None

snow=json.load(open(LOGS/"old-age-security-pension-crowdout-snowball.json"))["papers"]
tierA=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json"))
residual=[r for r in json.load(open(HERE/"retry_verified_final.json")) if r["verdict"]=="NOT_FOUND"]

# exclusion set: Tier A gold (56) + the 15 hard residuals (Tier A empirical, dev pool)
excl_title={norm(g["title"]) for g in tierA}
excl_doi={ndoi(g.get("doi")) for g in tierA if g.get("doi")}
excl_title|={norm(r["title"]) for r in residual}

rel=[p for p in snow if p.get("llm_verdict")=="RELEVANT"]
seen=set(); frame=[]; drop_excl=0; drop_dup=0
for p in rel:
    nt=norm(p["title"])
    if nt in excl_title or ndoi(p.get("doi")) in excl_doi: drop_excl+=1; continue
    if nt in seen: drop_dup+=1; continue
    seen.add(nt)
    frame.append({"paperId":p["paperId"],"title":p["title"],"snowballPhase":p.get("snowballPhase"),
                  "snow_confidence":p.get("llm_confidence"),"snow_reason":p.get("llm_reason")})

json.dump(frame,open(LOGS/"old-age-security-pension-crowdout-tier-b-frame.json","w"),indent=2)
print("=== Tier B frame (definition 1: unbiased orthogonally-sourced relevant set) ===",file=sys.stderr)
print(f"snowball RELEVANT          : {len(rel)}",file=sys.stderr)
print(f"  - Tier A / residual overlap: {drop_excl}",file=sys.stderr)
print(f"  - duplicate titles         : {drop_dup}",file=sys.stderr)
print(f"FRAME (distinct)           : {len(frame)}",file=sys.stderr)
print(f"  confidence: {dict(Counter(p['snow_confidence'] for p in frame))}",file=sys.stderr)
print(f"  phase     : {dict(Counter(p['snowballPhase'] for p in frame))}",file=sys.stderr)
wid=sum(1 for p in frame if (p['paperId'] or '').startswith('W'))
print(f"  resolvable by W-ID (OpenAlex citation graph): {wid}/{len(frame)}",file=sys.stderr)
print(f"\nwritten -> old-age-security-pension-crowdout-tier-b-frame.json",file=sys.stderr)
