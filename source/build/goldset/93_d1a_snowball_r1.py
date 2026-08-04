#!/usr/bin/env python3
r"""
93_d1a_snowball_r1.py — D.1.a, GACS channel 3, round 1. Build the orthogonal Tier-B frame.

SOURCES: Crossref (backward, reference lists) + Semantic Scholar (forward, citing papers).
NOT OpenAlex. Two reasons, one forced and one good:
  * Forced: OpenAlex moved the free tier to a metered budget. The 89/90/91/92 probe runs exhausted a
    full day's allowance in about an hour ("Insufficient budget ... Resets at midnight UTC"), and a
    snowball is an order of magnitude more requests than a probe. Note the six UNCONFIRMED rows in 92
    were this, not missing papers -- the three-state rule held the line correctly for the second time
    today.
  * Good: PROTOCOL 5.1 already names Semantic Scholar and Crossref as Phase 2b citation sources, and
    building the Tier-B frame off a DIFFERENT provider than the one that produced Tier A makes the
    frame orthogonal in infrastructure as well as in method. Recall(B) measured on an
    OpenAlex-independent frame is a stronger test than one measured on OpenAlex's own graph.

SEED DISCIPLINE (Tier-B integrity). Seeds are channel-1 and channel-2 only: the two regional reviews,
the four SDT-framework statements, and three resolved canon works. The keyword-scouted anchors from
89/90 are Tier-A eligible and are DELIBERATELY NOT SEEDS, per the constraint recorded on the C.2.c
run: a frame seeded from the query's own output makes Recall(B) circular.

SEED EXCLUSION, and this is a judgement worth stating. Hofstede 1980 (15,158 citations) and Schwartz
1992 resolved cleanly in 92 and are NOT seeded here. Their citation neighbourhoods are the management
and cross-cultural-psychology literatures -- they are canon for a CONSTRUCT, not for this treatment x
outcome pair -- and seeding them would swamp the frame with off-pair records and make the yield
statistic meaningless. Canonical status is not the seed criterion; the specificity of the citation
neighbourhood is. The alternative fix, keyword-filtering the frame down to fertility papers, is
REFUSED on purpose: it would bias Tier B toward keyword-reachable work and inflate Recall(B), which
is the exact error the OAS and C.2.c runs were burned by.

RELEVANCE-FILTER AUDIT (run 1, 2026-08-03). A 45-record hand read of what the filter admitted and
rejected -- the standing requirement from the C.2.c run, "require a read of a random sample of what
the relevance filter admits before any saturation number is trusted" -- found TWO bugs, both of the
class that produces plausible counts and wrong ones:

  BUG A, false positives. `reproduc\w+` in the outcome axis admits SOCIAL reproduction and
  REPRODUCTIVE HEALTH, neither of which is a fertility outcome. It scored Bourdieu's *Reproduction in
  Education, Culture and Society* as an on-pair record, and it would admit the whole
  sociology-of-education and SRH-services literatures. This is D.1.a's version of the C.2.c bug where
  bare `hous` and `rent` matched hOUSEhold and paRENT. Narrowed to specific phrases that actually
  denote fertility (reproductive behaviour/success/intentions/decisions).

  BUG B, false negatives. Quoted phrases were carried over from OpenAlex query syntax into a Python
  verbose regex, where `"second\s+demographic\s+transition"` matches only text containing literal
  DOUBLE-QUOTE CHARACTERS. The chapter's single most central phrase therefore never matched, and
  "An alternative perspective on the Second Demographic Transition in East Asia" was rejected as
  having no treatment term. Same for "family size" and "number of children" on the outcome axis.

Both were invisible in the aggregate: round 1 returned 79 relevant of 1,970 distinct and a yield of
1.63 per 50, a number that looked entirely reasonable and was built on a filter that was wrong in
both directions at once.

Output: temp/d1a/snowball-r1-pool.json
        literature/search-logs/{slug}-snowball-log.md
"""
import json, os, re, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
os.makedirs(TMP, exist_ok=True)
POOL = os.path.join(TMP, "snowball-r1-pool.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-snowball-log.md")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d1a_snowball_cache.json")
cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}

