---
name: workflow-orchestration
description: Phase coordination, agent handoffs, and workflow state machine management
triggers:
  - workflow
  - phase transition
  - orchestration
  - coordination
---

# Workflow Orchestration Skill

This skill provides patterns for coordinating workflow phases, managing agent handoffs, and maintaining the workflow state machine.

## Workflow State Machine

### Phase States

```
        ┌─────────────────────────────────────────────────┐
        │                                                 │
        v                                                 │
┌──────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐ │ ┌──────────┐
│   INIT   │ -> │ DISCUSS │ -> │   PLAN   │ -> │EXECUTE │-┘>│  VERIFY  │
└──────────┘    └─────────┘    └──────────┘    └────────┘   └──────────┘
                    ^               ^              │              │
                    │               │              │              │
                    └───────────────┴──────────────┘              │
                          (on issues found)                       │
                                                                  v
                                                            ┌──────────┐
                                                            │ COMPLETE │
                                                            └──────────┘
```

### Valid Transitions

| From | To | Condition |
|------|-----|-----------|
| INIT | DISCUSS | Initialization complete |
| DISCUSS | PLAN | Requirements captured |
| PLAN | EXECUTE | Plan approved |
| EXECUTE | VERIFY | All tasks complete |
| EXECUTE | DISCUSS | Major scope change needed |
| EXECUTE | PLAN | Task restructure needed |
| VERIFY | COMPLETE | Sign-off received |
| VERIFY | EXECUTE | Issues need fixing |

### Invalid Transitions

- INIT → PLAN (must discuss first)
- INIT → EXECUTE (must plan first)
- VERIFY → DISCUSS (must execute changes)
- COMPLETE → any (workflow finished)

## Phase Coordination

### Phase Entry Protocol

Before entering any phase:

```markdown
1. VERIFY previous phase complete
   - Check completion criteria
   - Verify artifacts exist
   - No active blockers

2. CREATE checkpoint in ITEM-XXX.md
   - Snapshot current state
   - Record transition reason
   - Note timestamp

3. UPDATE phase status
   - Set new phase
   - Reset progress to 0%
   - Record start time

4. PREPARE phase context
   - Load relevant state files
   - Identify agents needed
   - Clear stale context
```

### Phase Exit Protocol

Before exiting any phase:

```markdown
1. VERIFY completion criteria
   - Phase-specific requirements met
   - Artifacts created
   - No pending decisions

2. CREATE phase summary
   - What was accomplished
   - Decisions made
   - Artifacts produced

3. HANDOFF to next phase
   - What next phase needs to know
   - Key context to carry forward
   - Warnings or considerations
```

## Agent Handoff Protocols

### Spawning an Agent

```markdown
## Agent Spawn: [agent-name]

**Purpose**: [Clear objective]

**Context provided**:
- Phase: [current phase]
- Task: [specific task if applicable]
- Key decisions: [relevant decisions]
- Files: [files to read]

**Expected deliverable**:
- [What agent should produce]
- [Format expected]

**Constraints**:
- [Time/scope limits]
- [Must follow conventions]
- [Report blockers immediately]
```

### Receiving Agent Results

```markdown
## Agent Result: [agent-name]

**Status**: [SUCCESS/PARTIAL/FAILED]

**Deliverables**:
- [What was produced]
- [Where it's stored]

**Key findings**:
- [Important discovery]
- [Important discovery]

**Issues encountered**:
- [Issue if any]

**Next recommended action**:
- [What to do next]
```

### Multi-Agent Coordination

When multiple agents needed:

```markdown
## Coordination Plan

**Agents involved**:
1. [Agent A]: [Purpose]
2. [Agent B]: [Purpose]

**Sequence**:
A -> B (B depends on A's output)

**Handoff points**:
- A completes: [deliverable] -> B starts
- B completes: [deliverable] -> next phase

**Fallback**:
- If A fails: [contingency]
- If B fails: [contingency]
```

## Blocker Management

### Blocker Detection

Watch for:
- Explicit blockers from agents
- Missing prerequisites
- User unavailability
- Technical failures
- Conflicts requiring resolution

### Blocker Response

```markdown
## Blocker Detected

**Type**: [Technical/Decision/External/Conflict]
**Phase**: [current phase]
**Impact**: [what's blocked]

**Options**:
1. Resolve blocker directly
2. Work around blocker
3. Pause workflow
4. Escalate to user

**Recommended**: [option]
```

### Blocker Resolution Tracking

In ITEM-XXX.md:

```markdown
### BLOCKER-XXX: [Title]
**Status**: ACTIVE -> RESOLVED
**Detected**: [timestamp]
**Resolved**: [timestamp]
**Resolution**: [what was done]
**Impact on workflow**: [any changes made]
```

## Progress Tracking

### Phase Progress Calculation

| Phase | Progress Based On |
|-------|-------------------|
| INIT | Steps completed / total steps |
| DISCUSS | Areas explored / total areas |
| PLAN | Tasks defined / estimated total |
| EXECUTE | Tasks completed / total tasks |
| VERIFY | Checks passed / total checks |

### Progress Reporting

```markdown
## Workflow Progress

**Overall**: [X]%
**Phase**: [current phase] at [Y]%

**Phase breakdown**:
- [x] INIT: 100%
- [x] DISCUSS: 100%
- [ ] PLAN: 75%
- [ ] EXECUTE: 0%
- [ ] VERIFY: 0%

**Blockers**: [count]
**Next milestone**: [description]
```

## Rollback and Recovery

### Phase Rollback

When needing to return to earlier phase:

```markdown
## Phase Rollback

**From**: [current phase]
**To**: [target phase]
**Reason**: [why rolling back]

**Actions**:
1. Save current state as checkpoint
2. Preserve completed work
3. Update phase status
4. Clear invalid artifacts (if any)
5. Resume from target phase
```

### Recovery from Failure

```markdown
## Workflow Recovery

**Failure point**: [where it failed]
**Error**: [what happened]

**Recovery options**:
1. Retry from checkpoint
2. Skip failed item
3. Manual intervention
4. Abort with state preserved

**State preserved at**: .flow/FLOW.md and .flow/items/ITEM-XXX.md
**Resume command**: /flow-workflow:go
```

## Quick Mode Orchestration

For `/flow-workflow:quick`:

```markdown
## Quick Mode Flow

**Simplified phases**:
ASSESS -> CLARIFY -> IMPLEMENT -> VERIFY

**Shortcuts taken**:
- No FLOW.md or ITEM-XXX.md files created
- No detailed requirements gathering
- Direct execution
- Brief verification

**Escalation trigger**:
If complexity exceeds quick mode, escalate to full workflow with /flow-workflow:start
```

## Integration Points

### With State Management
- Update FLOW.md and ITEM-XXX.md on every transition
- Create checkpoints in ITEM-XXX.md at key points
- Maintain phase history in ITEM-XXX.md

### With Capability Discovery
- Route to appropriate agents based on FLOW.md cache
- Announce delegation decisions with reasoning
- Fallback to defaults when no match
- Log capability gaps in FLOW.md

### With Conflict Detection
- Block transitions on active conflicts
- Require resolution before proceeding
- Document resolved conflicts in ITEM-XXX.md

### With Context Engineering
- Fresh context per task
- Coordinator stays under 40%
- Spawn fresh agents when approaching threshold
