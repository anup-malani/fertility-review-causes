#!/usr/bin/env python3
"""348 — mine C.3.d seed records already sitting in other chapters' pools.

Port of C.2.f's `335_c2f_free_seeds.py` (itself C.2.b's `317_`, itself C.6.a's `305_`).
Neighbouring chapters screened quantity-quality records long before C.3.d existed and routed them
out. Recovering them costs nothing: `snowball-pools-omit-their-own-seeds` run in reverse.

C.3.d has an unusually rich donor set, and one donor is a direct handoff: **C.2.f's own free-seed
script computed a `c3d` flag on every record it kept**, because scope §4 of that chapter recorded
link 2 of its conjunction as C.3.d's chapter rather than its own. Other expected donors are C.2.b
(direct costs), A.12 (twinning — this chapter's link-2 instrument is that chapter's exposure),
D.2.d (intensive parenting), C.3.e, C.3.f, C.3.g, and Alexandra's compulsory-schooling workstream.

One term per pattern so yield per term is visible. A block of ORs hides the term doing the damage:
scope §3 measured `quantity-quality` carrying 494 of this chapter's 762-record frame, so it is
listed separately from every other term and its `only` column is the one to read.

**The flag that matters here is `backward`.** Scope §2 rules that the forward arm (return →
fertility) is the primary cell and the backward arm (family size → child outcomes) is mechanism
evidence on link 2, never pooled with it. A free-seed table that does not carry that distinction
hands stage 4 a pile in which the registry's own famous citation is indistinguishable from the
registered estimand. It is FLAGGED, never dropped — the backward arm is in scope, in its own cell.

No author-name terms — an author name is not in a title, so a zero from one is structural, not an
absence (`named-retry-author-queries-fake-zeros`). Becker, Galor, Doepke, Black, Devereux, Salvanes,
Angrist and Lavy resolve by author in the anchor resolver (349), not here.

Output: literature/search-logs/quantity-quality-tradeoff-free-seeds.{json,md}
"""
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"

TERMS = {
    # the dominant term, listed alone because scope §3 measured it at 65% of the frame
    "quantity-quality":   r"quantity.quality|quality.quantity|quantity and quality of (children|"
                          r"births|offspring)|trade.?off between quantity and quality",
    "child quality":      r"child quality|quality of children|children'?s? quality",
    "sibsize / sibship":  r"\bsibsize\b|sibship size|number of siblings|sibling size",
    "child investment":   r"child investment|investment in children|investment per child|"
                          r"parental investment|educational (spending|investment)",
    "child human capital": r"human capital of children|child human capital|children'?s? human capital",
    "returns to skill":   r"returns? to (education|schooling|human capital)|skill premium|"
                          r"college premium|wage premium|returns to college",
    "family-size instrument": r"twin (birth|instrument)|\btwins\b|sibling sex composition|"
                              r"same.sex sibling|sex composition of",
    "schooling reform":   r"compulsory (schooling|education)|school.leaving age|school construction|"
                          r"education expansion|universal primary education",
    "skill shock":        r"import competition|trade liberali|china shock|industrial robot|"
                          r"automation|routine.biased|skill.biased|technological change",
    "unified growth":     r"unified growth|malthus(ian)? to|from stagnation to growth|"
                          r"growth and the demographic transition",
    "resource dilution":  r"resource dilution|dilution of resources|confluence model",
}
KEEP = re.compile("|".join(f"(?:{p})" for p in TERMS.values()), re.I)

