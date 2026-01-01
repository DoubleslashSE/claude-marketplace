---
name: multi-agent-autonomous-workflow
description: Orchestrates multi-agent workflow for feature implementation using specialized subagents. Use when implementing features, epics, or complex multi-story tasks that need analyst, architect, developer, tester, reviewer, and security agents.
---

# Multi-Agent Autonomous Workflow

Orchestrates specialized subagents for **extended autonomous work** (minutes to hours) with minimal human intervention.

## Execution Model: Long-Running Until Complete

This workflow implements the **Ralph Wiggum pattern** for persistent autonomous execution:

> **The workflow NEVER exits until the goal is complete or a true blocker requires human intervention.**
> **Iterate continuously. Use previous failures as context for next attempt.**
> **State persists on disk. The Stop hook enforces completion before exit.**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      LONG-RUNNING EXECUTION MODEL                                │
│                                                                                  │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │                    OUTER LOOP: PHASES                                     │  │
│   │                                                                           │  │
│   │   Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ WORKFLOW_COMPLETE      │  │
│   │   (Setup)    (Analyze)   (Execute)   (Finalize)                           │  │
│   │                  │            │                                           │  │
│   │                  ▼            ▼                                           │  │
│   │              CLARIFY      ┌───────────────────────────────┐               │  │
│   │              QUESTIONS    │  MIDDLE LOOP: STORIES         │               │  │
│   │                           │                               │               │  │
│   │                           │  for each story:              │               │  │
│   │                           │    ┌────────────────────┐     │               │  │
│   │                           │    │ INNER LOOP: ITERATE│     │               │  │
│   │                           │    │ until ALL verified │     │               │  │
│   │                           │    │ or max retries     │     │               │  │
│   │                           │    └────────────────────┘     │               │  │
│   │                           └───────────────────────────────┘               │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│   COMPLETION: Stop hook blocks exit until WORKFLOW_COMPLETE marker is output    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Setup & Platform Detection

Before any work, set up the execution context. **This phase produces visible output.**

### Step 0.1: Session Recovery Check

**ALWAYS run at the start of every session:**

```bash
# Check if resuming existing workflow
python .claude/core/state.py recover
```

**If resuming:** Skip to the appropriate phase/story based on the recovered state.

**Output:**
```markdown
## Session Recovery

| Check | Result |
|-------|--------|
| Existing workflow | [Yes/No] |
| Workflow ID | [ID if resuming] |
| Current phase | [Phase name] |
| Stories completed | [X/Y] |
| Current story | [Story ID and title] |

[If resuming]: Continuing from [story/phase]. Skipping to Phase [N].
```

### Step 0.2: Discover Available Platforms (DYNAMIC)

**IMPORTANT:** Platform discovery is FULLY DYNAMIC. Never hardcode platform names or markers.

```bash
# Discover all platforms in the Workflows/platforms directory
# Each platform provides its own platform.json with markers
ls -d Workflows/platforms/*/ 2>/dev/null || ls -d ../Workflows/platforms/*/ 2>/dev/null
```

For each discovered platform directory, read its `platform.json` to get:
- `name`: Platform identifier
- `markers`: Files/patterns that identify this platform
- `matchMode`: "any" (match any marker) or "all" (match all markers)
- `priority`: Resolution priority when multiple match

**Output the discovery:**

```markdown
## Platform Discovery

Scanning for available platforms...

| Platform | Description | Markers | Match Mode |
|----------|-------------|---------|------------|
| {name} | {displayName} | {markers joined} | {matchMode} |
...

Found {N} platform configurations.
```

### Step 0.3: Match Platform to Codebase (DYNAMIC)

For each discovered platform, check if its markers exist in the codebase:

```python
# Pseudocode for platform matching
for platform in discovered_platforms:
    matched = check_markers(platform.markers, platform.matchMode)
    if matched:
        candidates.append((platform, platform.priority))

selected = max(candidates, key=lambda x: x[1])  # Highest priority wins
```

**Output the matching:**

```markdown
## Platform Detection

Scanning codebase for platform markers...

| Platform | Markers Checked | Found | Match Result |
|----------|-----------------|-------|--------------|
| {name} | {marker} | [Yes/No] | [MATCH/NO MATCH] |
...

**Selected Platform:** {platform.name} (priority: {priority})
**Reason:** {why this platform was selected}
```

### Step 0.4: Load Platform Configuration

