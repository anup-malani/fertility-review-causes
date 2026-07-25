#!/usr/bin/env python3
"""
80_d3b_production_query.py - D.3.b (climate anxiety / eco-doomerism), stage A6c.

Mirror of B.1's `70_b1_production_query.py`. Refit the 2-block production query on the FULL gold at
the CV-chosen breadth (Nf=3, Np=45; A6b showed the cause block binds and effect breadth saturates
after three terms), then answer the A6c fork WITH NUMBERS before any large universe pull:

  1. LOCAL recall (budget-free): match the compiled query against each gold paper's cached title, and
     against title+abstract. The gap is how much abstract matching rescues gold whose title alone does
     not carry both blocks (A6b's title-only CV ceiling was 64.6%). Reported overall, Recall(A) vs
     Recall(B), on the rare value-added core (DESIRE_INDEPENDENCE + PRIMARY_CARBON_ETHICS), and on
     REALIZED_FERTILITY outcomes.
  2. LIVE universe counts (cheap, one request each, per-page=1 so only meta.count is fetched):
     title.search vs title_and_abstract.search, so the title-versus-title-and-abstract choice is
     data-driven rather than assumed.

LEAKAGE WALL (binding, from A3): the PLOS Climate review's published search string does not appear
here in any form. Both blocks are a fixed a-priori backbone plus terms mined from our own screen.

Writes production-query.json regardless, so A6c-full can pull whichever operationalization we choose.

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json,
         literature/search-logs/{slug}-tier-b-frame.json (for gold abstracts)
Output : literature/search-logs/{slug}-production-query.json + {slug}-recall-probe.md
"""
import json, re, math, sys, subprocess
from pathlib import Path
from collections import Counter
from urllib.parse import quote

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
MAILTO = "shravanh@uchicago.edu"
NF, NP = 3, 45
ALPHA0 = 1000.0
MIN_GOLD_FOLD = 2
PRIMARY_EMPIRICAL = {"PRIMARY_HABITABILITY_FEAR", "PRIMARY_CARBON_ETHICS", "PRIMARY_ECO_PESSIMISM",
                     "DESIRE_INDEPENDENCE"}
RARE_CORE = {"DESIRE_INDEPENDENCE", "PRIMARY_CARBON_ETHICS"}
NON_EMPIRICAL_EVIDENCE = {"theory", "review"}

EFFECT_BACKBONE = ["fertility", "fertilit*", "birth*", "childbearing", "childbear*", "childless*",
                   "childfree", "child-free", "number of children", "offspring", "family size",
                   "reproductive", "reproduction", "reproducti*", "procreat*", "natality", "parity",
                   "have children", "having children", "fertility intention*",
                   "reproductive intention*", "childbearing intention*", "pregnancy intention*",
                   "remain childless", "voluntary childless*"]
CAUSE_BACKBONE = ["climate anxiety", "eco-anxiety", "eco anxiety", "climate distress", "climate worry",
                  "climate worries", "climate concern*", "climate grief", "climate emotion*",
                  "solastalgia", "eco-distress", "ecological grief",
                  "eco-doom*", "doomism", "eco-pessimis*", "climate pessimis*", "climate despair",
                  "climate dread", "climate doom", "apocalyp*", "collapse",
                  "carbon footprint", "carbon legacy", "antinatalis*", "anti-natalis*",
                  "environmental antinatalis*", "procreative ethic*", "population ethic*",
                  "overpopulation",
                  "habitabilit*", "bring a child into", "world to bring", "future for children",
                  "climate future", "planetary",
                  "climate change", "global warming", "climate crisis", "ecological crisis",
                  "environmental crisis"]

STOP = set("the a an of and in on for from to its by is with as at or be this that these those we our "
           "their his her it they i ii iii new evidence using based study studies analysis approach paper "
           "article effect effects impact role case among between within over under are was were has have "
           "had do does can could will would not no more less than into about across after before during "
           "toward towards via per vs versus also two three some how what why when where which who whom "
           "data model models results result human humans".split())
