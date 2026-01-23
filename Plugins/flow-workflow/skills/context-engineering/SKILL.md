---
name: context-engineering
description: Context window management techniques for maintaining efficiency and preventing context bloat
triggers:
  - context management
  - fresh context
  - context window
  - context bloat
---

# Context Engineering Skill

This skill provides techniques for managing context effectively throughout the workflow to prevent bloat and maintain efficiency.

## Core Principles

1. **Stay Under 40%**: Orchestrator should never exceed 40% context usage
2. **Fresh Context Per Task**: Each major task gets a fresh agent with clean context
3. **Load Only What's Needed**: Don't load full files when summaries suffice
4. **Delegate Deep Work**: Spawn agents for context-heavy operations

## Context Budget Guidelines

| Role | Context Budget | Reason |
|------|----------------|--------|
| Orchestrator | <40% | Needs room for coordination |
| Interviewer | <70% | Conversation history accumulates |
| Planner | <60% | Needs to see requirements + codebase patterns |
| Executor | <80% | Can focus on single task deeply |
| Verifier | <60% | Needs to cross-reference requirements and code |

## Context Loading Strategies

### Selective Loading

Instead of loading full files:

```markdown
BAD: Read entire codebase
GOOD: Read specific files needed for current task
BEST: Read summaries, then specific sections
```

### Hierarchical Loading

Load context in layers:
1. **L1 Summary**: High-level overview (FLOW.md)
2. **L2 Details**: Item-specific state (ITEM-XXX.md)
3. **L3 Specifics**: Task-specific files (only files in current task)

### Incremental Loading

Load more context only when needed:

```markdown
1. Start with minimal context
2. Identify what's missing
3. Load specific missing pieces
4. Repeat as needed
```

## Fresh Context Patterns

### When to Use Fresh Context

Spawn a fresh agent when:
- Starting a new task in EXECUTE phase
- Moving to a new phase
- Current context is getting heavy
- Deep codebase exploration needed

### Fresh Context Handoff

When spawning fresh agent:

```markdown
Include in handoff:
- Task ID and definition
- Key decisions from ITEM-XXX.md
- Relevant file paths
- Success criteria

Exclude:
- Full conversation history
- Files not related to task
- Exploration paths not taken
```

### Context Reset Points

Natural points to reset context:
- Phase transitions
- After each completed task
- After resolving a blocker
- After user requests fresh start

## Context Monitoring

### Signs of Context Bloat

Watch for:
- Repeated information in responses
- Slower response times
- Forgetting earlier context
- Inconsistent references

### Context Health Check

Periodically verify:
- Can still reference key decisions?
- Can identify current task?
- Can access state files?
- Response quality maintained?

## State File as External Memory

Use state files as external memory:

### What to Store in Files
- All decisions (ITEM-XXX.md Decisions section)
- Exploration progress (ITEM-XXX.md Exploration section)
- Task definitions (ITEM-XXX.md Tasks section)
- Requirements (ITEM-XXX.md Requirements section)

### What to Keep in Context
- Current phase and task
- Key constraints
- Immediate next steps
- Recent decisions (can reference file for older ones)

## Delegation Patterns

### Deep Exploration Delegation

```markdown
Task: Understand how authentication works in this codebase

Instead of:
- Loading all auth-related files into orchestrator context

Do:
- Spawn researcher agent with specific question
- Receive summary findings
- Keep summary in orchestrator context
```

### Implementation Delegation

```markdown
Task: Implement TASK-005

Instead of:
- Loading full codebase patterns and task into orchestrator

Do:
- Spawn executor with task definition + relevant files only
- Receive completion status
- Update state files
```

## Context Compression Techniques

### Summary Generation

After deep work, compress to summary:

```markdown
Before compression: [Full exploration transcript]

After compression:
**Exploration Result**: Authentication
- Uses JWT tokens
- Stored in localStorage
- Refresh flow in AuthService.refresh()
- Decision needed: token expiry duration
```

### Reference Instead of Inline

```markdown
BAD: Include full task XML in every message
GOOD: "Executing TASK-005 (see ITEM-XXX.md Tasks section)"
```

### Checkpoint Snapshots

At checkpoints, snapshot key state:

```markdown
### CHECKPOINT: EXECUTE-001
**Context snapshot**:
- Phase: EXECUTE
- Progress: 5/10 tasks
- Current: TASK-006
- Blocked: None
- Key decisions: Use JWT (DECISION-003)
```

## Integration with Workflow

### During DISCUSS
- Keep exploration map in ITEM-XXX.md
- Summarize findings per area
- Reference decisions by ID

### During PLAN
- Read requirements once, create tasks
- Don't reload requirements repeatedly
- Reference task IDs not full definitions

### During EXECUTE
- Fresh context per task
- Load only task + relevant files
- Update state after each task

### During VERIFY
- Load summary of completed work
- Cross-reference requirements by ID
- Keep verification results in ITEM-XXX.md

## Best Practices

1. **Reference, don't repeat**: Use IDs and file paths
2. **Summarize immediately**: After deep work, compress findings
3. **Clean handoffs**: Fresh agents get focused context
4. **Use state files**: They're your external memory
5. **Monitor bloat**: Watch for degradation signs
6. **Delegate proactively**: Don't wait until context is full