From selected `platform.json`, extract and cache:
- Commands (build, test, lint, coverage, etc.)
- Conventions (naming, patterns, commit format)
- Quality gates (coverage thresholds, required checks)
- Project structure patterns
- Skills to load

**Output:**

```markdown
## Platform Configuration Loaded

**Platform:** {displayName} (v{version})

### Commands
| Action | Command |
|--------|---------|
| {key} | `{command}` |
...

### Conventions
| Convention | Value |
|------------|-------|
| {key} | {value} |
...

### Quality Gates
| Gate | Threshold |
|------|-----------|
| Coverage (S) | {S}% |
| Coverage (M) | {M}% |
| Coverage (L) | {L}% |
| Coverage (XL) | {XL}% |

### Skills Loaded
{For each skill in platform.skills, list it}

---
Platform detection complete. Proceeding with workflow.
```

---

## Phase 1: Analysis & Planning

### Step 1.1: Pre-Analysis Clarification (REQUIRED CHECKPOINT)

**BEFORE invoking the analyst agent, you MUST ask clarifying questions.**

Use the `AskUserQuestion` tool to present questions about the goal:

```markdown
## Pre-Analysis Clarification Required

Before I begin analyzing your request, I need to clarify:
```

**Questions to ask (pick relevant ones):**
1. **Scope boundaries:** What is IN scope vs OUT of scope?
2. **Priority:** If there are multiple features, which is most important?
3. **Technical constraints:** Any specific technologies to use or avoid?
4. **Integration points:** How should this integrate with existing code?
5. **User requirements:** Any specific user-facing requirements mentioned?
6. **Data handling:** How should data be stored/processed?
7. **Error handling:** Any specific error handling requirements?

**When to ask fewer questions:**
- Goal is very specific and complete
- User provided detailed specifications
- Technical approach is obvious from context

**Always offer:** "Proceed with my best judgment" as an option.

**Question Timeout Behavior:**
- If no response within 5 minutes in autonomous mode: proceed with best judgment
- Log the assumed answers: `python .claude/core/state.py add-clarification "Question" "Assumed: best judgment" --phase pre-analysis --category scope`
- Always persist clarifications for session recovery

**Wait for user response before continuing to Step 1.2.**

### Step 1.1.1: Persist Clarifications

After receiving user answers, **ALWAYS persist them**:

```bash
# For each question answered:
python .claude/core/state.py add-clarification "What payment provider?" "Stripe" --phase pre-analysis --category technical
python .claude/core/state.py add-clarification "Real-time tech?" "SignalR" --phase pre-analysis --category technical
```

This ensures clarifications survive session restarts.

### Step 1.2: Initialize Workflow State

```bash
python .claude/core/state.py init "Goal: {User's goal}"
```

### Step 1.3: Invoke Analyst Subagent

```markdown
## Task for Analyst

{PLATFORM CONTEXT BLOCK}

**Goal:** {User's goal, incorporating clarifications}

Break this down into user stories with:
- Clear title
- Size estimate (S/M/L/XL)
- Acceptance criteria (testable)
- Security sensitivity flag (if applicable)
```

Parse analyst output and add stories to state:
```bash
python .claude/core/state.py add-story "Story title" --size M
python .claude/core/state.py add-story "Story title" --size L --security
# Repeat for each story
```

### Step 1.4: Pre-Plan Clarification (REQUIRED CHECKPOINT)

**BEFORE invoking the architect agent, you MUST review stories and ask for confirmation.**

Use the `AskUserQuestion` tool:

```markdown
## Pre-Plan Clarification Required

I've identified these stories from your request:

| # | Story | Size | Security |
|---|-------|------|----------|
| S1 | {title} | {size} | {Yes/No} |
| S2 | {title} | {size} | {Yes/No} |
...

Before I design the technical approach, please confirm:
```

**Questions to ask:**
1. **Story order:** Is this the right priority order? Any changes?
2. **Technical preferences:** Any specific patterns/libraries to use or avoid?
3. **Existing code concerns:** Any areas I should be careful modifying?
4. **Missing stories:** Anything I missed that should be included?

**Wait for user response before continuing to Step 1.5.**

### Step 1.5: Invoke Architect Subagent

```markdown
## Task for Architect

{PLATFORM CONTEXT BLOCK}

**Stories:** {List from analyst with user's priority adjustments}

Create technical design following:
- Platform project structure patterns
- Platform conventions
- Existing codebase patterns

For each story, identify:
- Files to create/modify
- Dependencies between stories
- Technical risks
```

