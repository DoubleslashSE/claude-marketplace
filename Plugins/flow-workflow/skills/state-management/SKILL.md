---
name: state-management
description: Simplified state file management with consolidated FLOW.md (project) and ITEM-XXX.md (per-item) files
triggers:
  - workflow state
  - state files
  - FLOW.md
  - checkpoint
  - resume
  - backlog
  - work item
---

# State Management Skill

This skill provides techniques for managing workflow state through simplified, consolidated markdown files. The refactored structure uses just two file patterns: a single `FLOW.md` at project level and one `ITEM-XXX.md` per work item.

## Core Principles

1. **Minimal Footprint**: Only two file patterns instead of 9+
2. **Single Source of Truth**: FLOW.md contains backlog + project context, ITEM-XXX.md contains everything about one item
3. **Human Readable**: All state in plain markdown, easy to edit
4. **Checkpoint Recovery**: State enables resumption from any interruption
5. **Context Budget Awareness**: Track and report context usage

## Directory Structure

```
.flow/
├── FLOW.md           # Project state + backlog (single file)
└── items/
    ├── ITEM-001.md   # All state for work item 001
    ├── ITEM-002.md   # All state for work item 002
    └── ...
```

## State Files Overview

| File | Purpose | Contains |
|------|---------|----------|
| `FLOW.md` | Project-level state | Vision, backlog, active item, capabilities cache |
| `ITEM-XXX.md` | Per-item state | Phase, decisions, requirements, tasks, checkpoint |

## FLOW.md Structure

The single project file contains:

### Sections

1. **Vision**: High-level project vision
2. **Backlog**: Table of all work items with status
3. **Active Item**: Currently active item pointer
4. **Capabilities Cache**: Discovered plugin mappings with timestamp

### Template

See `templates.md` for the full FLOW.md template.

## ITEM-XXX.md Structure

Each work item has a single consolidated file containing:

### Sections

1. **Header**: Item ID, title, timestamps
2. **Phase**: Current phase and progress (DISCUSS/PLAN/EXECUTE/VERIFY)
3. **Decisions**: Numbered decisions with rationale
4. **Requirements**: Extracted functional/non-functional requirements
5. **Tasks**: XML-structured atomic tasks (when in EXECUTE)
6. **Checkpoint**: Current state snapshot for resume

### Template

See `templates.md` for the full ITEM-XXX.md template.

## Work Item States

Items progress through these phases:

| Phase | Description | Next Phase |
|-------|-------------|------------|
| `BACKLOG` | Defined but not started | DISCUSS |
| `DISCUSS` | Gathering requirements | PLAN |
| `PLAN` | Creating task plan | EXECUTE |
| `EXECUTE` | Implementing tasks | VERIFY |
| `VERIFY` | Validating implementation | DONE |
| `DONE` | Completed | (terminal) |
| `ON_HOLD` | Paused intentionally | Previous |
| `BLOCKED` | Waiting on dependency | Previous |

## State Operations

### Initialize Project

```markdown
1. Create .flow/ directory if not exists
2. Create .flow/items/ directory
3. Scan for installed plugins
4. Detect project type from file patterns
5. Create FLOW.md with empty backlog + capabilities
```

### Create Work Item (`/flow:start`)

```markdown
1. Read FLOW.md to get next item number
2. Generate ITEM-XXX ID
3. Create .flow/items/ITEM-XXX.md with DISCUSS phase
4. Update FLOW.md backlog table
5. Set as active item in FLOW.md
```

### Switch Active Item

```markdown
1. Update checkpoint in current item's file
2. Update FLOW.md active item pointer
3. Load new item's context
```

### Phase Transition

```markdown
1. Verify completion criteria for current phase
2. Update phase in ITEM-XXX.md
3. Create checkpoint snapshot
4. Initialize next phase section
```

### Create Checkpoint

```markdown
1. Record current phase and task progress
2. Capture context budget percentage
3. List next recommended action
4. Add timestamp
```

### Resume from Checkpoint

```markdown
1. Read FLOW.md to get active item
2. Read ITEM-XXX.md checkpoint section
3. Restore context from checkpoint
4. Identify next action
5. Continue workflow
```

## Context Budget Tracking

Track context usage in FLOW.md and report:

```markdown
## Context Monitor

- Current session: [X]% (limit: 50% before fresh agent)
- Last auto-spawn: [TIMESTAMP]
- Fresh agents this session: [N]
```

## State Validation

Before any phase transition, validate:

1. **Completeness**: Required sections filled
2. **Consistency**: No contradictory decisions
3. **Recoverability**: Checkpoint exists for current progress

## Best Practices

### Writing State Updates

- Use timestamps in ISO format
- Include brief rationale for decisions
- Mark status clearly (DONE, BLOCKED, etc.)
- Keep checkpoint current

### Reading State for Context

- Load FLOW.md first for active item
- Load ITEM-XXX.md for current phase details
- Check checkpoint before proceeding

### Handling Phase Transitions

- Always create checkpoint before transition
- Update both FLOW.md backlog and ITEM-XXX.md
- Announce transition to user

## Migration from Old Format

If legacy `.flow/` structure detected (BACKLOG.md, ACTIVE.md, PROJECT.md, etc.):

1. Read existing state files
2. Consolidate into FLOW.md
3. Consolidate per-item files into ITEM-XXX.md
4. Backup old files to `.flow/legacy/`
5. Report migration complete

## Integration Points

State management integrates with:

- **Capability Discovery**: Cache plugin mappings in FLOW.md
- **Workflow Orchestration**: Phase transitions and checkpoints
- **Smart Continuation**: Resume from checkpoint via `/flow:go`

See `templates.md` for full file templates.