EFFECT = re.compile(r"fertil|childbear|childless|childfree|child-free|birth rate|birthrate|natalit|"
                    r"offspring|reproducti|number of children|family size|parity|procreat|babi|"
                    r"have children|having children|child rearing|childrearing|"
                    r"intention|intent to|desire for a child|remain childless|voluntary childless")
CAUSE = re.compile(
    r"\bclimate\b|\beco\b|anxiet|anxious|worri|\bworry\b|concern|emotion|feeling|"
    r"\bfear|afraid|distress|grief|guilt|hope\b|hopeless|"
    r"climate anxiet|eco-anxiet|eco anxiet|climate worr|climate concern|climate distress|"
    r"climate emotion|climate grief|solastalgia|environmental concern|environmental worr|"
    r"habitab|planetary|future for children|bring a child|uncertain future|climate future|"
    r"world to bring|liveab|livab|"
    r"carbon|footprint|emission|antinatal|anti-natal|overpopulat|population ethic|"
    r"procreat\w* ethic|environmental ethic|moral|ethic|"
    r"doom|apocalyp|collapse|catastroph|existential|pessimis|dread|despair|extinction|"
    r"end of the world|crisis|"
    r"reproductive decision|childbearing decision|decision-making|decision making|motivation|"
    r"attitude|willingness|"
    r"climate change|global warming|environment|ecolog|sustainab|green ")


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())).strip()


def utoks(t):
    return [w for w in norm(t).split() if len(w) > 2 and w not in STOP]


def cand_terms(t):
    u = utoks(t)
    return u + [f"{u[i]} {u[i+1]}" for i in range(len(u) - 1)]


def block_of(term):
    e, c = bool(EFFECT.search(term)), bool(CAUSE.search(term))
    return "effect" if (e and not c) else "cause" if (c and not e) else None


def compile_term(term):
    t = term.strip().lower()
    return ("prefix", norm(t[:-1])) if t.endswith("*") else ("phrase", norm(t))


def matches(ntext_padded, compiled):
    for kind, val in compiled:
        if not val:
            continue
        if kind == "prefix":
            if re.search(r"\b" + re.escape(val), ntext_padded):
                return True
        elif (" " + val + " ") in ntext_padded:
            return True
    return False


def mine(titles, nc, nn):
    gc = Counter()
    for t in titles:
        gc.update(cand_terms(t))
    ng = sum(gc.values())
    ncomb = ng + nn
    eff, cau = [], []
    for w in set(gc):
        if gc[w] < MIN_GOLD_FOLD:
            continue
        b = block_of(w)
        if b is None:
            continue
        aw = ALPHA0 * (gc[w] + nc.get(w, 0)) / ncomb
        delta = (math.log((gc[w] + aw) / (ng + ALPHA0 - gc[w] - aw))
                 - math.log((nc.get(w, 0) + aw) / (nn + ALPHA0 - nc.get(w, 0) - aw)))
        z = delta / math.sqrt(1.0 / (gc[w] + aw) + 1.0 / (nc.get(w, 0) + aw))
        (eff if b == "effect" else cau).append((w, round(z, 2)))
    eff.sort(key=lambda x: -x[1])
    cau.sort(key=lambda x: -x[1])
    return eff, cau