### Step 1.6: Gate G1 - Verify Design Complete

Check:
- [ ] All stories have technical design
- [ ] File changes identified per story
- [ ] Dependencies mapped
- [ ] No open questions blocking implementation

If not complete, iterate with architect.

---

## Phase 2: Story Execution Loop

This is the **main execution loop**. It runs until **ALL stories are completed**.

**CRITICAL RULES:**
1. Every iteration MUST run build and tests before completing
2. No story can be marked complete until ALL verification checks pass
3. The loop continues until there are no more incomplete stories
4. The Stop hook will block exit if any stories remain incomplete
5. **TDD phases must be followed: RED → GREEN → REFACTOR → VERIFY**
6. **Failures must be categorized for intelligent retry decisions**

### TDD Phase Enforcement

Each story MUST follow the TDD cycle. Track phases explicitly:

```bash
# 1. RED: Write failing test FIRST
python .claude/core/state.py tdd-phase S1 red
# Developer writes test that fails

# 2. GREEN: Minimum code to pass
python .claude/core/state.py tdd-phase S1 green
# Developer implements minimum code

# 3. REFACTOR: Clean up (optional for small changes)
python .claude/core/state.py tdd-phase S1 refactor
# Developer refactors without changing behavior

# 4. VERIFY: Run all checks
python .claude/core/state.py tdd-phase S1 verify
# All gates must pass
```

**Before moving to GREEN phase, validate:**
```bash
python .claude/core/state.py tdd-validate S1 green
# Returns: {"valid": true} or {"valid": false, "expected": "red"}
```

**If developer tries to write implementation before tests:**
```
STOP. TDD violation detected.
Current phase: none
Expected: red (write failing test first)

Developer must write a failing test before implementation.
```

### Failure Categorization

When a gate fails, **categorize the failure** for intelligent retry:

```bash
# Auto-categorize based on error message:
python .claude/core/state.py add-failure S1 "Connection refused: database not available"
# Output: Added failure: F1 [infra]

# Or explicitly categorize:
python .claude/core/state.py add-failure S1 "API key not configured" --category external
```

**Categories:**
| Category | Description | Retry Strategy |
|----------|-------------|----------------|
| `code` | Bug in implementation | Standard retry |
| `test` | Test itself is wrong | Fix test, retry |
| `infra` | DB, network, filesystem | Retry with backoff |
| `external` | API keys, external services | **ESCALATE** - needs human |
| `timeout` | Operation timed out | Retry with backoff |

**Get retry recommendation before retrying:**
```bash
python .claude/core/state.py retry-recommendation S1
# Returns: {"should_retry": true, "backoff_seconds": 30}
# OR: {"should_retry": false, "escalate": true, "reason": "External service failures"}
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           STORY EXECUTION LOOP                                   │
│                                                                                  │
│   while (incomplete_stories exist):                                              │
│       story = get_next_incomplete_story()                                        │
│       iteration = 0                                                              │
│       previous_failures = []                                                     │
│                                                                                  │
│       while (story NOT completed AND iteration < MAX_RETRIES):                   │
│           iteration++                                                            │
│                                                                                  │
│           ┌─────────────────────────────────────────────────────────────────┐   │
│           │ 1. DEVELOP                                                       │   │
│           │    Invoke developer agent with previous_failures context         │   │
│           │                                                                  │   │
│           │ 2. BUILD VERIFICATION (MANDATORY - Gate G2)                      │   │
│           │    Run: {platform.commands.build}                                │   │
│           │    If FAIL: add to previous_failures, CONTINUE to next iteration │   │
│           │                                                                  │   │
│           │ 3. TEST VERIFICATION (MANDATORY - Gate G3)                       │   │
│           │    Run: {platform.commands.test}                                 │   │
│           │    If FAIL: add to previous_failures, CONTINUE to next iteration │   │
│           │                                                                  │   │
│           │ 4. TESTER AGENT                                                  │   │
│           │    Verify acceptance criteria                                    │   │
│           │    If FAIL: add issues to previous_failures, CONTINUE            │   │
│           │                                                                  │   │
│           │ 5. REVIEWER AGENT                                                │   │
│           │    Code review and architecture compliance                       │   │
│           │    If CHANGES_REQUESTED: add to previous_failures, CONTINUE      │   │
│           │                                                                  │   │
│           │ 6. SECURITY AGENT (if story.securitySensitive)                   │   │
│           │    Security analysis and scanning                                │   │
│           │    If REMEDIATION_NEEDED: add to previous_failures, CONTINUE     │   │
│           │                                                                  │   │
│           │ 7. FINAL VERIFICATION (MANDATORY - Gate G5)                      │   │
│           │    Run: {platform.commands.build} && {platform.commands.test}    │   │
│           │    If FAIL: add to previous_failures, CONTINUE                   │   │
│           │    If PASS: Mark story COMPLETED, commit, break inner loop       │   │
│           └─────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│       if (story NOT completed after MAX_RETRIES):                               │
│           Escalate as blocker, continue to next story                           │
│                                                                                  │
│       Every 3 stories OR 30 minutes: Generate progress report                   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Mandatory Verification Commands

**Before ANY loop iteration can complete, run these platform commands:**

```bash
# Get commands from platform.json (resolved dynamically)
BUILD_CMD=$(python .claude/core/platform.py get-command build)
TEST_CMD=$(python .claude/core/platform.py get-command test)

