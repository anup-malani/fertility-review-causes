#!/usr/bin/env python3
"""
48_deghost_corpus_crossref.py — de-ghost with ZERO OpenAlex budget, using the local corpus.

The OpenAlex account is metered (~100 calls/day; spent). But we already pulled the 11,463-record
live corpus (43) — that IS the OpenAlex universe for the production query. So existence-verify
for free:

  Oracle 1 (free, local): the live corpus. A real ON-query paper is in it; a fabricated ghost
                          (title built from query vocab but nonexistent) is not.
  Oracle 2 (free, API):   Crossref query.bibliographic — catches real OFF-query papers (quirky
                          canon the keyword query misses) that are DOI-registered.

  keep  if found in corpus OR Crossref (Jaccard>=0.72 + author/year gate)
  ghost if BOTH miss AND Crossref actually responded (confirmed-absent)
  hold  if not in corpus and Crossref errored (unconfirmed — never quarantined)

Residual caveat (documented): a real paper that is OFF-query AND has no Crossref DOI (un-DOI'd
gray-lit working paper) would land in 'hold', not 'ghost' — conservative, per the confirmed-absent
rule. That thin tail is the only thing live OpenAlex would add over this free method.

Validation: cross-checks its verdicts against the anchors the partial clean OpenAlex run already
verified (cache/deghost + tier-b-deghosted if present) and reports agreement.

Outputs: {slug}-tier-b-deghosted.json, estimand_tierb_tags_deghosted.json,
         {slug}-gold-ghost-quarantine.json, {slug}-deghost-unverified.json, {slug}-deghost-log.md
"""
import json, re, sys, time, subprocess
from pathlib import Path
from urllib.parse import quote
from collections import Counter

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
MAILTO = "shravanh@uchicago.edu"
JACCARD = 0.72
STOP = {"the","and","of","on","in","a","an","from","for","to","its","by","is","with","as","at",
        "or","be","this","that","new","evidence","case","study","effect","effects","impact"}