FWD_CAP = 600          # per seed; guards against a canon work with an enormous neighbourhood
S2_PAGE = 100
S2_SLEEP = 1.6         # unauthenticated Semantic Scholar throttles hard

# label -> (doi, channel, family)
SEEDS = {
    "Zaidi & Morgan 2017 (SDT appraisal)": ("10.1146/annurev-soc-060116-053442", "ch2", "demography-SDT"),
    "Lesthaeghe 2020 (Genus retrospective)": ("10.1186/s41118-020-00077-4", "ch2", "demography-SDT"),
    "Lesthaeghe 2014 (PNAS overview)": ("10.1073/pnas.1420441111", "ch2", "demography-SDT"),
    "Fernandez (Does Culture Matter?)": ("10.1016/b978-0-444-53187-2.00011-5", "ch2", "econ-of-culture"),
    "SSA religions review 2023": ("10.29063/ajrh2023/v27i1.11", "ch1", "sociology-of-religion"),
    "SSA religion/religiosity review 2021": ("10.31237/osf.io/sezdq", "ch1", "sociology-of-religion"),
    "van de Kaa 1987": ("10.2307/2057518", "ch2", "demography-SDT"),
    "Lesthaeghe & Surkyn 1988": ("10.2307/1972499", "ch2", "demography-SDT"),
    "Norris & Inglehart 2004 (Sacred and Secular)": ("10.1017/cbo9780511791017", "ch2", "sociology-of-religion"),
}

# Relevance labelling. WORD-BOUNDARY ANCHORED, deliberately.
# The C.2.c run's headline methodological failure was a relevance filter matching bare `hous` and
# `rent`, which scored hOUSEhold, paRENT, cuRRENT and diffeRENT as housing terms and made 58% of the
# frame false positives -- inflating yield and making a converging snowball look non-converging.
# D.1.a's equivalents are worse, not better: `value` matches evaluation and valuable, `individual`
# matches "individual-level" and "individualised", `material` matches materials science, and
# `religio` is fine but `secular` also appears in "secular trend", a demography term of art meaning a
# long-run trend with no religious content at all.
TREATMENT = re.compile(r"""\b(
    religio\w* | secular(?:ism|ization|isation|ity)\b | church\w* | denominational?\b | faith\b |
    postmaterialis\w* | post-materialis\w* | individualism\b | individualist\w* |
    individuali[sz]ation\b | collectivism\b | autonomy\b | kinship\b |
    ideational\b | second\s+demographic\s+transition | consumerism\b | materialism\b |
    values?\b | norms?\b | culture\b | cultural\b | attitudes?\b | belief\w*
)""", re.I | re.X)
OUTCOME = re.compile(r"""\b(
    fertility\b | fertilit\w+ | birth\b | births\b | birthrate\b | childbearing\b | childless\w* |
    childfree\b | parity\b | natality\b | family\s+size | number\s+of\s+children |
    tfr\b | nuptialit\w+ | procreat\w+ |
    reproductive\s+(?:behavio\w+|success|intention\w*|decision\w*|career|outcome\w*)
)""", re.I | re.X)
# "secular trend" is a demography idiom with no religious content -- excluded explicitly.
SECULAR_TREND = re.compile(r"\bsecular\s+(trend|decline|increase|change\s+in\s+height)", re.I)


