---
name: project-persistence
description: Manages persistent project state across sessions for the business analyst plugin. Enables incremental requirements gathering over days or weeks.
allowed-tools: Read, Write, Edit, Glob
---

# Project Persistence Skill

## Overview

This skill enables the business analyst plugin to maintain state across multiple sessions. All project data is stored in a `.business-analyst/` directory within the user's project, allowing requirements to be gathered incrementally over days or weeks.

## Project Directory Structure

```
.business-analyst/
├── project.json              # Project metadata and current state
├── stakeholders.md           # Stakeholder register and RACI
├── requirements/
│   ├── functional.md         # Functional requirements (FR-XXX)
│   ├── non-functional.md     # Non-functional requirements (NFR-XXX)
│   ├── constraints.md        # Constraints (CON-XXX)
│   ├── assumptions.md        # Assumptions (ASM-XXX)
│   └── use-cases.md          # Use case catalog (UC-XXX)
├── risk-register.md          # Project risk register (RISK-XXX)
├── data-dictionary.md        # Data element definitions (DE-XXX)
├── traceability.md           # Traceability matrix
├── interview-log.md          # Log of all interview sessions
├── validation-history.md     # Validation scores over time
├── srs/
│   └── (generated SRS files) # Output SRS documents
└── changelog.md              # Log of all changes with timestamps
```

## project.json Schema

```json
{
  "name": "Project Name",
  "type": "greenfield | brownfield",
  "objective": "Why this analysis is being done",
  "domain": "healthcare | fintech | e-commerce | saas | government | education | logistics | iot | other",
  "created": "2026-04-06T10:00:00Z",
  "lastModified": "2026-04-06T15:30:00Z",
  "phase": "gathering | validating | drafting | approved",
  "counters": {
    "FR": 12,
    "NFR": 8,
    "CON": 3,
    "ASM": 5,
    "UC": 4,
    "RISK": 6,
    "DE": 15
  },
  "validation": {
    "lastRun": "2026-04-06T14:00:00Z",
    "completeness": 72,
    "quality": 68,
    "status": "FAIL",
    "openIssues": 8
  },
  "sessions": [
    {
      "date": "2026-04-06",
      "action": "Initial requirements review from requirements.md",
      "addedFR": 8,
      "addedNFR": 3,
      "questionsAsked": 12,
      "questionsAnswered": 10
    }
  ]
}
```

## State Operations

### Initialize Project

When starting a new project (first use of any command):

1. Check if `.business-analyst/` already exists
   - If yes: load existing state (offer `/business-analyst:resume`)
   - If no: create the directory structure
2. Create `project.json` with initial metadata
3. Create empty requirement files with header templates
4. Create `changelog.md` with initialization entry

### Save State

After any command that gathers or modifies requirements:

1. Write updated requirements to the appropriate `.md` files
2. Update counters in `project.json`
3. Update `lastModified` timestamp
4. Append session entry to `project.json.sessions`
5. Append change description to `changelog.md`

### Load State

When resuming or adding to a project:

1. Read `project.json` for project context
2. Read all requirement files
3. Read validation history
4. Present current state summary to user
5. Continue from where the project left off

### Merge New Requirements

When adding requirements to an existing project:

1. Read current requirements to determine next available IDs
2. Check for duplicates (similar descriptions)
3. Assign new IDs continuing from the current counters
4. Append to the appropriate requirement files
5. Flag new items for validation
6. Update counters and changelog

## File Templates

### requirements/functional.md
```markdown
# Functional Requirements

> Last updated: {timestamp}
> Total: {count} requirements

## {Feature Area 1}

### FR-001: {Title}

| Attribute | Value |
|-----------|-------|
| **ID** | FR-001 |
| **Priority** | Must / Should / Could |
| **Source** | {Stakeholder / Document / Session date} |
| **Status** | Proposed / Confirmed / Approved |
| **Added** | {date} |
| **Session** | {which session added this} |

**Description**: The system shall {requirement}

**Acceptance Criteria**:
- [ ] {Criterion}

---
```

### changelog.md
```markdown
# Project Changelog

## {Date} - {Session Summary}

### Added
- FR-013: {title}
- FR-014: {title}
- NFR-SEC-003: {title}

### Modified
- FR-005: Updated acceptance criteria based on stakeholder feedback

### Questions Resolved
- Confirmed authentication method is OAuth2 (was TBD)
- Confirmed 99.9% uptime target (was TBD)

### Still TBD
- FR-008: Exact report format pending design review
- ASM-003: Browser support needs confirmation

---
```

### interview-log.md
```markdown
# Interview Log

## Session: {Date} - {Topic}

**Duration**: {time}
**Stakeholder**: {role}
**Focus Area**: {topic}

### Questions Asked
1. Q: {question}
   A: {answer}
   → Generated: FR-013

2. Q: {question}
   A: {answer}
   → Updated: FR-005 (added acceptance criteria)

3. Q: {question}
   A: Deferred / TBD
   → Action: Follow up on {topic}

### Session Outcomes
- {N} new requirements added
- {N} existing requirements updated
- {N} questions deferred

---
```

## ID Management

### Counter-Based IDs
- IDs are assigned sequentially from counters in `project.json`
- When adding new requirements, read current counter, increment, save
- Never reuse deleted IDs (keeps audit trail clean)

### ID Format
```
FR-001 through FR-999      (functional)
NFR-PERF-001               (performance)
NFR-SEC-001                (security)
NFR-REL-001                (reliability)
NFR-USA-001                (usability)
NFR-MAINT-001              (maintainability)
CON-001                    (constraints)
ASM-001                    (assumptions)
UC-001                     (use cases)
RISK-001                   (risks)
DE-001                     (data elements)
```

## Duplicate Detection

When adding requirements, check for potential duplicates:

1. Compare new requirement description against existing ones
2. Look for similar key terms and phrases
3. If a likely duplicate is found, present to user:
   > "This looks similar to an existing requirement:
   > - **FR-005**: {existing description}
   > - **New**: {new description}
   >
   > Should I: (a) merge them, (b) keep both as separate, or (c) update the existing one?"

## TBD Tracking

Track all TBD items across the project:

1. When a question is deferred: add to TBD list in `project.json`
2. When resuming: present outstanding TBD items
3. When a TBD is resolved: remove from list, update changelog
4. Validation reports flag remaining TBDs
