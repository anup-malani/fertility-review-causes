#!/usr/bin/env python3
"""297 — C.3.e: find version pairs in the primary pool. TICK-077.

296's folded-title dedup found ZERO pairs in a pool where two were already known by hand. Both
escape title equality, and in different ways:

  * "...Evidence from an Aging SOCIETY" (2026) vs "...Evidence from an Aging ECONOMY" (2024)
    -- one word changed between versions.
  * "BEQUEST RECEIPT AND FAMILY SIZE EFFECTS" (2010) vs "Do Credit Constraints Explain Family
    Size Effects? Tests Based on Bequest Receipt and Family Earnings" (2005) -- no shared title
    at all; Jaccard is about 0.43.

A retitled version is invisible to title matching, which is the same failure the chapter already
hit on Yang ("More Credit, FEWER Babies?" -> "More Credit, MORE Babies?"). So:

  1. Human flags are authoritative. Pairs identified by reading are declared here, in the file.
  2. Automation SUPPLEMENTS them, on two rules, and never on title alone:
       - Jaccard >= 0.75 AND first-author agreement AND years within 10; or
       - full CONTAINMENT of the shorter title in the longer AND first-author agreement.
     Containment alone is unsound -- a short generic title sits inside many longer ones -- so the
     author gate is not optional here.
  3. Everything it proposes is printed for a human read, never auto-merged.

Usage: python3 297_c3e_version_pairs.py
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"

spec = importlib.util.spec_from_file_location("m283", GOLD / "283_c3e_boundary_hunt.py")
m283 = importlib.util.module_from_spec(spec)
sys.modules["m283"] = m283
spec.loader.exec_module(m283)
spec2 = importlib.util.spec_from_file_location("m277", GOLD / "277_c3e_snowball.py")
m277 = importlib.util.module_from_spec(spec2)
sys.modules["m277"] = m277
spec2.loader.exec_module(m277)
get, fold, SELECT = m283.get, m277.fold, m283.SELECT

# Pairs identified by reading. These are authoritative and are not subject to the scores below.
DECLARED = [
    ("W7154967232", "W4405014414",
     "Do Mortgage Interest Subsidies Affect Fertility... 'Aging Society' (2026) vs 'Aging Economy' "
     "(2024). One word apart; same study."),
    ("W2186788266", "W1979646151",
     "Do Credit Constraints Explain Family Size Effects? Tests Based on Bequest Receipt (2005) vs "
     "Bequest Receipt and Family Size Effects (2010). Retitled; no shared title."),
]
STOP = {"the", "and", "for", "from", "with", "evidence", "a", "an", "of", "in", "on", "do", "does"}


def toks(s):
    return {t for t in fold(s).split() if t not in STOP and len(t) > 2}


def main():
    res = json.loads((LOGS / "credit-constraints-screen-results.json").read_text())
    prim = [r for r in res["rows"] if r["cell"].startswith("PRIMARY_")]
    ids = [r["openalex"] for r in prim]
    meta = {}
    for i in range(0, len(ids), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(ids[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            continue
        for w in d["results"]:
            a = [x["author"]["display_name"] for x in (w.get("authorships") or [])]
            meta[w["id"].rsplit("/", 1)[-1]] = {"first": a[0] if a else "", "all": a}

    def surname(n):
        t = fold(n).split()
        return t[-1] if t else ""

    proposals = []
    for i in range(len(prim)):
        for j in range(i + 1, len(prim)):
            a, b = prim[i], prim[j]
            ta, tb = toks(a["title"]), toks(b["title"])
            if not ta or not tb:
                continue
            jac = len(ta & tb) / len(ta | tb)
            cont = len(ta & tb) / min(len(ta), len(tb))
            fa = surname(meta.get(a["openalex"], {}).get("first", ""))
            fb = surname(meta.get(b["openalex"], {}).get("first", ""))
            auth = bool(fa) and fa == fb
            ya = int(a["year"]) if str(a["year"]).isdigit() else 0
            yb = int(b["year"]) if str(b["year"]).isdigit() else 0
            near = abs(ya - yb) <= 10
            if (jac >= 0.75 and auth and near) or (cont >= 0.999 and auth):
                proposals.append({"a": a["openalex"], "b": b["openalex"],
                                  "title_a": a["title"], "title_b": b["title"],
                                  "jaccard": round(jac, 3), "containment": round(cont, 3),
                                  "first_author": fa, "years": [ya, yb],
                                  "rule": "jaccard+author" if jac >= 0.75 else "containment+author"})

    declared_ids = {(x, y) for x, y, _ in DECLARED} | {(y, x) for x, y, _ in DECLARED}
    new = [p for p in proposals if (p["a"], p["b"]) not in declared_ids]

    print(f"primary pool: {len(prim)}")
    print(f"declared by hand: {len(DECLARED)}")
    for x, y, why in DECLARED:
        print(f"  {x} == {y}   {why[:88]}")
    print(f"\nproposed by the automated rules, NOT auto-merged ({len(new)}):")
    for p in new:
        print(f"  [{p['rule']}] J={p['jaccard']} C={p['containment']} author={p['first_author']}")
        print(f"     A: {p['title_a'][:74]}")
        print(f"     B: {p['title_b'][:74]}")
    # did the rules re-find what the human declared?
    found = [p for p in proposals if (p["a"], p["b"]) in declared_ids]
    print(f"\nrules re-found {len(found)} of the {len(DECLARED)} hand-declared pairs "
          f"-- a recall check on the rules themselves")
    for p in found:
        print(f"   [{p['rule']}] {p['title_a'][:60]}")
    (LOGS / "credit-constraints-version-pairs.json").write_text(json.dumps(
        {"declared": [{"a": x, "b": y, "why": w} for x, y, w in DECLARED],
         "proposed": new, "rules_refound_declared": len(found)}, indent=1))


if __name__ == "__main__":
    main()
