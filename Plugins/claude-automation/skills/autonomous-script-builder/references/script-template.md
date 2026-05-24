# Script Template

This is the canonical skeleton for autonomous scripts produced by this skill. Adapt it to the chosen branches — don't include sections that aren't relevant (e.g. omit the PR step if Q9 said "just modify files").

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# ============================================================
# <SCRIPT_NAME>.sh
# Purpose: <one-line purpose from Q1/Q2>
# Schedule: <cron expression / GH Actions trigger / on-demand>
# Mode: <cron-style | plan-driven | queue-driven | event-driven>
# Companion services: <none | name + how deployed>
# Dependencies: claude CLI, gh CLI, jq, git
# Exit codes: 0=done, 1=error, 2=nothing-to-do, 3=locked
# ============================================================

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# --- Lock acquisition ---
# Variant A: lockfile (local cron)
LOCK_FILE=".claude-lock"
if [[ -f "$LOCK_FILE" ]]; then
  echo "Another run in progress (lock: $LOCK_FILE). Exiting." >&2
  exit 3
fi
trap 'rm -f "$LOCK_FILE"' EXIT
echo "$$ $(date -Iseconds)" > "$LOCK_FILE"

# Variant B: GitHub sentinel label (CI) — replace the above with something like:
# MUTEX_LABEL="<your-mutex-label>"   # e.g. "claude-working"
# if gh issue list --label "$MUTEX_LABEL" --state open | grep -q .; then
#   echo "Another run in progress (label: $MUTEX_LABEL). Exiting." >&2
#   exit 3
# fi
# Apply the label to a sentinel issue/PR while running; remove it on exit.

# --- Pre-flight ---
: "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY must be set}"
command -v claude >/dev/null || { echo "claude CLI not found" >&2; exit 1; }
command -v gh >/dev/null || { echo "gh CLI not found" >&2; exit 1; }

# Ensure clean working tree before starting
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree dirty — refusing to run." >&2
  exit 1
fi

# Sync with remote
git fetch origin
git checkout main
git pull --ff-only origin main

# --- Resource manifest ---
# Tell the agent exactly what's available. Be explicit. Replace the
# placeholders below with actual resources for THIS repo.
RESOURCES=$(cat <<EOF
Available resources:
- ANTHROPIC_API_KEY: present (use for API calls)
- GitHub permissions: can push branches, open PRs, comment on issues
- Repo: $(git remote get-url origin)
- <Optional companion service>: deployed at <PATH or URL> (must be kept in sync)
- Config files: ./config/, ./.env.example
- Important paths:
  * <list paths relevant to this script>
EOF
)

# --- Ledger read ---
LEDGER_FILE="SCOUT.md"   # or PLAN.md, JOURNAL.md depending on mode
if [[ ! -f "$LEDGER_FILE" ]]; then
  {
    echo "# Ledger"
    echo
    echo "## Suggested"
    echo
    echo "## Implemented"
  } > "$LEDGER_FILE"
fi

# --- Implementor: pick work + execute ---
BRANCH_NAME="claude/$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH_NAME"

IMPL_PROMPT=$(cat <<EOF
You are the implementor agent for this repository.

$RESOURCES

Current ledger ($LEDGER_FILE):
$(cat "$LEDGER_FILE")

Your task:
<task description from the interview — e.g. "Pick ONE improvement to implement
this run. Favor small, high-impact changes. Balance new features with fixes.
Update $LEDGER_FILE: move your choice from Suggested to Implemented with a
brief note. Then make the code changes.">

Constraints:
- One logical change only. One commit.
- Update $LEDGER_FILE in the same commit.
- Do not modify <list of off-limits paths>.
- If you cannot find suitable work, exit cleanly without changes.

When done, print a one-line summary prefixed with "SUMMARY: ".
EOF
)

IMPL_OUTPUT=$(claude -p "$IMPL_PROMPT" --output-format text)

# If no changes were made, treat as no-op
if [[ -z "$(git status --porcelain)" ]]; then
  echo "Implementor made no changes. Exiting clean."
  git checkout main
  git branch -D "$BRANCH_NAME"
  exit 2
fi

# --- Capture diff for reviewer ---
DIFF_FILE=$(mktemp)
git diff --staged > "$DIFF_FILE" 2>/dev/null || true
git diff >> "$DIFF_FILE"

# --- Adversarial reviewer ---
REVIEW_PROMPT=$(cat <<EOF
You are an adversarial code reviewer. Your job is to find problems, not to
approve. Look for:
- Bugs and regressions
- Security issues
- Tests that should exist but don't
- Plan-adherence: does the change actually match the stated intent below?
- Hidden complexity, dead code, accidental scope creep

Stated intent from implementor:
$IMPL_OUTPUT

Diff:
$(cat "$DIFF_FILE")

Output a numbered list of concerns. Be specific. If you genuinely find nothing
concerning, say so explicitly — but bias toward finding problems.
EOF
)

REVIEW_OUTPUT=$(claude -p "$REVIEW_PROMPT" --output-format text)
echo "--- Reviewer notes ---"
echo "$REVIEW_OUTPUT"
echo "----------------------"

# --- Implementor verdict on review ---
VERDICT_PROMPT=$(cat <<EOF
You are the implementor. The adversarial reviewer left these notes:

$REVIEW_OUTPUT

You have veto power. For each note, decide:
- ADDRESS — fix it now (then describe the fix)
- DEFER — add to $LEDGER_FILE Suggested section for later
- REJECT — explain why the note doesn't apply

If you choose ADDRESS for any note, make the additional code changes now.
Update $LEDGER_FILE with any deferred items.

Print a final SUMMARY: line.
EOF
)

claude -p "$VERDICT_PROMPT" --output-format text

# --- Commit + push + PR ---
git add -A
git commit -m "$(echo "$IMPL_OUTPUT" | grep '^SUMMARY:' | sed 's/^SUMMARY: //')"
git push -u origin "$BRANCH_NAME"

gh pr create \
  --title "$(git log -1 --pretty=%s)" \
  --body "Autonomous change. Reviewer notes and implementor verdict are in the commit history." \
  --draft   # default to draft — human reviews before merge

# --- Cleanup ---
rm -f "$DIFF_FILE"
git checkout main
echo "Done."
exit 0
```

## Adaptation notes

- **Plan-driven mode**: replace the "pick work" prompt with "read PLAN.md, find the first unchecked item, implement it, check it off". If plan lives in GitHub Issues, swap the ledger read for `gh issue list --label <ready-label> --json number,title,body --limit 1`.
- **Queue-driven mode**: same as plan-driven but loop semantics differ — usually you want one queue item per run, not the whole queue.
- **Event-driven mode**: the script is invoked by the event (GH Actions workflow), so the "pick work" step becomes "read the event payload from $GITHUB_EVENT_PATH". Skip the ledger entirely or use it as a journal.
- **No-commit mode** (Q9 = just modify files): omit `git push`, `gh pr create`, and the branch checkout. Leave changes in the working tree.
- **Direct-to-main mode** (Q9 = direct commit): omit the branch checkout and `gh pr create`; `git push origin main`. Warn the user.
- **Companion deployment** (Q7 = yes): add a "Deploy companion" section after the PR step (or before, depending on coupling). The script should detect the companion's current version and update it in lockstep, and roll back if either side fails.
