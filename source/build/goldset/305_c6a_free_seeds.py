#!/usr/bin/env python3
"""305 — mine C.6.a seed records already sitting in other chapters' pools.

Neighbouring chapters retrieved and screened Easterlin/cohort-size records long before C.6.a existed,
then routed them out. Those records are provenance-labelled hits from adjacent literatures and they
cost nothing to recover. This is `snowball-pools-omit-their-own-seeds` run in reverse: instead of
injecting hand-sourced anchors into a pool that lacks them, we harvest a pool that already has them.

Scans every branch (local and remote) for JSON under literature/, output/ and extraction/ whose text
mentions the C.6.a vocabulary, parses each unique blob once, walks it for anything record-shaped, and
keeps records whose TITLE matches. Matching on the title, not on the file, is what keeps this from
returning a chapter's whole corpus because one abstract somewhere said "cohort size".

Output: literature/search-logs/easterlin-relative-income-free-seeds.json
        literature/search-logs/easterlin-relative-income-free-seeds.md
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

# Title-level match, ONE PATTERN PER TERM so yield per term is visible. A block of ORs hides the
# term that is doing all the damage: the first run of this script matched a bare "baby boom" and
# returned 402 of 480 records, nearly all of them *Baby Boomers* the living generation — retirement
# planning, gerontology, generational marketing. That is `frame-growth-is-not-frame-gain`: run the
# candidate term alone, minus the rest of the axis, and read what is left.
TERMS = {
    "easterlin":        r"\beasterlin\b",
    "macunovich":       r"\bmacunovich\b",
    "butz":             r"\bbutz\b",
    "cohort size":      r"cohort size|size of (the )?cohort",
    "relative cohort":  r"relative cohort|cohort crowding",
    "relative income":  r"relative income",
    # "baby boom" is kept only where it is NOT "baby boomer(s)" — the generational label is the
    # homonym, the demographic event is the target.
    "baby boom/bust":   r"baby boom(?!er)|baby bust",
}
KEEP = re.compile("|".join(f"(?:{p})" for p in TERMS.values()), re.I)
# Two homonyms. The happiness one measures at 2 records against a fertility axis (scope §8 Wall 6),
# but these pools are not all fertility pools, so it is filtered rather than trusted. The
# generational-label one is what the first run found.
DROP = re.compile(r"easterlin paradox|life satisfaction|subjective well|happiness|"
                  r"baby boomer", re.I)

TITLE_KEYS = ("title", "display_name", "paper_title", "name")
ID_KEYS = ("doi", "DOI", "openalex_id", "id", "openalex", "ids")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def walk(node, out):
    """Yield every dict that looks like a bibliographic record."""
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
    branches = subprocess.run(
        ["git", "branch", "-a", "--format=%(refname:short)"],
        capture_output=True, text=True, cwd=ROOT).stdout.split()
    branches = [b for b in branches if "HEAD" not in b]

    # branch:path -> blob sha, so identical content shared across branches is parsed once.
    candidates = {}
    for b in branches:
        r = subprocess.run(
            ["git", "grep", "-l", "-i", "-E",
             "easterlin|cohort size|relative cohort|cohort crowding|macunovich|butz",
             b, "--", "literature", "output", "extraction"],
            capture_output=True, text=True, cwd=ROOT)
        for line in r.stdout.splitlines():
            if ":" not in line:
                continue
            _, path = line.split(":", 1)
            if path.endswith(".json"):
                candidates[(b, path)] = None

    seen_blob, records = set(), {}
    provenance = defaultdict(set)
    for (b, path) in sorted(candidates):
        raw = subprocess.run(["git", "show", f"{b}:{path}"],
                             capture_output=True, text=True, cwd=ROOT).stdout
        if not raw:
            continue
        h = hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()
        if h in seen_blob:
            provenance_only = True
        else:
            seen_blob.add(h)
            provenance_only = False
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        found = []
        walk(data, found)
        for rec in found:
            title = next((rec[k] for k in TITLE_KEYS
                          if isinstance(rec.get(k), str) and len(rec[k]) > 15), "")
            if not KEEP.search(title) or DROP.search(title):
                continue
            key = norm(title)
            if not key:
                continue
            provenance[key].add(Path(path).name)
            if key not in records:
                records[key] = {"title": title.strip(), "id": ident(rec),
                                "year": rec.get("publication_year") or rec.get("year") or ""}
        _ = provenance_only

    rows = []
    for key, rec in sorted(records.items(), key=lambda kv: -len(provenance[kv[0]])):
        hits = [name for name, pat in TERMS.items() if re.search(pat, rec["title"], re.I)]
        rows.append({**rec, "matched": hits, "seen_in": sorted(provenance[key])})

    # Yield per term, and yield of each term ALONE (records no other term would have caught).
    per_term = {}
    for name in TERMS:
        withterm = [r for r in rows if name in r["matched"]]
        per_term[name] = {"n": len(withterm),
                          "only": sum(1 for r in withterm if len(r["matched"]) == 1)}

    (LOGS / "easterlin-relative-income-free-seeds.json").write_text(
        json.dumps({"n_files_scanned": len(candidates), "n_unique_blobs": len(seen_blob),
                    "n_records": len(rows), "per_term": per_term, "records": rows},
                   indent=2) + "\n")

    lines = ["# C.6.a free seeds — records already in neighbouring chapters' pools", "",
             "Generated by `source/build/goldset/305_c6a_free_seeds.py`. Do not edit by hand.", "",
             f"Scanned **{len(candidates)}** branch:file pairs (**{len(seen_blob)}** unique blobs) "
             f"across every local and remote branch. Kept **{len(rows)}** distinct records whose "
             "*title* matches the C.6.a exposure vocabulary.", "",
             "These are candidates, not anchors. A record reaching this table means a neighbouring "
             "chapter retrieved it, not that it is C.6.a's — routing happens at the screen.", "",
             "## Yield per term, and per term alone", "",
             "`only` counts records no other term would have caught. A term with a high `n` and a "
             "low `only` is riding on its neighbours; a term with a high `only` and no usable "
             "records is importing a homonym.", "",
             "**Two of these terms cannot report what they look like they report.** `macunovich` and "
             "`butz` are AUTHOR names matched against TITLES, and an author name is not in a title: "
             "a zero from either is a structural zero, not an absence "
             "(`named-retry-author-queries-fake-zeros`). `butz` returns anything at all only because "
             "*Butz-Ward* is used as a model name in the title of papers testing it. Read "
             "`macunovich` = 0 as \"this channel cannot see authors\", and resolve those anchors by "
             "author in the resolver instead.", "",
             "**Three homonyms are in play on the `baby boom/bust` axis**, and only two are filtered. "
             "*Baby Boomer* the living generation is dropped (retirement, gerontology, generational "
             "marketing) and it was the whole story on the first run: 402 of 480 records. The "
             "Easterlin-paradox happiness cluster is dropped. The third is left in deliberately — "
             "*BABY BOOM* is also an Arabidopsis transcription factor, and a plant-tissue paper "
             "using the word *fertile* survives every filter here. One record, left for the screen "
             "to route: a species filter would risk more than it saves "
             "(`filter-can-delete-your-own-method-canon`).", "",
             "| term | n | only |", "|---|---|---|"]
    lines += [f"| `{k}` | {v['n']} | {v['only']} |" for k, v in per_term.items()]
    lines += ["", "## Records", "",
              "| # | year | title | id | matched | seen in |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        seen = ", ".join(f"`{s}`" for s in r["seen_in"][:3])
        if len(r["seen_in"]) > 3:
            seen += f" +{len(r['seen_in']) - 3}"
        lines.append(f"| {i} | {r['year']} | {r['title'][:120]} | {r['id'][:60]} | "
                     f"{', '.join(r['matched'])} | {seen} |")
    lines.append("")
    (LOGS / "easterlin-relative-income-free-seeds.md").write_text("\n".join(lines))
    print(f"{len(candidates)} branch:file pairs, {len(seen_blob)} unique blobs, {len(rows)} records")


main()
