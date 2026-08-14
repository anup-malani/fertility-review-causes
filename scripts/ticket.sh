#!/usr/bin/env bash
#
# ticket.sh — thin helper for the branch-per-ticket (Mode B) workflow.
#
# It runs the error-prone, repetitive parts of the loop so contributors spend
# their time on research, not on bookkeeping. It wraps `git` (and optional `gh`) and
# edits the two files a claim has to touch: the ticket and the QUEUE.md board. The
# judgment parts are left to you: which ticket to take, and the `## Log` you write
# before closing (Result + Workflow impact). The full loop and the Mode A fallback
# are documented in tickets/README.md; the decision is in
# decisions/2026-06-14-collab-system-design.md.
#
# Usage:
#   scripts/ticket.sh claim  NNN   # sync, preflight, branch, mark in-progress, move the board row
#   scripts/ticket.sh submit NNN   # push the branch and open a PR into main (uses gh if present)
#   scripts/ticket.sh close  NNN   # mark ticket done, then merge + delete the branch
#
# NNN may be given padded or not: "8" and "008" both resolve to TICK-008.
#
set -euo pipefail

die() { printf 'ticket.sh: %s\n' "$1" >&2; exit 1; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

cmd="${1:-}"
raw="${2:-}"
case "$cmd" in
  claim|submit|close) ;;
  *) die "usage: ticket.sh {claim|submit|close} NNN" ;;
esac
[ -n "$raw" ] || die "missing ticket number (e.g. 8 or 008)"
case "$raw" in *[!0-9]*) die "not a ticket number: $raw" ;; esac
num=$(printf '%03d' "$((10#$raw))")

root=$(git rev-parse --show-toplevel 2>/dev/null) || die "not inside a git repo"
cd "$root"

queue=tickets/QUEUE.md

# Locate the ticket file and derive the branch name from it.
shopt -s nullglob
matches=(tickets/TICK-"$num"-*.md)
shopt -u nullglob
[ "${#matches[@]}" -eq 1 ] || die "expected exactly one tickets/TICK-$num-*.md, found ${#matches[@]}"
ticket="${matches[0]}"
# Branch name = the ticket number + slug, lowercased, with the TICK- prefix dropped.
# e.g. TICK-008-collab-system-design -> 008-collab-system-design
branch=$(basename "$ticket" .md | sed -E 's/^TICK-//' | tr '[:upper:]' '[:lower:]')

# Replace the first "**Status:** ..." line in the ticket (portable across GNU/BSD sed).
set_status() {
  sed -i.bak -E "s/^\*\*Status:\*\*.*/**Status:** $1/" "$ticket"
  rm -f "$ticket.bak"
}

# Read a "**Field:** value" line out of the ticket. Prints the value, or nothing.
ticket_field() {
  sed -n -E "s/^\*\*$1:\*\*[[:space:]]*//p" "$ticket" | head -1
}