# ---------------------------------------------------------------- the two-tier keep rule
# The first run of this script kept 1,653 records and 1,065 of them came from two terms:
# `family-size instrument` (608) and `skill shock` (457). A random sample of the records ONLY those
# terms caught -- random, because `citation-sorted-head-is-not-the-population` -- was A.12's twin
# obstetrics corpus (twin gestational size, conjoined twins, twin speaker verification) and a
# labour-economics trade-and-automation corpus with no fertility or child outcome anywhere in it.
# Roughly 1 of 12 and 0 of 12 usable.
#
# The cause is a design error, not a bad word list. These patterns were lifted from the scope's
# THREE-AXIS PRODUCTION QUERY (§3), where a design axis and a shock axis are intersected with an
# outcome axis. Mining a neighbour's pool has no such intersection, so the design and shock terms
# match the DONOR's corpus rather than this chapter's -- A.12's pool is about twins, and D.3.c's
# tier-B frame is full of technological change. `diagnostic-and-retrieval-vocabularies-differ`: a
# list that is right for retrieval is not automatically right for mining.
#
# So the keep rule is two-tier. THEORY terms are self-sufficient: a title saying "quantity-quality"
# or "sibsize" is about this mechanism whatever else it says. DESIGN and SHOCK terms are only half a
# record and must co-occur with an outcome -- fertility, or a child-investment/attainment outcome --
# which is exactly the conjunction scope §4 says has to be present for a record to be C.3.d's.
# `births?` was in this list on the first pass and was scored alone afterwards, per
# `anchored-vocabulary-has-own-homonym`: it admitted 124 records of which ONE was C.3.d's
# ("Increasing the credibility of the twin birth instrument") -- the rest were A.12 twin
# epidemiology reaching the outcome tier through "twin births" and "multiple-birth family". Removed.
# The lost record is recoverable from the production query's design axis, which intersects an
# outcome, and from snowball; a 0.8%-precision term is not worth 123 false admits in a seed table.
OUTCOME_MARKER = re.compile(
    r"fertilit|childbearing|birth rate|family size|number of children|"
    r"completed famil|child quality|quality of children|educational attainment|test score|"
    r"years of schooling|child outcomes|school achievement|academic achievement|"
    r"cognitive|human capital|child investment|investment in children|investment per child|"
    r"parental investment|educational (spending|investment)|schooling of children|"
    r"fertility intention|desired family|quantity.quality", re.I)

# Terms that are only half a record on their own.
REQUIRE_OUTCOME = {"family-size instrument", "skill shock", "schooling reform", "returns to skill"}

# Measured homonym (scope §3): "fertility" is a soil-science and animal-husbandry word and
# `quantity-quality` is a stock phrase in both. Measured at 43 records, 5.6% of the frame, and 42 of
# the 43 sit under the single word "fertility". Small, so the filter is kept NARROW — a wide
# agricultural filter would delete the historical-agriculture records this chapter's FDT arm runs on
# (`filter-can-delete-your-own-method-canon`: a species filter flagged A.18's own method canon).
DROP = re.compile(r"soil fertilit|crop yield|grain yield|fertili[sz]er|\blivestock\b|dairy (cow|cattle)|"
                  r"broiler|silage|semen quality|agronomic|sperm (quality|motility)", re.I)

# THE flag of this chapter (scope §2). BACKWARD = family size is the EXPOSURE and a child outcome is
# the DEPENDENT variable. The registry's own cited evidence (Black-Devereux-Salvanes) is backward.
# Never dropped: it is link 2 of the conjunction and has its own estimand cell, `QQ_SUBSTITUTION`.
BACKWARD = re.compile(r"educational attainment|test score|cognitive (abilit|skill|outcome)|"
                      r"years of schooling|child outcomes|school achievement|academic achievement|"
                      r"effects? of family size|family size (and|on)|sibling size (and|on)|"
                      r"number of siblings (and|on)|birth order", re.I)

# Scope §8 Wall 2, the wall this chapter's scope ADDED and the one most likely to be violated
# silently: C.3.d owns the return to the CHILD's human capital, C.2.e the return to the PARENT's.
# A schooling-supply shock moves both, and §7 row 3 is the largest forward row.
WALL_C2E = re.compile(r"mother'?s? (education|schooling|wage)|maternal education|"
                      r"women'?s? (education|wage|schooling)|female (wage|labor|labour)|"
                      r"opportunity cost of (time|women)|female education", re.I)

