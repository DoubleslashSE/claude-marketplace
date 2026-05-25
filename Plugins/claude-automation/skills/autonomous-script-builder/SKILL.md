---
name: autonomous-script-builder
description: Use this skill whenever the user wants to create a bash script that drives an autonomous coding loop — scripts that run Claude Code on a schedule (cron, GitHub Actions, systemd timer) or on-demand to make repository improvements, execute plans, triage issues, or otherwise do agentic work with minimal human intervention. Triggers include phrases like "scout script", "autonomous script", "agent harness", "script that runs on a schedule", "script that implements a plan", ".scripts/*.sh", or any request for a bash script whose body is "run Claude Code with a prompt and commit the results". Always use this skill before writing such a script — it encodes the interview flow, the adversarial-reviewer pattern, and the locking/ledger conventions.
---

# Autonomous Script Builder

A skill for generating bash scripts that drive Claude Code in autonomous loops. The output is a single `.sh` file (plus a sibling `*.DECISIONS.md` recording the choices made) that the user can drop into a scripts directory and run on a schedule.

## When to use this skill

Use when the user asks for any script whose job is "wake up, figure out what to do, ask Claude Code to do it, commit the result." Examples that should trigger this skill:

- "I want a scout script that picks one improvement per run and implements it"
- "Write me a script that implements the plan in PLAN.md"
- "I need a script that picks up GitHub issues with a specific label and works them"
- "Make a CI failure handler that files an issue when the build breaks"
- "A nightly script that updates dependencies and opens a PR"

If the user just wants a one-shot bash script with no agent loop, this skill is overkill — write the script directly.

## Core conventions (always apply, no interview needed)

These are invariants. Every script this skill produces includes them.

1. **Strict bash** — `#!/usr/bin/env bash`, `set -euo pipefail`, `IFS=$'\n\t'`.
2. **Adversarial reviewer is on by default, and posts to the PR.** When the script opens a PR (Q9 default), the flow is: implementor commits → push → open draft PR → adversarial reviewer reads the PR diff and posts findings as a PR comment via `gh pr comment` → implementor verdict (ADDRESS / DEFER / REJECT each note, possibly with follow-up commits) is posted as a second PR comment. This way a human reviewer sees both the adversarial notes and the implementor's response in context on the PR itself, not buried in script logs. The implementor has veto power — not every note must be implemented. For no-commit or direct-to-main modes (no PR exists), the reviewer prints to stdout instead. Only skip the reviewer entirely if the user explicitly says "no review" and confirms.
3. **Mutex/lock** — pick a strategy in the interview (sentinel label in CI, lockfile on disk for local runs). Never run two instances concurrently.
4. **Resource manifest** — the script must explicitly tell the agent what resources exist (env vars present, API keys available, services reachable, paths to important files). Don't make the agent guess. A `cat <<EOF` block listing resources goes into the prompt.
5. **Ledger file** — every script maintains a markdown ledger appropriate to its mode (see branches below). Append-only where possible.
6. **One unit of work per run** — unless the user explicitly wants "run until done", one invocation = one logical change = one commit = one PR (or one push to a branch). Easier to roll back, easier to review.
7. **Companion-service awareness** — if the target system depends on a sidecar or host agent that must move in lockstep with the main deployable, the script should either deploy it too or surface the dependency loudly. Many autonomous-improvement scripts touch code that has a runtime companion; ignoring it leads to version skew.
8. **Exit codes** — 0 = work done, 1 = error, 2 = nothing to do (clean no-op), 3 = locked (another run in progress). Schedulers and CI care about this.
9. **Decisions record** — emit a `*.DECISIONS.md` next to the script recording which branches the interview took and why. Future maintainers (and future-you) will need this.
10. **Learnings loop (self-improvement).** Every script maintains two extra state files: `REVIEW_HISTORY.md` (append-only — verbatim reviewer notes + implementor verdict per run) and `LEARNINGS.md` (distilled signal). Every `LEARN_EVERY` runs (default 5), a fourth Claude invocation — the *distiller* — reads the last 5 history entries and updates `LEARNINGS.md` with recurring patterns from the implementor's `### Addressed` notes. Every implementor prompt then includes `LEARNINGS.md` in its resource manifest, so the loop self-corrects over time. The verdict prompt must emit structured `### Addressed` / `### Deferred` / `### Rejected` sections so the distiller can separate signal from noise.

