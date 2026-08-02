#!/usr/bin/env python3
"""
70_b1_production_query.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A6c.

Refit the 2-block production query on the FULL gold at the CV-chosen breadth (Nf=10, Np=20; A6b showed
the cause block binds and effect breadth is free), then answer the A6c fork WITH NUMBERS before any
big universe pull:

  1. LOCAL recall (budget-free): match the compiled query against each gold paper's cached title, and
     against title+abstract. The gap = how much abstract matching rescues B.1's outcome-only-title gold
     (A6b's title-only CV floor was 42%). Reported overall, Recall(A)/Recall(B), and on the rare
     PRIMARY_DECOUPLING/DESIRE core (does abstract matching lift the 23% title-only core recall?).
  2. LIVE universe counts (cheap, 1 request each): title.search vs title_and_abstract.search. OAS used
     title.search because broad mined singles (here: status/mating/evolutionary) explode across
     abstracts; this quantifies that trade-off for B.1 so title-vs-t&a is a data-driven choice.

Writes the production-query.json regardless (backbone + mined expansion per block) so A6c-full can pull
whichever operationalization we choose.

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json,
         literature/search-logs/{slug}-tier-b-frame.json (for gold abstracts)
Output : literature/search-logs/{slug}-production-query.json + {slug}-recall-probe.md
"""
import json, re, math, sys, subprocess
from pathlib import Path
from collections import Counter
from urllib.parse import quote

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
MAILTO = "shravanh@uchicago.edu"
NF, NP = 10, 20
ALPHA0 = 1000.0
MIN_GOLD_FOLD = 2
PRIMARY_EMPIRICAL = {"PROXIMATE_ULTIMATE", "PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE",
                     "MOTIVATION_DISTINCTNESS"}
RARE_CORE = {"PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE"}

EFFECT_BACKBONE = ["fertility", "fertilit*", "birth*", "reproductive success", "reproduction",
                   "reproductive", "childbearing", "childbear*", "number of children", "offspring",
                   "completed fertility", "family size", "childless*", "fecundit*", "natality", "parity"]
CAUSE_BACKBONE = ["decoupl*", "dissociat*", "uncoupl*", "sever*", "sex from reproduction",
                  "sex without reproduction", "sex without conception", "sex drive", "sexual selection",
                  "contracepti*", "oral contraceptive*", "the pill", "birth control", "family planning"]

STOP = set("the a an of and in on for from to its by is with as at or be this that these those we our "
           "their his her it they i ii iii new evidence using based study studies analysis approach paper "
           "article effect effects impact role case among between within over under are was were has have "
           "had do does can could will would not no more less than into about across after before during "
           "toward towards via per vs versus also two three some how what why when where which who whom "
           "data model models results result human humans".split())
EFFECT = re.compile(r"fertil|childbear|childless|birth|fecund|natalit|offspring|reproducti|"
                    r"number of children|family size|parity|completed fertilit|procreat|babi|quantum")
