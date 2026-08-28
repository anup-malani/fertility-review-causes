#!/usr/bin/env python3
"""
236_a23_free_twin_recovery.py — A.23, stage 5e. Look for a free TWIN of each unretrieved record.

WHY. Stage 5b asked, for each record, where a free copy of THAT WORK lives. That is the wrong
question for part of this literature. The Wall 1 packet already documents the structure: the JEEA
mortgage-cost paper and its SSRN preprint are both in the frame; so are the BE JEAP Spanish rental
subsidy and its SSRN version. **A version pair is one study.** If either member is readable the
chapter can read the study, and 5b treated the two as unrelated records and failed on both.

So this rung asks a different question — *does some other record of the same study have an open
copy?* — and it is a second channel rather than a retry, which is why it is worth running at all
after two passes that found nothing for these records.

**THE QUERY IS WHERE THIS GOES WRONG, AND EVERY KNOWN WAY IT GOES WRONG IS HANDLED EXPLICITLY.**
The project's search log has cost several chapters a false zero on each of these:

  * a **comma** inside an OpenAlex filter VALUE is fatal and percent-encoding does not save it;
  * a **`?`** inside `search=` is a wildcard and returns a 200 whose body reads as an empty
    literature;
  * a phrase beginning with **"not"** parses as a boolean NOT and silently searches for its
    own complement;
  * **stopwords are dropped** inside a phrase, so "no future" and "future" are the same query;
  * indexes drop **subtitles**, so a full title with its colon can refuse the very work it names.

The stem is therefore taken from before the first colon, folded, stripped of commas and question
marks, and refused if what remains is too short to identify anything — refused LOUDLY, as its own
outcome, rather than counted as a record with no twin.

**A CANDIDATE IS NOT A TWIN UNTIL ITS FIRST AUTHOR AGREES.** A title search returns reviews of the
work, comments on it, and unrelated papers that share a stem; the standing findings here are that a
review can list the reviewed author as a co-author, so membership is not enough, and that when the
resolver and the record disagree it is usually the CANDIDATE that is wrong. First-author last-name
agreement is required, and every rejection is logged with its reason so the gate can be audited
instead of trusted.

**IT READS THE WANTLIST, NOT THE HANDOFF, AND THE DIFFERENCE IS NOT COSMETIC.** The first version
took its input from `235`'s handoff worklist, which is rebuilt from what is on disk. A record
recovered on one run was therefore absent from the next run's input, and the log reported `0 twins`
while six twins sat in `literature/pdfs/` — the same defect as a cache erasing rung attribution, and
a circular dependency between two stages besides. Input is now the stage-5a wantlist minus whatever
is already on disk, which makes the pipeline linear: 233 → 234 → 236 → 235. Prior successes whose
files survive are carried forward so the totals are reported over the union.

**WHAT IS RECOVERED IS A DIFFERENT VERSION AND MUST BE TREATED AS ONE.** A working paper is not the
version of record: tables move, samples change, and the project has already been bitten by grading a
wrong-version anchor. Every twin is written with the twin's own OpenAlex id in its filename and
flagged in the log, so stage 6 reads it knowing which version it has.

Output: extraction/{slug}-twin-recovery.json
        literature/search-logs/{slug}-twin-recovery-log.md
        literature/pdfs/{slug}/{WID}__{title-slug}-TWIN-{TWINWID}.pdf
"""
import csv, importlib.util, json, os, re, subprocess, sys, threading, time, unicodedata
import urllib.parse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

SLUG = "co-residence-parents-household-delay"
MAILTO = "shravanh@uchicago.edu"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_JSON = os.path.join(EXTRACT, f"{SLUG}-twin-recovery.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-twin-recovery-log.md")

WORKERS = 8
MIN_STEM_WORDS = 4
JACCARD_FLOOR = 0.55
UA = f"fertility-review/1.0 (mailto:{MAILTO})"

TIER_ORDER = ["T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
              "T3_primary_uncertain", "T3_link1_identified",
              "T4_insufficient_resolve_at_retrieval", "T5_link1", "T6_theory_stream"]
DESIGN_RANK = {"identified": 0, "observational": 1, "cannot_tell": 2, "descriptive": 3, "theory": 4}

# The fetcher's own routines, imported rather than copied, so a twin is admitted on exactly the
# same terms as any other file — including the HTML full-text floor.
_spec = importlib.util.spec_from_file_location(
    "a23fetch", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "233_a23_fetch_fulltext.py"))
