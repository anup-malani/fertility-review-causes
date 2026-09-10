#!/usr/bin/env python3
"""
390 — C.3.f: render a screening batch for reading, without repeating TICK-085.

TICK-085 was opened because a 460-character abstract cap hid the dependent variable on 35.8% of
C.3.d's universe: a dissertation abstract enumerates its chapters in sequence, so the estimand of
essay 2 sits past any short window by construction. The fix there was to raise the cap to 1800.

That fix is right for the emitted batch FILE and wrong as a reading strategy: 60 records at 1800
characters is 100k characters a batch, and the screen is 4,181 records. So this renders a shorter
window and then does what the cap alone cannot — it **searches the whole abstract** for the two
things the routing turns on, and says when they appear beyond the window:

  OUTCOME   fertility, births, childbearing, family size, number of children
  FLOW      transfer, wealth flow, old-age support, child labour, bequest, inheritance, remittance

A record whose outcome vocabulary appears only past the window is printed with a `>>` marker and its
matching sentence, so the window never decides a routing on its own. Records with neither signal
anywhere in the full text are collapsed to one line: they cannot be in scope, and reading their
abstracts is the largest avoidable cost in the screen.

This is a reading aid, not a screen. Every row still gets a hand verdict.

Usage: python3 source/build/goldset/390_c3f_read_batch.py <batch-name> [--window 600]
"""
import argparse, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
BATCHES = ROOT / "extraction" / "wealth-flows-reversal-screen-batches"

# WIDENED after the first run collapsed a primary candidate. The rule below says "cannot be in
# scope", which is a confident negative, and the first version of these patterns produced one on
# "Women's Right to Property and the Quantity-Quality Trade-Off of Children" -- a property-rights
# design with children as the outcome, i.e. exactly this chapter's §7 row 2. It was missed because
# OUTCOME had "number of children" but not bare "children", and FLOW had "inherit" but not
# "property right". A title-only record has no second chance: the title is all there is.
#
# So both patterns are now deliberately loose. The cost of a false POSITIVE here is reading an
# abstract; the cost of a false negative is a discarded record reported as out of scope.
OUTCOME = re.compile(r"fertilit|birth|childbear|children|child\b|famil|number of children|"
                     r"childless|parity|reproduct|motherhood|marriage|marital|offspring|"
                     r"son\b|daughter|kids|population growth|natalit|nuptial|household size", re.I)
FLOW = re.compile(r"transfer|wealth|flow|old.age|support|child labou?r|bequest|inherit|"
                  r"remittance|dowry|bride price|filial|lifecycle deficit|life cycle deficit|"
                  r"national transfer account|value of children|children's work|land reform|"
                  r"land titl|property right|pension|social security|cost of children|"
                  r"economic value|investment|land|landhold|landown|tenure|estate|dowry|lifecycle surplus|life cycle surplus|generational|old age|elder", re.I)


def sentence_at(text, pos, span=190):
    lo = max(0, text.rfind(".", 0, pos) + 1)
    hi = text.find(".", pos)
    hi = len(text) if hi == -1 else hi + 1
    s = text[lo:hi].strip()
    return s if len(s) <= span else s[:span] + "…"