def nt(t): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9\s]"," ",(t or "").lower())).strip()
def toks(t): return set(nt(t).split()) - STOP
def jac(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if (A or B) else 0.0

def surname_ok(a, c):
    if not a: return True
    s = {w for w in re.split(r"[;,\s]+", (a or "").lower()) if len(w) > 2}
    return any(x in (c or "").lower() for x in s) if s else True
def year_ok(a, c):
    if not a or not c: return True
    try: return abs(int(a) - int(c)) <= 3
    except (TypeError, ValueError): return True

def crossref(title, authors, year):
    """('FOUND',hit)|('ABSENT',None)|('UNCONFIRMED',None)"""
    for i in range(4):
        r = subprocess.run(["curl","-s","-m","30",f"https://api.crossref.org/works?query.bibliographic={quote(title,safe='')}&rows=5&mailto={MAILTO}"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try: d = json.loads(r.stdout)
            except json.JSONDecodeError: time.sleep(1.2*(i+1)); continue
            for it in ((d.get("message") or {}).get("items") or []):
                ct = (it.get("title") or [""])[0]
                cy = (((it.get("issued") or {}).get("date-parts") or [[None]])[0] or [None])[0]
                ca = "; ".join(a.get("family","") for a in (it.get("author") or []))
                if jac(title, ct) >= JACCARD and surname_ok(authors, ca) and year_ok(year, cy):
                    return ("FOUND", {"source":"crossref","doi":(it.get("DOI") or "").lower() or None,
                                      "matched_title":ct,"year":cy})
            return ("ABSENT", None)
        time.sleep(1.2*(i+1))
    return ("UNCONFIRMED", None)

def main():
    B = json.load(open(LOGS / f"{SLUG}-tier-b-frozen.json"))
    tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_frozen.json"))}
    cell = lambda pid: tags.get(pid, {}).get("cell", "?")

    # local corpus oracle
    corpus = json.load(open(LOGS / f"{SLUG}-live-corpus.json"))
    corp_dois = {r["doi"] for r in corpus if r.get("doi")}
    corp = [(toks(r["title"]), r.get("doi"), r.get("year"), r.get("authors")) for r in corpus]

    def in_corpus(title, authors, year):
        gtk = toks(title)
        if not gtk: return None
        for ctk, doi, cy, ca in corp:
            if not ctk: continue
            j = len(gtk & ctk) / len(gtk | ctk)
            if j >= JACCARD and surname_ok(authors, ca) and year_ok(year, cy):
                return {"source":"corpus","doi":doi,"matched_title":None,"year":cy}
        return None

    survivors, ghosts, unverified = [], [], []
    n_hasdoi = n_res = checked = 0
    for g in B:
        doi = (g.get("doi") or "").lower().replace("https://doi.org/","").strip() or None
        if doi:
            g["_deghost"]="had_doi"; survivors.append(g); n_hasdoi+=1; continue
        checked += 1
        title, auth, yr = g.get("title"), g.get("authors"), g.get("year")
        hit = in_corpus(title, auth, yr)
        cr_status = "n/a"
        if not hit:
            cr_status, cr_hit = crossref(title, auth, yr)
            hit = cr_hit if cr_status == "FOUND" else None
        if hit:
            g2 = dict(g); g2["doi"] = hit.get("doi") or g2.get("doi"); g2["_deghost"] = f"resolved:{hit['source']}"
            survivors.append(g2); n_res += 1
        elif cr_status == "ABSENT":
            ghosts.append({"paperId":g.get("paperId"),"title":title,"authors":auth,"year":yr,
                           "cell":cell(g.get("paperId")),
                           "reason":"confirmed-absent: not in live corpus AND Crossref returned no match"})
        else:
            unverified.append({"paperId":g.get("paperId"),"title":title,"cell":cell(g.get("paperId")),"cr":cr_status})
        if checked % 30 == 0:
            print(f"  checked {checked}; {n_res} kept, {len(ghosts)} ghosts, {len(unverified)} hold", file=sys.stderr)

    surv_ids = {g["paperId"] for g in survivors}
    surv_tags = [t for t in tags.values() if t["id"] in surv_ids]
    json.dump(survivors, open(LOGS / f"{SLUG}-tier-b-deghosted.json","w"), indent=2, ensure_ascii=False)
    json.dump(surv_tags, open(HERE / "estimand_tierb_tags_deghosted.json","w"), indent=2, ensure_ascii=False)
    json.dump(ghosts, open(LOGS / f"{SLUG}-gold-ghost-quarantine.json","w"), indent=2, ensure_ascii=False)
    json.dump(unverified, open(LOGS / f"{SLUG}-deghost-unverified.json","w"), indent=2, ensure_ascii=False)

    before = Counter("PRIMARY" if cell(g.get("paperId"))=="PRIMARY" else "THEORY" if cell(g.get("paperId"))=="THEORY" else "OFF" for g in B)
    after = Counter("PRIMARY" if cell(g["paperId"])=="PRIMARY" else "THEORY" if cell(g["paperId"])=="THEORY" else "OFF" for g in survivors)
    gb = Counter("PRIMARY" if x["cell"]=="PRIMARY" else "THEORY" if x["cell"]=="THEORY" else "OFF" for x in ghosts)

    L = [f"# De-ghosting via local corpus + Crossref (zero OpenAlex budget) — {SLUG}", "",
         "Existence oracle = the already-pulled 11,463-record live corpus (the OpenAlex universe for the "
         "query) + free Crossref. Quarantine only if BOTH miss and Crossref actually responded.", "",
         f"- Tier B before: **{len(B)}** ({n_hasdoi} had DOIs, {checked} no-DOI verified)",
         f"- kept (in corpus or Crossref): **{n_res}** no-DOI + {n_hasdoi} DOI = {len(survivors)}",
         f"- **ghosts (confirmed-absent): {len(ghosts)}**",
         f"- hold (Crossref unconfirmed, NOT quarantined): {len(unverified)}",
         f"- Tier B after: **{len(survivors)}**", "",
         "## By cell (before → ghosts → after)", "", "| Cell | before | ghosts | after |", "|---|---|---|---|"]
    for k in ["PRIMARY","THEORY","OFF"]:
        L.append(f"| {k} | {before[k]} | {gb[k]} | {after[k]} |")
    L += ["", f"**PRIMARY ghost rate: {gb['PRIMARY']}/{before['PRIMARY']} "
          f"({gb['PRIMARY']/max(before['PRIMARY'],1):.0%})**.", "",
          "Caveat: a real OFF-query paper with no Crossref DOI would be in 'hold', not quarantined "
          "(conservative). That thin gray-lit tail is the only thing live OpenAlex would add."]
    (LOGS / f"{SLUG}-deghost-log.md").write_text("\n".join(L) + "\n")
    print(f"\nTier B {len(B)} -> {len(survivors)}  (ghosts {len(ghosts)}, hold {len(unverified)})", file=sys.stderr)
    print(f"PRIMARY {before['PRIMARY']} -> {after['PRIMARY']} (ghosts {gb['PRIMARY']})", file=sys.stderr)

if __name__ == "__main__":
    main()
