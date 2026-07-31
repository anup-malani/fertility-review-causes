#!/bin/bash
# Channel-3 snowball, SECOND MECHANICAL CONFIRMING ROUND for C.2.c (round 5).
#
# Round 4 returned 0.48 new relevant per 50 pulled -- below the §7.2 floor of 1.0. The rule requires
# TWO CONSECUTIVE below-floor rounds, so this round exists solely to complete the test.
#
# Same mechanical design as round 4: seed from every current Tier-B frame member not already used as
# a seed in rounds 1-4. Selection is by membership, never by judgement -- that is what makes the
# reading a measure of exhaustion rather than of RA imagination.
#
# NOTE: the frame this seeds from is the CORRECTED one (231 members, after the relevance-filter fix).
# Round 4's seed list came from the pre-correction frame, so some of its seeds were false positives;
# that does not invalidate round 4 -- extra seeds can only have made its yield reading more generous,
# and it still came in below floor.
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: snowball_r5.sh <outdir>}"
R4_SEEDS="${2:?usage: snowball_r5.sh <outdir> <round4_seed_ids.txt>}"
FRAME="literature/search-logs/housing-costs-tier-b-frame.json"
mkdir -p "$OUT"

NAMED_USED="W3024244835 W2017790450 W3037455063 W3131143603 W2037422701 W2035671284 W1578574739
W2125780906 W2065377959 W1509700920 W2131771089 W2532821622 W2099386106 W2129646919
W4395481274 W3217487213 W4392854776 W1693336056 W3028664058 W4399107829 W2086486830 W2132599910"

python3 - "$FRAME" "$OUT" "$R4_SEEDS" "$NAMED_USED" <<'PY'
import json, os, sys
frame, out, r4path, named = sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4].split())
used = set(named)
if os.path.exists(r4path):
    used |= {ln.strip() for ln in open(r4path) if ln.strip()}
ids = [r["openalex"] for r in json.load(open(frame)) if r["openalex"] not in used]
open(out + "/seed_ids.txt", "w").write("\n".join(ids))
print(f"round-5 seeds: {len(ids)} (frame members not seeded in rounds 1-4; {len(used)} already used)")
PY

echo "== backward refs =="
: > "$OUT/backrefs_all.txt"
n=0
while read -r wid; do
  curl -s --max-time 40 "https://api.openalex.org/works/$wid?mailto=$M" \
    | python3 -c "
import json,sys
try: w=json.load(sys.stdin)
except Exception: sys.exit()
for r in (w.get('referenced_works') or []): print(r.rsplit('/',1)[-1])
" >> "$OUT/backrefs_all.txt"
  n=$((n+1)); [ $((n % 25)) -eq 0 ] && echo "  ...$n seeds"
done < "$OUT/seed_ids.txt"
echo "  backward refs collected: $(wc -l < "$OUT/backrefs_all.txt")"

echo "== forward citations =="
: > "$OUT/fwd_all.jsonl"
n=0
while read -r wid; do
  page=1
  while : ; do
    resp=$(curl -s --max-time 60 -G "https://api.openalex.org/works" \
      --data-urlencode "filter=cites:$wid" --data-urlencode "per-page=200" \
      --data-urlencode "page=$page" --data-urlencode "mailto=$M" \
      --data-urlencode "select=id,doi,title,publication_year,type,cited_by_count,primary_location")
    cnt=$(printf '%s' "$resp" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null || echo 0)
    printf '%s\n' "$resp" >> "$OUT/fwd_all.jsonl"
    [ "$cnt" -lt 200 ] && break
    page=$((page+1)); [ "$page" -gt 3 ] && break
  done
  n=$((n+1)); [ $((n % 25)) -eq 0 ] && echo "  ...$n seeds"
done < "$OUT/seed_ids.txt"
echo "round-5 pull complete"
