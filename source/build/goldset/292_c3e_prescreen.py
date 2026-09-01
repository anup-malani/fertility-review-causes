#!/usr/bin/env python3
"""292 — C.3.e: deterministic prescreen, recall-checked, plus a stratified depth probe. TICK-077.

The universe is 7,309 records and the two channels are almost disjoint -- only 91 records are in
both the term frame and the round-1 snowball. That is not a detail: it means the strata have very
different priors, and screening them in one undifferentiated queue would spend the same effort per
record on a stratum that may yield nothing.

So this does two things and neither is a screen:

  A. DETERMINISTIC PRESCREEN. Every rule is recall-checked against the known-relevant set before
     it is allowed to fire. A rule that removes a single known-relevant record is rejected outright
     -- on an earlier chapter only two of a proposed prescreen's rules survived this test.
  B. STRATIFIED DEPTH PROBE. Rather than screening sequentially and discovering the yield curve at
     the end, sample each stratum and measure yield first. Spaced part-batches map the curve for
     roughly the cost of two batches.

The known-relevant set is the 26 resolved anchors (minus decoys) PLUS the studies later established
by hand: the four boundary-spanning composite studies, the six hand-picked arm seeds, and round 2's
identified candidates. Recall-checking a prescreen against the anchors alone would check it against
the very selection that 283 showed to be blind.

Usage: python3 292_c3e_prescreen.py
"""
import json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "credit-constraints-prescreen.json"
random.seed(77)

U = json.loads((LOGS / "credit-constraints-screen-universe.json").read_text())
recs = U["records"]
by_id = {r["openalex"]: r for r in recs}

# ---- the known-relevant set, deliberately wider than the anchor list -------------
anchors = json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())
known = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]
         for a in anchors if a.get("role") != "decoy"}
hunt = json.loads((LOGS / "credit-constraints-boundary-hunt.json").read_text())
for h in hunt["hits"]:
    if h["doi"] in ("10.1007/s13524-011-0029-0", "10.31899/pgy6.1016",
                    "10.1353/jda.2012.0037", "10.1080/00036846.2023.2244249"):
        known.add(h["openalex"])
known |= {"W3011170043", "W3122525178", "W4407312762", "W2998507442"}   # hand-picked arm seeds
r2 = json.loads((LOGS / "credit-constraints-round2-screen.json").read_text())
known |= {r["openalex"] for r in r2["identified"]}
# Match by FOLDED TITLE, not by id: dedup collapses a version pair into one keeper, so a
# known-relevant id can be "absent" while the study is present under its twin. Three of C.3.e's
# 34 known records are in exactly that position, and an id-only check reports them as lost.
import unicodedata as _u
def _fold(x):
    x = (x or "").lower()
    x = _u.normalize("NFKD", x)
    x = "".join(c for c in x if not _u.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", x)).strip()

_title_index = {}
for _r in recs:
    _t = _fold(_r.get("title"))
    if _t:
        _title_index.setdefault(_t, _r["openalex"])
_known_titles = {}
for _a in anchors:
    _tc = _a.get("top_candidate") or {}
    if _tc.get("oa_id"):
        _known_titles[_tc["oa_id"].rsplit("/", 1)[-1]] = _tc.get("title")
for _h in hunt["hits"]:
    _known_titles.setdefault(_h["openalex"], _h.get("title"))
for _r in r2["identified"]:
    _known_titles.setdefault(_r["openalex"], _r.get("title"))

known_in_universe = set()
for k in known:
    if k in by_id:
        known_in_universe.add(k)
    else:
        tw = _title_index.get(_fold(_known_titles.get(k)))
        if tw:
            known_in_universe.add(tw)          # present as its version twin
print(f"known-relevant set: {len(known)} records, {len(known_in_universe)} present in the universe")
missing = sorted(known - known_in_universe)
if missing:
    print(f"  NOT IN UNIVERSE ({len(missing)}): {', '.join(missing)}")

# ---- candidate prescreen rules --------------------------------------------------
def text(r):
    return ((r.get("title") or "") + " . " + (r.get("abstract") or "")).lower()

AGRO = re.compile(r"soil fertilit|fertiliz|fertilis|crop yield|agronom|nitrogen|"
                  r"livestock|cattle|poultry|maize|wheat yield", re.I)
VET = re.compile(r"\b(cow|sow|bovine|porcine|dairy herd|broiler|semen quality in bulls)\b", re.I)
NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "retraction"}