# Execute
eval "$BUILD_CMD"
eval "$TEST_CMD"
```

**If either command fails, DO NOT:**
- Exit the inner loop
- Mark the story as completed
- Proceed to the next story
- Create a PR

**Instead:**
- Log the failure
- Add to `previous_failures` context
- Retry with the developer agent

### Retry Context Template

When retrying development, ALWAYS provide this context to the developer:

```markdown
## Retry Context

**Story:** {story.id} - {story.title}
**Iteration:** {n}/{MAX_RETRIES}
**Previous Attempts:** {n-1}

### What Failed:
{For each failure:}
- **{failure_type}:** {description}
  - File: {file}:{line} (if applicable)
  - Error: {error_message}

### What To Fix:
{Specific actionable instructions derived from failures}

### Files Changed So Far:
{List of files modified in previous iterations}

### Verification Status:
| Check | Status |
|-------|--------|
| testsPass | {PASS/PENDING} |
| coverageMet | {PASS/PENDING} |
| reviewApproved | {PASS/PENDING} |
| securityCleared | {PASS/PENDING/N/A} |

### Retry Recommendation:
{Output from: python .claude/core/state.py retry-recommendation {story_id}}
```

### Reviewer Severity Levels

When the **Reviewer Agent** identifies issues, they MUST be categorized by severity:

```markdown
## Code Review Results

### BLOCKING Issues (Must Fix)
{Issues that block completion - security, correctness, architecture violations}
- **[BLOCKING]** SQL injection vulnerability in UserRepository.cs:45
- **[BLOCKING]** Missing null check causes crash in PaymentService

