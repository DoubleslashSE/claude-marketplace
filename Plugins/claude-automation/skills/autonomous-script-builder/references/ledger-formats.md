# Ledger Formats

The ledger is the script's memory between runs. Pick the format based on the mode chosen in Q1.

## Candidate ledger — cron-style autonomous (Q1 = cron-style)

Common filename: `SCOUT.md`, but any name works. Two sections: candidates the agent has identified, and work the agent has completed. The agent both adds candidates (when it spots opportunities) and consumes them (when it implements one).

```markdown
# Improvement Ledger

Maintained by .scripts/<name>.sh. The script is the only writer.

## Suggested

- [ ] (2026-05-20) Add retry logic to the log forwarder — small, high-impact (improves reliability of an existing flaky path)
- [ ] (2026-05-19) Migrate the legacy auth handler to the new middleware — medium, medium-impact
- [ ] (2026-05-18) Add dark mode toggle — small, low-impact (nice-to-have)
- [ ] (2026-05-17) Refactor rendering to use streaming — large, high-impact (defer until smaller wins are exhausted)

## Implemented

- [x] (2026-05-21) Fixed off-by-one in pagination calculation — was showing 11 items per page instead of 10. PR #142.
- [x] (2026-05-20) Added timeout to the upstream heartbeat check (was hanging on network partition). PR #141.
- [x] (2026-05-18) Surfaced the build version in the footer for easier triage. PR #138.
```

Conventions:
- Each item has a date prefix `(YYYY-MM-DD)`.
- Items in Suggested annotate size + impact so the agent can apply heuristics like "small high-impact first".
- Implemented items include the PR number for traceability.
- The agent appends to Suggested when it notices opportunities; it moves items from Suggested to Implemented when it works on them.

## Plan checklist — plan-driven, single file (Q1 = plan-driven)

Common filename: `PLAN.md`. Standard checkbox plan. The agent finds the first unchecked item, implements it, and checks it.

```markdown
# Project Plan

Maintained by humans (and by the script, which checks items off as it completes them).

## Milestone 1: Foundation

- [x] Set up repo skeleton
- [x] Configure CI
- [ ] Add database migrations infrastructure
- [ ] Wire up authentication
- [ ] Add health-check endpoint

## Milestone 2: Core features

- [ ] Implement the X feature
- [ ] Implement the Y feature
```

Conventions:
- Order matters — agent works top-to-bottom.
- If an item is ambiguous, the agent should either ask (open an issue tagged for human input) or skip and try the next one.
- The script may add a brief comment under a checked item if useful (PR link, gotchas discovered).

## Multi-source plans (Q1 = plan-driven, multiple sources)

When the plan lives in several places, no single ledger file holds it. Instead, the script needs a discovery procedure (see `prompt-patterns.md` under "Adapting prompts for plan-driven mode"). The script's *own* ledger then becomes a journal (next section), recording what was picked up and from where.

## Journal — append-only (any mode, optional)

Common filename: `JOURNAL.md`. When the work source is external (issues, queues, events), the ledger is just a record of what happened. Append-only.

```markdown
# Run Journal

Append-only. The script writes; nothing reads except humans curious about history.

## 2026-05-21 14:02 UTC
- Picked up: GH Issue #84 "Add CSV export to reports view"
- Branch: claude/20260521-140200
- Reviewer notes: 3 (1 addressed, 1 deferred to issue #92, 1 rejected — false positive about SQL injection in a query that uses parameterized inputs)
- PR: #143

## 2026-05-21 02:00 UTC
- Scheduled run, no eligible work found (no issues with the ready label)
- Exit code: 2

## 2026-05-20 14:02 UTC
- Picked up: PLAN.md line "Add health-check endpoint"
- ...
```

Conventions:
- One entry per run, regardless of outcome (including no-ops).
- Include the branch name and PR number for cross-referencing.
- Summarize the reviewer-verdict outcomes — useful for spotting patterns (e.g. "reviewer keeps flagging the same thing, maybe we should address the root cause").

## Choosing the right ledger

- **Q1 = cron-style** → candidate ledger (e.g. `SCOUT.md`)
- **Q1 = plan-driven, single file** → existing plan file + optional journal
- **Q1 = plan-driven, multiple sources** → journal only (the script's own record; plans live elsewhere)
- **Q1 = queue-driven** → journal only (the queue is the source of truth)
- **Q1 = event-driven** → journal only (events are the source of truth)

## REVIEW_HISTORY.md (always present)

Independent of mode. Append-only log of reviewer notes + implementor verdict per run. Source signal for the distiller — never edit by hand.

```markdown
# Review History

## Run 2026-05-25T13:42:11+02:00 — PR #142

### Reviewer notes

1. The new retry path has no exponential backoff; bursts will hammer upstream.
2. Missing test for the timeout edge case.

### Implementor verdict

### Addressed
- Backoff missing — added exponential backoff with jitter (1s, 2s, 4s, capped at 30s).

### Deferred
- Timeout test — deferred to a follow-up, added to SCOUT.md Suggested.

### Rejected
- _none_

SUMMARY: Added retry with backoff to log forwarder; deferred dedicated timeout test.
```

Distiller parses `### Run` markers to count runs and `### Addressed` blocks for signal.

## LEARNINGS.md (always present)

Distilled signal. Maintained by the distiller every `LEARN_EVERY` runs. Read by every implementor invocation.

```markdown
# Implementor Learnings

_Distilled from adversarial review notes the implementor accepted (ADDRESS verdict).
Read by every run. Updated every 5 runs._

## Patterns to apply

- Always add exponential backoff with jitter to new retry paths.
- When touching shared mutable state, prefer immutable replacement over in-place mutation.
- If a change touches the API surface, update the OpenAPI spec in the same commit.

_Last updated: 2026-05-25T13:42:11+02:00 (run #15)_
```

Keep terse. The distiller is told to cap at ~20 lines.