def get(url, tries=5, sleep=1.2):
    key = f"g::{url}"
    if key in cache:
        return cache[key]
    for a in range(tries):
        out = subprocess.run(["curl", "-s", "-m", "50", "-A", UA, url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().startswith("{"):
            try:
                d = json.loads(out.stdout)
            except Exception:  # noqa: BLE001
                time.sleep(sleep * (a + 2)); continue
            if "error" in d or d.get("message") == "Too Many Requests":
                time.sleep(sleep * (a + 2) * 2); continue
            cache[key] = d
            return d
        time.sleep(sleep * (a + 2))
    return None


def crossref_refs(doi):
    d = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}")
    if not d or "message" not in d:
        return None
    out = []
    for r in (d["message"].get("reference") or []):
        t = r.get("article-title") or r.get("volume-title") or r.get("unstructured") or ""
        out.append({"doi": (r.get("DOI") or "").lower() or None, "title": t.strip()[:300],
                    "year": r.get("year"), "venue": r.get("journal-title") or "",
                    "direction": "backward"})
    return out


def s2_citations(doi, cap=FWD_CAP):
    out, offset = [], 0
    while offset < cap:
        url = (f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}"
               f"/citations?fields=title,year,venue,externalIds&limit={S2_PAGE}&offset={offset}")
        d = get(url, sleep=S2_SLEEP)
        if d is None:
            return out if out else None
        data = d.get("data") or []
        for row in data:
            p = row.get("citingPaper") or {}
            ext = p.get("externalIds") or {}
            out.append({"doi": (ext.get("DOI") or "").lower() or None, "title": p.get("title") or "",
                        "year": p.get("year"), "venue": p.get("venue") or "",
                        "s2id": p.get("paperId"), "direction": "forward"})
        if len(data) < S2_PAGE or "next" not in d:
            break
        offset = d["next"]
        time.sleep(S2_SLEEP)
    return out


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def relevant(rec):
    """Returns (is_relevant, reason). Requires BOTH axes -- the treatment x outcome definition."""
    blob = f"{rec.get('title', '')} {rec.get('venue', '')}"
    if not blob.strip():
        return False, "no title"
    t = TREATMENT.search(blob)
    o = OUTCOME.search(blob)
    if t and SECULAR_TREND.search(blob) and t.group(0).lower().startswith("secular"):
        return False, "secular-trend idiom, no religious content"
    if t and o:
        return True, f"treatment={t.group(0)}; outcome={o.group(0)}"
    if not t:
        return False, "no treatment term"
    return False, "no outcome term"


def main():
    seeds_done, pool = {}, {}
    for label, (doi, ch, fam) in SEEDS.items():
        back = crossref_refs(doi)
        fwd = s2_citations(doi)
        seeds_done[label] = {"doi": doi, "channel": ch, "family": fam,
                             "backward": len(back) if back is not None else None,
                             "forward": len(fwd) if fwd is not None else None,
                             "backward_status": "OK" if back is not None else "UNCONFIRMED",
                             "forward_status": "OK" if fwd is not None else "UNCONFIRMED"}
        print(f"{label[:44]:46s} back={seeds_done[label]['backward']} "
              f"fwd={seeds_done[label]['forward']}", file=sys.stderr)
        for rec in (back or []) + (fwd or []):
            nt = norm_title(rec.get("title"))
            if not nt:
                continue
            # Twin merge: normalized TITLE is the key, not the DOI. The C.2.c run found four of five
            # strongest anchors had NBER/SSRN twins on separate DOIs with citation counts split across
            # versions, so DOI-keyed dedup silently keeps both. Title-keyed dedup catches them.
            key = nt[:120]
            if key in pool:
                pool[key]["seen_from"].append(label)
                if not pool[key].get("doi") and rec.get("doi"):
                    pool[key]["doi"] = rec["doi"]
            else:
                pool[key] = {**rec, "seen_from": [label]}
        json.dump(cache, open(CACHE_PATH, "w"))

    for k, v in pool.items():
        ok, why = relevant(v)
        v["relevant"], v["relevance_reason"] = ok, why

    recs = list(pool.values())
    rel = [r for r in recs if r["relevant"]]
    overlap = [r for r in recs if len(set(r["seen_from"])) > 1]
    pulled = sum((s["backward"] or 0) + (s["forward"] or 0) for s in seeds_done.values())
    yield_per_50 = (len(rel) / pulled * 50) if pulled else 0

    out = {"slug": SLUG, "round": 1, "sources": "Crossref backward + Semantic Scholar forward",
           "seeds": seeds_done,
           "counts": {"records_pulled": pulled, "distinct_after_title_dedup": len(recs),
                      "relevant": len(rel), "overlap_multi_seed": len(overlap),
                      "yield_per_50_pulled": round(yield_per_50, 2), "stop_floor_per_50": 1.0},
           "pool": recs}
    json.dump(out, open(POOL, "w"), indent=1)
    print(f"\npulled={pulled} distinct={len(recs)} relevant={len(rel)} "
          f"yield/50={yield_per_50:.2f} overlap={len(overlap)}", file=sys.stderr)
    print(f"wrote {POOL}", file=sys.stderr)


if __name__ == "__main__":
    main()
