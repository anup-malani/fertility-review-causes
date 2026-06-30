#!/usr/bin/env python3
"""
Part 1c — canon/theory + anchor related-work seed for Tier A, with authoritative DOI
resolution. Per method spec §3: Tier A = on-disk empirical core + canon + anchor related-work,
stratified (theory / NE-setting / era). This file enumerates the canon (the scholarly judgment
call) and resolves each DOI via Crossref.

CRITICAL: the DOIs hard-coded below are RECALLED HINTS ONLY (untrusted — recalled DOIs are
exactly what the corpus got wrong). Every entry is verified by Crossref title-match (J>=0.60,
classics have distinctive titles) AND |yearD|<=3; a failing hint falls back to bibliographic
search (search auto-accept needs J>=0.80). Books / pre-DOI chapters with no DOI are TITLE-KEYED.

Output: canon_resolved.json + stderr summary. NOT frozen into the gold set until RA sign-off.
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent; CACHE=HERE/"cache"; CACHE.mkdir(exist_ok=True)
LOG=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
CANON_OUT=LOG/"old-age-security-pension-crowdout-canon-resolved.json"
MAILTO="shravanh@uchicago.edu"; DOI_GUARD=0.60; SEARCH_GUARD=0.80
STOP={"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence","a"}
def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def curl(url,tag):
    cf=CACHE/f"{tag}_{hashlib.sha1(url.encode()).hexdigest()[:16]}.json"
    if cf.exists(): return json.load(open(cf))
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                      "-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n"); data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data,open(cf,"w")); time.sleep(1.0)
    return data
def meta(m):
    crt=(m.get("title") or [""])[0]
    cry=(m.get("issued",{}).get("date-parts",[[None]])[0][0]) or (m.get("published",{}).get("date-parts",[[None]])[0][0])
    return crt,cry,(m.get("DOI") or "").lower(),(m.get("container-title") or [""])[0]

# (title, authors, year, stratum, candidate_doi_hint or None, is_book/no_doi)
CANON=[
 # --- THEORY: foundational OAS hypothesis -------------------------------------------------
 ("Economic Backwardness and Economic Growth","Leibenstein",1957,"theory-foundational",None,True),
 ("Peasants, Procreation, and Pensions","Neher",1971,"theory-foundational",None,True),  # AER 1971: pre-DOI, not in Crossref -> title-key
 ("The Old Age Security Hypothesis and Population Growth","Willis",1980,"theory-foundational",None,True),
 ("The Old-Age Security Motive for Fertility","Nugent",1985,"theory-foundational","10.2307/1973379",False),
 ("Toward a Restatement of Demographic Transition Theory","Caldwell",1976,"theory-foundational","10.2307/1971615",False),
 # --- THEORY: formal PAYG / endogenous-fertility models -----------------------------------
 ("A Reformulation of the Economic Theory of Fertility","Becker; Barro",1988,"theory-formal","10.2307/1882640",False),
 ("Fertility Choice in a Model of Economic Growth","Barro; Becker",1989,"theory-formal","10.2307/1912563",False),
 ("Intergenerational Trade, Longevity, and Economic Growth","Ehrlich; Lui",1991,"theory-formal","10.1086/261788",False),
 ("Pay-as-you-go public pensions with endogenous fertility","Nishimura; Zhang",1992,"theory-formal","10.1016/0047-2727(92)90029-F",False),
 ("Intergenerational transfers without altruism: Family, market and state","Cigno",1993,"theory-formal","10.1016/0176-2680(93)90036-T",False),
 ("Pay-as-you-go financed public pensions in a model of endogenous growth and fertility","Wigger",1999,"theory-formal","10.1007/s001480050116",False),
 ("Mortality, Fertility, and Saving in a Malthusian Economy","Boldrin; Jones",2002,"theory-formal","10.1006/redy.2002.0186",False),
 ("The pay-as-you-go pension system as fertility insurance and an enforcement device","Sinn",2004,"theory-formal","10.1016/S0047-2727(03)00015-X",False),
 ("Fertility and Social Security","Boldrin; De Nardi; Jones",2015,"theory-formal","10.1017/dem.2015.4",False),
 ("Children and Pensions","Cigno; Werding",2007,"theory-formal",None,True),
 # --- THEORY/EMPIRICAL classic tests (children-as-insurance, early cross-national) ---------
 ("Risk and Insurance: Perspectives on Fertility and Agrarian Change in India and Bangladesh","Cain",1981,"empirical-classic","10.2307/1972894",False),
 ("Fertility as an Adjustment to Risk","Cain",1983,"empirical-classic","10.2307/1973326",False),
 ("Social Security and Fertility: An International Perspective","Hohm",1975,"empirical-classic","10.2307/2060719",False),
 ("Fertility and Pension Programs in LDCs: A Model of Mutual Reinforcement","Entwisle; Winegarden",1984,"empirical-classic","10.1086/451530",False),
 ("Old Age Pensions and Fertility in Rural Areas of Less Developed Countries: Some Evidence from Mexico","Nugent; Gillaspy",1983,"empirical-classic","10.1086/451353",False),
 ("The effects of financial markets and social security on saving and fertility behaviour in Italy","Cigno; Rosati",1992,"empirical-classic","10.1007/BF00163065",False),
 ("Jointly determined saving and fertility behaviour: Theory, and estimates for Germany, Italy, UK and USA","Cigno; Rosati",1996,"empirical-classic","10.1016/0014-2921(95)00035-6",False),
 # === Part 1c canon EXPANSION (2026-06-29, Shravan approved both inclusion calls) ===
 # --- THEORY: social-security <-> endogenous-fertility models (deep literature) ---
 ("An Economic Analysis of Fertility","Becker",1960,"theory-foundational",None,True),  # NBER/Columbia UP chapter
 ("The old age security hypothesis and optimal population growth","Bental",1989,"theory-formal","10.1007/BF00522411",False),
 ("Endogenous fertility and optimal population size","Eckstein; Wolpin",1985,"theory-formal","10.1016/0047-2727(85)90020-1",False),
 ("Endogenous fertility, altruistic behavior across generations, and social security systems","Prinz",1990,"theory-formal","10.1007/BF00163071",False),
 ("Social security and endogenous growth","Zhang",1995,"theory-formal","10.1016/0047-2727(94)01473-2",False),
 ("Social security in a non-altruistic model with uncertainty and endogenous fertility","Rosati",1996,"theory-formal","10.1016/0047-2727(95)01524-8",False),
 ("Social security and endogenous fertility: pensions and child allowances as siamese twins","van Groezen; Leers; Meijdam",2003,"theory-formal","10.1016/S0047-2727(01)00134-7",False),
 ("How does social security affect economic growth? Evidence from cross-country data","Zhang; Zhang",2004,"theory-formal","10.1007/s00148-004-0198-x",False),
 ("Pensions and fertility incentives","Fenge; Meier",2005,"theory-formal","10.1111/j.0008-4085.2005.00268.x",False),
 ("Social security and demographic trends: Theory and evidence from the international experience","Ehrlich; Kim",2007,"theory-formal","10.1016/j.red.2006.09.003",False),
 ("Are family allowances and fertility-related pensions perfect substitutes?","Fenge; Meier",2009,"theory-formal","10.1007/s10797-008-9079-7",False),
 ("Fertility, child care outside the home, and pay-as-you-go social security","Hirazawa; Yakita",2009,"theory-formal","10.1007/s00148-008-0214-7",False),
 ("Optimal social security in a dynastic model with human capital externalities, fertility and endogenous growth","Yew; Zhang",2009,"theory-formal","10.1016/j.jpubeco.2009.02.006",False),
 ("Pensions with endogenous and stochastic fertility","Cremer; Gahvari; Pestieau",2008,"theory-formal","10.1016/j.jpubeco.2008.07.001",False),
 # --- EMPIRICAL classic / cross-national OAS-motive tests ---
 ("An econometric analysis of the old-age security motive for childbearing","Jensen",1990,"empirical-classic","10.2307/2527025",False),
 ("An Old-Age Security Motive for Fertility in the United States?","Rendall; Bahchieva",1998,"empirical-classic","10.2307/2807975",False),
 ("Investing for the old age: pensions, children and savings","Galasso; Gatti; Profeta",2009,"empirical-classic","10.1007/s10797-009-9105-4",False),
 ("The Impact of Social Security on Saving and Fertility in Germany","Cigno; Casolaro; Rosati",2003,"empirical-classic","10.1628/0015221032500864",False),
]

def resolve(title,authors,year,stratum,hint,nodoi):
    rec={"title":title,"authors":authors,"year":year,"stratum":stratum,"candidate_hint":hint}
    if nodoi:
        rec.update(verdict="TITLE_KEY",final_doi=None,reason="book/chapter, no DOI"); return rec
    # 1) verify recalled hint
    if hint:
        d=curl(f"https://api.crossref.org/works/{urllib.parse.quote(hint.lower())}?mailto={MAILTO}","verifydoi")
        if d.get("_http")=="200":
            crt,cry,rdoi,ven=meta(d.get("message",{})); sim=jacc(title,crt)
            yr_ok=(cry is None or abs((cry or 0)-year)<=3)
            if sim>=DOI_GUARD and yr_ok:
                rec.update(verdict="VERIFIED",final_doi=rdoi,via="hint",jaccard=round(sim,3),
                           crossref_title=crt,crossref_year=cry,venue=ven); return rec
            rec["hint_failed"]=f"J={sim:.2f} yr {cry} -> {crt[:50]}"
        else:
            rec["hint_failed"]=f"crossref {d.get('_http')}"
    # 2) bibliographic search fallback
    q=urllib.parse.quote(title)
    url=f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(title+' '+authors)}&rows=5&mailto={MAILTO}"
    d=curl(url,"crsearch")
    best=None
    for it in d.get("message",{}).get("items",[]):
        crt,cry,rdoi,ven=meta(it); sim=jacc(title,crt)
        yr_ok=(cry is None or abs((cry or 0)-year)<=3)
        if sim>=SEARCH_GUARD and yr_ok and (best is None or sim>best["jaccard"]):
            best={"final_doi":rdoi,"jaccard":round(sim,3),"crossref_title":crt,"crossref_year":cry,"venue":ven}
    if best:
        rec.update(verdict="VERIFIED",via="search",**best)
    else:
        rec.update(verdict="NOT_FOUND",final_doi=None)
    return rec

# verifier false-negatives accepted manually (Crossref title differs from canonical title):
# Cigno 1993 -> Crossref dropped the subtitle "Family, market and state" so J=0.57<guard,
# but DOI is confirmed correct (European Journal of Political Economy 1993).
MANUAL={("Cigno",1993):{"final_doi":"10.1016/0176-2680(93)90036-t","via":"manual (verifier FN: subtitle dropped)",
                        "crossref_title":"Intergenerational transfers without altruism","crossref_year":1993,
                        "venue":"European Journal of Political Economy","jaccard":0.57}}
def main():
    out=[resolve(*c) for c in CANON]
    for r in out:
        key=(r["authors"],r["year"])
        if r["verdict"]=="NOT_FOUND" and key in MANUAL:
            r.update(verdict="VERIFIED",**MANUAL[key])
    json.dump(out,open(CANON_OUT,"w"),indent=2)
    c=Counter(r["verdict"] for r in out)
    print("=== canon resolution ===",file=sys.stderr)
    for k,v in c.most_common(): print(f"  {k}: {v}",file=sys.stderr)
    print(f"\nseed size: {len(out)} canon/theory/anchor",file=sys.stderr)
    for r in out:
        tag={"VERIFIED":"OK ","TITLE_KEY":"TK ","NOT_FOUND":"!! "}[r["verdict"]]
        d=r.get("final_doi") or "(title-key)" if r["verdict"]!="NOT_FOUND" else "*** UNRESOLVED ***"
        extra=f" J={r.get('jaccard')} via {r.get('via')}" if r["verdict"]=="VERIFIED" else (" "+r.get("hint_failed","") if r.get("hint_failed") else "")
        print(f"  {tag}[{r.get('stratum','')}] {r['authors']} {r['year']}: {d}{extra}",file=sys.stderr)
    print(f"\nwritten -> {CANON_OUT.name}",file=sys.stderr)
if __name__=="__main__":
    # attach stratum (kept out of resolve() signature for clarity)
    for c in CANON: pass
    main()