## The interview

Before writing anything, run the interview below. **Skip any question whose answer is already in the conversation** — don't re-ask things the user already said. State the inferred answer and move on. If the user has given a long brief, extract everything you can from it first and only ask what's genuinely ambiguous.

Use the `ask_user_input_v0` tool for the questions when possible — it's faster than typing on mobile.

### Q1 — Trigger model (required, almost always ask)

How does this script get invoked?

- **Cron-style / scheduled autonomous** — runs on a timer, picks its own work each time (e.g. a "scout" that finds and implements improvements)
- **Plan-driven** — there's a specific plan somewhere, run until it's complete (or one step per run)
- **Queue-driven** — picks up items from a queue (GitHub issues with a label, files in a directory, rows in a table)
- **Event-driven** — fires in response to something (CI failure, webhook, new PR)

This is the master switch. Subsequent questions branch off it.

### Q2 — Work selection (only if Q1 = cron-style or queue-driven)

How does the agent choose what to do?

- **Agent decides from a ledger of candidates** — the ledger has "suggested" and "implemented" sections, agent picks next
- **Queue order** — FIFO, oldest issue first, etc.
- **Priority rules** — e.g. small-high-impact before large-low-impact; explicitly state the heuristic
- **Random from eligible set**

If the user has already described a heuristic ("favor small changes with high impact", "balance features and fixes"), encode it directly and don't re-ask.

### Q3 — Plan location (only if Q1 = plan-driven)

Where does the plan live? Multiple answers OK:

- **A single `.md` file at a known path** (e.g. `PLAN.md`, `docs/roadmap.md`)
- **Multiple `.md` files in a directory** (e.g. `plans/*.md`, agent picks which)
- **GitHub Issues** (filter by label, milestone, or assignee)
- **GitHub Project board** (specific column)
- **A mix** — explicitly enumerate sources and the order to check them

If the user is unsure, ask follow-ups: "Is the plan already written? Where is it now? Should the script look in more than one place?"

### Q4 — Completion criterion (always ask)

When is the script "done" for this run?

- **One unit of work, then exit** (default — recommended)
- **Run until plan complete** (loops until no more checkboxes / no more candidates)
- **Run for N minutes / N iterations**
- **Run until a specific condition** (e.g. tests pass, ledger empty)

Default to "one unit of work" unless the user pushes back. It's safer and easier to debug.

### Q5 — Adversarial reviewer scope (sometimes ask)

The reviewer is on by default. Confirm scope:

- **Diff review only** — reviewer sees the diff, comments on code quality, bugs, regressions
- **Diff + plan adherence** (default) — reviewer also checks whether the change matches the stated intent
- **Diff + security pass** — reviewer specifically looks for security issues

If unsure, default to "diff + plan adherence" — it catches the most common failure mode (agent doing something different from what it said it would do).

### Q6 — Mutex strategy (ask if not obvious from Q1)

- **GitHub sentinel label** — a label like `claude-working` (or any name) applied to a sentinel issue/PR while the script runs; good for CI/Actions
- **Lockfile on disk** — a `.claude-lock` file (or similar) at the repo root; good for local cron
- **None** — only if user is sure concurrent runs are fine

### Q7 — Companion deployment (ask only if relevant)

Does this system depend on a sidecar, host agent, or external service that should be deployed alongside?

