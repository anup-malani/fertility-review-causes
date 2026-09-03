#!/usr/bin/env python3
"""317 — mine C.2.b seed records already sitting in other chapters' pools.

Direct port of C.6.a's `305_c6a_free_seeds.py`. Neighbouring chapters retrieved and screened
cost-of-children records long before C.2.b existed, then routed them out. Those records are
provenance-labelled hits from adjacent literatures and cost nothing to recover. This is
`snowball-pools-omit-their-own-seeds` run in reverse: rather than injecting hand-sourced anchors into
a pool that lacks them, harvest a pool that already has them. C.2.c, D.2.d, C.3.b, C.3.e and C.3.c
are the expected donors.

Scans every branch (local and remote) for JSON under literature/, output/ and extraction/ whose text
mentions the C.2.b vocabulary, parses each unique blob once, walks it for anything record-shaped, and
keeps records whose TITLE matches. Matching on the title, not on the file, is what stops this
returning a donor chapter's whole corpus because one abstract somewhere said "cost of children".

One term per pattern, so yield per term is visible. A block of ORs hides the term doing the damage:
on C.6.a a bare "baby boom" returned 402 of 480 records, nearly all *Baby Boomers* the living
generation (`frame-growth-is-not-frame-gain`).

No author-name terms. An author name is not in a title, so a zero from one is a structural zero and
not an absence (`named-retry-author-queries-fake-zeros`). Lino, Folbre, Doepke, Kindermann and
Caldwell are resolved by author in the resolver (script 319), not here.

Output: literature/search-logs/child-cost-direct-free-seeds.json
        literature/search-logs/child-cost-direct-free-seeds.md
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
    "cost of children":   r"cost(s)? of (a |the )?child(ren)?\b",
    "cost of raising":    r"cost(s)? of (raising|rearing|bringing up)",
    "child-rearing cost": r"child ?rearing cost|child ?rearing expenditure",
    "expenditure":        r"expenditure(s)? on child|child expenditure|spending on children",
    "price of children":  r"price of (a |the )?child(ren)?|child price|relative price of child",
    "school fees":        r"school fee|user fee|fee abolition|free primary education|"
                          r"free basic education|school cost",
    "tuition":            r"\btuition\b",
    "equivalence scale":  r"equivalence scale",
    "cost of childbearing": r"cost(s)? of childbearing|cost(s)? of parenthood|"
                            r"cost(s)? of motherhood",
}
KEEP = re.compile("|".join(f"(?:{p})" for p in TERMS.values()), re.I)

# The measured homonym is the paediatric cost-of-illness literature: scope §8 Wall 9 puts it at 206
# of 740 records unrestricted and 10 inside the fertility-restricted frame. These pools are not all
# fertility pools, so it is filtered here rather than trusted. Kept deliberately NARROW — a wide
# clinical filter would delete the child-health-price designs that populate a primary cell
# (`filter-can-delete-your-own-method-canon`). It drops cost-OF-ILLNESS vocabulary, never
# cost-of-health-CARE vocabulary.
DROP = re.compile(r"cost of illness|cost-of-illness|cost.effectiveness|burden of disease|"
                  r"hospitali[sz]|inpatient|chemotherap|asthma|diabet|autism|leukemia|leukaemia|"
                  r"cystic fibrosis|congenital", re.I)

# The first run found something scope §8 Wall 4 registered as a ROUTING problem and not as a
# VOCABULARY one: "cost of children" is the shared phrase of two literatures, and in these pools the
# TIME-cost / child-penalty literature (C.2.e's estimand) is the larger of the two. It is measured
# here per term rather than dropped, because a boundary record is worth keeping
# (`decoy-clouds-are-boundary-cases`) and because the point is to size the contamination, not to hide
# it (`homonym-shares-outcome-vocabulary`).
TIMECOST = re.compile(r"time cost|career cost|opportunity cost|child penalty|motherhood penalty|"
                      r"for(e)?gone|time use|time-use|labour market cost|labor market cost|"
                      r"indirect cost|implicit cost|household production|foregone leisure", re.I)

# Peer-review and replication apparatus carries the parent title verbatim, so both the title gate and
# the author gate pass. Named qualifiers only — suffix containment is unsound (`shadow-record-gate`,
# `replication-deposits-are-shadow-records`).
SHADOW = re.compile(r"^\s*(review for|decision letter for|author response for|"
                    r"editorial comment to|comment on|correction to|erratum|"
                    r"faculty opinions recommendation of|supplemental material for|"
                    r"data and code for|replication (data|package) for)\b", re.I)

TITLE_KEYS = ("title", "display_name", "paper_title", "name")
ID_KEYS = ("doi", "DOI", "openalex_id", "id", "openalex", "ids")

GREP = ("cost of child|cost of a child|costs of children|child cost|cost of raising|"
        "cost of rearing|child rearing cost|childrearing cost|expenditure on child|"
        "expenditures on children|child expenditure|price of children|child price|"
        "school fee|user fee|free primary education|equivalence scale|cost of childbearing|"
        "tuition")


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
                     "timecost": bool(TIMECOST.search(rec["title"]))})

    per_term = {}
    for name in TERMS:
        withterm = [r for r in rows if name in r["matched"]]
        per_term[name] = {"n": len(withterm),
                          "only": sum(1 for r in withterm if len(r["matched"]) == 1),
                          "timecost": sum(1 for r in withterm if r["timecost"])}

    (LOGS / "child-cost-direct-free-seeds.json").write_text(
        json.dumps({"n_files_scanned": len(candidates), "n_unique_blobs": len(seen_blob),
                    "n_records": len(rows), "n_dropped_homonym": dropped_homonym, "n_dropped_shadow": dropped_shadow,
                    "n_timecost": sum(1 for r in rows if r["timecost"]),
                    "per_term": per_term, "records": rows}, indent=2) + "\n")

    lines = ["# C.2.b free seeds — records already in neighbouring chapters' pools", "",
             "Generated by `source/build/goldset/317_c2b_free_seeds.py`. Do not edit by hand.", "",
             f"Scanned **{len(candidates)}** branch:file pairs (**{len(seen_blob)}** unique blobs) "
             f"across every local and remote branch. Kept **{len(rows)}** distinct records whose "
             f"*title* matches the C.2.b vocabulary; **{dropped_homonym}** title matches were "
             "dropped by the cost-of-illness filter.", "",
             "These are candidates, not anchors. A record reaching this table means a neighbouring "
             "chapter retrieved it, not that it is C.2.b's — routing happens at the screen, and "
             "scope §8 has nine walls waiting for exactly these records.", "",
             "**`tuition` is a boundary term, not a homonym.** It is expected to import C.3.g "
             "(student debt — the prospective parent's own prior debt) and C.3.d (higher education "
             "as chosen quality). It is kept because scope §7 row 8 registers the anticipated future "
             "cost of a child as admissible variation, and its yield is reported separately so the "
             "cost of keeping it is visible.", "",
             "**No author terms.** An author name is not in a title, so `lino`, `folbre`, `doepke` "
             "and `caldwell` would return structural zeros and read as absences "
             "(`named-retry-author-queries-fake-zeros`). Those anchors resolve by author in script "
             "319.", "",
             "## Yield per term, and per term alone", "",
             "`only` counts records no other term would have caught. A term with a high `n` and a "
             "low `only` is riding on its neighbours; a term with a high `only` and no usable "
             "records is importing a homonym.", "",
             "`time` counts records whose title is the TIME-cost / child-penalty literature — "
             "C.2.e's estimand, not this chapter's. It is reported, not dropped: those records are "
             "scope §8 Wall 4's packet.", "",
             "| term | n | only | time |", "|---|---|---|---|"]
    lines += [f"| `{k}` | {v['n']} | {v['only']} | {v['timecost']} |" for k, v in per_term.items()]
    lines += ["", "## Records", "",
              "| # | year | title | id | matched | seen in |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        seen = ", ".join(f"`{s}`" for s in r["seen_in"][:3])
        if len(r["seen_in"]) > 3:
            seen += f" +{len(r['seen_in']) - 3}"
        lines.append(f"| {i} | {r['year']} | {r['title'][:120]} | {r['id'][:60]} | "
                     f"{', '.join(r['matched'])} | {seen} |")
    lines.append("")
    (LOGS / "child-cost-direct-free-seeds.md").write_text("\n".join(lines))
    print(f"{len(candidates)} branch:file pairs, {len(seen_blob)} unique blobs, "
          f"{len(rows)} records kept, {dropped_homonym} dropped as cost-of-illness, "
          f"{dropped_shadow} as shadow records, "
          f"{sum(1 for r in rows if r['timecost'])} of the kept are time-cost (C.2.e)")


main()
