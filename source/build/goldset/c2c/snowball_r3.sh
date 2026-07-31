#!/bin/bash
# Channel-3 snowball, ROUND 3 for C.2.c.
#
# Rounds 1-2 seeded the econ-price canon and the demog-tenure/family-formation family.
# Round 3 targets what those under-reached: the MODERN price-variation empirics (2015-2025,
# China / NL / US clusters), the SPACE-and-crowding cell, the tenure-ASYMMETRY cell, the
# AFFORDABILITY cell, and the LONG-RUN/FDT panel.
#
# Seed rule (tightened and made explicit this round): a round-3 seed must already appear in the
# merged snowball pool, i.e. be CITATION-REACHABLE from the canon. That is the operational form of
# the Tier-B integrity constraint -- what must be excluded is a paper reachable ONLY by keyword,
# since seeding off it would centre the neighbourhood on the query's own reach. A paper that is
# citation-reachable does not reimport keyword bias even if a keyword sweep also found it.
# Li 2024 qualifies under this rule and is seeded; Yi & Zhang 2010 does NOT (keyword-only, see log).
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: snowball_r3.sh <outdir>}"
mkdir -p "$OUT"

SEEDS=(
  "10.1016/j.chieco.2020.101496"   # House price, fertility rates and reproductive intentions (China)
  "10.1007/s00148-021-00879-6"     # Housing wealth and fertility: evidence from China
  "10.1002/psp.2787"               # House prices and fertility: Dutch housing crisis
  "10.4054/demres.2007.17.26"      # Fertility differences by housing type (space/quantity cell)
  "10.1086/225997"                 # Crowded apartment living, AJS 1975 (historical space cell)
  "10.1007/s11150-016-9355-8"      # The asymmetric housing wealth effect on childbirth (tenure asymmetry)
  "10.1007/s11113-024-09865-8"     # Housing Affordability Crisis and Delayed Fertility, USA
  "10.1016/j.labeco.2024.102572"   # Li 2024, global 1870-2012 (long-run / FDT)
)

echo "== resolving round-3 seeds =="
: > "$OUT/seeds.tsv"
for doi in "${SEEDS[@]}"; do
  curl -s --max-time 40 -G "https://api.openalex.org/works/https://doi.org/$doi" \
    --data-urlencode "mailto=$M" > "$OUT/seed_$(echo "$doi" | tr '/.:' '___').json"
done

python3 - "$OUT" <<'PY'
import glob, json, os, sys
out = sys.argv[1]
rows = []
for f in sorted(glob.glob(os.path.join(out, "seed_*.json"))):
    w = json.load(open(f))
    if "id" not in w:
        print("UNRESOLVED", f); continue
    wid = w["id"].rsplit("/", 1)[-1]
    rows.append((wid, w.get("doi", ""), len(w.get("referenced_works") or []), w.get("cited_by_count"), (w.get("title") or "")[:58]))
    json.dump(w.get("referenced_works") or [], open(os.path.join(out, f"back_{wid}.json"), "w"))
with open(os.path.join(out, "seeds.tsv"), "w") as fh:
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")
        print("seed", r[0], "backrefs=", r[2], "fwd=", r[3], r[4])
PY

echo "== forward citations =="
while IFS=$'\t' read -r wid doi nback nfwd title; do
  page=1; : > "$OUT/fwd_$wid.jsonl"
  while : ; do
    resp=$(curl -s --max-time 60 -G "https://api.openalex.org/works" \
      --data-urlencode "filter=cites:$wid" --data-urlencode "per-page=200" \
      --data-urlencode "page=$page" --data-urlencode "mailto=$M" \
      --data-urlencode "select=id,doi,title,publication_year,type,cited_by_count,primary_location")
    n=$(printf '%s' "$resp" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('results',[])))")
    printf '%s\n' "$resp" >> "$OUT/fwd_$wid.jsonl"
    [ "$n" -lt 200 ] && break
    page=$((page+1)); [ "$page" -gt 6 ] && break
  done
  echo "  fwd $wid pages=$page"
done < "$OUT/seeds.tsv"
echo "done"
