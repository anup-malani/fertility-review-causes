#!/usr/bin/env python3
"""
171_a24_named_recheck.py — A.24, re-resolution of the recon probe's named-work zeros.

170_'s pass-2 returned ZERO for all fifteen alternate wordings, and pass-1 returned zero for four
works that are known to exist (Finkel et al.'s Psychological Science in the Public Interest review is
cited in four figures). A zero that dense is a property of the QUERY, not of the literature, and the
standing rule in this repo is that a refused or malformed request must never be recorded as an
absence. This script establishes which it is before anything reaches the scope document.

Two changes from 170_:
  * queries go through `search=` (relevance search over title, abstract and fulltext metadata)
    instead of `filter=title.search:`. `title.search` matches the TITLE FIELD only, so any query
    carrying an author surname is unsatisfiable by construction — which is exactly the shape of all
    fifteen pass-2 queries. If that is the explanation, `search=` recovers them.
  * the abstract is reconstructed from OpenAlex's inverted index and the opening sentences printed,
    because for the four studies that carry this chapter's identification the SIGN of the estimate is
    the thing the scope needs and a title does not carry it.

Output: literature/search-logs/dating-apps-union-formation-friction-named-recheck.md
"""
import json, os, subprocess, sys, time

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-named-recheck.md")
ERROR_ABORT_SHARE = 0.20


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = openalex_key()

# (label, search terms). Group 1 re-runs 170_'s zeros. Group 2 is the identification set whose SIGN
# the scope needs: each of these is a candidate for the only estimated link this chapter can reach.
ZEROS = [
    ("v5 seminal — Rosenfeld & Thomas searching for a mate", "Rosenfeld Thomas searching for a mate internet social intermediary"),
    ("Finkel et al. — online dating critical analysis", "Finkel Eastwick Karney Reis Sprecher online dating critical analysis psychological science"),
    ("Cacioppo — marital satisfaction by meeting venue", "Cacioppo marital satisfaction break-ups online offline meeting venues"),
    ("Ortega & Hergovich — strength of absent ties", "Ortega Hergovich strength of absent ties online dating"),
    ("Hitsch Hortacsu Ariely — matching and sorting", "Hitsch Hortacsu Ariely matching and sorting in online dating"),
    ("Tyson et al. — first look at Tinder", "Tyson Perta Haddadi Seto first look at user activity on Tinder"),
    ("Bruch & Newman — aspirational pursuit", "Bruch Newman aspirational pursuit of mates online dating markets"),
]

IDENT = [
    ("Internet diffusion and marriage rates — the broadband IV", "impact of Internet diffusion on marriage rates evidence from the broadband market"),
    ("Mobile app adoption in online dating — Love Unshackled", "Love Unshackled identifying the effect of mobile app adoption in online dating"),
    ("Cellular data and fertility", "the effect of cellular data on fertility"),
    ("High speed internet and reproductive behaviour in Russia", "impact of high speed internet on reproductive behavior in Russia"),
    ("Broadband and fertility — any identified estimate", "broadband internet rollout fertility birth rates causal effect"),
    ("Rejection mind-set — choice overload in online dating", "rejection mind-set choice overload in online dating"),
    ("Choice overload and reversibility — plenty of fish", "plenty of fish in the sea choice overload reversibility online dating"),
    ("Tinder use and romantic relationship formation", "Tinder use and romantic relationship formations large-scale longitudinal"),
    ("Demography of swiping right", "demography of swiping right couples who met through dating apps Switzerland"),
    ("Marriage choice and couplehood in the age of the internet", "marriage choice and couplehood in the age of the internet"),
]

errors, rows = [], []


def oa(url):
    try:
        r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if r.returncode != 0:
            return {"__err": f"curl exit {r.returncode}"}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__err": str(e)[:140]}


def abstract_of(w, n_chars=520):
    """Reconstruct the abstract from OpenAlex's inverted index. Returns '' when absent."""
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = {}
    for term, idxs in inv.items():
        for i in idxs:
            pos[i] = term
    if not pos:
        return ""
    txt = " ".join(pos[i] for i in sorted(pos))
    return txt[:n_chars].replace("|", "/")


def search(terms, per_page=3):
    url = ("https://api.openalex.org/works?search=" + terms.replace(" ", "%20") +
           f"&per-page={per_page}&select=id,doi,display_name,publication_year,cited_by_count,type,"
           f"primary_location,authorships,abstract_inverted_index&api_key={KEY}")
    return oa(url)


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    n_req = 0
    for group, items in (("Re-resolution of 170_'s zeros", ZEROS),
                         ("Identification set — sign and design", IDENT)):
        for label, terms in items:
            n_req += 1
            d = search(terms)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                res = []
                for w in d["results"]:
                    auths = [a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])][:4]
                    loc = (w.get("primary_location") or {}).get("source") or {}
                    res.append(dict(title=w.get("display_name") or "", year=w.get("publication_year"),
                                    cites=w.get("cited_by_count"), type=w.get("type"),
                                    venue=loc.get("display_name") or "",
                                    doi=(w.get("doi") or "").replace("https://doi.org/", ""),
                                    auths="; ".join(a for a in auths if a),
                                    abstract=abstract_of(w)))
                rows.append((group, label, terms, d["meta"]["count"], res))
            time.sleep(0.2)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        sys.stderr.write(f"ABORT: {len(errors)}/{n_req} failed ({share:.0%}); not writing.\n")
        sys.exit(1)

    L = [f"# Named-work re-check — {SLUG}\n",
         "**Hypothesis:** A.24 · **Ticket:** TICK-071\n",
         "**Generated by:** `source/build/goldset/171_a24_named_recheck.py`\n",
         f"**Requests:** {n_req} · **Failed:** {len(errors)} ({share:.1%})\n",
         "\nQueries go through `search=` rather than `filter=title.search:`. Any zero below is "
         "therefore a zero against title, abstract and indexed metadata together, not against the "
         "title field alone.\n"]
    for group in ("Re-resolution of 170_'s zeros", "Identification set — sign and design"):
        L.append(f"\n## {group}\n")
        for g, label, terms, count, res in rows:
            if g != group:
                continue
            L.append(f"\n### {label} — **n = {count:,}**\n")
            L.append(f"`search={terms}`\n\n")
            if not res:
                L.append("*(no records)*\n")
                continue
            for r in res:
                L.append(f"- **{r['title'][:110]}** ({r['year']}, {r['cites']:,} cites, {r['type']}) — "
                         f"{r['auths'][:80]} · *{r['venue'][:45]}* · `{r['doi']}`\n")
                if r["abstract"]:
                    L.append(f"  > {r['abstract']}\n")
    if errors:
        L.append("\n## Failed requests\n\n")
        for lbl, e in errors:
            L.append(f"- `{lbl}` — {e}\n")
    open(OUT_MD, "w").write("".join(L))
    print(f"wrote {OUT_MD} ({n_req} requests, {len(errors)} failed)")


if __name__ == "__main__":
    main()
