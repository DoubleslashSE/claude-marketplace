---
description: Initialize project, create new work item, or switch to existing item - all in one command
---

# Start Command

Initialize, create, or switch work items: **$ARGUMENTS**

This command handles initialization, work item creation, and item switching in one unified interface.

## Usage

```
/flow-workflow:start                     # Initialize if needed, show backlog
/flow-workflow:start "Add auth"          # Create/switch to item named "Add auth"
/flow-workflow:start ITEM-001            # Switch to existing item
/flow-workflow:start "Fix bug" --priority P0  # Create P0 priority item
```

## Behavior

### No Arguments: Initialize / Show Status

If no arguments provided:

1. Check if `.flow/FLOW.md` exists
2. If not initialized:
   - Create `.flow/` directory structure
   - Scan plugins for capabilities
   - Detect project type
   - Create `FLOW.md` with empty backlog
3. If initialized:
   - Show current active item
   - Show backlog summary
   - Suggest next actions

### With Item Name: Create or Switch

If item name provided:

1. Check if it matches existing item (ITEM-XXX pattern or title)
2. If existing item found:
   - Checkpoint current item (if any)
   - Switch active item to matched item
   - Show item status
3. If new item:
   - Generate next ITEM-XXX ID
   - Create `ITEM-XXX.md` in `.flow/items/`
   - Update `FLOW.md` backlog
   - Set as active item
   - Begin DISCUSS phase

## Initialization Steps

When initializing a new project:

### Step 1: Create Directory Structure

```
.flow/
└── items/          # Work item files go here
```

### Step 2: Scan for Plugins

```markdown
1. List directories in Plugins/
2. For each plugin:
   - Read .claude-plugin/plugin.json
   - Scan agents/*.md for descriptions
   - Scan commands/*.md for descriptions
   - Match to capability categories using keywords
3. Build capability map
```

### Step 3: Detect Project Type

| File Pattern | Project Type |
|--------------|--------------|
| `*.csproj`, `*.sln` | dotnet |
| `package.json` | node |
| `*.py`, `requirements.txt` | python |
| `go.mod` | go |
| `Cargo.toml` | rust |
| `pom.xml`, `build.gradle` | java |

### Step 4: Create FLOW.md

```markdown
# Flow Project State

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Project Type**: [detected]

## Vision

[To be defined]

## Backlog

| ID | Name | Status | Priority | Progress |
|----|------|--------|----------|----------|

**Summary**: 0 items

## Active Item

**Current**: None

## Capabilities Cache

**Last Scanned**: [TIMESTAMP]

| Capability | Matched Plugin | Agent/Command |
|------------|----------------|---------------|
[discovered capabilities]

## Context Monitor

- Coordinator usage: 0%
- Fresh agents spawned: 0
```

## Creating New Work Item

### Step 1: Generate ID

Read FLOW.md to find highest ITEM-XXX number, increment.

### Step 2: Create ITEM-XXX.md

```markdown
# ITEM-XXX: [Title]

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Phase: DISCUSS (0%)

Starting requirements exploration.

## Decisions

[No decisions yet]

## Requirements

[To be gathered]

## Tasks

[To be created during PLAN]

## Checkpoint

**Timestamp**: [TIMESTAMP]
**Phase**: DISCUSS
**Progress**: 0%
**Next Action**: Begin requirements exploration
```

### Step 3: Update FLOW.md Backlog

Add row to backlog table:

```markdown
| ITEM-XXX | [Title] | DISCUSS | [Priority] | 0% |
```

### Step 4: Set Active Item

Update Active Item section in FLOW.md.

## Switching Items

### Step 1: Checkpoint Current Item

Update checkpoint in current ITEM-XXX.md.

### Step 2: Update Active Item

Change Active Item section in FLOW.md.

### Step 3: Load New Item Context

Read ITEM-XXX.md for new item's state.

## Output Format

### Initialization Complete

```markdown
**Flow Workflow Initialized**

**Project Type**: [type]

**Capabilities Discovered**:
| Capability | Plugin | Agent |
|------------|--------|-------|
[capabilities]

**Next Steps**:
- `/flow-workflow:start "item name"` - Create work item
- `/flow-workflow:quick "task"` - Quick execution
```

### Item Created

```markdown
**Work Item Created**

**ID**: ITEM-XXX
**Title**: [title]
**Priority**: [priority]
**Phase**: DISCUSS

Beginning requirements exploration...

[Spawns interviewer or discovered agent]
```

### Item Switched

```markdown
**Switched to ITEM-XXX**

**Title**: [title]
**Phase**: [phase]
**Progress**: [progress]%

**Last checkpoint**: [summary]

Ready to continue. Use `/flow-workflow:go` to resume.
```

### Already Initialized (No Args)

```markdown
**Flow Workflow Status**

**Active Item**: [ITEM-XXX - Title] or "None"
**Phase**: [phase]

**Backlog**: [N] items
- [N] in progress
- [N] in backlog
- [N] completed

**Next Steps**:
- `/flow-workflow:go` - Continue current work
- `/flow-workflow:start "name"` - Create new item
- `/flow-workflow:backlog` - View all items
```

## Error Handling

### Directory Creation Failure

```markdown
**Error**: Could not create .flow/ directory
Check file permissions.
```

### Item Not Found (When Switching)

```markdown
**Item Not Found**: "[input]"

Did you mean one of these?
- ITEM-001: [similar title]
- ITEM-002: [similar title]

Or create new: `/flow-workflow:start "[input]"`
```

## Integration

This command uses:
- **state-management** skill for file creation
- **capability-discovery** skill for plugin scanning
- **coordinator** agent for spawning phase agents
