#!/bin/bash
# Channel-3 snowball, ROUND 2 for C.2.c.
#
# Round 1 seeded off the four channel-2 canon anchors, which were 3 econ-price + 1
# macro-comparative and ZERO demog-tenure. Round 2 adds demography-side seeds so the
# Housing Studies / Demography / EJP vocabulary family is not reached only through
# Mulder & Billari.
#
# Seed provenance: these are CITATION-discovered in round 1, not keyword-discovered.
# That matters -- the Tier-B integrity constraint is about keyword bias, and a paper
# reached by citation from a canon seed does not reimport it. They are hop-2 relative
# to the original canon, so watch round-2 output for topic drift.
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: snowball_r2.sh <outdir>}"
mkdir -p "$OUT"

SEEDS=(
  "10.1007/s10901-006-9050-9"            # Mulder, Home-ownership and family formation
  "10.1023/a:1010706308868"              # Family formation & first-time home ownership, NL
  "10.1002/psp.1716"                     # A Home to Plan the First Child? Italy
  "10.4054/demres.2013.29.14"            # Family dynamics and housing
  "10.4054/demres.2012.27.1"             # Do women delay family formation in expensive housing markets?
  "10.1093/oxfordjournals.esr.a036390"   # Housing tenure and family formation in Britain (1985)
  "10.1080/02673031003771109"            # Housing and Family: An Introduction
)

echo "== resolving round-2 seeds =="
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
