# Flow Workflow Plugin

A **lightweight meta-orchestrator** for Claude Code that leverages your installed plugin ecosystem. Unlike monolithic workflow systems, flow-workflow delegates to specialized plugins when available and falls back to built-in defaults otherwise.

## Key Differentiator

**"The meta-workflow that makes your plugins work together."**

Flow-workflow is technology-agnostic and plugin-aware. It discovers what plugins you have installed and routes work to the best-matched agent for each capability needed.

## Overview

Flow Workflow helps you manage complex development tasks through structured phases:

```
DISCUSS → PLAN → EXECUTE → VERIFY → DONE
```

With just **5 commands** and **2 state files**, it provides:
- Backlog management for multiple work items
- Capability-based routing to installed plugins
- Explicit state tracking with checkpoint/resume
- Context budget awareness (stays under 40%)

## Quick Start

### Start a Work Item

```
/flow:start "Add user authentication"
```

This initializes the project (if needed), creates a work item, and begins the DISCUSS phase.

### Continue Working

```
/flow:go
```

Smart continuation from current state - automatically routes to the right phase and agent.

### Quick Task (No State Files)

```
/flow:quick "Fix the typo in README"
```

Direct execution for small, well-defined tasks.

## Commands (5 Total)

| Command | Description |
|---------|-------------|
| `/flow:start [name]` | Initialize, create item, or switch to existing |
| `/flow:go` | Smart continuation from current state |
| `/flow:status` | Show state, context budget, capabilities |
| `/flow:backlog` | List and filter work items |
| `/flow:quick "task"` | Direct execution without state |

## State Files (2 Patterns)

### FLOW.md (Project Level)

```markdown
# Flow Project State

## Vision
[Project vision]

## Backlog
| ID | Name | Status | Priority | Progress |
|----|------|--------|----------|----------|
| ITEM-001 | Auth | EXECUTE | P1 | 60% |

## Active Item
ITEM-001

## Capabilities Cache
[Discovered plugin mappings]
```

### ITEM-XXX.md (Per Work Item)

```markdown
# ITEM-001: User Authentication

## Phase: EXECUTE (task 3/5)

## Decisions
[Numbered decisions with rationale]

## Requirements
[Captured requirements]

## Tasks
[XML-structured atomic tasks]

## Checkpoint
[Current state for resume]
```

## Capability-Based Routing

Flow-workflow discovers installed plugins and routes work based on capabilities:

| Capability | When Used | If No Plugin |
|------------|-----------|--------------|
| requirements-gathering | DISCUSS | defaults/interviewer |
| brainstorming | DISCUSS | defaults/interviewer |
| codebase-analysis | DISCUSS, PLAN | defaults/researcher |
| tdd-implementation | EXECUTE | defaults/executor |
| code-implementation | EXECUTE | defaults/executor |
| infrastructure | EXECUTE | defaults/executor |
| code-review | VERIFY | validator |
| requirements-validation | VERIFY | validator |

### Delegation Announcement

When routing, you'll see:

```markdown
**Delegating tdd-implementation** → dotnet-tdd:implementer
Matched via keyword scoring (High confidence)
```

Or when using built-in:

```markdown
**Using built-in agent** for infrastructure → flow-workflow:defaults/executor
No installed plugin matched this capability
```

## Agents

| Agent | Role |
|-------|------|
| `coordinator` | Core orchestration, phase transitions, capability routing |
| `validator` | Built-in UAT + delegates code-review to plugins |
| `defaults/interviewer` | Fallback for requirements/brainstorming |
| `defaults/researcher` | Fallback for codebase analysis |
| `defaults/executor` | Fallback for implementation |

## Workflow Phases

### DISCUSS Phase

- Gathers requirements through adaptive questioning
- Records decisions with rationale
- Detects and resolves conflicts
- Delegates to `requirements-gathering` capability (or defaults/interviewer)

### PLAN Phase

- Decomposes work into atomic, committable tasks
- Handled by coordinator (built-in)
- May use `codebase-analysis` for understanding existing code

### EXECUTE Phase

- Implements tasks one at a time
- Routes based on task type:
  - TDD tasks → `tdd-implementation` capability
  - Infrastructure → `infrastructure` capability
  - General code → `code-implementation` capability
- Creates atomic commits on success

### VERIFY Phase

- Runs automated checks (build, test, lint)
- Delegates code review to discovered plugin
- Conducts user acceptance testing
- Collects sign-off

## Atomic Task Format

Tasks in ITEM-XXX.md use XML:

```xml
<task id="TASK-001" status="pending">
  <name>Implement user service</name>
  <files>
    <file action="create">src/services/UserService.ts</file>
  </files>
  <actions>
    <action>Create UserService class</action>
    <action>Add CRUD methods</action>
  </actions>
  <verify>
    <step>npm test -- UserService</step>
  </verify>
  <commit>feat(user): add UserService with CRUD</commit>
</task>
```

## Context Budget

The coordinator monitors context usage:

```markdown
## Context Monitor
- Current: 32%
- Threshold: 50%
- Fresh agents spawned: 3
```

When approaching 50%, it spawns fresh agents to continue with clean context.

## Skills

| Skill | Purpose |
|-------|---------|
| `state-management` | FLOW.md and ITEM-XXX.md operations |
| `capability-discovery` | Plugin enumeration and routing |
| `atomic-tasks` | Task structure and XML format |
| `exploration-tracking` | Discussion territory tracking |
| `conflict-detection` | Conflict identification |
| `context-engineering` | Context window management |
| `workflow-orchestration` | Phase coordination |

## Plugin Integration

Flow-workflow works with installed plugins:

| Plugin | Capabilities Provided |
|--------|----------------------|
| business-analyst | requirements-gathering, codebase-analysis |
| dotnet-tdd | tdd-implementation, code-review |
| node-tdd | tdd-implementation, code-review |
| workshop-facilitator | brainstorming |
| devops-azure-infrastructure | infrastructure |

If you don't have specialized plugins, built-in defaults handle all capabilities.

## Example Session

```
> /flow:start "Add user registration"

**Work Item Created**: ITEM-001
**Phase**: DISCUSS

**Delegating requirements-gathering** → business-analyst:stakeholder-interviewer
Matched via keyword scoring

[Interview begins...]

> /flow:go

**Phase Transition**: DISCUSS → PLAN
Creating atomic tasks...

> /flow:go

**Continuing EXECUTE** (task 1/4)
**Delegating tdd-implementation** → dotnet-tdd:implementer

[Implementation continues...]

> /flow:status

**Active Item**: ITEM-001 - Add user registration
**Phase**: EXECUTE (task 3/4)
**Progress**: 75%

**Context**: 28% (within budget)

**Capabilities**:
- tdd-implementation: dotnet-tdd:implementer (High)
- code-review: dotnet-tdd:reviewer (High)
```

## Comparison

| Metric | Before | After |
|--------|--------|-------|
| Commands | 12 | 5 |
| Agents | 6 | 3 + 3 defaults |
| State files per item | 5+ | 1 |
| Unique value | Capability discovery | **Plugin ecosystem orchestration** |

## Best Practices

1. **Use `/flow:go`** - It figures out what to do next
2. **Check `/flow:status`** - See context budget and capabilities
3. **Install specialized plugins** - Better quality than defaults
4. **Don't skip VERIFY** - Even for small changes
5. **Review state files** - They're human-readable for a reason

## License

MIT
