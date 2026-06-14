#!/usr/bin/env bash
#
# ticket.sh — thin helper for the branch-per-ticket (Mode B) workflow.
#
# It runs the error-prone, repetitive git parts of the loop so contributors spend
# their time on research, not on git. It only wraps `git` (and optional `gh`); the
# judgment parts are left to you: moving the ticket's row on the QUEUE.md board and
# writing the `## Log` (Result + Workflow impact). The full loop and the Mode A
# fallback are documented in tickets/README.md; the decision is in
# decisions/2026-06-14-collab-system-design.md.
#
# Usage:
#   scripts/ticket.sh claim  NNN   # sync main, create+push NNN-slug branch, mark ticket in-progress
#   scripts/ticket.sh submit NNN   # push the branch and open a PR into main (uses gh if present)
#   scripts/ticket.sh close  NNN   # mark ticket done, then merge + delete the branch
#
# NNN may be given padded or not: "8" and "008" both resolve to TICK-008.
#
set -euo pipefail

die() { printf 'ticket.sh: %s\n' "$1" >&2; exit 1; }

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

case "$cmd" in
  claim)
    git checkout main
    git pull --ff-only
    if git ls-remote --exit-code --heads origin "$branch" >/dev/null 2>&1; then
      die "branch $branch already exists on origin — TICK-$num is already claimed"
    fi
    git checkout -b "$branch"
    set_status "in-progress"
    git add "$ticket"
    git commit -m "claim TICK-$num"
    git push -u origin "$branch"
    cat <<EOF

Claimed TICK-$num on branch '$branch'.
Now, by hand:
  1. Add its row to the In progress board in tickets/QUEUE.md (owner, branch, UTC).
  2. Do the work, committing as you go.
  3. Write the ## Log (Result + Workflow impact) before running 'close'.
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
