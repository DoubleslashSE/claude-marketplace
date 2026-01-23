# Context Engineering Patterns

## Pattern: Fresh Task Context

**When**: Starting each task in EXECUTE phase

**Structure**:
```markdown
## Task Context for TASK-XXX

**Task Definition**:
[XML task from ITEM-XXX.md Tasks section]

**Relevant Files**:
- [file1]: [why needed]
- [file2]: [why needed]

**Key Decisions**:
- DECISION-XXX: [relevant decision]

**Conventions**:
- [coding convention to follow]

**Success Criteria**:
- [from task <done> criteria]
```

**What to Exclude**:
- Other tasks not being executed
- Full exploration history
- Resolved conflicts
- Completed task details

---

## Pattern: Phase Transition Summary

**When**: Moving from one phase to another

**Structure**:
```markdown
## Phase Transition: [FROM] → [TO]

**Completed in [FROM]**:
- [Key accomplishment 1]
- [Key accomplishment 2]

**Artifacts created**:
- [file]: [brief description]

**Carrying forward**:
- [Key decision or context needed in next phase]

**Starting [TO] with**:
- [Initial focus]
```

**What to Exclude**:
- Detailed exploration paths not taken
- Verbose transcripts
- Intermediate states

---

## Pattern: Exploration Summary

**When**: Completing exploration of an area in DISCUSS

**Structure**:
```markdown
## [Area Name] - Exploration Summary

**Status**: EXPLORED

**Key Findings**:
1. [Finding 1]
2. [Finding 2]

**Decisions Made**:
- DECISION-XXX: [Summary]

**Open Questions** (if any):
- [Question]

**Related Areas**: [links to related explored areas]
```

**What to Exclude**:
- Full question/answer transcript
- Rejected options (unless critical)
- Tangential discussions

---

## Pattern: Research Findings

**When**: Researcher agent returns from codebase exploration

**Structure**:
```markdown
## Research: [Topic]

**Question**: [What was investigated]

**Findings**:
- [Key finding with file reference]
- [Key finding with file reference]

**Patterns Identified**:
- [Pattern name]: [Where used, example]

**Recommendations**:
1. [Recommendation]

**Files of Interest**:
- [path]: [relevance]
```

**What to Exclude**:
- Full file contents
- Dead ends explored
- Verbose grep/glob results

---

## Pattern: Task Completion Report

**When**: Executor completes a task

**Structure**:
```markdown
## TASK-XXX: Complete

**Summary**: [One sentence of what was done]

**Files Modified**:
- [path]: [what changed]

**Verification**:
- [step]: PASS/FAIL

**Commit**: [hash] - [message]

**Notes** (if any): [Anything noteworthy for future tasks]
```

**What to Exclude**:
- Full code that was written
- Detailed step-by-step log
- Intermediate states

---

## Pattern: Verification Report

**When**: Verifier completes verification

**Structure**:
```markdown
## Verification Report

**Automated Checks**: PASS/FAIL
- Build: [status]
- Tests: [X/Y passed]
- Lint: [status]

**Requirements Coverage**: X/Y
| Requirement | Verified |
|-------------|----------|
| FR-001 | YES |

**UAT Results**: PASS/FAIL
- [Scenario]: [result]

**Issues**: [count]
[List if any]

**Recommendation**: APPROVE / NEEDS_WORK
```

**What to Exclude**:
- Full test output
- Verbose build logs
- Passing scenarios details (only note failures)

---

## Pattern: Checkpoint Context

**When**: Creating a checkpoint for resume capability

**Structure**:
```markdown
### CHECKPOINT: [PHASE]-[TIMESTAMP]

**Phase**: [current phase]
**Progress**: [X%]

**State**:
- Decisions: [count]
- Tasks: [completed/total]
- Blockers: [count]

**Current Focus**: [what's being worked on]

**Next Action**: [specific next step]

**Key Context**:
- [Essential item to remember]
- [Essential item to remember]
```

**What to Exclude**:
- Full history of how we got here
- All decisions (they're in ITEM-XXX.md)
- Completed work details

---

## Pattern: Conflict Presentation

**When**: Presenting a conflict to user

**Structure**:
```markdown
## Conflict Detected

**Between**:
- A: [Item A - concise]
- B: [Item B - concise]

**Why they conflict**: [One sentence explanation]

**Options**:
1. [Option with implication]
2. [Option with implication]
3. [Option with implication]

**Waiting for**: User resolution
```

**What to Exclude**:
- Full context of how each item arose
- All possible options (pick top 3-4)
- Technical details unless necessary

---

## Pattern: Agent Spawn Request

**When**: Orchestrator spawns a specialized agent

**Structure**:
```markdown
## Spawn Request: [agent-name]

**Purpose**: [One sentence]

**Context to provide**:
- [Specific item]
- [Specific item]

**Expected output**: [What to return]

**Files agent should read**:
- [path]
- [path]

**Constraints**:
- [Any limits or guidelines]
```

**What to Exclude**:
- Full workflow history
- Unrelated state
- Other phases' details

---

## Anti-Patterns to Avoid

### The Memory Hoarder
```markdown
BAD: Keeping full transcripts of all conversations
GOOD: Summarize and reference ITEM-XXX.md for history
```

### The File Dumper
```markdown
BAD: Loading entire files into context repeatedly
GOOD: Load once, reference by path, load sections as needed
```

### The Everything Reporter
```markdown
BAD: Agent returns full code + all steps + full logs
GOOD: Agent returns summary + key findings + next actions
```

### The Context Repeater
```markdown
BAD: Including same context in every message
GOOD: "Continuing TASK-005" (context established)
```

### The Inline Expander
```markdown
BAD: "The task definition is: [full XML]..."
GOOD: "Task TASK-005 (see ITEM-XXX.md Tasks section)"
```