- **Yes — deploy together** (script handles both)
- **Yes — but managed separately** (note it loudly in the script's header comment so future maintainers know)
- **No**

If the target sounds like a deployable application with a runtime companion (dashboards with host agents, services with sidecars, anything that runs as a pair), ask.

### Q8 — Resources available to the agent (always ask, brief)

What does the agent need to know it has access to? Common items:

- API keys (`ANTHROPIC_API_KEY`, third-party keys)
- Database connection strings
- File paths (config files, data directories)
- External services (URLs, endpoints)
- GitHub permissions (can it push? open PRs? close issues?)

Don't write a generic "the agent has the usual stuff" — be specific. The agent needs an explicit manifest.

### Q9 — Where does work end up? (always ask)

- **Direct commit to main** (rare, only for trusted/low-risk loops)
- **Push to a branch named `claude/<topic>` and open a PR**
- **Open a draft PR for human review** (default — safer)
- **Just modify files, don't commit** (the human runs the script and reviews the working tree)

## After the interview

1. Echo back the chosen branches in a short summary ("Got it — cron-style, agent picks from a candidate ledger, one improvement per run, reviewer does diff+plan adherence, lockfile, opens a draft PR on `claude/<topic>`").
2. Confirm before writing.
3. Generate the script using the template in `references/script-template.md` as a starting structure.
4. Generate the `*.DECISIONS.md` alongside it.

## Structure of the generated script

Every generated script follows this skeleton (full template in `references/script-template.md`):

```
1. Shebang + strict mode
2. Header comment: purpose, schedule, dependencies, companion services
3. Lock acquisition (or exit 3)
4. Pre-flight checks: required env vars, claude CLI present, git clean state
5. Persistent state file init: `LEDGER_FILE`, `REVIEW_HISTORY_FILE`, `LEARNINGS_FILE` (+ `LEARN_EVERY` constant)
6. Resource manifest assembly (the cat <<EOF block — **must include `$(cat $LEARNINGS_FILE)`**)
7. Implementor invocation (claude -p with prompt + resource manifest + ledger excerpt + learnings)
8. Ledger update (append what was done) — committed alongside code changes
9. Commit + push + open draft PR (per Q9) — so the reviewer has a PR to comment on
10. Diff capture (`gh pr diff "$PR_NUMBER"`)
11. Adversarial reviewer invocation (claude -p with diff + adversarial system prompt) → posted to PR via `gh pr comment`
12. Implementor verdict (claude -p — given review, decides what to change, may re-edit; emits structured `### Addressed` / `### Deferred` / `### Rejected` sections) → follow-up commit pushed if needed, verdict posted to PR via `gh pr comment`
13. Append `### Reviewer notes` + `### Implementor verdict` block to `REVIEW_HISTORY.md`
14. If `RUN_COUNT % LEARN_EVERY == 0`, invoke the distiller (claude -p with the last `LEARN_EVERY` history entries + current `LEARNINGS.md`); overwrite `LEARNINGS.md` with its output
15. Commit `REVIEW_HISTORY.md` (and `LEARNINGS.md` if updated) onto the PR branch
16. Lock release
17. Exit with appropriate code

For no-commit and direct-to-main modes (no PR exists), reviewer + verdict print to stdout instead of posting comments. The history-append + distiller steps still run.
```

Read `references/script-template.md` for the actual bash skeleton before generating.
Read `references/prompt-patterns.md` for the implementor, reviewer, verdict, and distiller prompt templates.
Read `references/ledger-formats.md` for the per-mode ledger structure.

## Things to push back on

- **"Skip the reviewer"** — ask once whether they're sure. The reviewer catches more than it costs. If they confirm, comply.
- **"Make the loop run forever"** — strongly suggest a bounded version (max iterations, max wall time). Unbounded loops on cron are a footgun.
- **"Let the agent decide everything including the prompt"** — push back. The prompt is the contract. Pin it.
- **"Direct commit to main"** — ask whether a draft PR would work instead. If they insist, comply.

## Output

The skill produces two files:

1. `<name>.sh` — the executable script, `chmod +x` ready
2. `<name>.DECISIONS.md` — a record of which interview branches were taken, with one-line rationales

Place them wherever the user keeps automation scripts (commonly `.scripts/` or `scripts/`); ask if it's not obvious.