def curl_count(search_field, query):
    url = (f"https://api.openalex.org/works?filter={search_field}:{quote(query, safe='')}"
           f"&per-page=1&mailto={MAILTO}")
    r = subprocess.run(["curl", "-s", "-m", "40", "-A", f"d3b-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        return d.get("meta", {}).get("count")
    except Exception:
        return None


def clean_term(t):
    return re.sub(r"\s+", " ", t.strip().lower().rstrip("*").replace("-", " ")).strip()


def build_group(terms):
    seen, out = set(), []
    for t in terms:
        c = clean_term(t)
        if c and c not in seen:
            seen.add(c)
            out.append(f'"{c}"' if " " in c else c)
    return "(" + " OR ".join(out) + ")"


def main():
    rows = json.load(open(OUT / f"{SLUG}-screen-tiers.json"))
    seeds = json.load(open(LOGS / f"{SLUG}-tier-a.json"))
    frame_abs = {r["paperId"]: (r.get("abstract") or "")
                 for r in json.load(open(LOGS / f"{SLUG}-tier-b-frame.json"))}
    gold = [{"title": s["title"], "abstract": s.get("abstract") or "", "tier": "A",
             "cell": s.get("provisional_cell"), "outcome_level": None}
            for s in seeds if s.get("title")]
    for r in rows:
        if (r["verdict"] == "RELEVANT"
                and r.get("cell") in PRIMARY_EMPIRICAL
                and r.get("evidence_type") not in NON_EMPIRICAL_EVIDENCE
                and r.get("title")):
            gold.append({"title": r["title"], "abstract": frame_abs.get(r["paperId"], ""),
                         "tier": "B", "cell": r["cell"], "outcome_level": r.get("outcome_level")})
    neg = [r["title"] for r in rows if r["verdict"] == "NOT_RELEVANT" and r.get("title")]
    nc = Counter()
    for t in neg:
        nc.update(cand_terms(t))
    nn = sum(nc.values())

    eff_mined, cau_mined = mine([g["title"] for g in gold], nc, nn)
    eff_exp = [w for w, _ in eff_mined[:NF]]
    cau_exp = [w for w, _ in cau_mined[:NP]]
    pq = {"slug": SLUG, "breadth": {"Nf": NF, "Np": NP},
          "effect_block": {"backbone": EFFECT_BACKBONE, "mined_expansion": eff_exp},
          "cause_block": {"backbone": CAUSE_BACKBONE, "mined_expansion": cau_exp},
          "leakage_wall": "No term derives from the PLOS Climate review's published search string.",
          "gold_excludes_theory": sorted(NON_EMPIRICAL_EVIDENCE)}
    json.dump(pq, open(LOGS / f"{SLUG}-production-query.json", "w"), indent=2)

    eff_c = [compile_term(t) for t in EFFECT_BACKBONE + eff_exp]
    cau_c = [compile_term(t) for t in CAUSE_BACKBONE + cau_exp]

    n_with_abs = sum(1 for g in gold if g["abstract"])

    def recall(use_abstract):
        h = {"A": 0, "B": 0}
        t = {"A": 0, "B": 0}
        ch = ct = rh = rt = 0
        for g in gold:
            text = g["title"] + (" " + g["abstract"] if use_abstract else "")
            nt = " " + norm(text) + " "
            ok = matches(nt, eff_c) and matches(nt, cau_c)
            t[g["tier"]] += 1
            core = g["cell"] in RARE_CORE
            real = g.get("outcome_level") in ("REALIZED_FERTILITY", "BOTH")
            ct += core
            rt += real
            if ok:
                h[g["tier"]] += 1
                ch += core
                rh += real
        tot = t["A"] + t["B"]
        return {"overall": (h["A"] + h["B"]) / tot, "A": h["A"] / t["A"] if t["A"] else 0,
                "B": h["B"] / t["B"] if t["B"] else 0,
                "core": ch / ct if ct else 0, "core_hit": ch, "core_tot": ct,
                "real": rh / rt if rt else 0, "real_hit": rh, "real_tot": rt}

    r_title = recall(False)
    r_ta = recall(True)

    query = f"{build_group(EFFECT_BACKBONE + eff_exp)} AND {build_group(CAUSE_BACKBONE + cau_exp)}"
    n_title = curl_count("title.search", query)
    n_ta = curl_count("title_and_abstract.search", query)

    L = [f"# A6c production query + recall probe - {SLUG}", "",
         f"Production query refit on full gold at CV breadth Nf={NF}, Np={NP}. "
         "Local recall is budget-free (compiled query against gold's cached title, then "
         "title+abstract); universe counts are one cheap OpenAlex request each.", "",
         f"Gold = {len(gold)} empirical records ({sum(1 for g in gold if g['tier']=='A')} Tier-A seeds, "
         f"{sum(1 for g in gold if g['tier']=='B')} screen-relevant empirical). Theory is excluded by "
         "design and does not count toward recall. **Caveat on the abstract row:** only "
         f"{n_with_abs} of {len(gold)} gold records carry a cached abstract, so the title+abstract line "
         "understates what a live abstract-indexed search would reach.", "",
         "## Local recall - how much does abstract matching rescue?", "",
         "| basis | overall | Recall(A) | Recall(B) | rare value-added core | realized fertility |",
         "|---|---|---|---|---|---|",
         f"| title only | {r_title['overall']:.1%} | {r_title['A']:.1%} | {r_title['B']:.1%} | "
         f"{r_title['core']:.0%} ({r_title['core_hit']}/{r_title['core_tot']}) | "
         f"{r_title['real']:.0%} ({r_title['real_hit']}/{r_title['real_tot']}) |",
         f"| **title + abstract** | **{r_ta['overall']:.1%}** | {r_ta['A']:.1%} | {r_ta['B']:.1%} | "
         f"{r_ta['core']:.0%} ({r_ta['core_hit']}/{r_ta['core_tot']}) | "
         f"{r_ta['real']:.0%} ({r_ta['real_hit']}/{r_ta['real_tot']}) |", "",
         f"Abstract matching lifts overall recall {r_title['overall']:.0%} to **{r_ta['overall']:.0%}**, "
         f"the rare value-added core {r_title['core']:.0%} to **{r_ta['core']:.0%}**, and "
         f"realized-fertility recall {r_title['real']:.0%} to **{r_ta['real']:.0%}**.", "",
         "## Live universe counts - the budget cost of abstract matching", "",
         "| operationalization | universe (meta.count) |", "|---|---|",
         f"| `title.search` | {n_title:,} |" if n_title is not None else "| `title.search` | (no response) |",
         f"| `title_and_abstract.search` | {n_ta:,} |" if n_ta is not None
         else "| `title_and_abstract.search` | (no response) |",
         "", "## The fork (data-driven)", "",
         "- `title.search`: faithful to the title-only CV; smaller universe; caps recall at the "
         "title-only number.",
         "- `title_and_abstract.search`: recovers the abstract-only gold, at the cost of a larger "
         "universe, because the broad cause-side singles (climate, concern, crisis, environment) match "
         "across abstracts far more loosely than across titles.",
         "- D.3.b-specific: the effect block carries `fertility`, which A6a found to be a NEGATIVE "
         "discriminator inside this frame. It is kept for scope-definitional reasons, but it is the "
         "main reason the universe inflates, since climate-and-fertility papers of the "
         "physical-exposure kind are exactly what it retrieves. If the universe is unmanageable, the "
         "first tightening to try is phrase-restricting the effect block rather than the cause block.", "",
         "## Query (cleaned Boolean)", "", f"    {query}"]
    (LOGS / f"{SLUG}-recall-probe.md").write_text("\n".join(L) + "\n")

    print(f"gold {len(gold)} (A {sum(1 for g in gold if g['tier']=='A')}, "
          f"B {sum(1 for g in gold if g['tier']=='B')}; with abstract {n_with_abs})", file=sys.stderr)
    print(f"mined effect top{NF}: {eff_exp}", file=sys.stderr)
    print(f"mined cause  top{NP}: {cau_exp}", file=sys.stderr)
    print(f"LOCAL title-only: overall {r_title['overall']:.1%} (A {r_title['A']:.0%}/B {r_title['B']:.0%}) "
          f"core {r_title['core']:.0%} realized {r_title['real']:.0%}", file=sys.stderr)
    print(f"LOCAL title+abs : overall {r_ta['overall']:.1%} (A {r_ta['A']:.0%}/B {r_ta['B']:.0%}) "
          f"core {r_ta['core']:.0%} realized {r_ta['real']:.0%}", file=sys.stderr)
    print(f"UNIVERSE title.search = {n_title} | title_and_abstract.search = {n_ta}", file=sys.stderr)


if __name__ == "__main__":
    main()
