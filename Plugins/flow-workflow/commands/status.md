---
name: status
description: Show current workflow state, context budget, discovered capabilities, and active item progress
user_invocable: true
args: "[--refresh]"
---

# Status Command

Display comprehensive workflow status including active item, context budget, and discovered capabilities.

## Usage

```
/flow:status              # Show current status
/flow:status --refresh    # Refresh capability cache and show status
```

## What It Shows

### 1. Active Item Status

```markdown
## Active Item

**Item**: ITEM-001 - Add user authentication
**Phase**: EXECUTE (task 3/5)
**Progress**: 60%

**Current Task**: TASK-003 - Implement validation logic
**Started**: 2024-01-23T10:30:00Z

**Last Checkpoint**:
- Phase: EXECUTE
- Task: TASK-002 completed
- Next: Continue to TASK-003
```

### 2. Context Budget

```markdown
## Context Monitor

| Metric | Value |
|--------|-------|
| Coordinator usage | 32% |
| Auto-spawn threshold | 50% |
| Fresh agents this session | 2 |

**Status**: ✓ Within budget
```

Or when approaching limit:

```markdown
## Context Monitor

| Metric | Value |
|--------|-------|
| Coordinator usage | 47% |
| Auto-spawn threshold | 50% |
| Fresh agents this session | 4 |

**Status**: ⚠ Approaching threshold - will spawn fresh agent soon
```

### 3. Discovered Capabilities

```markdown
## Capabilities

**Project Type**: dotnet
**Last Scanned**: 2024-01-23T09:00:00Z

| Capability | Plugin | Agent | Confidence |
|------------|--------|-------|------------|
| requirements-gathering | business-analyst | stakeholder-interviewer | High |
| tdd-implementation | dotnet-tdd | implementer | High |
| code-review | dotnet-tdd | reviewer | High |
| codebase-analysis | business-analyst | codebase-analyzer | Medium |
| brainstorming | workshop-facilitator | brainstorm | High |
| infrastructure | - | (default) | - |
| code-implementation | - | (default) | - |

**Defaults in use**: 2 capabilities using built-in agents
```

### 4. Backlog Summary

```markdown
## Backlog Summary

| Status | Count |
|--------|-------|
| In Progress | 1 |
| Backlog | 2 |
| Done | 3 |
| **Total** | **6** |

**Recent Items**:
- ITEM-001: Add auth (EXECUTE 60%)
- ITEM-002: Dashboard (BACKLOG)
- ITEM-003: User profile (BACKLOG)
```

## Full Output Format

```markdown
# Flow Workflow Status

## Active Item

**Item**: ITEM-001 - [Title]
**Phase**: [PHASE] ([progress])
**Current**: [task or activity]

**Checkpoint**:
- [checkpoint details]

---

## Context Monitor

- Coordinator: [X]%
- Threshold: 50%
- Fresh agents: [N]
- Status: [✓ OK | ⚠ Warning]

---

## Capabilities

**Project**: [type]
**Scanned**: [timestamp]

| Capability | Plugin | Confidence |
|------------|--------|------------|
[capability rows]

**Gaps**: [N] using defaults

---

## Backlog

| Status | Count |
|--------|-------|
[status counts]

---

## Quick Commands

- `/flow:go` - Continue work
- `/flow:start "name"` - New item
- `/flow:backlog` - Full backlog
- `/flow:quick "task"` - Quick execution
```

## Refresh Option

When `--refresh` is provided:

1. Re-scan Plugins/ directory
2. Rebuild capability map with fresh keyword matching
3. Update FLOW.md capability cache
4. Report any changes

```markdown
**Capability Refresh**

Scanned: [N] plugins
Changes detected:
- Added: [plugin:agent] → [capability]
- Removed: [plugin:agent] (plugin uninstalled)
- Updated: [plugin:agent] confidence changed

Cache updated in FLOW.md.
```

## Not Initialized

If `.flow/FLOW.md` doesn't exist:

```markdown
**Workflow Not Initialized**

No .flow/ directory found.

Initialize with: `/flow:start`
```

## No Active Item

If initialized but no active item:

```markdown
## Active Item

**Current**: None

Start working:
- `/flow:start "item name"` - Create new item
- `/flow:start ITEM-XXX` - Resume existing item
- `/flow:backlog` - View all items
```

## Reading State

This command reads:

1. **FLOW.md**:
   - Active item pointer
   - Backlog table
   - Capabilities cache
   - Project type

2. **ITEM-XXX.md** (if active item):
   - Current phase
   - Phase progress
   - Current task
   - Checkpoint

## Integration

Uses:
- **state-management** skill for reading files
- **capability-discovery** skill for refresh