CAUSE = re.compile(r"evolution|darwin|selection|sociobiolog|life history|adaptive|fitness|biosocial|"
                   r"mating|sexual|sex drive|coital|intercourse|status|wealth|mate |dominance|"
                   r"decoupl|dissociat|sever|uncoupl|contracept|\bpill\b|family planning|birth control|"
                   r"desire for children|childbearing motiv|motivation|proximate|ultimate")


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
    r = subprocess.run(["curl", "-s", "-m", "40", "-A", f"b1-review/1.0 (mailto:{MAILTO})", url],
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
    frame_abs = {r["paperId"]: (r.get("abstract") or "") for r in json.load(open(LOGS / f"{SLUG}-tier-b-frame.json"))}
    # gold with abstract
    gold = [{"title": s["title"], "abstract": s.get("abstract") or "", "tier": "A", "cell": s.get("provisional_cell")}
            for s in seeds if s.get("title")]
    for r in rows:
        if r["verdict"] == "RELEVANT" and r.get("evidence_type") != "theory" and r.get("title"):
            gold.append({"title": r["title"], "abstract": frame_abs.get(r["paperId"], ""),
                         "tier": "B", "cell": r["cell"]})
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
          "cause_block": {"backbone": CAUSE_BACKBONE, "mined_expansion": cau_exp}}
    json.dump(pq, open(LOGS / f"{SLUG}-production-query.json", "w"), indent=2)

    eff_c = [compile_term(t) for t in EFFECT_BACKBONE + eff_exp]
    cau_c = [compile_term(t) for t in CAUSE_BACKBONE + cau_exp]

    def recall(use_abstract):
        h = {"A": 0, "B": 0}
        t = {"A": 0, "B": 0}
        ch = ct = 0
        for g in gold:
            text = g["title"] + (" " + g["abstract"] if use_abstract else "")
            nt = " " + norm(text) + " "
            ok = matches(nt, eff_c) and matches(nt, cau_c)
            t[g["tier"]] += 1
            core = g["cell"] in RARE_CORE
            ct += core
            if ok:
                h[g["tier"]] += 1
                ch += core
        tot = t["A"] + t["B"]
        return {"overall": (h["A"] + h["B"]) / tot, "A": h["A"] / t["A"] if t["A"] else 0,
                "B": h["B"] / t["B"] if t["B"] else 0,
                "core": ch / ct if ct else 0, "core_hit": ch, "core_tot": ct}

    r_title = recall(False)
    r_ta = recall(True)

    # live universe counts (cheap)
    query = f"{build_group(EFFECT_BACKBONE + eff_exp)} AND {build_group(CAUSE_BACKBONE + cau_exp)}"
    n_title = curl_count("title.search", query)
    n_ta = curl_count("title_and_abstract.search", query)

    L = [f"# A6c production query + recall probe — {SLUG}", "",
         f"Production query refit on full gold at CV breadth Nf={NF}, Np={NP}. "
         "Local recall is budget-free (compiled query vs gold's cached title / title+abstract); universe "
         "counts are 1 cheap OpenAlex request each.", "",
         "## Local recall — how much does abstract matching rescue?", "",
         "| basis | overall | Recall(A) | Recall(B) | rare-core |", "|---|---|---|---|---|",
         f"| title only | {r_title['overall']:.1%} | {r_title['A']:.1%} | {r_title['B']:.1%} | "
         f"{r_title['core']:.0%} ({r_title['core_hit']}/{r_title['core_tot']}) |",
         f"| **title + abstract** | **{r_ta['overall']:.1%}** | {r_ta['A']:.1%} | {r_ta['B']:.1%} | "
         f"{r_ta['core']:.0%} ({r_ta['core_hit']}/{r_ta['core_tot']}) |", "",
         f"Abstract matching lifts overall recall {r_title['overall']:.0%} → **{r_ta['overall']:.0%}** and "
         f"the rare decoupling/desire core {r_title['core']:.0%} → **{r_ta['core']:.0%}**.", "",
         "## Live universe counts — the budget cost of abstract matching", "",
         "| operationalization | universe (meta.count) |", "|---|---|",
         f"| `title.search` | {n_title:,} |" if n_title is not None else "| `title.search` | (no response) |",
         f"| `title_and_abstract.search` | {n_ta:,} |" if n_ta is not None else "| `title_and_abstract.search` | (no response) |",
         "", "## The fork (data-driven)", "",
         "- `title.search`: faithful to the title-only CV; smaller universe; but caps recall at the "
         "title-only number (misses B.1's outcome-only-title gold).",
         "- `title_and_abstract.search`: recovers the abstract-only gold (higher recall) but the broad "
         "mined cause singles (status/mating/evolutionary) inflate the universe — the budget/precision "
         "cost quantified above. If the universe is unmanageable, tighten the cause block to phrases.", "",
         "## Query (cleaned Boolean)", "", f"    {query}"]
    (LOGS / f"{SLUG}-recall-probe.md").write_text("\n".join(L) + "\n")

    print(f"gold {len(gold)} (A {sum(1 for g in gold if g['tier']=='A')}, B {sum(1 for g in gold if g['tier']=='B')})",
          file=sys.stderr)
    print(f"mined effect top{NF}: {eff_exp}", file=sys.stderr)
    print(f"mined cause  top{NP}: {cau_exp}", file=sys.stderr)
    print(f"LOCAL recall  title-only: overall {r_title['overall']:.1%} (A {r_title['A']:.0%}/B {r_title['B']:.0%}) "
          f"core {r_title['core']:.0%}", file=sys.stderr)
    print(f"LOCAL recall  title+abs : overall {r_ta['overall']:.1%} (A {r_ta['A']:.0%}/B {r_ta['B']:.0%}) "
          f"core {r_ta['core']:.0%}", file=sys.stderr)
    print(f"UNIVERSE  title.search = {n_title} | title_and_abstract.search = {n_ta}", file=sys.stderr)


if __name__ == "__main__":
    main()