# Scope §8 Wall 5: A.12 owns twinning AS AN EXPOSURE (an accounting identity on the birth rate);
# C.3.d uses twin births AS AN INSTRUMENT for family size. Same variable, different roles
# (`snowball-the-estimand-not-the-estimator`). A.12 is drafted, so these are checkable against a
# written pool rather than re-derived.
WALL_A12 = re.compile(r"\btwin(s|ning)?\b|multiple (birth|gestation|pregnanc)", re.I)

# The Trivers / behavioural-ecology reading of "parental investment" — resource allocation to
# offspring affecting fitness — which shares BOTH the exposure phrase and the outcome vocabulary
# (`homonym-shares-outcome-vocabulary`). FLAGGED not dropped: C.2.f measured this cloud at 23% of
# the term rather than the "mostly" a citation-sorted head suggested, and a decoy cloud is where
# boundary cases live (`decoy-clouds-are-boundary-cases`).
EVO = re.compile(r"reproductive success|sexual selection|life.histor|evolutionary|forager|"
                 r"hunter.gatherer|natural selection|\bfitness\b|primate|\bmating\b|"
                 r"offspring survival|anthropolog|\bHadza\b|behavioural ecolog|behavioral ecolog", re.I)

# Scope §9 and §13 call 4: calibrated unified-growth and OLG models are THEORY, context only, never
# an identified estimate. Flagged so the size of that cell is visible before the PI is asked.
THEORY = re.compile(r"unified growth|overlapping generations|calibrat|a model of|theory of|"
                    r"general equilibrium|quantitative (model|theory)|numerical", re.I)

# Peer-review and replication apparatus carries the parent title verbatim, so both the title gate and
# the author gate pass. Named qualifiers only — suffix containment is unsound (`shadow-record-gate`,
# `replication-deposits-are-shadow-records`).
SHADOW = re.compile(r"^\s*(review for|decision letter for|author response for|"
                    r"editorial comment to|comment on|correction to|erratum|"
                    r"faculty opinions recommendation of|supplemental material for|"
                    r"data and code for|replication (data|package) for)\b", re.I)

TITLE_KEYS = ("title", "display_name", "paper_title", "name")
ID_KEYS = ("doi", "DOI", "openalex_id", "id", "openalex", "ids")

GREP = ("quantity-quality|quantity quality|quality-quantity|child quality|quality of children|"
        "sibsize|sibship|number of siblings|child investment|investment in children|"
        "parental investment|human capital of children|child human capital|"
        "returns to schooling|returns to education|skill premium|college premium|"
        "twin birth|sibling sex composition|compulsory schooling|compulsory education|"
        "school construction|import competition|china shock|industrial robot|skill-biased|"
        "unified growth|resource dilution")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def walk(node, out):
    """Collect every dict that looks like a bibliographic record."""
    if isinstance(node, dict):
        title = next((node[k] for k in TITLE_KEYS
                      if isinstance(node.get(k), str) and len(node[k]) > 15), None)
        if title:
            out.append(node)
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def ident(rec):
    for k in ID_KEYS:
        v = rec.get(k)
        if isinstance(v, str) and v:
            return v
        if isinstance(v, dict):
            for kk in ("doi", "openalex"):
                if isinstance(v.get(kk), str):
                    return v[kk]
    return ""


