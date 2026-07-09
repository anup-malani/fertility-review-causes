#!/usr/bin/env python3
"""
52_apply_ra_gate.py — fold the RA-gate verdicts back into the pipeline.

Reads the decisions file exported by the interactive gate
(51_build_ra_gate.py -> output/{slug}-ra-gate.html -> Export JSON) and applies
the RA's calls to the two review streams:

  POOLING SET (61)  confirm -> stays in the finalized estimand-ready set
                    demote  -> removed from the pool, retained on an off-cell
                               record (routed to its own cell later)
                    unsure  -> held out of the final set, flagged for a 2nd look
  UNCERTAINS (88)   relevant -> verdict promoted to RELEVANT in the tiers file
                    not      -> verdict set to NOT_RELEVANT
                    unsure   -> left UNCERTAIN (residual)

Deterministic, LLM/OpenAlex-free. Non-destructive: reads the committed
screen-tiers.json / estimand-ready-set.json as INPUTS and writes NEW *-final /
*-ra-signed artifacts plus a changelog; it never clobbers the inputs. Safe to
run on a partial (or missing) decisions file — undecided papers are reported as
pending and carried through unchanged.

Usage:
  python3 52_apply_ra_gate.py [path/to/decisions.json]
If no path is given it looks for, in order:
  output/{slug}-ra-gate-decisions.json, then ~/Downloads/{slug}-ra-gate-decisions.json
"""
import json, os, sys, glob, datetime

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)

def find_decisions():
    if len(sys.argv) > 1:
        return sys.argv[1]
    cands = [rp("output", f"{SLUG}-ra-gate-decisions.json"),
             os.path.expanduser(f"~/Downloads/{SLUG}-ra-gate-decisions.json")]
    cands += sorted(glob.glob(os.path.expanduser(f"~/Downloads/{SLUG}-ra-gate-decisions*.json")))
    for c in cands:
        if os.path.exists(c):
            return c
    return None

# ---- load inputs ----
tiers = json.load(open(rp("output", f"{SLUG}-screen-tiers.json")))
pool  = json.load(open(rp("output", f"{SLUG}-estimand-ready-set.json")))

dpath = find_decisions()
if dpath and os.path.exists(dpath):
    dec = json.load(open(dpath)).get("decisions", {})
    print(f"decisions: {dpath} ({len(dec)} verdicts)")
else:
    dec = {}
    print("decisions: NONE FOUND — running in carry-through mode (nothing applied yet).")
    print("  export from the gate, then re-run:  python3 52_apply_ra_gate.py [path]")

def verdict(pid):
    d = dec.get(pid)
    return (d.get("v"), d.get("bucket") or "", d.get("note") or "") if d else (None, "", "")

# ---- POOLING SET fold-back ----
final_pool, off_cell, held = [], [], []
for r in pool:
    v, bucket, note = verdict(r["paperId"])
    rec = dict(r, ra_verdict=v, ra_bucket=bucket, ra_note=note, ra_signed=bool(v))
    if v == "confirm":
        final_pool.append(rec)
    elif v == "demote":
        off_cell.append(rec)
    elif v == "unsure":
        held.append(rec)
    else:                      # undecided -> carry through as still-tentative
        held.append(dict(rec, ra_verdict="pending"))
pending_pool = sum(1 for r in held if r.get("ra_verdict") == "pending")

# ---- UNCERTAIN fold-back (write a new ra-signed tiers file) ----
VMAP = {"relevant": "RELEVANT", "not": "NOT_RELEVANT"}
promoted = demoted_unc = still_uncertain = 0
tiers_out = []
for r in tiers:
    r = dict(r)
    if r["verdict"] == "UNCERTAIN":
        v, _, note = verdict(r["paperId"])
        if v in VMAP:
            r["verdict"] = VMAP[v]
            r["ra_signed"] = True
            if note: r["ra_note"] = note
            if v == "relevant": promoted += 1
            else: demoted_unc += 1
        else:
            still_uncertain += 1
    tiers_out.append(r)

# ---- write artifacts ----
os.makedirs(rp("output"), exist_ok=True)
json.dump(final_pool, open(rp("output", f"{SLUG}-pooling-set-final.json"), "w"),
          ensure_ascii=False, indent=1)
