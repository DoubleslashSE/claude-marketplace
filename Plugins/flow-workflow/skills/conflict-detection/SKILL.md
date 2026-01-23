---
name: conflict-detection
description: Conflict identification and resolution patterns for requirements, decisions, and plans
triggers:
  - conflict
  - contradiction
  - inconsistency
  - incompatible
---

# Conflict Detection Skill

This skill provides patterns for detecting and resolving conflicts between requirements, decisions, and plans throughout the workflow.

## Core Principles

1. **Early Detection**: Catch conflicts as soon as they arise
2. **Immediate Stop**: Halt workflow when conflict detected
3. **User Resolution**: Never auto-resolve conflicts
4. **Documented Rationale**: Record why resolutions were chosen

## Conflict Types

### Requirement vs Requirement
Two requirements that cannot both be satisfied.

**Detection Point**: DISCUSS phase
**Example**: "User wants real-time updates AND offline mode"

**Indicators**:
- Mutually exclusive features
- Resource contention
- Contradictory behaviors

---

### Decision vs Decision
A new decision contradicts an earlier decision.

**Detection Point**: DISCUSS phase
**Example**: "Earlier said 'no database', now requesting PostgreSQL"

**Indicators**:
- Opposite stance on same topic
- Changed constraints
- Reversed priorities

---

### New vs Existing Plan
Proposed work conflicts with pending tasks.

**Detection Point**: PLAN phase
**Example**: "This change conflicts with TASK-003 in current ITEM-XXX.md"

**Indicators**:
- Same files modified differently
- Contradicting goals
- Circular dependencies

---

### Scope vs Timeline
Requested features exceed achievable scope.

**Detection Point**: DISCUSS phase
**Example**: "Features exceed what's achievable in stated timeline"

**Indicators**:
- Too many must-haves
- Complex features with tight deadline
- Dependencies on unavailable resources

---

### Tech vs Requirement
Chosen technology cannot support a requirement.

**Detection Point**: PLAN phase
**Example**: "Chosen tech doesn't support requested feature"

**Indicators**:
- Technical limitations
- Incompatible versions
- Missing capabilities

---

## Detection Protocol

### On Each New Input

```
┌─────────────────────────────────────────────────────────────────┐
│              CONFLICT DETECTION FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. EXTRACT assertions from new input                           │
│     ├─ Requirements stated                                      │
│     ├─ Decisions made                                           │
│     ├─ Constraints imposed                                      │
│     └─ Priorities expressed                                     │
│                                                                 │
│  2. SCAN for contradictions                                     │
│     ├─ Compare against ITEM-XXX.md decisions                    │
│     ├─ Compare against ITEM-XXX.md requirements                 │
│     ├─ Compare against existing tasks in ITEM-XXX.md            │
│     └─ Check implicit assumptions                               │
│                                                                 │
│  3. IF CONFLICT DETECTED:                                       │
│     ├─ STOP workflow immediately                                │
│     ├─ Document conflict in ITEM-XXX.md                         │
│     ├─ Present conflict clearly to user                         │
│     └─ Wait for resolution before continuing                    │
│                                                                 │
│  4. IF NO CONFLICT:                                             │
│     └─ Continue workflow normally                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Comparison Matrix

For each new assertion, check against:

| Compare Against | Looking For |
|-----------------|-------------|
| Previous decisions | Contradictions |
| Stated requirements | Incompatibilities |
| Technical choices | Capability gaps |
| Implicit assumptions | Hidden conflicts |
| Pending tasks | Execution conflicts |

## Conflict Documentation

### In ITEM-XXX.md

```markdown
## Conflicts

### CONFLICT-001: [Descriptive Title]
**Status**: ACTIVE | RESOLVED | DEFERRED
**Detected**: [TIMESTAMP]
**Type**: Requirement | Decision | Plan | Technical | Scope

**What conflicts:**
- A: [First item with reference]
- B: [Second item with reference]

**Why they conflict:**
[Clear explanation of why both cannot coexist]

**Resolution options:**
1. [Option 1 - description and implications]
2. [Option 2 - description and implications]
3. [Option 3 - description and implications]

**User choice**: [PENDING | Option N]
**Rationale**: [Why user chose this option]
**Resolved**: [TIMESTAMP]
**Actions taken**: [What changed as a result]
```

## Automatic Triggers

The system MUST stop and present conflict when detecting:

### Contradictory Statements
```
Trigger: "You said X earlier, now saying not-X"
Example: "Earlier you said no database needed, but now you're
         asking for PostgreSQL integration"
```

### Mutually Exclusive Features
```
Trigger: "Feature A requires condition C, Feature B requires not-C"
Example: "Real-time sync requires constant internet, but you also
         want full offline functionality"
```

### Resource Conflicts
```
Trigger: "Both items need exclusive access to same resource"
Example: "Two tasks both want to restructure the database schema
         in incompatible ways"
```

### Timeline Impossibilities
```
Trigger: "Features exceed reasonable scope for constraints"
Example: "You're asking for 15 major features with a 2-week deadline"
```

### Technical Incompatibilities
```
Trigger: "Technologies don't work together"
Example: "You want to use Library A and Library B, but they have
         conflicting peer dependencies"
```

## Resolution Options

### Option 1: Prioritize One
Choose one item over the other.

```markdown
Resolution: Prioritize A over B
- A remains as requirement
- B is removed or deferred
- Rationale recorded
```

### Option 2: Modify One
Adjust one item to remove conflict.

```markdown
Resolution: Modify B to accommodate A
- A remains unchanged
- B is adjusted: [specific changes]
- Both now compatible
```

### Option 3: Modify Both
Adjust both items to find middle ground.

```markdown
Resolution: Adjust both for compromise
- A adjusted: [changes]
- B adjusted: [changes]
- Trade-off documented
```

### Option 4: Accept with Trade-off
Keep both, document the trade-off.

```markdown
Resolution: Accept both with trade-off
- Both remain
- Trade-off: [what is sacrificed]
- Risk documented
```

### Option 5: Defer
Postpone resolution.

```markdown
Resolution: Deferred
- Marked as DEFERRED
- Reason: [why can't resolve now]
- Blocker for: [what can't proceed]
- Revisit: [when/condition]
```

## Cross-Plan Verification

Before creating tasks, verify:

```markdown
## Cross-Plan Verification Checklist

**Against ITEM-XXX.md requirements:**
- [ ] All requirements have at least one task
- [ ] No tasks contradict requirements
- [ ] Priority order respected
- [ ] No requirements orphaned

**Against ITEM-XXX.md decisions:**
- [ ] Tasks align with recorded decisions
- [ ] No tasks contradict decisions
- [ ] Deferred items not accidentally included

**Against existing tasks in ITEM-XXX.md:**
- [ ] New tasks don't conflict with pending tasks
- [ ] File modifications don't overlap dangerously
- [ ] Dependency order preserved
- [ ] No circular dependencies created

**Against FLOW.md backlog:**
- [ ] Tasks fit within item scope
- [ ] No scope creep detected
- [ ] Dependencies on other items documented

**Conflicts found**: [List or "None"]
```

## Integration Points

- **State Management**: Document conflicts in ITEM-XXX.md
- **Exploration Tracking**: Flag areas with detected conflicts
- **Interviewer Agent**: Stop and present conflicts during discussion
- **Planner Agent**: Verify cross-plan consistency
- **Workflow Orchestration**: Block phase transitions on active conflicts

See `resolution.md` for detailed resolution strategies.