def main():
    branches = subprocess.run(["git", "branch", "-a", "--format=%(refname:short)"],
                              capture_output=True, text=True, cwd=ROOT).stdout.split()
    branches = [b for b in branches if "HEAD" not in b]

    candidates = {}
    for b in branches:
        r = subprocess.run(
            ["git", "grep", "-l", "-i", "-E", GREP, b, "--", "literature", "output", "extraction"],
            capture_output=True, text=True, cwd=ROOT)
        for line in r.stdout.splitlines():
            if ":" not in line:
                continue
            _, path = line.split(":", 1)
            if path.endswith(".json"):
                candidates[(b, path)] = None

    seen_blob, records = set(), {}
    provenance = defaultdict(set)
    dropped_homonym = dropped_shadow = 0
    refused_half = []
    for (b, path) in sorted(candidates):
        raw = subprocess.run(["git", "show", f"{b}:{path}"],
                             capture_output=True, text=True, cwd=ROOT).stdout
        if not raw:
            continue
        h = hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()
        if h in seen_blob:
            continue
        seen_blob.add(h)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        found = []
        walk(data, found)
        for rec in found:
            title = next((rec[k] for k in TITLE_KEYS
                          if isinstance(rec.get(k), str) and len(rec[k]) > 15), "")
            if not KEEP.search(title):
                continue
            # DROP and SHADOW run FIRST so their counters stay meaningful. When the half-record
            # rule ran ahead of them the soil/livestock counter fell from 12 to 0 -- not because
            # the contamination had gone but because the earlier filter was eating it
            # (`dedup-before-counting-hides-redundant-rung`: a filter ahead of a counter makes the
            # counter read zero, and REDUNDANT is not EMPTY).
            if DROP.search(title):
                dropped_homonym += 1
                continue
            if SHADOW.match(title):
                dropped_shadow += 1
                continue
            hits_here = [n for n, pat in TERMS.items() if re.search(pat, title, re.I)]
            # Two-tier keep: a record surviving only on design/shock terms needs an outcome too.
            if all(n in REQUIRE_OUTCOME for n in hits_here) and not OUTCOME_MARKER.search(title):
                refused_half.append({"title": title.strip(), "matched": hits_here})
                continue
            key = norm(title)
            if not key:
                continue
            provenance[key].add(Path(path).name)
            if key not in records:
                records[key] = {"title": title.strip(), "id": ident(rec),
                                "year": rec.get("publication_year") or rec.get("year") or ""}

    rows = []
    for key, rec in sorted(records.items(), key=lambda kv: -len(provenance[kv[0]])):
        hits = [name for name, pat in TERMS.items() if re.search(pat, rec["title"], re.I)]
        rows.append({**rec, "matched": hits, "seen_in": sorted(provenance[key]),
                     "backward": bool(BACKWARD.search(rec["title"])),
                     "wall_c2e": bool(WALL_C2E.search(rec["title"])),
                     "wall_a12": bool(WALL_A12.search(rec["title"])),
                     "evo": bool(EVO.search(rec["title"])),
                     "theory": bool(THEORY.search(rec["title"]))})

    per_term = {}
    for name in TERMS:
        wt = [r for r in rows if name in r["matched"]]
        per_term[name] = {"n": len(wt),
                          "only": sum(1 for r in wt if len(r["matched"]) == 1),
                          "backward": sum(1 for r in wt if r["backward"]),
                          "wall_c2e": sum(1 for r in wt if r["wall_c2e"]),
                          "wall_a12": sum(1 for r in wt if r["wall_a12"]),
                          "evo": sum(1 for r in wt if r["evo"]),
                          "theory": sum(1 for r in wt if r["theory"])}

    n_back = sum(1 for r in rows if r["backward"])
    (LOGS / "quantity-quality-tradeoff-free-seeds.json").write_text(
        json.dumps({"n_files_scanned": len(candidates), "n_unique_blobs": len(seen_blob),
                    "n_records": len(rows), "n_dropped_homonym": dropped_homonym,
                    "n_dropped_shadow": dropped_shadow, "n_backward": n_back,
                    "n_refused_half_record": len(refused_half),
                    "per_term": per_term, "records": rows,
                    "refused_half_record": refused_half}, indent=2) + "\n")

    lines = ["# C.3.d free seeds — records already in neighbouring chapters' pools", "",
             "Generated by `source/build/goldset/348_c3d_free_seeds.py`. Do not edit by hand.", "",
             f"Scanned **{len(candidates)}** branch:file pairs (**{len(seen_blob)}** unique blobs) "
             f"across every local and remote branch. Kept **{len(rows)}** distinct records whose "
             f"*title* matches the C.3.d vocabulary; **{dropped_homonym}** were dropped by the "
             f"soil/livestock filter and **{dropped_shadow}** as shadow records.", "",
             f"**{len(refused_half)} further titles were refused as half a record**: they matched "
             "only a DESIGN or SHOCK term (`family-size instrument`, `skill shock`, "
             "`schooling reform`, `returns to skill`) and carried no fertility or child-outcome "
             "word. Those axes are half of a conjunction in the production query (scope §3) and "
             "match a donor's whole corpus when mined on their own — the first run of this script "
             "kept 1,653 records of which A.12's twin-obstetrics pool and a trade-and-automation "
             "labour corpus were 1,065. The refusals are listed in the JSON so the rule can be "
             "audited rather than trusted.", "",
             "These are candidates, not anchors. A record reaching this table means a neighbouring "
             "chapter retrieved it, not that it is C.3.d's — routing happens at the screen, and "
             "scope §8 has ten walls waiting for exactly these records.", "",
             f"**`backward` is the flag that matters: {n_back} of {len(rows)} records.** Scope §2 "
             "rules that the forward arm (return → fertility) is the primary cell and the backward "
             "arm (family size → child outcomes) is mechanism evidence on link 2, in its own "
             "estimand cell, never pooled. The registry's own cited evidence "
             "(Black-Devereux-Salvanes) is backward. Flagged, never dropped.", "",
             "**No author terms.** An author name is not in a title, so `becker`, `galor`, `doepke` "
             "and `salvanes` would return structural zeros and read as absences "
             "(`named-retry-author-queries-fake-zeros`). Those anchors resolve by author in 349.", "",
             "## Yield per term, and per term alone", "",
             "`only` counts records no other term would have caught. A term with a high `n` and a "
             "low `only` is riding on its neighbours; a term with a high `only` and no usable "
             "records is importing a homonym.", "",
             "`C.2.e` and `A.12` count scope §8's walls 2 and 5 — the return to the *parent's* human "
             "capital rather than the child's, and twinning as an exposure rather than as an "
             "instrument. `evo-sense` counts the Trivers reading of \"parental investment\". "
             "`theory` counts calibrated models, which scope §9 makes context-only and §13 call 4 "
             "puts to the PI. None is dropped.", "",
             "| term | n | only | backward | C.2.e (W2) | A.12 (W5) | evo-sense | theory |",
             "|---|---|---|---|---|---|---|---|"]
    lines += [f"| `{k}` | {v['n']} | {v['only']} | {v['backward']} | {v['wall_c2e']} | "
              f"{v['wall_a12']} | {v['evo']} | {v['theory']} |" for k, v in per_term.items()]
    lines += ["", "## Records", "",
              "| # | year | dir | title | id | matched | seen in |", "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        seen = ", ".join(f"`{s}`" for s in r["seen_in"][:3])
        if len(r["seen_in"]) > 3:
            seen += f" +{len(r['seen_in']) - 3}"
        lines.append(f"| {i} | {r['year']} | {'BACK' if r['backward'] else 'fwd'} | "
                     f"{r['title'][:110]} | {r['id'][:52]} | {', '.join(r['matched'])} | {seen} |")
    lines.append("")
    (LOGS / "quantity-quality-tradeoff-free-seeds.md").write_text("\n".join(lines))
    print(f"{len(candidates)} branch:file pairs, {len(seen_blob)} unique blobs, "
          f"{len(rows)} records kept, {dropped_homonym} dropped as soil/livestock, "
          f"{dropped_shadow} as shadow records, {len(refused_half)} refused as half a record; "
          f"{n_back} of the kept are BACKWARD (scope §2)")


main()