### SUGGESTIONS (Recommended)
{Improvements that should be made but don't block completion}
- **[SUGGESTION]** Consider using MediatR pipeline for validation
- **[SUGGESTION]** Extract magic number to named constant

### INFO (For Future Reference)
{Non-actionable observations}
- **[INFO]** This pattern could be simplified in future refactoring
- **[INFO]** Consider adding integration tests for edge cases
```

**Retry Logic Based on Severity:**
- **BLOCKING issues found:** MUST retry, add to `previous_failures`
- **Only SUGGESTIONS:** Mark review approved, note suggestions for developer
- **Only INFO:** Mark review approved, continue

### External Dependency Detection

Before development, check for **external dependencies** that may require special handling:

```bash
# Check if story requires external services
# Look for keywords in acceptance criteria and design
```

**External Dependency Types:**

| Type | Detection Keywords | Handling |
|------|-------------------|----------|
| **Payment APIs** | stripe, paypal, payment, checkout | Use mock/sandbox in tests |
| **Email Services** | email, smtp, sendgrid, mailgun | Mock email sending |
| **SMS/Push** | sms, twilio, push notification | Mock notification service |
| **OAuth/SSO** | oauth, sso, google auth, azure ad | Use test credentials |
| **Cloud Storage** | s3, azure blob, gcs, file upload | Use local storage mock |
| **External APIs** | api key, third-party, integration | Create mock responses |

**When external dependency detected:**

1. **Log dependency:**
   ```bash
   python .claude/core/state.py add-clarification "External dependency: Stripe API" "Using sandbox mode for tests" --phase development --category external
   ```

2. **Add mock strategy to developer context:**
   ```markdown
   ## External Dependencies

   This story requires: Stripe Payment API

   **Test Strategy:**
   - Use Stripe test mode API keys
   - Mock Stripe responses for unit tests
   - Mark AC requiring live Stripe as "MANUAL_VERIFICATION_REQUIRED"
   ```

3. **If no mock possible:**
   ```bash
   python .claude/core/state.py add-blocker "Stripe API credentials not available for testing" --severity high
   # Escalate to user
   ```

### Progress Reports

Generate a progress report every **3 completed stories** OR every **30 minutes**:

```markdown
## Progress Report

**Workflow:** {goal}
**Workflow ID:** {workflowId}
**Runtime:** {elapsed_time}
**Iteration:** {current_iteration}

### Stories Progress
| Status | Count |
|--------|-------|
| Completed | {X} |
| In Progress | {Y} |
| Pending | {Z} |
| Blocked | {B} |

### Recently Completed:
{For each recently completed story:}
- [{id}] {title} - {iterations} iterations

### Current Story:
- [{id}] {title}
- Status: {status}
- Iteration: {n}/{MAX_RETRIES}
- Verification: {checks summary}

### Blockers:
{List any blockers or "None"}

### Next Steps:
1. {Current action}
2. {Next story after this}
```

---

## Phase 2.5: Lint Fix Loop (Non-Story Fixes)

When **Gate G7 fails on lint** but build/tests pass, enter this special loop:

**Purpose:** Fix lint/formatting issues without creating a new story iteration.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           LINT FIX LOOP                                          │
│                                                                                  │
│   Gate G7 fails on lint (build + test passed)                                   │
│                                                                                  │
│   while (lint_fails AND attempts < 3):                                          │
│       1. Get lint errors:                                                       │
│          LINT_CMD=$(python .claude/core/platform.py get-command lint)           │
│          eval "$LINT_CMD" 2>&1 | tee lint_errors.txt                            │
│                                                                                  │
│       2. Fix lint issues (DO NOT change logic):                                 │
│          - Formatting only                                                      │
│          - No new features                                                      │
│          - No refactoring                                                       │
│                                                                                  │
│       3. Re-run verification:                                                   │
│          - Build (should still pass)                                            │
│          - Test (should still pass)                                             │
│          - Lint (check if fixed)                                                │
│                                                                                  │
│       4. If lint passes: Exit loop, continue to Phase 3                         │
│          If lint fails: Increment attempts, retry                               │
│                                                                                  │
│   if (attempts >= 3):                                                           │
│       Log blocker: "Unable to fix lint issues after 3 attempts"                 │
│       Continue to Phase 3 anyway (lint is non-blocking for PR)                  │
│       Note in PR: "Lint issues remain - manual review needed"                   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Key Rules for Lint Fix Loop:**
1. **DO NOT** modify any logic or behavior
2. **DO NOT** add new tests or features
3. **ONLY** fix formatting, whitespace, import order, etc.
4. **Verify tests still pass** after each fix
5. **If tests break:** Revert lint fix, continue with lint warnings

```bash
# Run lint fix loop
python .claude/core/state.py update-phase lint-fix

# Get lint command and run
LINT_CMD=$(python .claude/core/platform.py get-command lint)
eval "$LINT_CMD" 2>&1

# If platform has auto-fix:
LINT_FIX=$(python .claude/core/platform.py get-command lintFix 2>/dev/null || echo "")
if [ -n "$LINT_FIX" ]; then
    eval "$LINT_FIX"
fi

# Verify tests still pass after lint fix
TEST_CMD=$(python .claude/core/platform.py get-command test)
eval "$TEST_CMD"
```

---

## Phase 3: Completion & PR Creation

### Step 3.1: Verify All Stories Complete

```bash
python .claude/core/state.py status
```

**All stories must have status `completed` with all verification checks passed.**

If any story is not completed, return to Phase 2.

### Step 3.2: Final Build & Test Verification (MANDATORY - Gate G7)

**Before creating a PR, run a COMPLETE verification cycle:**

```bash
# Get commands from platform
BUILD_CMD=$(python .claude/core/platform.py get-command build)
TEST_CMD=$(python .claude/core/platform.py get-command test)
LINT_CMD=$(python .claude/core/platform.py get-command lint 2>/dev/null || echo "")

# Run all checks
eval "$BUILD_CMD"
eval "$TEST_CMD"
if [ -n "$LINT_CMD" ]; then
    eval "$LINT_CMD"
fi
```

**Output verification results:**

```markdown
## Pre-PR Verification (Gate G7)

| Check | Command | Result |
|-------|---------|--------|
| Build | `{build_cmd}` | {PASS/FAIL} |
| Tests | `{test_cmd}` | {PASS/FAIL} ({test_count} tests) |
| Lint | `{lint_cmd}` | {PASS/FAIL/N/A} |

{If ALL PASS}: All verification checks passed. Proceeding with PR creation.
{If ANY FAIL}: Verification failed. Returning to Phase 2 to fix issues.
```

**If ANY check fails:**
- DO NOT create the PR
- Return to Phase 2 to fix the issues
- Re-run verification after fixes

### Step 3.3: Invoke DevOps (if needed)

If deployment configuration is required:
```markdown
## Task for DevOps

{PLATFORM CONTEXT BLOCK}

Create/update deployment configuration for implemented features.
```

### Step 3.4: Create Pull Request

```bash
# Ensure clean working state
git status

# Push branch
git push -u origin HEAD

# Create PR with comprehensive body
gh pr create --title "[Feature] {Goal Summary}" --body "$(cat <<'EOF'
## Summary
{Brief description of implementation}

## Stories Implemented
{For each story:}
- **{story.id}:** {story.title}

## Key Changes
{Major files/features changed, grouped logically}

## Testing
- All {test_count} tests passing
- Coverage thresholds met for all stories

## Verification Checklist
- [x] Build passes ({platform.commands.build})
- [x] All tests pass ({platform.commands.test})
- [x] Lint checks pass (if applicable)
- [x] Code review approved by reviewer agent
- [x] Security review passed (if applicable)
- [x] All acceptance criteria verified by tester agent

## Workflow Metrics
- **Workflow ID:** {workflowId}
- **Runtime:** {total_time}
- **Stories:** {completed}/{total}
- **Total Iterations:** {sum of all story iterations}

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 3.5: Complete Workflow State

```bash
python .claude/core/state.py complete
```

### Step 3.6: Output Completion Marker (CRITICAL)

**This marker is REQUIRED for the Stop hook to allow exit:**

```markdown
## WORKFLOW_COMPLETE

**Goal:** {goal}
**Status:** SUCCESS
**PR URL:** {pr_url}
**Workflow ID:** {workflowId}
**Runtime:** {total_time}
**Stories Completed:** {completed}/{total}

All stories verified. Pull request created. Workflow complete.
```

---

## Architecture

```
ORCHESTRATOR (You) ─── Drives workflow through all phases
    │
    │   Phase 0
    ├── Platform Detection (dynamic discovery)
    │
    │   Phase 1
    ├── CLARIFY ──────▶ (Pre-Analysis Questions - REQUIRED)
    ├── analyst ──────▶ Requirements & user stories
    ├── CLARIFY ──────▶ (Pre-Plan Questions - REQUIRED)
    ├── architect ────▶ Technical design
    │
    │   Phase 2 (Loop until all complete)
    ├── developer ────▶ Implementation (TDD)
    ├── BUILD ────────▶ {platform.commands.build} (MANDATORY)
    ├── TEST ─────────▶ {platform.commands.test} (MANDATORY)
    ├── tester ───────▶ Acceptance verification
    ├── reviewer ─────▶ Code review
    ├── security ─────▶ Security audit (if flagged)
    │
    │   Phase 3
    ├── VERIFY ───────▶ Final build/test/lint (MANDATORY)
    ├── devops ───────▶ Infrastructure & deployment
    └── PR ───────────▶ Create pull request + WORKFLOW_COMPLETE
```

---

## State Management

### Persistence Commands

```bash
# Initialize workflow
python .claude/core/state.py init "Goal description"

# Session recovery (ALWAYS run at session start)
python .claude/core/state.py recover

# Story management
python .claude/core/state.py add-story "Title" --size M [--security]
python .claude/core/state.py update-story S1 in_progress
python .claude/core/state.py update-story S1 testing
python .claude/core/state.py update-story S1 review
python .claude/core/state.py update-story S1 completed

# Verification checks (fail-first pattern)
python .claude/core/state.py verify S1 testsPass --passed
python .claude/core/state.py verify S1 coverageMet --passed --details "85%"
python .claude/core/state.py verify S1 reviewApproved --passed
python .claude/core/state.py verify S1 securityCleared --passed

# Progress tracking
python .claude/core/state.py status
python .claude/core/state.py progress --lines 20
python .claude/core/state.py compact-context

# Context management (for long runs)
python .claude/core/state.py trim-progress --lines 100

# Git recovery
python .claude/core/state.py mark-working-state
python .claude/core/state.py rollback-to-checkpoint

# Completion
python .claude/core/state.py complete
```

### State File Location

State persists in `.claude/workflow-state.json`. This enables:
- Session recovery after interruptions
- Progress tracking across long runs
- Stop hook completion detection
- Rollback capability per story

---

## Long-Running Execution Strategies

### Stop Hook Behavior

The Stop hook (`stop.py`) implements the Ralph Wiggum pattern:

1. **On exit attempt:** Hook intercepts and checks for completion
2. **If WORKFLOW_COMPLETE not found:** Block exit, provide continuation context
3. **If WORKFLOW_COMPLETE found:** Allow normal exit
4. **Safety limit:** Max iterations (default 100) prevents infinite loops

### Context Management for Extended Runs

**For Runs Under 1 Hour:**
- Update state after each story completion
- Generate progress report every 3 stories

**For Runs 1-4 Hours:**
- Update state after each phase transition
- Generate progress report every 30 minutes
- Checkpoint review at 5-story intervals
- Trim progress file to 100 lines

**For Runs 4+ Hours:**
- Aggressive context management
- Keep only: current story (full) + completed stories (summary only)
- Drop: full implementation details, raw test output
- State sync every 15 minutes
- Consider natural breakpoints for session handoff

### Recovery After Interruption

When resuming:
1. Run `python .claude/core/state.py recover`
2. Check git status for uncommitted changes
3. Validate build/test before continuing
4. Jump to current story/phase from state

---

## Quality Gates

| Gate | When | Check | On Fail |
|------|------|-------|---------|
| G1 | Before dev | Design complete, AC clear | Clarify with analyst/architect |
| G2 | After dev | `{platform.commands.build}` passes | Retry developer with build error |
| G3 | After build | `{platform.commands.test}` passes | Retry developer with test failures |
| G4 | After test | Coverage threshold met | Add tests, retry |
| G5 | Before story complete | Final build + test | DO NOT complete story, retry |
| G6 | If security-sensitive | Security scan passes | Remediate, retry |
| G7 | Before PR | Full build + test + lint | DO NOT create PR, return to Phase 2 |

---

## Clarifying Question Guidelines

### Pre-Analysis Questions (Step 1.1)

**Always ask when:**
- Goal is vague or multi-part without priority
- Technical constraints not specified
- Integration requirements unclear
- User data handling involved but not specified
- Multiple valid interpretations exist

**Ask fewer questions when:**
- Requirements are explicit and complete
- User provided detailed specifications
- Context makes approach obvious

### Pre-Plan Questions (Step 1.4)

**Always ask when:**
- Multiple valid technical approaches exist
- Story order could significantly impact development
- Dependencies between stories are complex
- User has shown strong opinions about technology

**Ask fewer questions when:**
- Standard patterns clearly apply
- Single obvious approach exists
- User explicitly requested autonomous execution

### How to Ask

1. Be specific - ask about concrete decisions
2. Offer options when possible (2-4 choices)
3. Provide your recommendation with rationale
4. Always include "Proceed with your judgment" as an option
5. Use the AskUserQuestion tool for structured questions

---

## Escalation Triggers

| Trigger | Action |
|---------|--------|
| 3 failed iterations on same story | Log blocker, output ESCALATION_REQUIRED |
| Security vulnerability found | Immediate escalation |
| 5 stories completed | Optional checkpoint |
| External dependency unavailable | Log blocker, escalate |
| User intervention requested | Output HUMAN_INTERVENTION_NEEDED |

---

## Commands Reference

- `/workflow [goal]` - Start full autonomous workflow
- `/status` - Check current progress
- `/implement [story]` - Implement single story with iteration loop
- `/review [files]` - Run code review

---

## Summary: Key Behavioral Rules

1. **Never exit without WORKFLOW_COMPLETE marker** (Stop hook enforces this)
2. **Always ask clarifying questions** before analysis and before planning
3. **Never skip build/test verification** - mandatory at every iteration
4. **Platform detection is dynamic** - never hardcode platform names or commands
5. **Iterate on failures** - use previous_failures context for retries
6. **Persist state** - enable recovery from any interruption
7. **Progress reports** - visibility every 3 stories or 30 minutes
8. **PR only after full verification** - Gate G7 must pass
