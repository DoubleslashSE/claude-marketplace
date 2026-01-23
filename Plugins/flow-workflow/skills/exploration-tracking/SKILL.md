---
name: exploration-tracking
description: Exploration map management for tracking discussed areas and uncharted territory during DISCUSS phase
triggers:
  - exploration map
  - territory tracking
  - discussion progress
  - uncharted areas
---

# Exploration Tracking Skill

This skill provides techniques for maintaining awareness of explored vs. uncharted territory during the DISCUSS phase, ensuring comprehensive coverage and documented gaps.

## Core Principles

1. **No Silent Omissions**: Always document what was NOT discussed, not just what was
2. **Visual Progress**: Use tree visualization for quick comprehension
3. **Explicit Skipping**: When skipping an area, record the reason
4. **Backtracking Support**: Enable return to partially explored areas

## Territory Status Indicators

| Symbol | Status | Meaning |
|--------|--------|---------|
| ✓ | EXPLORED | Fully discussed, decisions made |
| ◐ | PARTIAL | Started but incomplete, some findings |
| → | CURRENT | Currently exploring this area |
| ○ | UNCHARTED | Identified but not yet explored |
| ⊘ | SKIPPED | User chose to skip (reason recorded) |
| ⚑ | FLAGGED | Needs follow-up or has blockers |

## Exploration Map Structure

### Tree Format

```
[MAIN TOPIC]
├── ✓ EXPLORED: [Area 1]
│   ├── ✓ [Sub-area 1.1] - [Summary of findings]
│   └── ◐ PARTIAL: [Sub-area 1.2] - [What we know, what's unclear]
├── → CURRENT: [Area 2]
│   ├── ✓ [Sub-area 2.1] - [Completed]
│   └── ○ UNCHARTED: [Sub-area 2.2]
├── ○ UNCHARTED: [Area 3]
│   └── [Suspected sub-topics]
└── ⊘ SKIPPED: [Area 4] - [Reason]
```

### Exploration Depth Levels

| Level | Purpose | Example |
|-------|---------|---------|
| L1 | Main topic areas | "Authentication", "Data Storage" |
| L2 | Sub-areas within topic | "Login flow", "Session management" |
| L3 | Specific details | "Password requirements", "Token expiry" |
| L4+ | Deep specifics | "Bcrypt vs Argon2", "JWT claims" |

## Map Operations

### Initialize Map

```markdown
1. Add Exploration Map section to ITEM-XXX.md
2. Set topic from user's initial request
3. Identify initial L1 areas from topic
4. Mark all as UNCHARTED
5. Set status to IN_PROGRESS
```

### Update Current Position

```markdown
1. Mark previous CURRENT as appropriate status
   - EXPLORED if complete
   - PARTIAL if interrupted
   - SKIPPED if user chose to skip
2. Mark new area as CURRENT
3. Record timestamp
4. Add any newly discovered sub-areas
```

### Add Discovered Areas

When conversation reveals new areas:

```markdown
1. Identify where in tree the area belongs
2. Add as child of appropriate parent
3. Mark as UNCHARTED
4. Note discovery context
```

### Mark Area Complete

```markdown
1. Change status to EXPLORED
2. Add summary of findings
3. Link to relevant decisions (DECISION-XXX)
4. Record timestamp
5. Update CURRENT to next area
```

### Skip Area

```markdown
1. Change status to SKIPPED
2. Record reason for skipping
3. Note if should revisit later
4. Move to next area
```

### Flag for Follow-up

```markdown
1. Change status to FLAGGED
2. Record what's blocking
3. Note required action
4. Continue to next area
```

## Checkpoint Protocol

At regular intervals and phase transitions:

### Display Checkpoint

```markdown
**Exploration Checkpoint**

Current position: [CURRENT AREA]
Just explored: [What we covered]
Key findings: [Summary]

**Map so far:**
[Visual tree with status indicators]

**Options:**
1. Dig deeper into [current area]
2. Move to [next uncharted area]
3. Return to [partial area]
4. Skip [current] and note reason
5. Mark discussion complete
```

### User Choice Handling

| Choice | Action |
|--------|--------|
| Dig deeper | Add sub-areas to current, continue exploring |
| Move on | Mark current as EXPLORED, go to next UNCHARTED |
| Return to partial | Mark current as PARTIAL, resume flagged area |
| Skip | Mark as SKIPPED with reason, go to next |
| Complete | Finalize map, transition to PLAN phase |

## Backtracking Protocol

### When to Backtrack

1. Deep dive complete, surface to parent area
2. User wants to revisit earlier topic
3. Blocked area now unblocked
4. Discovered new info affects earlier area

### Backtrack Process

```markdown
1. Mark current position appropriately
2. Navigate to target area in map
3. Update target status to CURRENT
4. Resume exploration with prior context
5. Note backtrack in exploration log
```

## Coverage Analysis

### Before Completing DISCUSS Phase

```markdown
Coverage Analysis:
- Total areas identified: [N]
- Fully explored: [X] (✓)
- Partially explored: [Y] (◐)
- Uncharted: [Z] (○)
- Skipped: [W] (⊘)
- Flagged: [V] (⚑)

Coverage: [X/(N-W)]%

Uncharted areas:
1. [Area] - [Why not explored]
2. [Area] - [Why not explored]

Skipped areas:
1. [Area] - [Reason skipped]

Flagged areas:
1. [Area] - [What's blocking]
```

### Coverage Thresholds

| Coverage | Recommendation |
|----------|----------------|
| 90%+ | Safe to proceed to PLAN |
| 70-89% | Review uncharted areas with user |
| <70% | Continue DISCUSS phase |

## Integration Points

- **State Management**: Store exploration map in ITEM-XXX.md
- **Conflict Detection**: Flag conflicting areas
- **Interviewer Agent**: Uses map to guide questioning
- **Workflow Orchestration**: Phase transition based on coverage

## Best Practices

### Naming Areas
- Use noun phrases: "User authentication", not "Authenticate users"
- Be specific: "Password requirements", not "Security stuff"
- Match user's vocabulary when possible

### Recording Findings
- Keep summaries to one line
- Reference decisions by ID
- Note uncertainties explicitly

### Managing Depth
- Don't go deeper than needed
- Ask user about depth preferences
- Default to L2 for initial exploration

See `questioning.md` for adaptive questioning patterns that drive exploration.
