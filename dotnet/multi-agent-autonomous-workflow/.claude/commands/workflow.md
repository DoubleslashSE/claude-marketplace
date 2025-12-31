---
description: Start the multi-agent autonomous workflow for feature implementation
argument-hint: [goal description]
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Multi-Agent Workflow

You are starting the multi-agent autonomous workflow for this goal:

**Goal:** $ARGUMENTS

## Your Role as Orchestrator

You are the **autonomous controller** responsible for driving this workflow to completion. You must continuously iterate through the workflow phases until all stories are complete or you encounter an unrecoverable blocker.

## CRITICAL: Autonomous Execution Protocol

This workflow is designed to run for **minutes to hours** without human intervention. Follow these principles:

1. **Never stop prematurely** - Continue executing until ALL stories are complete
2. **Iterate on failures** - When a step fails, analyze, adjust, and retry (up to 3 times)
3. **Maintain state** - Update workflow state after each significant action
4. **Self-correct** - Use verification results to guide corrections
5. **Escalate only when truly blocked** - Exhaust retry options first

## Initialization

```bash
# Initialize workflow state (run this first)
python .claude/hooks/state.py init "$ARGUMENTS"
```

## Phase 1: Analysis (Run Once)

1. Invoke `analyst` subagent with the goal
2. For each story returned, add to state:
   ```bash
   python .claude/hooks/state.py add-story "Story title" --size M
   ```
3. Invoke `architect` for technical design
4. **Quality Gate G1:** Verify design is complete before proceeding

## Phase 2: Story Execution Loop (ITERATE UNTIL ALL COMPLETE)

```
WHILE stories remain with status != 'completed':

    1. SELECT next pending story (or retry failed story if attempts < 3)

    2. UPDATE state:
       python .claude/hooks/state.py update-story S{n} in_progress

    3. INVOKE developer with story + design context
       - If build/tests FAIL → analyze error, retry developer (max 3 attempts)
       - If 3 failures → invoke architect for redesign, then retry

    4. INVOKE tester to verify implementation
       - If FAIL → send failure details back to developer
       - REPEAT developer↔tester loop (max 3 iterations)

    5. INVOKE reviewer for code review
       - If CHANGES_REQUESTED → send feedback to developer, loop back to step 3

    6. IF story is [SECURITY-SENSITIVE]:
       INVOKE security subagent
       - If NEEDS_REMEDIATION → loop back to step 3

    7. UPDATE state:
       python .claude/hooks/state.py update-story S{n} completed

    8. CHECK checkpoint:
       - If 5 stories completed since last review → pause for human checkpoint
       - Otherwise → continue to next story
```

## Phase 3: Completion

1. Verify ALL stories have status 'completed':
   ```bash
   python .claude/hooks/state.py status
   ```
2. If deployment needed, invoke `devops` subagent
3. Complete workflow:
   ```bash
   python .claude/hooks/state.py complete
   ```
4. Generate final summary report

## Iteration Recovery Strategies

### When Developer Fails (build/test errors)
1. Read the error output carefully
2. Check if it's a missing dependency, typo, or logic error
3. Provide specific error context to developer on retry
4. After 3 failures: invoke architect to reconsider approach

### When Tester Finds Issues
1. Parse the test failure report
2. Extract specific failing acceptance criteria
3. Pass failure details to developer with clear fix instructions
4. Track iteration count - escalate after 3 dev↔test cycles

### When Reviewer Requests Changes
1. Compile all requested changes into actionable items
2. Re-invoke developer with change requests as requirements
3. Re-run tester after changes
4. Re-submit for review

### When Stuck (True Blocker)
1. Document exactly what was tried
2. Record in state:
   ```bash
   python .claude/hooks/state.py add-blocker "Description" --severity high
   ```
3. Escalate to human with full context

## Escalation Protocol

When escalating to human (after 3+ failed iterations or critical blocker):

### Step 1: Record the Blocker
```bash
python .claude/hooks/state.py add-blocker "Detailed description of what's blocking" --severity high
```

### Step 2: Generate Escalation Summary
Output a structured escalation report:
```markdown
## ESCALATION: Human Review Required

**Story:** S{n} - [Title]
**Severity:** high/critical
**Attempts Made:** 3/3

### What Was Tried
1. [First approach and outcome]
2. [Second approach and outcome]
3. [Third approach and outcome]

### Root Cause Analysis
[Your analysis of why this is failing]

### Blocking Issue
[Specific technical or requirements issue]

### Recommended Options
1. [Option A] - [Trade-offs]
2. [Option B] - [Trade-offs]
3. [Redesign/split story]

### Files Affected
- `path/to/file.cs` - [current state]
```

### Step 3: PAUSE Workflow
- **DO NOT** continue to the next story
- **DO NOT** attempt further fixes without human input
- Wait for human to review and provide direction

### Step 4: Human Resolution
Human resolves by running one of:
```bash
# Option A: Resolve blocker and continue
python .claude/hooks/state.py resolve-blocker 0

# Option B: Skip story and continue
python .claude/hooks/state.py update-story S{n} skipped

# Option C: Provide new direction (then resume workflow)
```

### Exit Codes
- `0` - Success
- `1` - Error
- `2` - Checkpoint due (human review recommended, not blocking)
- `3` - Blocked (workflow paused, human action required)

## Progress Reporting (Every 3 Stories or 60 Minutes)

Generate and display:
```markdown
## Workflow Progress Report

**Goal:** [Original goal]
**Status:** X/Y stories complete (Z%)

**Completed Stories:**
- [x] S1: [Title]
- [x] S2: [Title]

**In Progress:**
- [ ] S3: [Title] - Attempt 2/3

**Metrics:**
- Build: PASSING
- Tests: X passing, Y total
- Coverage: Z%

**Decisions Made:**
- ADR-001: [Decision]

**Next Actions:**
1. [What you'll do next]
```

## Important Guidelines

- **ALWAYS** update state after completing each story
- **NEVER** leave a story in 'in_progress' state indefinitely
- Use the Task tool to invoke subagents with FULL context
- Each subagent returns structured output - parse it to determine next action
- Escalate to human only at checkpoints OR on true blockers (after 3+ retries)
- Mark stories as `[SECURITY-SENSITIVE]` if they involve auth, payments, or user data

Begin by initializing workflow state and invoking the analyst subagent.
