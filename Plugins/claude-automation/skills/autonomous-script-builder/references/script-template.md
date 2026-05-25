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

# --- Persistent state files ---
LEDGER_FILE="SCOUT.md"                # or PLAN.md, JOURNAL.md depending on mode
REVIEW_HISTORY_FILE="REVIEW_HISTORY.md"   # append-only log of reviewer notes + verdicts
LEARNINGS_FILE="LEARNINGS.md"             # distilled signal from ADDRESSED notes
LEARN_EVERY=5                              # run the distiller every N runs

if [[ ! -f "$LEDGER_FILE" ]]; then
  {
    echo "# Ledger"
    echo
    echo "## Suggested"
    echo
    echo "## Implemented"
  } > "$LEDGER_FILE"
fi
[[ -f "$REVIEW_HISTORY_FILE" ]] || echo "# Review History" > "$REVIEW_HISTORY_FILE"
[[ -f "$LEARNINGS_FILE" ]] || {
  {
    echo "# Implementor Learnings"
    echo
    echo "_Distilled from adversarial review notes the implementor accepted (ADDRESS verdict)."
    echo "Read by every run. Updated every $LEARN_EVERY runs._"
    echo
  } > "$LEARNINGS_FILE"
}

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

Past learnings ($LEARNINGS_FILE — distilled from adversarial reviews; apply these proactively):
$(cat "$LEARNINGS_FILE")
EOF
)

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

# --- Commit + push + open draft PR (BEFORE review, so reviewer can comment on it) ---
git add -A
git commit -m "$(echo "$IMPL_OUTPUT" | grep '^SUMMARY:' | sed 's/^SUMMARY: //')"
git push -u origin "$BRANCH_NAME"

PR_URL=$(gh pr create \
  --title "$(git log -1 --pretty=%s)" \
  --body "Autonomous change. Adversarial review will be posted as a PR comment shortly." \
  --draft)
PR_NUMBER="${PR_URL##*/}"
echo "Opened draft PR: $PR_URL"

# --- Capture diff from the PR for the reviewer ---
DIFF_FILE=$(mktemp)
gh pr diff "$PR_NUMBER" > "$DIFF_FILE"

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

Diff (from PR #$PR_NUMBER):
$(cat "$DIFF_FILE")

Output a GitHub-flavored markdown comment with a numbered list of concerns.
Be specific. Reference file paths and line numbers where you can. If you
genuinely find nothing concerning, say so explicitly — but bias toward finding
problems.
EOF
)

REVIEW_OUTPUT=$(claude -p "$REVIEW_PROMPT" --output-format text)

# Post the review onto the PR as a comment so a human can see it in context
gh pr comment "$PR_NUMBER" --body "$(cat <<EOF
## Adversarial review

$REVIEW_OUTPUT
EOF
)"

# --- Implementor verdict on review ---
VERDICT_PROMPT=$(cat <<EOF
You are the implementor. The adversarial reviewer left these notes on
PR #$PR_NUMBER:

$REVIEW_OUTPUT

You have veto power. For each note, decide:
- ADDRESS — fix it now (then describe the fix)
- DEFER — add to $LEDGER_FILE Suggested section for later
- REJECT — explain why the note doesn't apply

If you choose ADDRESS for any note, make the additional code changes now.
Update $LEDGER_FILE with any deferred items.

Output a GitHub-flavored markdown comment with EXACTLY this structure so the
distiller can parse it later:

### Addressed
- <note summary> — <fix you made>
- ...

### Deferred
- <note summary> — <why deferred>
- ...

### Rejected
- <note summary> — <why doesn't apply>
- ...

SUMMARY: <one-line summary>

If a section has no items, write "_none_" beneath the heading. Keep section
headings exactly as shown.
EOF
)

VERDICT_OUTPUT=$(claude -p "$VERDICT_PROMPT" --output-format text)

# If the verdict step made additional code changes, commit & push as a follow-up
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "address adversarial review on PR #$PR_NUMBER"
  git push origin "$BRANCH_NAME"
fi

# Post the verdict onto the PR
gh pr comment "$PR_NUMBER" --body "$(cat <<EOF
## Implementor verdict

$VERDICT_OUTPUT
EOF
)"

# --- Append this run to REVIEW_HISTORY.md (source signal for the distiller) ---
{
  echo
  echo "## Run $(date -Iseconds) — PR #$PR_NUMBER"
  echo
  echo "### Reviewer notes"
  echo
  echo "$REVIEW_OUTPUT"
  echo
  echo "### Implementor verdict"
  echo
  echo "$VERDICT_OUTPUT"
} >> "$REVIEW_HISTORY_FILE"

