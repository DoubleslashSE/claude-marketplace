# Agent Handoff Protocols

## Overview

This document defines the protocols for passing work between agents in the flow-workflow system. Clean handoffs ensure context is preserved while keeping each agent focused.

## Handoff Types

### 1. Phase Handoff

Transfer control between phases (DISCUSS → PLAN, PLAN → EXECUTE, etc.)

**Protocol**:
```markdown
## Phase Handoff: [FROM] → [TO]

**Completed in [FROM]**:
- [Summary of accomplishments]

**Artifacts for [TO]**:
- [file]: [what it contains]

**Key context**:
- [Decision or finding relevant to next phase]

**Recommended first action**:
- [What the next phase should start with]
```

**Example - DISCUSS → PLAN**:
```markdown
## Phase Handoff: DISCUSS → PLAN

**Completed in DISCUSS**:
- 5 areas explored
- 12 decisions made
- 8 functional requirements identified

**Artifacts for PLAN**:
- ITEM-XXX.md: 8 FR, 3 NFR documented, full exploration map, decisions recorded

**Key context**:
- Auth must use OAuth (DECISION-004)
- Performance target: <200ms response (NFR-001)
- Database: PostgreSQL (DECISION-007)

**Recommended first action**:
- Create tasks for FR-001 (user registration) first
```

---

### 2. Task Handoff

Transfer a specific task to an executor agent

**Protocol**:
```markdown
## Task Handoff: TASK-XXX

**Task definition**:
[XML task from ITEM-XXX.md Tasks section]

**Context**:
- Preceding tasks: [completed tasks that affect this one]
- Key decisions: [relevant decisions]
- Patterns to follow: [established patterns]

**Files to read**:
- [path]: [why]

**Success criteria**:
- [from task <done>]

**Report back**:
- Task status (completed/blocked)
- Files modified
- Commit created (or error encountered)
```

**Example**:
```markdown
## Task Handoff: TASK-005

**Task definition**:
<task id="TASK-005" status="pending">
  <name>Add email validation to registration</name>
  <description>Implement email format validation</description>
  <files>
    <file action="modify">src/services/UserService.ts</file>
    <file action="modify">src/validators/index.ts</file>
  </files>
  <actions>
    <action>Add validateEmail function to validators</action>
    <action>Call validator in UserService.register</action>
    <action>Return appropriate error on invalid email</action>
  </actions>
  <verify>
    <step>npm test -- email</step>
  </verify>
  <done>
    <criterion>Invalid emails rejected with clear error</criterion>
  </done>
  <commit>feat(user): add email validation to registration</commit>
</task>

**Context**:
- Preceding tasks: TASK-001 (UserService created)
- Key decisions: Use Zod for validation (DECISION-009)
- Patterns to follow: See existing validators in src/validators/

**Files to read**:
- src/services/UserService.ts: Where to add validation call
- src/validators/index.ts: Existing validation patterns

**Success criteria**:
- Invalid emails rejected with clear error

**Report back**:
- Task status
- Files modified
- Commit hash and message
```

---

### 3. Research Handoff

Request codebase investigation from researcher agent

**Protocol**:
```markdown
## Research Request

**Question**: [Specific question to answer]

**Scope**:
- Directories: [where to look]
- File types: [what kinds of files]
- Depth: [how deep to go]

**Looking for**:
- [Specific pattern or information]
- [Specific pattern or information]

**Report format**:
- Findings summary
- Relevant file paths
- Recommendations
```

**Example**:
```markdown
## Research Request

**Question**: How are API endpoints authenticated in this codebase?

**Scope**:
- Directories: src/api/, src/middleware/
- File types: *.ts
- Depth: All files in scope

**Looking for**:
- Authentication middleware
- JWT or session handling
- Authorization patterns

**Report format**:
- Findings summary
- Relevant file paths with line numbers
- Recommendation for adding new authenticated endpoint
```

---

### 4. Verification Handoff

Request verification from verifier agent

**Protocol**:
```markdown
## Verification Request

**What to verify**:
- [Scope of verification]

**Checks to run**:
- [Automated check]
- [Automated check]

**Requirements to validate**:
- [FR-XXX]
- [FR-XXX]

**UAT scenarios**:
- [Scenario to test with user]

**Report format**:
- Pass/fail per check
- Requirements traceability
- UAT results
- Issues found (if any)
- Recommendation
```

---

### 5. Interview Handoff

Request requirements gathering from interviewer

**Protocol**:
```markdown
## Interview Request

**Topic**: [What to explore]

**Initial areas**:
- [Area 1]
- [Area 2]

**Context from prior work**:
- [Relevant existing decisions]

**Depth**: [Light/Medium/Deep]

**Report format**:
- Exploration map
- Decisions made
- Requirements captured
- Conflicts identified
```

---

## Handoff Best Practices

### Include
- Specific task/question
- Relevant context only
- Success criteria
- Expected output format

### Exclude
- Full workflow history
- Unrelated decisions
- Completed task details
- Large file contents (reference instead)

### Format Consistency

Always structure handoffs with:
1. **What**: Task or question
2. **Context**: Essential background
3. **Scope**: Boundaries and constraints
4. **Deliverable**: Expected output

---

## Receiving Results

### From Executor
```markdown
## Executor Result: TASK-XXX

**Status**: completed
**Files modified**:
- src/services/UserService.ts (added validation)
- src/validators/index.ts (new validateEmail)

**Commit**: a1b2c3d - feat(user): add email validation

**Verification**: All steps passed

**Notes**: Used existing validator pattern
```

### From Researcher
```markdown
## Research Result

**Question**: [original question]
**Confidence**: [High/Medium/Low]

**Findings**:
1. [Finding] - [file:line]
2. [Finding] - [file:line]

**Recommendations**:
- [Recommendation based on findings]

**Uncertainties**:
- [What couldn't be determined]
```

### From Verifier
```markdown
## Verification Result

**Overall**: PASS/FAIL

**Automated**:
- Build: PASS
- Tests: PASS (50/50)
- Lint: PASS

**Requirements**: 8/8 verified

**UAT**: PASS
- [Scenario 1]: PASS
- [Scenario 2]: PASS

**Recommendation**: Ready for completion
```

### From Interviewer
```markdown
## Interview Result

**Topic**: [topic explored]
**Coverage**: [X]%

**Exploration map**: [summary or reference to ITEM-XXX.md exploration section]

**Decisions captured**:
- DECISION-XXX: [summary]
- DECISION-YYY: [summary]

**Requirements identified**: [count]

**Conflicts found**: [count or "None"]

**Recommendation**: [Ready for PLAN / Continue exploring]
```

---

## Error Handling in Handoffs

### Agent Failure
```markdown
## Agent Error: [agent]

**Task**: [what was requested]
**Error**: [what happened]
**State**: [what's preserved]

**Options**:
1. Retry with same agent
2. Try alternative agent
3. Manual intervention
4. Skip and continue
```

### Incomplete Result
```markdown
## Incomplete Result: [agent]

**Completed**: [what was done]
**Incomplete**: [what wasn't]
**Reason**: [why]

**Options**:
1. Continue with another agent
2. Accept partial result
3. Request completion
```