FETCH = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FETCH)

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}


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


def fold(s):
    """Accent-tolerant fold that TRANSLITERATES. Never maps a letter to a space — the A.12 finding:
    a fold that turns non-ASCII into whitespace shatters names and the author gate then compares
    fragments."""
    if not s:
        return ""
    s = s.lower()
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def jaccard(a, b):
    A, B = set(fold(a).split()), set(fold(b).split())
    return len(A & B) / len(A | B) if A and B else 0.0


def stem_of(title):
    """(stem, refusal). Everything the index or the query parser is known to mishandle is removed
    here, and a stem too short to identify a work is REFUSED rather than searched.

    **THE SUBTITLE IS DROPPED, AND THEN PUT BACK IF DROPPING IT LEFT NOTHING.** Indexes drop
    subtitles, so a full title with its colon can refuse the very work it names — that is why the
    stem is taken from before the colon. But the smoke test caught the rule eating a Wall 1
    identified record: *Fostering Household Formation: Evidence from a Spanish Rental Subsidy* has a
    three-word stem, and refusing it would have reported no twin for one of the six records the
    chapter's identified core depends on. A short stem now falls back to the full title, which is a
    worse query than a good stem and a far better one than none."""
    def clean(x):
        x = re.sub(r"^(not|no)\s+", "", fold(x))   # a leading NOT parses as a boolean operator
        return [w for w in x.split() if len(w) > 1]

    words = clean((title or "").split(":")[0].split(" - ")[0])
    if len(words) < MIN_STEM_WORDS:
        words = clean(title or "")
        if len(words) < MIN_STEM_WORDS:
            return None, f"stem_too_short:{len(words)}w"
    return " ".join(words[:14]), None


def get(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True, errors="replace")
    return r.stdout if r.returncode == 0 else None


def first_author(work):
    for a in (work.get("authorships") or []):
        if a.get("author_position") == "first":
            return (a.get("author") or {}).get("display_name") or ""
    aus = work.get("authorships") or []
    return ((aus[0].get("author") or {}).get("display_name") or "") if aus else ""


def last_name(name):
    parts = fold(name).split()
    return parts[-1] if parts else ""


def author_agrees(a, b):
    """Token overlap, not last-token equality.

    The smoke test found the reason: Aparicio-Fenoll is rendered `Aparicio Fenoll` on one OpenAlex
    record and `Fenoll` on another, so a last-token comparison called the paper's own preprint a
    different author's work — the same class of error as the fold that compared last LETTERS. Two
    first-author names agree if their folded token sets share any token of three characters or
    more, which survives compound and hyphenated surnames and initial-versus-full given names.
    It is deliberately permissive and it is not load-bearing alone: a candidate must ALSO clear the
    title Jaccard floor, and every rejection is logged."""
    A = {w for w in fold(a).split() if len(w) >= 3}
    B = {w for w in fold(b).split() if len(w) >= 3}
    return bool(A & B)


def candidates_for(stem):
    """title.search carries no comma by construction — the stem is folded to alphanumerics first,
    which is what makes the filter safe rather than percent-encoding, which does not work."""
    q = urllib.parse.quote(stem, safe=" ").replace(" ", "%20")
    url = (f"https://api.openalex.org/works?filter=title.search:{q}"
           f"&select=id,doi,title,authorships,locations,best_oa_location,open_access,type,"
           f"publication_year&per-page=25&api_key={KEY}")
    d = get(url)
    try:
        return json.loads(d).get("results") or [] if d else []
    except Exception:
        return []


def own_first_author_name(wid):
    """Asked directly rather than read off the title search. If the record does not happen to rank
    in its own stem's top results the gate would otherwise have nothing to compare against and would
    refuse every candidate — a silent no-op of exactly the kind the standing rule warns about."""
    d = get(f"https://api.openalex.org/works/{wid}?select=authorships&api_key={KEY}")
    try:
        return first_author(json.loads(d)) if d else ""
    except Exception:
        return ""


