# Prompt Patterns

These are the prompt templates for the three Claude Code invocations in a standard script. Customize the bracketed parts per script — don't copy verbatim.

## 1. Implementor prompt (the worker)

The implementor prompt is the contract. It should be specific enough that a fresh agent with no memory can produce the right output.

Required ingredients:
- Role declaration ("You are the implementor agent for X")
- Resource manifest (verbatim from the bash $RESOURCES variable)
- Current state (ledger contents, plan contents, issue body — whatever the source of truth is)
- The task — what to do, what *not* to do, what to favor
- Constraints — file path restrictions, commit policy, off-limits operations
- Output contract — must end with a `SUMMARY:` line for the bash script to parse

Anti-patterns to avoid:
- Vague tasks ("improve the dashboard"). Be specific about heuristics: "favor small high-impact changes, balance features and fixes".
- Letting the agent commit. The bash script controls git; the agent only modifies files.
- Open-ended scope. State explicitly: "one logical change, one commit's worth of work".

## 2. Reviewer prompt (the adversary)

The reviewer's job is to find problems, not to approve. Frame it adversarially.

Required ingredients:
- Adversarial framing ("Your job is to find problems, not to approve")
- Specific things to look for (bugs, security, tests, plan adherence, scope creep)
- The stated intent (so it can check adherence)
- The diff (use `gh pr diff "$PR_NUMBER"` once the PR is open)
- Output contract — GitHub-flavored markdown with a numbered list of concerns, with file paths and line numbers where possible (the bash script posts this verbatim via `gh pr comment`)

Variants by Q5 choice:

**Diff review only** — drop the plan-adherence bullet, keep code-quality focus.

**Diff + plan adherence** (default) — include the stated intent and ask explicitly whether the diff matches it. This catches the single most common failure: the agent doing something different from what it said it would do.

**Diff + security pass** — add explicit security checklist: input validation, secret handling, auth changes, injection vectors, dependency additions.

Anti-patterns to avoid:
- Letting the reviewer be polite. "Bias toward finding problems" is in the prompt for a reason.
- Combining implementor and reviewer in one call. Separate calls = separate context = real adversarial value.
- Asking the reviewer to fix things. The reviewer reports; the implementor fixes.

## 3. Verdict prompt (the implementor's response to review)

This is the implementor's second turn, given the reviewer's notes. It exists because not every reviewer note should be acted on — some are wrong, some are out of scope, some should be deferred.

Required ingredients:
- Restate the implementor role
- The reviewer notes
- The three-way verdict instruction: ADDRESS / DEFER / REJECT
- What to do per verdict:
  - ADDRESS — make additional code changes now (the bash script will commit + push them as a follow-up commit on the same PR)
  - DEFER — add to the ledger's Suggested section
  - REJECT — explain why in the output
- Output contract — GitHub-flavored markdown summarizing the verdict per-note, ending with a `SUMMARY:` line (the bash script posts this verbatim to the PR via `gh pr comment`)

Anti-patterns to avoid:
- Auto-accepting all reviewer notes. The reviewer is adversarial — accepting everything would cause scope creep and over-engineering.
- Letting the verdict step skip the ledger update. Deferred items must land in the ledger or they're lost.
- Free-form verdict output. The verdict must emit structured `### Addressed` / `### Deferred` / `### Rejected` sections so the distiller (see #4) can parse it. Free-form prose breaks the learning loop.

## 4. Distiller prompt (the meta-learner)

Runs every `LEARN_EVERY` runs (default 5). Reads the last 5 entries of `REVIEW_HISTORY.md` and updates `LEARNINGS.md`. The implementor reads `LEARNINGS.md` at the start of every run, so the loop self-corrects: patterns the reviewer keeps catching get internalized.

Required ingredients:
- Restate that the input is reviewer + verdict history, and the signal of interest is the `### Addressed` sections (notes the implementor agreed with — those reveal what the implementor consistently misses).
- The last `LEARN_EVERY` history entries.
- The current `LEARNINGS.md` (so the distiller can refine/age, not just append).
- Rules: terse imperative voice, threshold (pattern in ≥2 runs OR a single serious issue), refine wording, prune stale, cap at ~20 lines.
- Output contract: emit the FULL new contents of `LEARNINGS.md` to stdout (the bash redirects it to the file). End with a `_Last updated: <iso> (run #N)_` trailer.

Anti-patterns to avoid:
- Treating DEFER/REJECT as signal. Those are noise for this purpose — only `### Addressed` items count.
- Letting the file grow unbounded. Force pruning when over the cap.
- Vague learnings ("be careful with tests"). Reject anything that wouldn't help the implementor make a different decision next run.
- Distilling on every run. The whole point is amortization — a single Addressed note isn't a pattern.

## Tone of all four prompts

Be terse and operational. These are agents doing work, not assistants helping a human. Don't say "please" or "if you would". Say what to do.

End every prompt with the output contract. The bash script parses output; ambiguous contracts break parsing.

## Adapting prompts for plan-driven mode

Replace the ledger-read section with plan-read. If the plan is in a `.md` file:

```
Current plan (PLAN.md):
<contents>

Find the first unchecked item ([ ]). Implement it. Mark it checked ([x]) in the same commit.
```

If the plan is in GitHub Issues:

```
Current task (GitHub Issue #<N>):
Title: <title>
Body: <body>

Implement this issue. When done, the bash script will close it.
```

If there are multiple plan sources, give the agent a discovery procedure:

```
Plan sources, in priority order:
1. GitHub Issues labeled "claude-ready" (oldest first)
2. Unchecked items in docs/roadmap.md
3. Unchecked items in any plans/*.md file

Find the first available item across these sources and implement it.
```
