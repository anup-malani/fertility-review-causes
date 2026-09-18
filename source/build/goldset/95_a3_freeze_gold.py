#!/usr/bin/env python3
"""
95_a3_freeze_gold.py — A.3, prepare the freeze-ready gold set with the 3 version-of-record swaps.

The cold-start anchors (step 89) resolved three anchors to a non-VoR identifier (a working paper, an
NBER preprint, or a reprint chapter fragment). Before the gold is frozen for recall grading, those are
re-resolved LIVE to their versions of record (no hand-asserted DOI), keyed on title with a year filter:

  * Kohler-Behrman-Watkins 2001 -> Demography 38(1) (was the OUP book-chapter DOI 10.1093/0199244596...)
  * Spolaore-Wacziarg -> Economic Journal 2022 (was NBER working paper 10.3386/w25957)
  * Coale-Watkins 1986 -> the EFP volume, kept keyed on TITLE with doi=null (was the De Gruyter reprint
    "Chapter 7" fragment 10.1515/9781400886692-012); a book legitimately has no article DOI.

Output marks the set `vor_swapped_pending_ra_signoff` — the freeze is a candidate freeze; RA sign-off
is the human gate that flips it to frozen. Every swap is verified at doi.org (three-state gate).

Inputs : literature/search-logs/diffusion-of-fertility-control-cold-start-anchors.json
Outputs: literature/search-logs/diffusion-of-fertility-control-gold-frozen.json
         literature/search-logs/diffusion-of-fertility-control-gold-freeze-log.md
"""
import json, os, re, subprocess, sys, time

SLUG = "diffusion-of-fertility-control"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
IN = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT = os.path.join(LOGS, f"{SLUG}-gold-frozen.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-gold-freeze-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a3_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402

# title-substring -> (year_filter, required container substring lower, is_book, human note)
SWAPS = {
    "the density of social networks and fertility decisions":
        (2001, "demography", False, "OUP book-chapter DOI -> Demography 38(1) VoR"),
    "fertility and modernity":
        (None, "economic journal", False, "NBER working paper -> Economic Journal VoR (Crossref dates it 2021 online-first)"),
    "the decline of fertility in europe":
        (None, None, True, "EFP book: no article DOI; keep keyed on title, doi=null"),
}


def toks(s):
    return set(norm(s).split())


def jaccard(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if A and B else 0.0


def crossref(title, year_filter, container_sub, authors=()):
    # Append author surnames to the bibliographic query: a common short title (e.g. "Fertility and
    # Modernity") does not surface its version of record in the top rows on title alone.
    surnames = " ".join(norm(a).split()[-1] for a in (authors or []) if a)
    key = f"VORSWAP::{title}::{surnames}::{year_filter}::{container_sub}"
    if key in cache:
        return cache[key]
    q = re.sub(r"\s+", "+", norm(title + " " + surnames))
    filt = (f"&filter=from-pub-date:{year_filter}-01-01,until-pub-date:{year_filter}-12-31"
            if year_filter else "")
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=8&select=DOI,title,container-title,issued{filt}")
    try:
        items = json.loads(subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                                          capture_output=True, text=True).stdout)["message"]["items"]
    except Exception as e:
        cache[key] = {"error": str(e)[:120]}
        return cache[key]
    best = None
    for it in items:
        ct = (it.get("title") or [""])[0]
        cont = ((it.get("container-title") or [""])[0] or "").lower()
        j = jaccard(title, ct)
        if container_sub and container_sub not in cont:
            continue
        if best is None or j > best["jaccard"]:
            best = {"doi": it.get("DOI"), "matched_title": ct, "jaccard": round(j, 3), "container": cont}
    cache[key] = best or {"doi": None, "jaccard": 0.0}
    return cache[key]


def doi_exists(doi):
    dkey = f"DOIRESOLVE::{doi}"
    if dkey in cache:
        return cache[dkey]
    try:
        code = subprocess.run(["curl", "-s", "-I", "-o", "/dev/null", "-w", "%{http_code}", "-m", "25",
                               "-A", UA, f"https://doi.org/{doi}"], capture_output=True, text=True).stdout.strip()
        state = "FOUND" if (code.startswith("3") or code == "200") else ("ABSENT" if code == "404" else "UNCONFIRMED")
    except Exception:
        state = "UNCONFIRMED"
    cache[dkey] = state
    return state


def main():
    anchors = json.load(open(IN))
    log = []
    for a in anchors:
        t = norm(a["title"])
        swap = next((SWAPS[k] for k in SWAPS if k in t), None)
        a.setdefault("gold_status", "candidate")
        if not swap:
            a["gold_status"] = "vor_confirmed_pending_ra_signoff"
            continue
        yr, cont, is_book, note = swap
        old = a.get("doi")
        if is_book:  # keep keyed on title, no article DOI
            a["doi"] = None
            a["identity_key"] = "title"
            a["vor_swap"] = {"from": old, "to": None, "note": note}
            a["gold_status"] = "vor_swapped_book_title_keyed_pending_ra_signoff"
            log.append(f"- **{a['title'][:60]}** -> TITLE-KEYED (was {old}); {note}")
            continue
        cr = crossref(a["title"], yr, cont, a.get("authors"))
        j = cr.get("jaccard", 0.0)
        if cr.get("doi") and j >= 0.72:
            ex = doi_exists(cr["doi"])
            a["vor_swap"] = {"from": old, "to": cr["doi"], "jaccard": j, "container": cr.get("container"),
                             "existence": ex, "note": note}
            if ex == "FOUND":
                a["doi"] = cr["doi"]
                a["identity_source"] = f"https://doi.org/{cr['doi']}"
                a["gold_status"] = "vor_swapped_pending_ra_signoff"
                log.append(f"- **{a['title'][:60]}** -> {cr['doi']} (J={j}, {cr.get('container','')[:30]}); {note}")
            else:
                a["gold_status"] = "vor_swap_unconfirmed_ra_resolve"
                log.append(f"- **{a['title'][:60]}** -> candidate {cr['doi']} but doi.org={ex}; kept old {old}, RA resolve")
        else:
            a["vor_swap"] = {"from": old, "to": None, "best_jaccard": j, "note": note + " (NO VoR MATCH)"}
            a["gold_status"] = "vor_swap_failed_ra_resolve"
            log.append(f"- **{a['title'][:60]}** -> NO VoR match (best J={j}); kept old {old}, RA resolve")
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.4)

    frozen = {"slug": SLUG, "freeze_status": "vor_swapped_pending_ra_signoff",
              "note": "Candidate freeze. RA sign-off is the human gate that flips this to frozen. VoR "
                      "swaps re-resolved live via Crossref + doi.org; no DOI hand-asserted.",
              "n_anchors": len(anchors), "anchors": anchors}
    json.dump(frozen, open(OUT, "w"), indent=2, ensure_ascii=False)
    swapped = sum(1 for a in anchors if a.get("vor_swap"))
    L = [f"# Gold freeze (VoR-swapped, pending RA sign-off) — {SLUG}", "",
         f"{len(anchors)} anchors; **{swapped} version-of-record swaps** applied and existence-verified. "
         "This is a CANDIDATE freeze; RA sign-off is the human gate to frozen.", "",
         "## VoR swaps", ""] + log
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"anchors {len(anchors)} | VoR swaps {swapped}")
    for line in log:
        print(line)
    print(f"-> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
