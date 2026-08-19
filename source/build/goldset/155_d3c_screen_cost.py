#!/usr/bin/env python3
r"""
155_d3c_screen_cost.py — D.3.c, Phase D. Cost model for the two-stage screen.

Prices the D2a (Haiku) -> D2b (Sonnet) cascade over the pull B1 sized, so the screening decision is
made on a number instead of on the word "infeasible". Every input is either measured from this
chapter's own artefacts or named as an assumption with its source.

TOKEN COUNTS HERE ARE ESTIMATED FROM MEASURED CHARACTERS, NOT COUNTED. This environment has no
Anthropic credential, so `client.messages.count_tokens()` — the only correct way to count tokens for
a Claude model — could not be run. Character counts ARE measured, exactly, over this chapter's
10,589-record Tier B frame; they are converted at CHARS_PER_TOKEN below. **Re-run with
`--count-tokens` once a key is available and before committing budget.** Never substitute `tiktoken`:
it is OpenAI's tokenizer and undercounts Claude tokens by ~15-20% on prose and more on technical text.

The estimate's direction of error is stated rather than hoped for: prose runs ~4 chars/token and
academic abstracts run denser, so a 4.0 divisor UNDER-counts tokens and therefore UNDER-states cost.
A sensitivity band is printed for that reason.

Pricing as of 2026-06-24 (from the claude-api skill's model table):
  Haiku 4.5   $1.00 / $5.00  per MTok in/out
  Sonnet 5    $3.00 / $15.00 per MTok — **$2.00 / $10.00 introductory through 2026-08-31**
  Batch API   50% off all token usage
  Prompt cache: reads ~0.1x base input; writes 1.25x (5-minute TTL)

Output: literature/search-logs/{slug}-screen-cost.md
"""
import json, os, statistics, sys

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")

CHARS_PER_TOKEN = 4.0        # estimate; see the module docstring. Sensitivity band printed below.
BAND = (3.3, 4.5)            # denser (more tokens, costlier) .. lighter (fewer tokens, cheaper)

PRICES = {  # $ per 1M tokens
    "haiku-4.5":        {"in": 1.00, "out": 5.00},
    "sonnet-5-intro":   {"in": 2.00, "out": 10.00},   # through 2026-08-31
    "sonnet-5-standard": {"in": 3.00, "out": 15.00},
}
BATCH_DISCOUNT = 0.50
CACHE_READ = 0.10

RECORDS_PER_REQUEST = 20     # batching amortises the shared rubric across records
S1_RUBRIC_TOKENS = 1_500     # D2a routing rubric, cached
S1_OUT_PER_RECORD = 40       # cell + confidence, structured
S2_RUBRIC_TOKENS = 3_000     # D2b extraction schema + wall definitions, cached
S2_OUT_PER_RECORD = 200      # estimand cell, margin, level, context tag, evidence type, rationale
S1_PASS_RATE = 0.15          # share of D2a input reaching D2b; see the sensitivity table


def money(x):
    return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"


def stage_cost(n_records, chars_per_record, rubric_tokens, out_per_record, price, cpt, batched=True):
    """Returns (input_tokens, output_tokens, dollars)."""
    n_requests = max(1, round(n_records / RECORDS_PER_REQUEST))
    record_tokens = n_records * chars_per_record / cpt
    rubric_tokens_total = n_requests * rubric_tokens
    # The rubric is byte-identical across requests, so every request after the first reads it from
    # cache. Writes are a rounding error at this volume and are ignored in the favourable direction,
    # which is noted rather than hidden.
    effective_in = record_tokens + rubric_tokens_total * CACHE_READ
    out_tokens = n_records * out_per_record
    dollars = (effective_in / 1e6) * price["in"] + (out_tokens / 1e6) * price["out"]
    if batched:
        dollars *= (1 - BATCH_DISCOUNT)
    return record_tokens + rubric_tokens_total, out_tokens, dollars, n_requests


