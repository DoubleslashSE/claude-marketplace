---
name: go
description: Smart continuation - automatically resumes from current state, transitions phases, and routes to appropriate agents
user_invocable: true
---

# Go Command

This is the primary command for continuing workflow execution. It reads current state and intelligently determines the next action.

## Usage

```
/flow:go                    # Continue from current state
```

## Smart Continuation Logic

```markdown
1. Read FLOW.md to get active item
2. If no active item:
   → Prompt user to /flow:start
3. Read ITEM-XXX.md to get current phase/task
4. Determine next action based on state:

   DISCUSS incomplete → Continue with interviewer/discovered agent
   DISCUSS complete   → Transition to PLAN
   PLAN incomplete    → Continue planning (coordinator)
   PLAN complete      → Transition to EXECUTE
   EXECUTE incomplete → Execute next task (delegate or default)
   EXECUTE complete   → Transition to VERIFY
   VERIFY incomplete  → Continue verification (validator)
   VERIFY complete    → Mark DONE, suggest next item

5. Route to appropriate agent
6. Update checkpoint after action
```

## Phase Continuation Details

### DISCUSS Phase

**When incomplete:**
1. Check capability cache for `requirements-gathering` or `brainstorming` match
2. Announce delegation decision
3. Spawn matched agent or `defaults/interviewer`
4. Agent continues from last checkpoint in ITEM-XXX.md

**When complete:**
1. Create checkpoint with "DISCUSS complete"
2. Update phase to PLAN in ITEM-XXX.md
3. Update FLOW.md backlog status
4. Announce: "Transitioning to PLAN phase"
5. Begin task decomposition (coordinator handles this)

### PLAN Phase

**When incomplete:**
1. Coordinator continues creating atomic tasks
2. Read requirements from ITEM-XXX.md
3. May use `codebase-analysis` capability if needed
4. Update tasks section in ITEM-XXX.md

**When complete:**
1. Create checkpoint with "PLAN complete"
2. Update phase to EXECUTE in ITEM-XXX.md
3. Update FLOW.md backlog status
4. Announce: "Transitioning to EXECUTE phase"
5. Determine first task to execute

### EXECUTE Phase

**When incomplete:**
1. Find next pending task in ITEM-XXX.md
2. Determine capability needed:
   - TDD task? → `tdd-implementation`
   - Infra task? → `infrastructure`
   - General code? → `code-implementation`
3. Check capability cache for match
4. Announce delegation decision
5. Spawn matched agent or `defaults/executor`
6. Agent executes single task, updates status

**When complete:**
1. All tasks marked `completed`
2. Create checkpoint with "EXECUTE complete"
3. Update phase to VERIFY in ITEM-XXX.md
4. Update FLOW.md backlog status
5. Announce: "Transitioning to VERIFY phase"

### VERIFY Phase

**When incomplete:**
1. Spawn validator agent
2. Validator runs automated checks
3. Validator may delegate code review to discovered plugin
4. Validator guides UAT
5. Validator collects sign-off

**When complete:**
1. User approved implementation
2. Mark item as DONE in both files
3. Clear or update active item in FLOW.md
4. Announce completion summary
5. Suggest next item if any in backlog

## State Reading

### From FLOW.md

```markdown
Extract:
- Active item ID
- Project type (for capability routing)
- Capability cache (for delegation)
```

### From ITEM-XXX.md

```markdown
Extract:
- Current phase
- Phase progress
- Current task (if EXECUTE)
- Last checkpoint
- Blockers (if any)
```

## Delegation Routing

### Capability Lookup

```markdown
1. Determine capability needed
2. Read capability cache from FLOW.md
3. If match found:
   → Announce: "Delegating [capability] to [plugin:agent]"
   → Spawn via Task tool
4. If no match:
   → Announce: "Using built-in [default-agent]"
   → Spawn default agent
```

### Delegation Announcement

```markdown
**Continuing EXECUTE phase** (task 3/5)

**Delegating code-implementation** → developer:implementer
Matched via keyword scoring (High confidence)

Spawning agent for TASK-003...
```

Or:

```markdown
**Continuing DISCUSS phase**

**Using built-in agent** → flow-workflow:defaults/interviewer
No plugin matched requirements-gathering

Beginning requirements exploration...
```

## Output Format

### Continuing Phase

```markdown
**Continuing [PHASE]**

**Item**: ITEM-XXX - [Title]
**Progress**: [X]%
**Current**: [What's being done]

**Delegation**: [capability] → [agent] (reason)

[Phase-specific status]
```

### Phase Transition

```markdown
**Phase Transition**

**Completed**: [PHASE]
**Next**: [NEW_PHASE]

**Summary**: [What was accomplished]

Beginning [NEW_PHASE]...
```

### No Active Item

```markdown
**No Active Work Item**

Create or select a work item first:

- `/flow:start "item name"` - Create new item
- `/flow:start ITEM-XXX` - Switch to existing item
- `/flow:backlog` - View all items
```

### Workflow Complete

```markdown
**Workflow Complete!**

**Item**: ITEM-XXX - [Title]
**Duration**: [time]
**Tasks completed**: [N]
**Commits created**: [N]

**Next in backlog**:
- ITEM-YYY: [Title] (BACKLOG)

Start next item? `/flow:start ITEM-YYY`
```

## Error Handling

### Blocker Detected

```markdown
**Workflow Blocked**

**Item**: ITEM-XXX
**Phase**: [phase]
**Blocker**: [description]

**Options**:
1. Address the blocker manually
2. Skip and continue (if possible)
3. Mark item as ON_HOLD
```

### Agent Failure

```markdown
**Agent Error**

The [agent] encountered an error:
[error description]

**State preserved** at checkpoint.

**Options**:
1. Retry with `/flow:go`
2. Check `/flow:status` for details
3. Manual intervention needed
```

## Context Budget Awareness

Before spawning agent, check context budget:

```markdown
If coordinator context > 40%:
  - Create checkpoint
  - Spawn fresh agent
  - Agent continues from checkpoint

Report in output:
  **Context**: 32% (spawning within budget)
  or
  **Context**: 45% → Spawning fresh agent to continue
```

## Integration

This command:
1. Reads state via **state-management** skill
2. Routes via **capability-discovery** skill
3. Delegates to **coordinator** agent for orchestration
4. Spawns appropriate agents via Task tool
