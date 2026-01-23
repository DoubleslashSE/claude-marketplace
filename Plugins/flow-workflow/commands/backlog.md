---
description: List and filter work items from FLOW.md backlog
---

# Backlog Command

Display and filter work items: **$ARGUMENTS**

Display and filter work items from the FLOW.md backlog.

## Usage

```
/flow-workflow:backlog                    # Show all items
/flow-workflow:backlog --status EXECUTE   # Filter by status
/flow-workflow:backlog --priority P0      # Filter by priority
/flow-workflow:backlog --status BACKLOG --priority P1  # Combined filter
```

## Available Filters

### Status Filter

| Status | Description |
|--------|-------------|
| `BACKLOG` | Not started |
| `DISCUSS` | In requirements gathering |
| `PLAN` | Creating task plan |
| `EXECUTE` | Implementing |
| `VERIFY` | Validating |
| `DONE` | Completed |
| `ON_HOLD` | Paused |
| `BLOCKED` | Waiting on dependency |

### Priority Filter

| Priority | Description |
|----------|-------------|
| `P0` | Critical |
| `P1` | High |
| `P2` | Medium |
| `P3` | Low |

## Output Format

### Full Backlog (No Filters)

```markdown
# Work Item Backlog

**Total**: 6 items
**Active**: ITEM-001

## Summary

| Status | Count |
|--------|-------|
| EXECUTE | 1 |
| BACKLOG | 2 |
| DONE | 3 |

## In Progress

### ITEM-001: Add user authentication ⬅ ACTIVE
**Status**: EXECUTE (task 3/5)
**Priority**: P1
**Progress**: 60%
**Phase**: Implementing validation logic

### ITEM-004: Fix cart calculation
**Status**: DISCUSS
**Priority**: P0
**Progress**: 25%
**Phase**: Gathering requirements

## Ready to Start

### ITEM-002: Dashboard improvements
**Priority**: P2
**Created**: 2024-01-20

### ITEM-003: User profile page
**Priority**: P3
**Created**: 2024-01-21

## Completed

### ITEM-005: Login page redesign ✓
**Completed**: 2024-01-22
**Duration**: 2 days

### ITEM-006: API rate limiting ✓
**Completed**: 2024-01-21
**Duration**: 1 day

---

**Commands**:
- `/flow-workflow:start ITEM-XXX` - Switch to item
- `/flow-workflow:go` - Continue active item
- `/flow-workflow:start "name"` - Create new item
```

### Filtered Backlog

```markdown
# Backlog: EXECUTE Status

**Filter**: status=EXECUTE
**Results**: 1 item

### ITEM-001: Add user authentication ⬅ ACTIVE
**Priority**: P1
**Progress**: 60%
**Current Task**: TASK-003 - Implement validation

---

**Other statuses**: BACKLOG (2), DONE (3)
**Clear filter**: `/flow-workflow:backlog`
```

### By Priority

```markdown
# Backlog: P0 Priority

**Filter**: priority=P0
**Results**: 1 item

### ITEM-004: Fix cart calculation
**Status**: DISCUSS
**Progress**: 25%
**Note**: Critical bug affecting checkout

---

**Other priorities**: P1 (2), P2 (2), P3 (1)
```

### Empty Results

```markdown
# Backlog: BLOCKED Status

**Filter**: status=BLOCKED
**Results**: 0 items

No blocked items.

**Suggestion**: View all items with `/flow-workflow:backlog`
```

## Reading from FLOW.md

Extract backlog table:

```markdown
## Backlog

| ID | Name | Status | Priority | Progress |
|----|------|--------|----------|----------|
| ITEM-001 | Add auth | EXECUTE | P1 | 60% |
| ITEM-002 | Dashboard | BACKLOG | P2 | 0% |
...
```

Parse each row and apply filters.

## Item Details

For each item in output, show:

**In Progress items:**
- ID and title
- Status with sub-status (task N/M)
- Priority
- Progress percentage
- Current activity

**Backlog items:**
- ID and title
- Priority
- Created date

**Completed items:**
- ID and title (with ✓)
- Completed date
- Duration

## Active Item Indicator

Mark the active item with `⬅ ACTIVE`:

```markdown
### ITEM-001: Add auth ⬅ ACTIVE
```

## Not Initialized

If no FLOW.md:

```markdown
**Workflow Not Initialized**

No backlog exists yet.

Initialize with: `/flow-workflow:start`
```

## Empty Backlog

If FLOW.md exists but no items:

```markdown
# Work Item Backlog

**Total**: 0 items

No work items yet.

**Create one**: `/flow-workflow:start "item name"`
**Quick task**: `/flow-workflow:quick "task"`
```

## Integration

Uses **state-management** skill to read FLOW.md backlog section.
