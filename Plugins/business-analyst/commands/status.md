---
description: Show current status of a business analysis project. Displays requirement counts, validation scores, outstanding TBDs, and recent changes.
---

# Project Status

Show status for: **$ARGUMENTS**

## Overview

Quick view of your project's current state. Shows what you have, what's missing, and what to do next.

## Process

### Step 1: Load Project

1. Locate `.business-analyst/` directory (from path argument or current directory)
2. If not found: "No project found. Start with `/business-analyst:analyze`, `/business-analyst:review`, or `/business-analyst:greenfield`."
3. Read `project.json` and all requirement files

### Step 2: Display Status

```markdown
## Project: {name}
**Type**: {greenfield/brownfield} | **Domain**: {domain}
**Objective**: {objective}
**Phase**: {phase} | **Created**: {date} | **Last Modified**: {date}

---

### Requirements Summary

| Category | Count | Must | Should | Could | TBD |
|----------|-------|------|--------|-------|-----|
| Functional (FR) | {N} | {N} | {N} | {N} | {N} |
| Performance (NFR-PERF) | {N} | {N} | {N} | {N} | {N} |
| Security (NFR-SEC) | {N} | {N} | {N} | {N} | {N} |
| Reliability (NFR-REL) | {N} | {N} | {N} | {N} | {N} |
| Usability (NFR-USA) | {N} | {N} | {N} | {N} | {N} |
| Maintainability (NFR-MAINT) | {N} | {N} | {N} | {N} | {N} |
| Constraints (CON) | {N} | - | - | - | {N} |
| Assumptions (ASM) | {N} | - | - | - | {N} |
| Use Cases (UC) | {N} | - | - | - | - |
| Risks (RISK) | {N} | - | - | - | - |
| Data Elements (DE) | {N} | - | - | - | - |
| **Total** | **{N}** | | | | **{N}** |

### Validation Status

| Metric | Score | Status |
|--------|-------|--------|
| Completeness | {X}% | {bar} |
| Quality | {X}% | {bar} |
| Overall | {status} | {PASS / CONDITIONAL / FAIL / Not yet validated} |

### Outstanding TBD Items ({N})
{List TBD items, newest first}

### Recent Activity
{Last 5 changelog entries}

---

### Suggested Next Steps
{Context-aware suggestions based on current state}
```

### Step 3: Suggest Next Steps

Based on the current state, recommend actions:

**If never validated:**
> Run `/business-analyst:validate` to check your specification quality.

**If completeness < 75%:**
> Key gaps: {missing categories}. Run `/business-analyst:add {category}` to fill them.

**If there are TBDs:**
> You have {N} unresolved items. Run `/business-analyst:resume` to work through them.

**If completeness >= 90% and quality >= 90%:**
> Your specification looks ready! Run `/business-analyst:generate-srs` to produce the final document.

**If SRS exists but requirements changed since last generation:**
> Requirements have changed since the last SRS was generated. Run `/business-analyst:generate-srs` to update it.

## Usage Examples

```bash
# Status for current directory project
/business-analyst:status

# Status for specific project
/business-analyst:status ./my-project
```