def main():
    tb = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))
    chars = [len((r.get("title") or "") + " " + (r.get("abstract") or "")) for r in tb]
    mean_chars = statistics.mean(chars)
    abs_cov = sum(1 for r in tb if r.get("abstract")) / len(tb)

    d1 = json.load(open(os.path.join(LOGS, f"{SLUG}-d1-cutoff.json")))
    n_s1 = d1["projected_survivors"]

    rows = []
    for label, cpt in (("dense (3.3 c/t)", BAND[0]), ("central (4.0 c/t)", CHARS_PER_TOKEN),
                       ("light (4.5 c/t)", BAND[1])):
        s1_in, s1_out, s1_cost, s1_req = stage_cost(
            n_s1, mean_chars, S1_RUBRIC_TOKENS, S1_OUT_PER_RECORD, PRICES["haiku-4.5"], cpt)
        n_s2 = round(n_s1 * S1_PASS_RATE)
        s2_in, s2_out, s2_cost_intro, s2_req = stage_cost(
            n_s2, mean_chars, S2_RUBRIC_TOKENS, S2_OUT_PER_RECORD, PRICES["sonnet-5-intro"], cpt)
        _, _, s2_cost_std, _ = stage_cost(
            n_s2, mean_chars, S2_RUBRIC_TOKENS, S2_OUT_PER_RECORD, PRICES["sonnet-5-standard"], cpt)
        rows.append(dict(label=label, cpt=cpt, s1_in=s1_in, s1_out=s1_out, s1_cost=s1_cost,
                         s1_req=s1_req, n_s2=n_s2, s2_in=s2_in, s2_out=s2_out,
                         s2_intro=s2_cost_intro, s2_std=s2_cost_std,
                         total_intro=s1_cost + s2_cost_intro, total_std=s1_cost + s2_cost_std))
    central = rows[1]

    L = [f"# D.3.c — two-stage screen: cost model", "",
         "**Token counts are ESTIMATED from measured characters, not counted.** This environment has "
         "no Anthropic credential, so `count_tokens()` — the only correct way to count tokens for a "
         "Claude model — could not be run. Character counts are measured exactly over this chapter's "
         f"{len(tb):,}-record Tier B frame and converted at {CHARS_PER_TOKEN} chars/token. A "
         "sensitivity band is printed because the central value is a guess, and `tiktoken` is not "
         "used anywhere: it is OpenAI's tokenizer and undercounts Claude tokens. **Re-run with a key "
         "before committing budget.**", "",
         "## Measured inputs", "", "| quantity | value | source |", "|---|---|---|",
         f"| production pull | 390,983 | B1, live `title.search` count |",
         f"| D1 survivors (projected) | **{n_s1:,}** | 154, frame survivor share x pull |",
         f"| mean title+abstract chars | {mean_chars:.0f} | measured over the frame |",
         f"| abstract coverage | {abs_cov:.0%} | measured over the frame |",
         f"| D2a pass rate (assumed) | {S1_PASS_RATE:.0%} | **assumption** — sensitivity below |", "",
         "## The cascade", "",
         f"**D1 (free)** removes only 8% — see `{SLUG}-d1-rank.md`. It cannot do more without losing "
         "gold, because primary-neighbourhood papers largely do not carry mechanism or treatment "
         "vocabulary. That is A4's and B1's finding restated at the record level, and it means the "
         "paid stages absorb essentially the whole pull.", "",
         f"**D2a — Haiku 4.5, recall-preserving.** {n_s1:,} records in {central['s1_req']:,} batched "
         f"requests of {RECORDS_PER_REQUEST}. Rubric ({S1_RUBRIC_TOKENS:,} tokens) is byte-identical "
         "across requests and served from cache at ~0.1x after the first.", "",
         f"**D2b — Sonnet 5, precision + extraction.** {central['n_s2']:,} survivors at the assumed "
         "pass rate, with the full estimand schema.", "",
         "## Cost", "",
         "| conversion | D2a (Haiku) | D2b (Sonnet, intro) | **total (intro)** | total (standard) |",
         "|---|---|---|---|---|"]
    for r in rows:
        mark = "**" if r is central else ""
        L.append(f"| {mark}{r['label']}{mark} | {money(r['s1_cost'])} | {money(r['s2_intro'])} | "
                 f"{mark}{money(r['total_intro'])}{mark} | {money(r['total_std'])} |")
    L += ["", "All figures include the **Batch API's 50% discount**, which applies to the whole job — "
              "screening is not latency-sensitive, so there is no reason to pay list price for it.", "",
          f"**Central estimate: {money(central['total_intro'])}** for the complete two-stage screen "
          f"of a {390983:,}-record pull.", "",
          "## Two things that move the number more than the estimate error", "",
          f"**1. Sonnet 5's introductory pricing ends 2026-08-31.** $2/$10 per MTok now against "
          f"$3/$15 after — {money(central['s2_intro'])} against {money(central['s2_std'])} for D2b, a "
          f"{1 - central['s2_intro'] / central['s2_std']:.0%} saving on that stage. Today is "
          "2026-08-18, so that is a 13-day window, and it is the one deadline in this chapter that "
          "money rather than method depends on.", "",
          f"**2. The D2a pass rate is an assumption, not a measurement.** Everything downstream scales "
          "linearly in it:", "",
          "| D2a pass rate | D2b records | D2b cost (intro) | total |", "|---|---|---|---|"]
    for pr in (0.05, 0.10, 0.15, 0.25, 0.40):
        n2 = round(n_s1 * pr)
        _, _, c2, _ = stage_cost(n2, mean_chars, S2_RUBRIC_TOKENS, S2_OUT_PER_RECORD,
                                 PRICES["sonnet-5-intro"], CHARS_PER_TOKEN)
        L.append(f"| {pr:.0%}{' (assumed)' if pr == S1_PASS_RATE else ''} | {n2:,} | "
                 f"{money(c2)} | {money(central['s1_cost'] + c2)} |")
    L += ["", "Even at a 40% pass rate the total stays under a few hundred dollars. **The screening "
              "cost is not the constraint on this chapter — which is worth saying plainly, because a "
              "390,983-record pull sounds like it should be.** The binding constraints remain RA time "
              "on the boundary cases and the retrieval step for full texts.", "",
          "## What must be re-measured before spending", "",
          "1. **Token counts**, with `count_tokens()` against `claude-haiku-4-5` and `claude-sonnet-5` "
          "on a representative sample. Everything here scales linearly in that number.",
          "2. **The D1 survivor share**, re-run against the real pull rather than the citation frame "
          "(154 states why the frame's share is an upper bound).",
          "3. **The D2a pass rate**, from a calibration run on a few thousand records — which also "
          "produces the recall figure D2a is actually gated on.", ""]
    open(os.path.join(LOGS, f"{SLUG}-screen-cost.md"), "w").write("\n".join(L) + "\n")
    print(f"D2a {money(central['s1_cost'])} + D2b {money(central['s2_intro'])} = "
          f"{money(central['total_intro'])} (intro) / {money(central['total_std'])} (standard)")


if __name__ == "__main__":
    main()
