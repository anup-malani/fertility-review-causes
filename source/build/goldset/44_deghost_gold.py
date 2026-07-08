#!/usr/bin/env python3
"""
44_deghost_gold.py — existence-verify the frozen gold's no-DOI anchors; quarantine ghosts.

The live pull (43) exposed that the frozen Tier-B recall denominator is contaminated with
ghost citations (hallucinated snowball titles; 35/36 probed PRIMARY no-DOI anchors return
OpenAlex count=0). This resolves every no-DOI anchor against BOTH OpenAlex and Crossref and
quarantines an anchor as a ghost ONLY IF BOTH return no confident match (the "confirmed-absent"
rule — conservative; keeps anything that resolves anywhere).

Match rule (§5 title-matching machinery, lightweight form): normalize titles, require token
Jaccard >= 0.72 on the content tokens, with an author-surname OR year gate when metadata is
present (a title match alone suffices if no author/year is available on the anchor). A DOI-
bearing anchor is kept as-is (already real).

Resolvable no-DOI anchor -> keep, backfilled with the found DOI + source.
Confirmed-absent      -> quarantine (recorded, never silently dropped — the ghost rate is a finding).

Outputs (non-destructive; the pre-deghost frozen files stay in git history):
  {slug}-tier-b-deghosted.json            surviving real Tier-B anchors (DOI-backfilled)
  estimand_tierb_tags_deghosted.json      tags trimmed to survivors
  {slug}-gold-ghost-quarantine.json       quarantined ghosts w/ evidence (for RA sign-off)
  {slug}-deghost-log.md                    counts by cell, ghost rate
  cache/deghost/*.json                     per-anchor API cache (resumable)
"""
import json, re, sys, time, subprocess
from pathlib import Path
from urllib.parse import quote
from collections import Counter

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = HERE / "cache" / "deghost"
CACHE.mkdir(parents=True, exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
JACCARD = 0.72

STOP = {"the","and","of","on","in","a","an","from","for","to","its","by","is","with","as","at",
        "or","be","this","that","new","evidence","case","study","effect","effects","impact"}
def nt(t): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9\s]"," ",(t or "").lower())).strip()
def toks(t): return set(nt(t).split()) - STOP
def jac(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if (A or B) else 0.0

class BudgetExhausted(Exception):
    """Raised when OpenAlex returns 429/insufficient-budget. Caller halts-and-resumes;
    an anchor is NEVER quarantined on this — 'could not confirm' != 'confirmed absent'.
    (This is the exact conflation that let ghosts in; the verifier must not repeat it.)"""

def curl_json(url, tries=4):
    """Returns (data, status). status in {'ok','ratelimit','fail'}. A 429/budget response
    is 'ratelimit' (NOT an empty result) so the caller can distinguish absence from outage."""
    for i in range(tries):
        r = subprocess.run(["curl","-s","-m","30","-A",f"oas-deghost/1.0 (mailto:{MAILTO})",url],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                d = json.loads(r.stdout)
            except json.JSONDecodeError:
                time.sleep(1.5 * (i + 1)); continue
            err = (d.get("error") or "") if isinstance(d, dict) else ""
            msg = (d.get("message") or "") if isinstance(d, dict) else ""
            if "rate limit" in str(err).lower() or "budget" in str(msg).lower():
                return None, "ratelimit"
            return d, "ok"
        time.sleep(1.5 * (i + 1))
    return None, "fail"

def surname_ok(anchor_authors, cand_authors):
    """True if any anchor surname appears among candidate authors, or if we can't tell."""
    if not anchor_authors: return True
    a_surn = {w for w in re.split(r"[;,\s]+", (anchor_authors or "").lower()) if len(w) > 2}
    c = (cand_authors or "").lower()
    return any(s in c for s in a_surn) if a_surn else True

def year_ok(anchor_year, cand_year):
    if not anchor_year or not cand_year: return True
    try: return abs(int(anchor_year) - int(cand_year)) <= 3
    except (TypeError, ValueError): return True

def _cached_ok(ck):
    """Return cached data only if it is a real 'ok' payload — never a stale 429/error."""
    if not ck.exists():
        return None
    try:
        d = json.load(open(ck))
    except json.JSONDecodeError:
        return None
    if isinstance(d, dict) and (str(d.get("error","")).lower().find("rate limit") >= 0
                                or "budget" in str(d.get("message","")).lower()):
        return None            # poisoned cache entry — ignore, force refetch
    return d

def probe_openalex(title, authors, year):
    """Returns ('FOUND', hit) | ('ABSENT', None) | ('UNCONFIRMED', None); raises BudgetExhausted on 429."""
    ck = CACHE / f"oa_{abs(hash(title)) % (10**12)}.json"
    d = _cached_ok(ck)
    if d is None:
        d, status = curl_json(
            f"https://api.openalex.org/works?filter=title.search:{quote(title, safe='')}"
            f"&select=id,doi,title,publication_year,authorships&per-page=5&mailto={MAILTO}")
        if status == "ratelimit":
            raise BudgetExhausted("openalex")
        if status != "ok":
            return ("UNCONFIRMED", None)
        json.dump(d, open(ck, "w")); time.sleep(0.3)
    for r in d.get("results", []):
        cand_auth = "; ".join(a.get("author", {}).get("display_name","") for a in (r.get("authorships") or []))
        if jac(title, r.get("title")) >= JACCARD and surname_ok(authors, cand_auth) and year_ok(year, r.get("publication_year")):
            doi = (r.get("doi") or "").lower().replace("https://doi.org/","") or None
            return ("FOUND", {"source": "openalex", "doi": doi, "matched_title": r.get("title"), "year": r.get("publication_year")})
    return ("ABSENT", None)     # a real 200 response with no matching result = confirmed absent

def probe_crossref(title, authors, year):
    """Returns ('FOUND', hit) | ('ABSENT', None) | ('UNCONFIRMED', None)."""
    ck = CACHE / f"cr_{abs(hash(title)) % (10**12)}.json"
    d = _cached_ok(ck)
    if d is None:
        d, status = curl_json(f"https://api.crossref.org/works?query.bibliographic={quote(title, safe='')}&rows=5&mailto={MAILTO}")
        if status != "ok":
            return ("UNCONFIRMED", None)
        json.dump(d, open(ck, "w")); time.sleep(0.3)
    for r in ((d or {}).get("message") or {}).get("items") or []:
        ct = (r.get("title") or [""])[0]
        cy = (((r.get("issued") or {}).get("date-parts") or [[None]])[0] or [None])[0]
        cauth = "; ".join(f"{a.get('family','')}" for a in (r.get("author") or []))
        if jac(title, ct) >= JACCARD and surname_ok(authors, cauth) and year_ok(year, cy):
            return ("FOUND", {"source": "crossref", "doi": (r.get("DOI") or "").lower() or None, "matched_title": ct, "year": cy})
    return ("ABSENT", None)

def main():
    B = json.load(open(LOGS / f"{SLUG}-tier-b-frozen.json"))
    tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_frozen.json"))}
    cell = lambda pid: tags.get(pid, {}).get("cell", "?")
    def cellk(pid):
        c = cell(pid); return "PRIMARY" if c == "PRIMARY" else "THEORY" if c == "THEORY" else "OFF"

    survivors, ghosts, unverified = [], [], []
    n_hasdoi = n_resolved = 0
    checked = 0
    total_nodoi = sum(1 for g in B if not (g.get("doi") or "").strip())
    try:
        for g in B:
            doi = (g.get("doi") or "").lower().replace("https://doi.org/","").strip() or None
            if doi:
                g["_deghost"] = "had_doi"; survivors.append(g); n_hasdoi += 1; continue
            checked += 1
            cr_status = None
            title, auth, yr = g.get("title"), g.get("authors"), g.get("year")
            oa_status, oa_hit = probe_openalex(title, auth, yr)      # may raise BudgetExhausted
            if oa_status == "FOUND":
                hit = oa_hit
            else:
                cr_status, cr_hit = probe_crossref(title, auth, yr)
                hit = cr_hit if cr_status == "FOUND" else None
            if hit:
                g2 = dict(g); g2["doi"] = hit["doi"]; g2["_deghost"] = f"resolved:{hit['source']}"
                g2["_resolved_from"] = hit; survivors.append(g2); n_resolved += 1
            elif oa_status == "ABSENT" and cr_status == "ABSENT":
                # confirmed absent by BOTH real 200-responses — a genuine ghost
                ghosts.append({"paperId": g.get("paperId"), "title": title, "authors": auth,
                               "year": yr, "cell": cell(g.get("paperId")),
                               "reason": "confirmed-absent: OpenAlex AND Crossref both returned no match >= %.2f jaccard" % JACCARD})
            else:
                # at least one API could not confirm — NEVER quarantine on this; retry next run
                unverified.append({"paperId": g.get("paperId"), "title": title,
                                   "oa": oa_status, "cr": cr_status})
            if checked % 20 == 0:
                print(f"  checked {checked}/{total_nodoi}; {len(ghosts)} ghosts, {len(unverified)} unverified", file=sys.stderr)
    except BudgetExhausted as e:
        print(f"\nBUDGET EXHAUSTED ({e}) after {checked} anchors — HALT-AND-RESUME. "
              f"Re-run after the OpenAlex daily reset (midnight UTC); completed probes are cached. "
              f"NOTHING quarantined on the outage.", file=sys.stderr)
        sys.exit(3)

    if unverified:
        print(f"\n⚠️  {len(unverified)} anchors UNVERIFIED (API could not confirm) — NOT quarantined. "
              f"Re-run after the reset to resolve them before trusting the counts.", file=sys.stderr)
        json.dump(unverified, open(LOGS / f"{SLUG}-deghost-unverified.json", "w"), indent=2, ensure_ascii=False)

    surv_ids = {g["paperId"] for g in survivors}
    surv_tags = [t for t in tags.values() if t["id"] in surv_ids]

    json.dump(survivors, open(LOGS / f"{SLUG}-tier-b-deghosted.json", "w"), indent=2, ensure_ascii=False)
    json.dump(surv_tags, open(HERE / "estimand_tierb_tags_deghosted.json", "w"), indent=2, ensure_ascii=False)
    json.dump(ghosts, open(LOGS / f"{SLUG}-gold-ghost-quarantine.json", "w"), indent=2, ensure_ascii=False)

    # stats by cell
    before = Counter(cellk(g.get("paperId")) for g in B)
    after = Counter(cellk(g["paperId"]) for g in survivors)
    ghost_by = Counter("PRIMARY" if x["cell"]=="PRIMARY" else "THEORY" if x["cell"]=="THEORY" else "OFF" for x in ghosts)

    L = [f"# De-ghosting the frozen gold — {SLUG}", "",
         "Existence-verify every no-DOI Tier-B anchor against **both** OpenAlex and Crossref; quarantine "
         "as ghost only if **both** return no confident title match (Jaccard ≥ %.2f + author/year gate) — "
         "the conservative 'confirmed-absent' rule. DOI-bearing anchors are kept as real." % JACCARD, "",
         f"- Tier B before: **{len(B)}**  ({n_hasdoi} had DOIs, {total_nodoi} no-DOI to verify)",
         f"- no-DOI anchors **resolved** (real, DOI backfilled): **{n_resolved}**",
         f"- no-DOI anchors **quarantined as ghosts**: **{len(ghosts)}**",
         f"- Tier B after de-ghosting: **{len(survivors)}**", "",
         "## By estimand cell (before → after; ghosts removed)", "",
         "| Cell | before | ghosts quarantined | after |", "|---|---|---|---|"]
    for k in ["PRIMARY","THEORY","OFF"]:
        L.append(f"| {k} | {before[k]} | {ghost_by[k]} | {after[k]} |")
    L += ["",
          f"**PRIMARY-cell ghost rate: {ghost_by['PRIMARY']}/{before['PRIMARY']} "
          f"({ghost_by['PRIMARY']/max(before['PRIMARY'],1):.0%})** — the snowball's forward-citation "
          "hallucination, concentrated in the primary pooling cell. The quarantine list "
          f"(`{SLUG}-gold-ghost-quarantine.json`) is for RA sign-off; nothing is silently dropped.", "",
          "*Next: re-freeze on the survivors and re-run the recall re-grade (45) against the de-ghosted "
          "denominator vs the pre-registered 0.80 bar — the honest number.*"]
    (LOGS / f"{SLUG}-deghost-log.md").write_text("\n".join(L) + "\n")

    print(f"\nTier B {len(B)} -> {len(survivors)} ({n_resolved} resolved, {len(ghosts)} ghosts)", file=sys.stderr)
    print(f"PRIMARY {before['PRIMARY']} -> {after['PRIMARY']} (ghosts {ghost_by['PRIMARY']})", file=sys.stderr)
    print(f"-> tier-b-deghosted.json, tags-deghosted, ghost-quarantine.json, deghost-log.md", file=sys.stderr)

if __name__ == "__main__":
    main()