def oa_urls(work):
    out = []
    b = work.get("best_oa_location") or {}
    u = b.get("pdf_url") or b.get("landing_page_url")
    if u:
        out.append(u)
    for l in (work.get("locations") or []):
        if l.get("is_oa"):
            v = l.get("pdf_url") or l.get("landing_page_url")
            if v and v not in out:
                out.append(v)
    return out


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    os.makedirs(PDF_DIR, exist_ok=True)
    on_disk = {f.split("__")[0] for f in os.listdir(PDF_DIR)
               if os.path.getsize(os.path.join(PDF_DIR, f)) > 1024}
    prior = {}
    if os.path.exists(OUT_JSON):
        for x in json.load(open(OUT_JSON)):
            if x["outcome"] in ("pdf", "html_text") and x["id"] in on_disk:
                prior[x["id"]] = x
    todo = [dict(id=m["id"], tier=m["tier"], design=m["design"], title=m["title"] or "",
                 work="")
            for m in json.load(open(OA))
            if m["id"] not in on_disk or m["id"] in prior]
    todo = [r for r in todo if r["id"] not in prior]
    lock = threading.Lock()
    done = [0]
    tally = Counter()

    def work(r):
        out = dict(id=r["id"], tier=r["tier"], design=r["design"], work=r["work"],
                   title=r["title"], outcome="no_twin", twin=None, twin_doi=None,
                   twin_year=None, twin_type=None, url=None, note="", rejected=[],
                   blocked_twins=[])
        stem, refusal = stem_of(r["title"])
        if refusal:
            out["outcome"], out["note"] = "stem_refused", refusal
        else:
            self_name = own_first_author_name(r["id"])
            for c in candidates_for(stem):
                cid = c["id"].rsplit("/", 1)[-1]
                if cid == r["id"]:
                    continue
                j = jaccard(c.get("title") or "", r["title"])
                cname = first_author(c)
                if j < JACCARD_FLOOR:
                    out["rejected"].append(f"{cid}:jaccard={j:.2f}")
                    continue
                if not self_name:
                    out["rejected"].append(f"{cid}:self_first_author_unknown")
                    continue
                if not cname:
                    out["rejected"].append(f"{cid}:twin_first_author_unknown")
                    continue
                if not author_agrees(self_name, cname):
                    out["rejected"].append(
                        f"{cid}:first_author={last_name(cname)}!={last_name(self_name)}")
                    continue
                urls = oa_urls(c)
                if not urls:
                    out["rejected"].append(f"{cid}:twin_not_open")
                    continue
                base = f"{r['id']}__{FETCH.slugify(r['title'])}-TWIN-{cid}"
                tried = []
                for u in urls:
                    oc, n = FETCH.fetch_one(u, os.path.join(PDF_DIR, base + ".pdf"),
                                            os.path.join(PDF_DIR, base + ".html.txt"))
                    if oc in ("pdf", "html_text"):
                        out.update(outcome=oc, twin=cid, twin_doi=(c.get("doi") or "").replace(
                            "https://doi.org/", ""), twin_year=c.get("publication_year"),
                            twin_type=c.get("type"), url=u, note=n)
                        break
                    out["note"] = n
                    tried.append(f"{n.split(':')[0]} {u}")
                if out["twin"]:
                    break
                # A twin that cleared the gate and would not deliver is a BROWSER JOB, and the
                # handoff cannot act on it unless it says WHICH twin and which url. Recording only
                # the outcome, as the first version did, left 17 rows unactionable.
                out["blocked_twins"].append(dict(twin=cid, doi=(c.get("doi") or "").replace(
                    "https://doi.org/", ""), year=c.get("publication_year"), type=c.get("type"),
                    urls=tried))
                out["outcome"] = "twin_open_but_blocked" if out["outcome"] == "no_twin" \
                    else out["outcome"]
        with lock:
            tally[out["outcome"]] += 1
            done[0] += 1
            if done[0] % 25 == 0:
                print(f"  {done[0]}/{len(todo)} — {tally['pdf'] + tally['html_text']} twins",
                      flush=True)
        return out

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        res = list(ex.map(work, todo)) + list(prior.values())
    json.dump(res, open(OUT_JSON, "w"), indent=2)
    for x in prior.values():
        tally[x["outcome"]] += 1

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    won = [r for r in res if r["outcome"] in ("pdf", "html_text")]
    crit = [r for r in res if r["tier"].startswith("T1") or r["design"] == "identified"]
    crit_won = [r for r in crit if r["outcome"] in ("pdf", "html_text")]
    refused = [r for r in res if r["outcome"] == "stem_refused"]
    by_tier = defaultdict(lambda: [0, 0])
    for r in res:
        by_tier[r["tier"]][0] += 1
        if r["outcome"] in ("pdf", "html_text"):
            by_tier[r["tier"]][1] += 1
    rej = Counter(x.split(":", 1)[1].split("=")[0] for r in res for x in r["rejected"])

    L = [f"# Stage 5e free-twin recovery — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/236_a23_free_twin_recovery.py`", "",
         f"**{len(won)} of {len(res)} records were recovered through a twin "
         f"({pc(len(won), len(res))})**, and **{len(crit_won)} of the {len(crit)} critical ones** "
         "— Wall 1 packet or an identified design. "
         f"({len(prior)} of those {len(won)} were carried forward from a prior run of this script, "
         "whose files are still on disk; this run queried " + str(len(todo)) + " records.)", "",
         "Stage 5b asked where a free copy of each WORK lives. This asks whether some other record "
         "of the same STUDY has one, because a version pair is one study and the Wall 1 packet "
         "already documents two of them inside this frame — the JEEA mortgage-cost paper with its "
         "SSRN preprint, and the BE JEAP Spanish rental subsidy with its SSRN version. 5b treated "
         "each pair as two unrelated records and failed on both members.", "",
         "## Yield by tier", "", "| Tier | Still missing after 5d | Recovered by twin | |",
         "|---|---|---|---|"]
    for t in TIER_ORDER:
        if t in by_tier:
            n, g = by_tier[t]
            L.append(f"| `{t}` | {n} | {g} | {pc(g, n)} |")
    L += ["", "## What the gate refused, and why", "",
          "A title search returns reviews of a work, comments on it, and unrelated papers sharing a "
          "stem. First-author last-name agreement is required — membership is not enough, because a "
          "review can carry the reviewed author as a co-author — and every rejection is recorded so "
          "the gate is auditable rather than trusted.", "",
          "| Rejection | n |", "|---|---|"]
    for k, n in rej.most_common():
        L.append(f"| `{k}` | {n} |")
    L += ["", f"**{len(refused)} records were REFUSED before any query was sent**, because the "
          f"title stem left fewer than {MIN_STEM_WORDS} usable words. That is reported as its own "
          "outcome and not as a record with no twin: a query too short to identify a work returns "
          "an answer about the query, not about the literature.", ""]
    if won:
        L += ["## The twins recovered", "",
              "**Each is a DIFFERENT VERSION of the record it stands in for**, and the filename "
              "carries the twin's own OpenAlex id so stage 6 reads it knowing which version it has. "
              "A working paper is not the version of record — tables move and samples change "
              "between them.", "",
              "| Tier | Design | Record | Twin | Twin year | Twin type |",
              "|---|---|---|---|---|---|"]
        for r in sorted(won, key=lambda x: (TIER_ORDER.index(x["tier"])
                                            if x["tier"] in TIER_ORDER else 9,
                                            DESIGN_RANK.get(x["design"], 9))):
            L.append(f"| `{r['tier']}` | `{r['design']}` | {r['title'][:66]} | "
                     f"`{r['twin']}` {r['twin_doi'] or ''} | {r['twin_year'] or '—'} | "
                     f"{r['twin_type'] or '—'} |")
        L.append("")
    L += ["## Outcomes", "", "| Outcome | n |", "|---|---|"]
    for k, n in tally.most_common():
        L.append(f"| `{k}` | {n} |")
    blocked = [r for r in res if r["outcome"] == "twin_open_but_blocked"]
    L += ["", "`twin_open_but_blocked` is a twin that passed the author gate and had an open "
          "location that would not deliver — a browser job, not an absence. The twin's id and the "
          "urls tried are recorded for each, because an outcome without them is not something "
          "anyone can act on.", ""]
    if blocked:
        L += ["| Tier | Design | Record | Blocked twin | Url tried |", "|---|---|---|---|---|"]
        for r in sorted(blocked, key=lambda x: (TIER_ORDER.index(x["tier"])
                                                if x["tier"] in TIER_ORDER else 9,
                                                DESIGN_RANK.get(x["design"], 9))):
            for b in r["blocked_twins"]:
                u = (b["urls"] or ["—"])[0]
                L.append(f"| `{r['tier']}` | `{r['design']}` | {r['title'][:56]} | "
                         f"`{b['twin']}` {b['doi'] or ''} ({b['type'] or '—'}) | {u[:80]} |")
        L.append("")
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\ntwins {len(won)}/{len(todo)} ({pc(len(won), len(todo))}); "
          f"critical {len(crit_won)}/{len(crit)}")
    print("outcomes:", dict(tally))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
