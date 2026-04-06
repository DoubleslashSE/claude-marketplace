---
description: Resume a business analysis project from saved state. Loads all previously gathered requirements, shows progress, outstanding TBDs, and lets you continue where you left off.
---

# Resume Business Analysis Project

Resume project from: **$ARGUMENTS**

## Overview

This command loads your saved project state from the `.business-analyst/` directory and lets you continue working on your specification. Use this at the start of a new session to pick up where you left off.

## Resume Process

### Step 1: Load Project State

1. **Locate project directory**
   - If path provided: look for `.business-analyst/` in that path
   - If no path: look for `.business-analyst/` in the current directory
   - If not found: inform user and suggest starting with `/business-analyst:analyze` or `/business-analyst:review`

2. **Read project.json** to get:
   - Project name, type, and objective
   - Current phase
   - Requirement counts
   - Last validation scores
   - Session history

3. **Read all requirement files** to load current state

### Step 2: Present Project Summary

```markdown
## Project: {name}
**Type**: {greenfield/brownfield} | **Domain**: {domain} | **Phase**: {phase}
**Objective**: {objective}

### Current Progress
| Category | Count | Last Modified |
|----------|-------|---------------|
| Functional Requirements | {N} | {date} |
| Non-Functional Requirements | {N} | {date} |
| Use Cases | {N} | {date} |
| Constraints | {N} | {date} |
| Assumptions | {N} | {date} |
| Risks | {N} | {date} |
| Data Elements | {N} | {date} |

### Last Validation
| Completeness | Quality | Status | Open Issues |
|--------------|---------|--------|-------------|
| {X}% | {X}% | {PASS/COND/FAIL} | {N} |

### Outstanding TBD Items ({N})
1. {TBD item} (from session on {date})
2. {TBD item}

### Session History
| Date | Action | Items Added |
|------|--------|-------------|
| {date} | {description} | +{N} FR, +{N} NFR |
| {date} | {description} | +{N} FR |

### Recent Changes
{Last 5 entries from changelog.md}
```

### Step 3: Offer Next Actions

Based on project state, suggest the most useful next action:

**If phase = "gathering" and there are many TBDs:**
> "You have {N} outstanding TBD items. Want me to walk through them and try to resolve them?"

**If phase = "gathering" and validation score < 75%:**
> "Your specification is at {X}% completeness. The main gaps are {gaps}. Want to work on filling those?"

**If phase = "gathering" and validation score >= 75%:**
> "Good progress! You're at {X}% completeness. Want to:
> 1. Add more requirements
> 2. Resolve TBD items
> 3. Run validation
> 4. Generate the SRS draft"

**If phase = "validating":**
> "Last validation found {N} issues. Want to work through them?"

**If phase = "drafting":**
> "SRS draft exists. Want to:
> 1. Add new requirements and regenerate
> 2. Review and refine the draft
> 3. Run final validation"

### Step 4: Continue Working

Based on user's choice, hand off to the appropriate workflow:
- **Add requirements** → Same as `/business-analyst:add` flow
- **Resolve TBDs** → Present each TBD with context, ask targeted questions
- **Fill gaps** → Run gap analysis, ask questions for missing categories
- **Run validation** → Execute `/business-analyst:validate` flow
- **Generate SRS** → Execute `/business-analyst:generate-srs` flow

All work in this session is saved back to the `.business-analyst/` directory.

## Handling Multiple Projects

If the user has multiple `.business-analyst/` directories (e.g., in subdirectories):

```bash
# Resume specific project
/business-analyst:resume ./projects/timetracker

# Resume from current directory
/business-analyst:resume
```

## Session Tracking

When resuming, create a new session entry in `project.json`:

```json
{
  "date": "{today}",
  "action": "Resumed project",
  "startingState": {
    "completeness": 72,
    "totalRequirements": 20,
    "openTBDs": 5
  }
}
```

At the end of the session (before the conversation ends or when the user switches tasks), update the session entry with outcomes:

```json
{
  "date": "{today}",
  "action": "Resumed project - focused on security requirements",
  "startingState": { "completeness": 72, "totalRequirements": 20, "openTBDs": 5 },
  "endingState": { "completeness": 81, "totalRequirements": 25, "openTBDs": 3 },
  "addedFR": 3,
  "addedNFR": 2,
  "questionsAsked": 8,
  "questionsAnswered": 7,
  "tbdsResolved": 2
}
```

## State Persistence Reminder

**IMPORTANT**: At the end of any work session, always:

1. Save all new/modified requirements to the appropriate files
2. Update `project.json` with new counts and session data
3. Append to `changelog.md`
4. Inform the user: "I've saved your progress. You have {N} requirements across {categories}. Run `/business-analyst:resume` next time to continue."

## Usage Examples

```bash
# Resume from current directory
/business-analyst:resume

# Resume from specific path
/business-analyst:resume ./my-project

# Resume and immediately add requirements
/business-analyst:resume then add requirements

# Resume and generate SRS
/business-analyst:resume then generate-srs
```