RULES = {
    "agronomy_soil_fertility_homonym": lambda r: bool(AGRO.search(text(r))),
    "veterinary_animal_reproduction": lambda r: bool(VET.search(text(r))),
    "non_study_record_type": lambda r: (r.get("type") or "").lower() in NON_STUDY,
    "no_abstract_and_no_outcome_word_in_title":
        lambda r: (not r.get("abstract")) and not re.search(
            r"fertilit|birth|childbear|children|family size|baby", (r.get("title") or ""), re.I),
}

print("\nRULE RECALL CHECK — a rule that removes ANY known-relevant record is rejected\n")
verdicts, kept_rules = {}, []
for name, fn in RULES.items():
    fires = [r["openalex"] for r in recs if fn(r)]
    harmed = sorted(set(fires) & known_in_universe)
    ok = not harmed
    verdicts[name] = {"would_remove": len(fires), "known_relevant_removed": harmed,
                      "accepted": ok}
    print(f"  {'ACCEPT' if ok else 'REJECT':7s} {name:44s} removes {len(fires):5d}"
          + (f"   HARMS: {', '.join(harmed)}" if harmed else ""))
    if ok:
        kept_rules.append((name, fn))

survivors = [r for r in recs if not any(fn(r) for _, fn in kept_rules)]
removed = len(recs) - len(survivors)
print(f"\nprescreen: {len(recs)} -> {len(survivors)} survivors ({removed} removed, "
      f"{round(100*removed/len(recs),1)}%)")
print(f"  known-relevant surviving: {len([k for k in known_in_universe if k in {s['openalex'] for s in survivors}])}"
      f"/{len(known_in_universe)}")

# ---- stratify and sample for the depth probe ------------------------------------
def stratum(r):
    """Strata describe how the PIPELINE would find a record.

    Hand-sourced studies are already known, so they are their own stratum -- leaving them in a
    discovery stratum both inflates that stratum's apparent yield and empties the others. Before
    this split, every known-relevant record landed in `both_channels` and `frame_only` showed a
    yield of exactly zero, which is an artefact of the labelling, not a property of the frame.
    """
    p = set(r["provenance"])
    if any(x.startswith("hand_") for x in p):
        return "hand_sourced"
    disc = {x for x in p if not x.startswith("hand_")}
    if "frame" in disc and len(disc) > 1:
        return "both_channels"
    if "frame" in disc:
        return "frame_only"
    if "snowball_r2" in disc:
        return "snowball_r2_only"
    return "snowball_r1_only"

strata = {}
for r in survivors:
    strata.setdefault(stratum(r), []).append(r)
print("\nstrata among survivors:")
probe = {}
for k, v in sorted(strata.items(), key=lambda kv: -len(kv[1])):
    n_known = len([x for x in v if x["openalex"] in known_in_universe])
    size = min(40, len(v))
    probe[k] = random.sample(v, size)
    print(f"  {k:20s} {len(v):5d}  (known-relevant inside: {n_known})  -> probe {size}")

OUT.write_text(json.dumps(
    {"rule_verdicts": verdicts,
     "accepted_rules": [n for n, _ in kept_rules],
     "universe": len(recs), "survivors": len(survivors),
     "known_relevant_in_universe": sorted(known_in_universe),
     "strata_sizes": {k: len(v) for k, v in strata.items()},
     "probe_batches": {k: [{"openalex": r["openalex"], "title": r.get("title"),
                            "year": r.get("year"), "venue": r.get("venue"),
                            "abstract": (r.get("abstract") or "")[:700]} for r in v]
                       for k, v in probe.items()}}, indent=1))
print(f"\nwritten: {OUT}")
