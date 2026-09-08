#!/usr/bin/env python3
"""335 — mine C.2.f seed records already sitting in other chapters' pools.

Port of C.2.b's `317_c2b_free_seeds.py` (itself C.6.a's `305_`). Neighbouring chapters screened
inequality-and-investment records long before C.2.f existed and routed them out. Recovering them
costs nothing: `snowball-pools-omit-their-own-seeds` run in reverse. Expected donors are D.2.d
(intensive parenting), C.6.a (Easterlin), C.2.b (direct costs), C.3.e (credit), C.3.g (student debt)
and D.3.c (despair — Kearney-Levine lives there).

Scans every branch for JSON under literature/, output/ and extraction/, parses each unique blob
once, and keeps records whose TITLE matches the C.2.f vocabulary. Title-matching rather than
file-matching is what stops this returning a donor chapter's whole corpus because one abstract
somewhere said "inequality".

One term per pattern so yield per term is visible. A block of ORs hides the term doing the damage:
scope §3 measured `"income inequality"` carrying 635 of this chapter's 716-record frame, so it is
listed separately from every mechanism term and its `only` column is the one to read.

No author-name terms — an author name is not in a title, so a zero from one is structural, not an
absence (`named-retry-author-queries-fake-zeros`). de la Croix, Doepke, Kearney, Levine and Frank
resolve by author in the anchor resolver (336), not here.

Output: literature/search-logs/rising-inequality-and-status-competition-free-seeds.{json,md}
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
    # the general-purpose exposure term, listed alone because scope §3 measured it at 89% of frame
    "income inequality":  r"income inequalit|inequality of income|earnings inequalit",
    "distribution stat":  r"gini|top income share|top 1 ?(%|percent)|income concentration|"
                          r"90/10|income dispersion|wage dispersion",
    "relative deprivation": r"relative deprivation|status anxiety",
    "status competition": r"status competition|positional competition|status seeking|"
                          r"competition for status",
    "positional":         r"positional good|positional externalit|positional concern",
    "relative status":    r"relative status|relative standing|social rank|social position",
    "social comparison":  r"social comparison|keeping up with|conspicuous consumption",
    "arms race":          r"arms race|credential inflation|rat race",
    "shadow education":   r"shadow education|private tutoring|cram school|supplementary education",
    "investment per child": r"parental investment|investment (in|per) child|child investment|"
                            r"educational spending|enrichment (expenditure|activit)",
}
KEEP = re.compile("|".join(f"(?:{p})" for p in TERMS.values()), re.I)

# Measured homonyms (scope §8 Wall 10): "inequality" that is GENDER inequality — D.2.a's estimand —
# or health/educational inequality as an OUTCOME, neither being a distribution statistic. Measured at
# 30 and 8 records inside the fertility-restricted frame, so this is small and the filter is kept
# NARROW: a wide "inequality" filter would delete the distribution-statistic records this chapter
# runs on (`filter-can-delete-your-own-method-canon`).
DROP = re.compile(r"gender inequalit|gender gap|gender equit|health inequalit|health disparit|"
                  r"racial disparit|inequality in health|educational inequalit", re.I)

# Scope §8 Wall 9: C.2.f needs inequality as the CAUSE. The literature in which differential
# fertility CAUSES inequality, and the cross-sectional income-gradient literature, share every term
# above. Measured at 25 and 26 records inside the frame. FLAGGED, not dropped — a boundary record is
# worth keeping (`decoy-clouds-are-boundary-cases`) and the point is to size the contamination rather
# than hide it (`homonym-shares-outcome-vocabulary`).
WRONGDIR = re.compile(r"differential fertilit|fertility differential|assortative mating|"
                      r"income gradient|socioeconomic gradient|education gradient|"
                      r"consequences? of (differential )?fertilit", re.I)

# Two further clouds inside the `investment per child` term, both FLAGGED and neither dropped.
# The first run of this script returned 143 records on that term and I read the head of the list as
# "mostly evolutionary" -- it is 23%. Reading a citation-sorted head is not reading the population
# (`citation-sorted-head-is-not-the-population`), so both clouds are now counted rather than eyeballed.
#
# EVO: "parental investment" in the Trivers / behavioural-ecology sense -- resource allocation to
# offspring affecting fitness -- which shares BOTH the exposure phrase and the outcome vocabulary
# (`homonym-shares-outcome-vocabulary`). Not dropped: 9 records are evolutionary AND carry a C.2.f
# exposure term (conspicuous-consumption signalling, sexual selection and economic growth), and a
# decoy cloud is where boundary cases live (`decoy-clouds-are-boundary-cases`).
EVO = re.compile(r"reproductive success|sexual selection|life.history|evolutionary|human behavio|"
                 r"forager|hunter.gatherer|natural selection|\bfitness\b|grandparent|grandmother|"
                 r"allomaternal|primate|mating|offspring survival|anthropolog|Hadza|pastoral", re.I)

# C3D: the economics sense, which is the LARGER import and belongs to scope §8 Wall 1 -- C.3.d's
# quantity-quality literature, i.e. link 2 of this chapter's conjunction, which §4 records as C.3.d's
# chapter and not C.2.f's. Sizing it is the point: it is Wall 1's packet, not contamination.
C3D = re.compile(r"quantity.quality|child quality|family size|sibship|number of children|"
                 r"quality of children|trade.?off", re.I)

# Peer-review and replication apparatus carries the parent title verbatim, so both the title gate and
# the author gate pass. Named qualifiers only — suffix containment is unsound (`shadow-record-gate`,
# `replication-deposits-are-shadow-records`).
SHADOW = re.compile(r"^\s*(review for|decision letter for|author response for|"
                    r"editorial comment to|comment on|correction to|erratum|"
                    r"faculty opinions recommendation of|supplemental material for|"
                    r"data and code for|replication (data|package) for)\b", re.I)

TITLE_KEYS = ("title", "display_name", "paper_title", "name")
ID_KEYS = ("doi", "DOI", "openalex_id", "id", "openalex", "ids")

GREP = ("income inequality|earnings inequality|gini|top income share|income concentration|"
        "status competition|positional|relative status|social comparison|arms race|"
        "credential inflation|conspicuous consumption|relative deprivation|status anxiety|"
        "shadow education|private tutoring|parental investment|child investment|"
        "educational spending")


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
    dropped_homonym = 0
    dropped_shadow = 0
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
            if DROP.search(title):
                dropped_homonym += 1
                continue
            if SHADOW.match(title):
                dropped_shadow += 1
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
                     "wrongdir": bool(WRONGDIR.search(rec["title"])),
                     "evo": bool(EVO.search(rec["title"])),
                     "c3d": bool(C3D.search(rec["title"]))})

    per_term = {}
    for name in TERMS:
        withterm = [r for r in rows if name in r["matched"]]
        per_term[name] = {"n": len(withterm),
                          "only": sum(1 for r in withterm if len(r["matched"]) == 1),
                          "wrongdir": sum(1 for r in withterm if r["wrongdir"]),
                          "evo": sum(1 for r in withterm if r["evo"]),
                          "c3d": sum(1 for r in withterm if r["c3d"])}

    (LOGS / "rising-inequality-and-status-competition-free-seeds.json").write_text(
        json.dumps({"n_files_scanned": len(candidates), "n_unique_blobs": len(seen_blob),
                    "n_records": len(rows), "n_dropped_homonym": dropped_homonym, "n_dropped_shadow": dropped_shadow,
                    "n_timecost": sum(1 for r in rows if r["wrongdir"]),
                    "per_term": per_term, "records": rows}, indent=2) + "\n")

    lines = ["# C.2.f free seeds — records already in neighbouring chapters' pools", "",
             "Generated by `source/build/goldset/335_c2f_free_seeds.py`. Do not edit by hand.", "",
             f"Scanned **{len(candidates)}** branch:file pairs (**{len(seen_blob)}** unique blobs) "
             f"across every local and remote branch. Kept **{len(rows)}** distinct records whose "
             f"*title* matches the C.2.f vocabulary; **{dropped_homonym}** title matches were "
             "dropped by the gender/health-inequality filter.", "",
             "These are candidates, not anchors. A record reaching this table means a neighbouring "
             "chapter retrieved it, not that it is C.2.b's — routing happens at the screen, and "
             "scope §8 has ten walls waiting for exactly these records.", "",
             "**`investment per child` is a boundary term, not a homonym.** It is expected to "
             "import C.3.d (chosen quality) and D.2.d (the parenting norm). It is kept because it "
             "is link 1 of this chapter's own conjunction — scope §4 measures that link at 580 "
             "records against ~2 for the full chain — and its yield is reported separately so the "
             "cost of keeping it is visible.", "",
             "**No author terms.** An author name is not in a title, so `doepke`, `kearney`, "
             "`levine` and `frank` would return structural zeros and read as absences "
             "(`named-retry-author-queries-fake-zeros`). Those anchors resolve by author in script "
             "336.", "",
             "## Yield per term, and per term alone", "",
             "`only` counts records no other term would have caught. A term with a high `n` and a "
             "low `only` is riding on its neighbours; a term with a high `only` and no usable "
             "records is importing a homonym.", "",
             "`evo-sense` counts the Trivers / behavioural-ecology reading of "
             "\"parental investment\" — a homonym sharing both the exposure phrase and the outcome "
             "vocabulary. `C.3.d (Wall 1)` counts the quantity-quality reading, which is the larger "
             "import and is link 2 of this chapter's conjunction. Neither is dropped: the first is "
             "where boundary cases live, the second IS Wall 1's packet.", "",
             "`wrong-dir` counts records whose title is Wall 9's — "
             "the WRONG CAUSAL DIRECTION — differential fertility causing inequality, or a "
             "cross-sectional income gradient. It is reported, not dropped: those records are "
             "scope §8 Wall 4's packet.", "",
             "| term | n | only | wrong-dir | evo-sense | C.3.d (Wall 1) |", "|---|---|---|---|---|---|"]
    lines += [f"| `{k}` | {v['n']} | {v['only']} | {v['wrongdir']} | {v['evo']} | {v['c3d']} |"
              for k, v in per_term.items()]
    lines += ["", "## Records", "",
              "| # | year | title | id | matched | seen in |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        seen = ", ".join(f"`{s}`" for s in r["seen_in"][:3])
        if len(r["seen_in"]) > 3:
            seen += f" +{len(r['seen_in']) - 3}"
        lines.append(f"| {i} | {r['year']} | {r['title'][:120]} | {r['id'][:60]} | "
                     f"{', '.join(r['matched'])} | {seen} |")
    lines.append("")
    (LOGS / "rising-inequality-and-status-competition-free-seeds.md").write_text("\n".join(lines))
    print(f"{len(candidates)} branch:file pairs, {len(seen_blob)} unique blobs, "
          f"{len(rows)} records kept, {dropped_homonym} dropped as gender/health inequality, "
          f"{dropped_shadow} as shadow records, "
          f"{sum(1 for r in rows if r['wrongdir'])} of the kept are wrong-direction (Wall 9)")


main()
