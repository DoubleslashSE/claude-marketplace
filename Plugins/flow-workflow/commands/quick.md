---
name: quick
description: Direct task execution without state files - for small, well-defined tasks that don't need workflow tracking
user_invocable: true
args: "<task description>"
---

# Quick Command

Execute a small, well-defined task directly without creating state files. This is the lightweight path for tasks that don't need full workflow tracking.

## Usage

```
/flow:quick "Fix the typo in README"
/flow:quick "Add null check to getUserById"
/flow:quick "Update the version to 2.0.0"
```

## When to Use Quick Mode

**Appropriate for:**
- Single, well-defined changes
- Bug fixes with obvious solutions
- Small features with clear requirements
- Tasks completable in <5 steps
- No stakeholder discussion needed

**Not appropriate for:**
- Complex features with unclear requirements
- Changes affecting multiple systems
- Work requiring extensive planning
- Tasks with potential conflicts

## What Quick Mode Does

1. **Assess task** - Verify it's suitable for quick mode
2. **Clarify** (if needed) - Ask 1-2 critical questions max
3. **Plan minimally** - Create 1-3 mental tasks
4. **Execute directly** - Implement the change
5. **Verify** - Run basic checks
6. **Commit** - Create atomic commit
7. **Done** - No state files created

## Execution Flow

### Step 1: Task Assessment

```markdown
**Quick Mode Assessment**

Task: "[description]"

Suitability:
- [x] Single, focused change
- [x] Clear requirements
- [x] Limited scope (1-5 files)
- [x] No complex dependencies

**Assessment**: SUITABLE for quick mode
```

If not suitable:
```markdown
**Task May Be Too Complex**

This task might need full workflow:
- [reason 1]
- [reason 2]

Options:
1. Continue with quick mode anyway
2. Use full workflow: `/flow:start "[task]"`
```

### Step 2: Clarification (If Needed)

Only ask if critical ambiguity:

```javascript
AskUserQuestion({
  questions: [{
    question: "Quick clarification: [specific question]?",
    header: "Clarify",
    options: [
      { label: "[Option A]", description: "[brief]" },
      { label: "[Option B]", description: "[brief]" }
    ]
  }]
})
```

Skip if task is clear enough.

### Step 3: Direct Execution

Execute the task directly:

1. Read relevant files
2. Make the changes
3. Verify changes work
4. Create commit

### Step 4: Verification

Run minimal checks:

```bash
# Build check
[build command]

# Test relevant area (if applicable)
[test command]
```

### Step 5: Commit

```bash
git add [changed files]
git commit -m "[commit message]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Output Format

### Starting

```markdown
**Quick Mode**

Task: "[description]"

Executing directly...
```

### During Execution

```markdown
**Quick Progress**

- [x] Read [file]
- [x] Made change
- [ ] Verifying...
```

### Completion

```markdown
**Quick Mode Complete**

Task: "[description]"

**Changes**:
- [file]: [what changed]

**Verification**:
- Build: ✓ PASS
- Tests: ✓ PASS

**Commit**: [hash] - [message]

Done!
```

## No State Files

Quick mode does **not** create:
- `.flow/` directory
- `FLOW.md`
- `ITEM-XXX.md`

The task is executed and completed without persisting workflow state.

## Capability Routing

Quick mode still uses capability discovery for complex tasks:

1. If task appears to need TDD → Check for `tdd-implementation` capability
2. If task is infrastructure → Check for `infrastructure` capability
3. Route to discovered plugin or use built-in skills

But routing is implicit, not announced verbosely.

## Escalation

If during execution you discover the task is more complex:

```markdown
**Escalating to Full Workflow**

Quick mode revealed complexity:
- [reason]

Creating work item and transitioning...

Use `/flow:go` to continue with full workflow.
```

This creates state files and transitions to regular workflow.

## Signs to Escalate

- More than 3 clarifying questions needed
- More than 5 files affected
- Discovering unclear requirements
- Finding conflicts with other code
- Needing stakeholder input

## Comparison to Full Workflow

| Aspect | Quick Mode | Full Workflow |
|--------|------------|---------------|
| State files | None | FLOW.md + ITEM-XXX.md |
| Phases | None | DISCUSS → PLAN → EXECUTE → VERIFY |
| Tracking | None | Full checkpoint/resume |
| Suitable for | Small tasks | Complex features |
| Time | Fast | Thorough |

## Error Handling

### Verification Failure

```markdown
**Quick Mode Failed**

Verification error: [error]

Options:
1. Fix and retry
2. Escalate to full workflow
3. Abort
```

### Commit Failure

```markdown
**Commit Failed**

Error: [pre-commit hook error]

Fixing and retrying...
```