def validate_collapse_rule():
    """The collapse rule states a confident negative, so it is checked against every record already
    hand-routed to a primary cell. If the rule would have hidden one, it is broken and the script
    refuses to run (`safeguards-must-be-measured-not-trusted`,
    `validate-a-null-detector-on-positives`)."""
    import csv
    v = ROOT / "extraction" / "wealth-flows-reversal-screen-verdicts.csv"
    h = ROOT / "temp" / "c3f-universe-hydrated.json"
    if not (v.exists() and h.exists()):
        return
    primary = {r["screen_id"] for r in csv.DictReader(v.open())
               if r["cell"] in ("NET_FLOW_FERTILITY", "SHOCK_NET_FERTILITY")}
    recs = {r["screen_id"]: r for r in json.loads(h.read_text())["records"] if r.get("screen_id")}
    hidden = []
    for sid in sorted(primary):
        r = recs.get(sid)
        if not r:
            continue
        blob = f"{r.get('title') or ''} {r.get('abstract') or ''}"
        if (r.get("abstract") or "").strip() and not FLOW.search(blob):  # tier 2
            hidden.append((sid, (r.get("title") or "")[:70]))
        if (r.get("abstract") or "").strip() and not OUTCOME.search(blob) \
                and not FLOW.search(blob):  # tier 1
            hidden.append((sid, (r.get("title") or "")[:70]))
    if hidden:
        for sid, t in hidden:
            print(f"  COLLAPSE RULE WOULD HIDE {sid}  {t}", file=sys.stderr)
        sys.exit(f"the collapse rule would hide {len(hidden)} of {len(primary)} known primary "
                 "records. Widen the patterns before reading anything with it.")
    print(f"[collapse rules checked against {len(primary)} known primary records — including the "
          f"stricter flow-only tier: hides none]",
          file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--window", type=int, default=600)
    ap.add_argument("--flow-only", action="store_true",
                    help="RETIRED -- see the comment in main(). It hid a record whose twin "
                         "was already routed primary. Kept only so old commands do not break.")
    a = ap.parse_args()
    validate_collapse_rule()
    p = BATCHES / f"{a.batch}.json"
    if not p.exists():
        sys.exit(f"no such batch: {p}")
    recs = json.loads(p.read_text())["records"]

    # TIER 2 (--flow-only): C.3.f's estimand requires a resource flow between parents and children.
    # A record with an outcome word but NO flow vocabulary anywhere in its full text cannot be in
    # any of this chapter's cells -- not even FLOW_MEASUREMENT, which is defined by measuring a
    # flow. Collapsing those to a title line is the largest available saving in a 4,181-record
    # screen, and like tier 1 it is a confident negative, so it is validated against every known
    # primary record before it is allowed to run.
    skipped, flow_only = [], []
    for r in recs:
        ab = (r.get("abstract") or "").strip()
        blob = f"{r.get('title') or ''} {ab}"
        mo, mf = OUTCOME.search(blob), FLOW.search(blob)
        # BOTH tiers apply only to records that HAVE an abstract. Tier 1 hid
        # "Landowning, Status and Population Growth" -- a title-only record, and the same work as a
        # record already routed primary -- because OUTCOME lacked "population growth" and FLOW
        # lacked bare "land". That is the second time a title-only record slipped a collapse rule.
        # Ten words of title is not enough evidence to state a confident negative on, whatever the
        # patterns say, so title-only records are now always read.
        if ab and not mo and not mf:
            skipped.append(r)
            continue
        # Only for records that HAVE an abstract. The validation refused the first version of this
        # tier: it would have hidden 3 of 21 known primary records, and all three were TITLE-ONLY
        # ("Lithium-ion Batteries and Fertility in Africa"; "Women's Right to Property and the
        # Quantity-Quality Trade-Off of Children"). A title carries ~10 words, so a vocabulary test
        # on it is far weaker evidence than the same test on 200 words of abstract, and the flow is
        # often implied by the topic rather than named. Title-only records are always shown.
        # RETIRED 2026-09-10. The tier is off by default and --flow-only now warns. It collapsed
        # "Rural Agricultural Change and Fertility Transition in Nepal" -- whose twin was already
        # routed primary -- because the abstract says "modern farm technologies" and the FLOW
        # pattern has land, labour and tenure but not farm technology. That is the third record a
        # collapse rule has hidden. The flow in this chapter is usually IMPLIED BY THE SETTING (a
        # farm, a mine, a landholding) rather than named, so no vocabulary test can stand in for
        # reading. Extra reading is the cheaper error.
        if a.flow_only and ab and not mf:
            flow_only.append(r)
            continue
        print(f"{r['screen_id']} | {r.get('year')} | "
              f"{(r.get('venue') or 'no venue')[:30]} | c{r.get('cited_by')}")
        print(f"  T: {r.get('title')}")
        print(f"  A: {ab[:a.window] if ab else '**NO ABSTRACT**'}"
              f"{'…' if len(ab) > a.window else ''}")
        for label, m in (("OUTCOME", mo), ("FLOW", mf)):
            if m and m.start() > a.window:
                print(f"  >> {label} appears beyond the window at char {m.start()}: "
                      f"{sentence_at(blob, m.start())}")
        print()

    for label, group in (("NO outcome and NO flow vocabulary", skipped),
                         ("an outcome word but NO FLOW vocabulary anywhere", flow_only)):
        if group:
            print(f"--- {len(group)} records with {label} in the full text. "
                  f"They cannot be in a C.3.f cell; titles only: ---")
            for r in group:
                print(f"  {r['screen_id']}  {r.get('year')}  {(r.get('title') or '')[:96]}")
            print()
    shown = len(recs) - len(skipped) - len(flow_only)
    print(f"[{len(recs)} records: {shown} shown in full, {len(skipped)} no-signal, "
          f"{len(flow_only)} outcome-only]")


main()