case "$cmd" in
  claim)
    # ---------------------------------------------------------------------
    # Preflight. Everything that can refuse the claim runs before the branch
    # is created, so a rejected claim leaves the repo exactly as it found it.
    # ---------------------------------------------------------------------
    [ -z "$(git status --porcelain)" ] || die "working tree is dirty — commit or stash first"
    [ -f "$queue" ] || die "$queue not found"
    # Scratch files live next to QUEUE.md; make sure a failed run cannot leave one
    # behind to trip the clean-tree check on the next claim.
    trap 'rm -f "$queue.tmp" "$queue.outcome"' EXIT

    git checkout --quiet main
    git pull --quiet --ff-only
    ok "main synced, tree clean"

    if git ls-remote --exit-code --heads origin "$branch" >/dev/null 2>&1; then
      die "branch $branch already exists on origin — TICK-$num is already claimed"
    fi
    ok "no $num-* branch on origin"

    # Fields the board row is built from. Title comes from the H1 rather than the
    # existing Open row, because a row wrapped across two physical lines (as
    # TICK-063's is) cannot be re-read reliably.
    title=$(sed -n -E "s/^# TICK-$num:[[:space:]]*//p" "$ticket" | head -1)
    [ -n "$title" ] || die "$ticket has no '# TICK-$num: <title>' heading"
    owner=$(ticket_field "Assigned")
    [ -n "$owner" ] || die "$ticket has no '**Assigned:**' line"
    touches=$(ticket_field "Touches")
    [ -n "$touches" ] || warn "$ticket has no '**Touches:**' line — overlap check skipped"
    grep -q '^## Log' "$ticket" || warn "$ticket has no ## Log heading — 'close' will refuse it later"

    # Overlap warning against live In-progress rows. Advisory only: overlapping
    # Touches is common and legitimate, it just needs to be a decision rather
    # than a surprise. This reads the board, so it also sees the Mode A rows
    # whose Branch column is "—" and which no origin branch would reveal.
    if [ -n "$touches" ]; then
      overlaps=$(
        NUM="$num" TOUCHES="$touches" awk '
          # Reduce a path to a comparison key: its directory plus the first three
          # hyphen-groups of its basename. That is coarse enough to see that
          # extraction/<slug>-ra-gate.csv and extraction/<slug>-fulltext.csv are the
          # same workstream, and specific enough not to collide two hypotheses that
          # merely share a directory.
          function key(t,   d, b, p, n, i, r) {
            gsub(/[`,;]/, "", t); sub(/\{.*$/, "", t); sub(/\*.*$/, "", t)
            if (t == "") return ""
            if (match(t, /^.*\//)) { d = substr(t, 1, RLENGTH); b = substr(t, RLENGTH + 1) }
            else                   { d = "";                   b = t }
            n = split(b, p, "-"); r = ""
            for (i = 1; i <= n && i <= 3; i++) r = (r == "" ? p[i] : r "-" p[i])
            return d r
          }
          function shares(a, b) { return (a != "" && b != "" && (index(a, b) == 1 || index(b, a) == 1)) }
          BEGIN { insec = 0; mine_n = 0
                  gsub(/[`,;]/, " ", ENVIRON["TOUCHES"])
                  split(ENVIRON["TOUCHES"], raw, /[ \t]+/)
                  for (i in raw) { k = key(raw[i]); if (length(k) > 3) mine[++mine_n] = k } }
          /^## / { insec = ($0 ~ /^## In progress/) }
          insec && /^\| \[TICK-/ {
            if ($0 ~ ("^\\| \\[TICK-" ENVIRON["NUM"] "\\]")) next
            if (match($0, /^\| \[TICK-[0-9]+\]/)) other = substr($0, RSTART + 3, RLENGTH - 4)
            # Compare against the Touches column only. Titles quote paths too, and
            # matching those produces overlaps that are not real.
            n = split($0, cells, "|"); if (n < 3) next
            gsub(/[`,;]/, " ", cells[n - 1])
            split(cells[n - 1], theirs, /[ \t]+/)
            for (i in theirs) {
              tk = key(theirs[i]); if (length(tk) <= 3) continue
              for (j = 1; j <= mine_n; j++)
                if (shares(mine[j], tk)) { print other " on " tk; next_row = 1; break }
              if (next_row) { next_row = 0; next }
            }
          }
        ' "$queue"
      )
      if [ -n "$overlaps" ]; then
        while IFS= read -r line; do warn "Touches overlap: $line"; done <<<"$overlaps"
      else
        ok "Touches overlap: none"
      fi
    fi

    # ---------------------------------------------------------------------
    # Mutate. Past this point the claim is going through.
    # ---------------------------------------------------------------------
    stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    git checkout --quiet -b "$branch"
    ok "branch $branch created"

    set_status "in-progress"
    ok "status → in-progress"

    # Make the values safe to drop into a markdown table cell: a bare `|` would end
    # the cell, and an unquoted Touches list with two `*` globs renders as italics.
    cell_title=${title//|/\\|}
    cell_touches=${touches//|/\\|}
    case "$cell_touches" in
      ""|*'`'*) ;;
      *) cell_touches="\`$cell_touches\`" ;;
    esac

    # A Mode A claim leaves an In-progress row with no branch behind it, which the
    # origin-branch check above cannot see. If one is already there this is a
    # takeover: update that row's Branch and Claimed cells in place rather than
    # writing a second row for the same ticket.
    insert=1
    if NUM="$num" awk '
         /^## / { insec = ($0 ~ /^## In progress/) }
         insec && $0 ~ ("^\\| \\[TICK-" ENVIRON["NUM"] "\\]") { found = 1 }
         END { exit !found }' "$queue"; then
      insert=0
      warn "TICK-$num already has an In-progress row — updating it in place (takeover)"
    fi

    # Move the row from Open (or Blocked) to In progress. A row is swallowed until
    # it has the 5 pipes of a complete 4-column row, so a row wrapped across two
    # physical lines is removed whole. The new row is built from the ticket, not
    # from the old row's text. The outcome is reported via $queue.outcome so the
    # summary printed below says what actually happened.
    NUM="$num" FILE="$(basename "$ticket")" TITLE="$cell_title" OWNER="$owner" \
    BRANCH="$branch" STAMP="$stamp" TOUCHES="$cell_touches" INSERT="$insert" \
    OUTCOME="$queue.outcome" \
      awk '
        BEGIN { sec = ""; swallow = 0; pipes = 0; inserted = 0; removed = 0; updated = 0 }
        function count(s,   c, i) { c = 0; for (i = 1; i <= length(s); i++) if (substr(s, i, 1) == "|") c++; return c }
        # Swallow the remaining physical lines of a wrapped row.
        swallow { pipes += count($0); if (pipes >= 5) swallow = 0; next }
        /^## / { if ($0 ~ /^## Open/)        sec = "open"
                 else if ($0 ~ /^## In progress/) sec = "prog"
                 else if ($0 ~ /^## Blocked/)     sec = "blocked"
                 else                             sec = "other" }
        # Drop the existing row wherever it is claimable from.
        (sec == "open" || sec == "blocked") && $0 ~ ("^\\| \\[TICK-" ENVIRON["NUM"] "\\]") {
          removed = 1; pipes = count($0); if (pipes < 5) swallow = 1; next }
        # Takeover: refresh Branch and Claimed on the row that is already there, so
        # the board stops showing a claim with no branch behind it.
        sec == "prog" && ENVIRON["INSERT"] == "0" && $0 ~ ("^\\| \\[TICK-" ENVIRON["NUM"] "\\]") {
          n = split($0, c, "|")
          if (n == 8) {
            c[5] = " `" ENVIRON["BRANCH"] "` "; c[6] = " " ENVIRON["STAMP"] " "
            line = ""; for (i = 2; i <= n - 1; i++) line = line "|" c[i]
            print line "|"; updated = 1; next
          }
        }
        { print }
        # Insert directly under the In-progress header divider.
        sec == "prog" && !inserted && ENVIRON["INSERT"] == "1" && /^\|[-]+\|/ {
          inserted = 1
          printf "| [TICK-%s](%s) | %s | %s | `%s` | %s | %s |\n",
            ENVIRON["NUM"], ENVIRON["FILE"], ENVIRON["TITLE"], ENVIRON["OWNER"],
            ENVIRON["BRANCH"], ENVIRON["STAMP"], ENVIRON["TOUCHES"]
        }
        END { print (removed ? "removed" : "-") " " (inserted ? "inserted" : (updated ? "updated" : "-")) > ENVIRON["OUTCOME"]
              if (!inserted && !updated && ENVIRON["INSERT"] == "1")
                print "ticket.sh: warning: could not find the In-progress table to insert into" > "/dev/stderr" }
      ' "$queue" > "$queue.tmp"
    mv "$queue.tmp" "$queue"
    read -r did_remove did_add < "$queue.outcome"; rm -f "$queue.outcome"

    case "$did_remove/$did_add" in
      removed/inserted) ok "QUEUE.md: row moved Open → In progress" ;;
      -/inserted)       ok "QUEUE.md: In-progress row added (no Open row existed)" ;;
      */updated)        ok "QUEUE.md: existing In-progress row updated" ;;
      *)                warn "QUEUE.md: board unchanged — move the row by hand" ;;
    esac
    printf '      branch  %s\n      claimed %s\n' "$branch" "$stamp"

    git add "$ticket" "$queue"
    git commit --quiet -m "claim TICK-$num"
    git push --quiet -u origin "$branch"
    ok "pushed — the branch is the claim"

    cat <<EOF

Claimed TICK-$num on branch '$branch'.
Next:
  1. Do the work, committing as you go.
  2. Write the ## Log (Result + Workflow impact) before running 'close'.
Then: scripts/ticket.sh submit $num   (open the PR)
EOF
    ;;

  submit)
    cur=$(git rev-parse --abbrev-ref HEAD)
    [ "$cur" = "$branch" ] || die "you are on '$cur', not '$branch' — checkout the ticket branch first"
    git push -u origin "$branch"
    if command -v gh >/dev/null 2>&1; then
      gh pr create --base main --head "$branch" --fill || gh pr view "$branch" --web
    else
      echo "gh CLI not found. Open a PR manually on GitHub: base 'main' <- '$branch'."
    fi
    ;;

  close)
    cur=$(git rev-parse --abbrev-ref HEAD)
    [ "$cur" = "$branch" ] || die "you are on '$cur', not '$branch' — checkout the ticket branch first"
    grep -q '^## Log' "$ticket" || die "$ticket has no ## Log section — write Result + Workflow impact first"
    set_status "done"
    git add "$ticket"
    git commit -m "close TICK-$num" || echo "(nothing new to commit)"
    git push origin "$branch"
    if command -v gh >/dev/null 2>&1; then
      gh pr merge "$branch" --merge --delete-branch
    else
      echo "gh CLI not found. Merge the PR for '$branch' into main, then:"
      echo "  git checkout main && git pull && git branch -d $branch && git push origin --delete $branch"
      exit 0
    fi
    git checkout main
    git pull --ff-only
    cat <<EOF

Closed TICK-$num (merged and branch deleted).
Don't forget: move its row to the Done section in tickets/QUEUE.md.
EOF
    ;;
esac