# --- Every LEARN_EVERY runs, distill ADDRESSED notes into LEARNINGS.md ---
# `|| true` neutralises grep's exit 1 when there are no matches yet (set -e safety).
RUN_COUNT=$(grep -c '^## Run ' "$REVIEW_HISTORY_FILE" 2>/dev/null || true)
RUN_COUNT=${RUN_COUNT:-0}
if (( RUN_COUNT > 0 && RUN_COUNT % LEARN_EVERY == 0 )); then
  echo "Run #$RUN_COUNT — invoking distiller (every $LEARN_EVERY runs)"

  # Slice the last LEARN_EVERY run entries from REVIEW_HISTORY.md
  START_RUN=$((RUN_COUNT - LEARN_EVERY + 1))
  START_LINE=$(grep -n '^## Run ' "$REVIEW_HISTORY_FILE" | sed -n "${START_RUN}p" | cut -d: -f1)
  RECENT_HISTORY=$(sed -n "${START_LINE},\$p" "$REVIEW_HISTORY_FILE")

  DISTILL_PROMPT=$(cat <<EOF
You are the distiller. Read the last $LEARN_EVERY runs of adversarial review +
implementor verdict below, and update $LEARNINGS_FILE.

Focus on the "### Addressed" sections — those are notes the implementor agreed
with and fixed. They reveal what the implementor consistently misses on the
first pass. DEFER and REJECT entries are context only.

Recent history (last $LEARN_EVERY runs):
$RECENT_HISTORY

Current $LEARNINGS_FILE:
$(cat "$LEARNINGS_FILE")

Rules:
- One terse line per learning, imperative voice ("Always update CHANGELOG when
  bumping versions", "Don't add deps without checking license").
- Only add a learning if a pattern appears in at least 2 of the last
  $LEARN_EVERY runs, OR a single Addressed note represents a serious quality
  issue worth preempting.
- Refine wording of existing learnings if recent evidence sharpens them.
- Remove learnings that haven't been triggered in the recent window and look
  stale or wrong.
- Cap the file at ~20 learnings. If pruning is needed, drop the oldest /
  weakest signals.

Output the FULL new contents of $LEARNINGS_FILE (the bash script overwrites
the file with your output). Preserve the header. End with a comment line:
_Last updated: $(date -Iseconds) (run #$RUN_COUNT)_
EOF
)

  claude -p "$DISTILL_PROMPT" --output-format text > "$LEARNINGS_FILE"
  echo "Distiller updated $LEARNINGS_FILE"
fi

# Commit the history + learnings update onto the PR branch
if [[ -n "$(git status --porcelain "$REVIEW_HISTORY_FILE" "$LEARNINGS_FILE")" ]]; then
  git add "$REVIEW_HISTORY_FILE" "$LEARNINGS_FILE"
  git commit -m "update review history + learnings (run #$RUN_COUNT)"
  git push origin "$BRANCH_NAME"
fi

# --- Cleanup ---
rm -f "$DIFF_FILE"
git checkout main
echo "Done. PR: $PR_URL"
exit 0
```

## Adaptation notes

- **Plan-driven mode**: replace the "pick work" prompt with "read PLAN.md, find the first unchecked item, implement it, check it off". If plan lives in GitHub Issues, swap the ledger read for `gh issue list --label <ready-label> --json number,title,body --limit 1`.
- **Queue-driven mode**: same as plan-driven but loop semantics differ — usually you want one queue item per run, not the whole queue.
- **Event-driven mode**: the script is invoked by the event (GH Actions workflow), so the "pick work" step becomes "read the event payload from $GITHUB_EVENT_PATH". Skip the ledger entirely or use it as a journal.
- **No-commit mode** (Q9 = just modify files): omit `git push`, `gh pr create`, and the branch checkout. The reviewer can't post to a PR (none exists) — print its notes to stdout instead of `gh pr comment`. Verdict prints to stdout too.
- **Direct-to-main mode** (Q9 = direct commit): omit the branch checkout and `gh pr create`; `git push origin main`. Warn the user. As with no-commit mode, the reviewer prints to stdout (no PR to comment on). If the user wants the reviewer's notes preserved, write them into the commit message trailer or a sibling log file.
- **Companion deployment** (Q7 = yes): add a "Deploy companion" section after the PR step (or before, depending on coupling). The script should detect the companion's current version and update it in lockstep, and roll back if either side fails.
