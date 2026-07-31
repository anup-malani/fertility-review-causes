#!/bin/bash
# Channel-3 citation snowball for C.2.c.
# Seeds MUST be channel-1/2 only (canon), never keyword-scouted, or Tier B becomes circular.
# Backward: all referenced_works, <=1 hop. Forward: works citing the seed, <=1 hop, topic-specific seeds.
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: snowball.sh <outdir>}"
mkdir -p "$OUT"

SEEDS=(
  "10.1080/02673031003711469"
  "10.1016/j.jpubeco.2013.09.009"
  "10.1162/rest_a_00266"
  "10.1016/j.jpubeco.2021.104366"
)

echo "== resolving seeds =="
: > "$OUT/seeds.tsv"
for doi in "${SEEDS[@]}"; do
  curl -s --max-time 40 -G "https://api.openalex.org/works/https://doi.org/$doi" \
    --data-urlencode "mailto=$M" > "$OUT/seed_$(echo "$doi" | tr '/.' '__').json"
done

python3 - "$OUT" <<'PY'
import glob, json, os, sys
out = sys.argv[1]
rows = []
for f in sorted(glob.glob(os.path.join(out, "seed_*.json"))):
    w = json.load(open(f))
    wid = w["id"].rsplit("/", 1)[-1]
    rows.append((wid, w.get("doi", ""), len(w.get("referenced_works") or []), w.get("cited_by_count"), (w.get("title") or "")[:60]))
    json.dump(w.get("referenced_works") or [], open(os.path.join(out, f"back_{wid}.json"), "w"))
with open(os.path.join(out, "seeds.tsv"), "w") as fh:
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")
        print("seed", r[0], "backrefs=", r[2], "fwd=", r[3], r[4])
PY

echo "== forward citations =="
while IFS=$'\t' read -r wid doi nback nfwd title; do
  page=1
  : > "$OUT/fwd_$wid.jsonl"
  while : ; do
    resp=$(curl -s --max-time 60 -G "https://api.openalex.org/works" \
      --data-urlencode "filter=cites:$wid" --data-urlencode "per-page=200" \
      --data-urlencode "page=$page" --data-urlencode "mailto=$M" \
      --data-urlencode "select=id,doi,title,publication_year,type,cited_by_count,primary_location")
    n=$(printf '%s' "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('results',[])))")
    printf '%s\n' "$resp" >> "$OUT/fwd_$wid.jsonl"
    [ "$n" -lt 200 ] && break
    page=$((page+1))
    [ "$page" -gt 6 ] && break
  done
  echo "  fwd $wid pages=$page"
done < "$OUT/seeds.tsv"
echo "done"