json.dump(off_cell, open(rp("output", f"{SLUG}-pooling-offcell.json"), "w"),
          ensure_ascii=False, indent=1)
json.dump(tiers_out, open(rp("output", f"{SLUG}-screen-tiers-ra-signed.json"), "w"),
          ensure_ascii=False, indent=1)

# finalized pooling-set markdown
def md_row(i, r):
    g = " ·gold" if r.get("is_gold") else ""
    return f"| {i} | {r['title']}{g} | {r.get('outcome','')} | {r.get('mechanism','')} | {r.get('direction','')} |"
lines = [f"# Finalized estimand-ready pooling set — {SLUG}", "",
         "Papers the automated estimand gate placed in the primary cell "
         "(OAS-motive → fertility, forward, fertility-outcome) **and** the RA confirmed. "
         "Demoted / held papers are listed below the table.", ""]
if dec:
    lines.append(f"**RA-signed:** {len(final_pool)} confirmed · {len(off_cell)} demoted off-cell · "
                 f"{len(held)-pending_pool} held (unsure) · {pending_pool} still pending review.")
else:
    lines.append("**Status:** no RA decisions applied yet — all 61 carried through as pending.")
lines += ["", "| # | Study | Outcome | Mechanism | Direction |",
          "|---|---|---|---|---|"]
lines += [md_row(i+1, r) for i, r in enumerate(final_pool)]
if off_cell:
    lines += ["", "## Demoted off-cell (retained for their own cells)", ""]
    from collections import Counter
    for b, n in Counter(r["ra_bucket"] for r in off_cell).most_common():
        lines.append(f"- **{b or 'unspecified'}** — {n}")
    lines.append("")
    for r in off_cell:
        lines.append(f"  - {r['title']} — _{r['ra_bucket'] or '?'}_"
                     + (f" ({r['ra_note']})" if r["ra_note"] else ""))
open(rp("output", f"{SLUG}-pooling-set-final.md"), "w").write("\n".join(lines) + "\n")

# changelog
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
cl = [f"# RA-gate changelog — {SLUG}", "", f"Applied {stamp} by `52_apply_ra_gate.py`",
      f"from `{os.path.basename(dpath) if dpath else '(none)'}`.", "",
      "## Pooling set (61 → finalized)",
      f"- confirmed in-cell: **{len(final_pool)}**",
      f"- demoted off-cell: **{len(off_cell)}**",
      f"- held (unsure): **{len(held)-pending_pool}**",
      f"- still pending: **{pending_pool}**", "",
      "## UNCERTAINs (88 → resolved)",
      f"- promoted to RELEVANT: **{promoted}**",
      f"- set NOT_RELEVANT: **{demoted_unc}**",
      f"- left UNCERTAIN: **{still_uncertain}**", "",
      "## Outputs",
      f"- `{SLUG}-pooling-set-final.json` / `.md` — the finalized pooling set",
      f"- `{SLUG}-pooling-offcell.json` — demoted papers, routed to their own cells",
      f"- `{SLUG}-screen-tiers-ra-signed.json` — tiers with UNCERTAINs resolved"]
open(rp("output", f"{SLUG}-ra-gate-changelog.md"), "w").write("\n".join(cl) + "\n")

# ---- console report ----
print("\n=== fold-back applied ===")
print(f"POOLING 61 -> confirmed {len(final_pool)} | demoted {len(off_cell)} | "
      f"held {len(held)-pending_pool} | pending {pending_pool}")
print(f"UNCERTAIN 88 -> RELEVANT {promoted} | NOT_RELEVANT {demoted_unc} | UNCERTAIN {still_uncertain}")
print("wrote:")
for f in ["pooling-set-final.json", "pooling-set-final.md", "pooling-offcell.json",
          "screen-tiers-ra-signed.json", "ra-gate-changelog.md"]:
    print(f"  output/{SLUG}-{f}")
if pending_pool or still_uncertain:
    print(f"\nNOTE: {pending_pool} pooling + {still_uncertain} uncertain still un-reviewed — "
          "re-run after finishing the gate to finalize.")
