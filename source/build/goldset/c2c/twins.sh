#!/bin/bash
# Forward citations accrue to preprint/WP twins on separate DOIs. Same study, split citation set.
# Merging them recovers the true forward frontier. Twins are NOT separate anchors.
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: twins.sh <outdir>}"
TWINS=(
  "10.3386/w17485"        # Dettling & Kearney, NBER WP
  "10.2139/ssrn.1544607"  # Lovenheim & Mumford, SSRN
  "10.3386/w27469"        # Daysal et al., NBER WP
)
for doi in "${TWINS[@]}"; do
  wid=$(curl -s --max-time 40 -G "https://api.openalex.org/works/https://doi.org/$doi" \
    --data-urlencode "mailto=$M" \
    | python3 -c "import json,sys; w=json.load(sys.stdin); print(w['id'].rsplit('/',1)[-1], w.get('cited_by_count'))")
  set -- $wid
  id=$1; nc=$2
  echo "twin $doi -> $id (cited_by=$nc)"
  page=1; : > "$OUT/fwd_twin_$id.jsonl"
  while : ; do
    resp=$(curl -s --max-time 60 -G "https://api.openalex.org/works" \
      --data-urlencode "filter=cites:$id" --data-urlencode "per-page=200" \
      --data-urlencode "page=$page" --data-urlencode "mailto=$M" \
      --data-urlencode "select=id,doi,title,publication_year,type,cited_by_count,primary_location")
    n=$(printf '%s' "$resp" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('results',[])))")
    printf '%s\n' "$resp" >> "$OUT/fwd_twin_$id.jsonl"
    [ "$n" -lt 200 ] && break
    page=$((page+1)); [ "$page" -gt 6 ] && break
  done
done
