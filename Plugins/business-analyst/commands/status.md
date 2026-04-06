---
description: Show current status of a business analysis project. Detects conflicting requirements, identifies areas needing exploration, displays requirement counts, validation scores, outstanding TBDs, and recent changes.
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

### Step 2: Analyze Requirements

Before displaying status, perform two critical analyses on the loaded requirements:

#### 2a: Conflict Detection

Scan all requirements for conflicts. A conflict exists when:

1. **Direct contradiction**: Two requirements specify opposite behaviors
   - e.g., FR-012 "All users can view all reports" vs FR-045 "Only managers can view financial reports"
2. **Resource conflict**: Requirements compete for the same constrained resource
   - e.g., NFR-PERF-001 "Response time < 200ms" with FR-030 "Run full virus scan on every upload"
3. **Priority conflict**: Same feature has different priorities from different stakeholders
   - e.g., FR-010 marked "Must" by Product but "Won't" by Engineering
4. **Assumption conflict**: An assumption contradicts a stated requirement or another assumption
   - e.g., ASM-003 "Users have modern browsers" vs NFR-USA-002 "Support IE11"
5. **Scope conflict**: A requirement contradicts the stated scope boundaries
   - e.g., Scope says "No mobile support" but FR-025 describes a mobile workflow

For each conflict found, record:
- The conflicting requirement IDs
- The nature of the conflict
- A suggested resolution approach

#### 2b: Coverage Gap Analysis

Analyze what areas need further exploration by checking:

**FURPS+ Coverage Gaps**
- For each FURPS+ category, check if requirements exist
- Flag any category with zero requirements as "Needs exploration"
- Flag any category with only vague/TBD requirements as "Needs detail"

**Structural Gaps**
- Requirements without acceptance criteria → "Needs detail"
- Requirements without priority → "Needs prioritization"
- Requirements without business justification → "Needs traceability"
- Features mentioned in functional requirements but with no corresponding NFRs → "Needs NFR coverage"
- Integrations mentioned but without error handling / SLA requirements → "Needs integration detail"
- Data entities referenced but not in the data dictionary → "Needs data definition"
- High-complexity requirements without use cases → "Needs behavioral detail"

**Domain-Specific Gaps**
Based on the project's domain (from `project.json`):
- Healthcare without HIPAA/PHI requirements → flag
- Fintech without PCI/AML/KYC requirements → flag
- E-commerce without payment/fulfillment NFRs → flag
- SaaS without multi-tenancy/billing requirements → flag
- Government without accessibility/compliance requirements → flag
- Any domain without security requirements → flag

**Risk Coverage Gaps**
- High-priority (Must) requirements without associated risks → "Needs risk assessment"
- External integrations without failure/fallback risks → "Needs risk assessment"
- Assumptions not linked to any risk → "Consider risk if assumption is wrong"

### Step 3: Display Status

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

### Conflicts ({N} found)

{If no conflicts:}
> No conflicting requirements detected.

{If conflicts found, list each:}

| # | Conflict | Requirements | Type | Suggested Resolution |
|---|----------|-------------|------|---------------------|
| 1 | {description} | FR-012 vs FR-045 | Direct contradiction | Clarify scope of FR-012 with stakeholder |
| 2 | {description} | NFR-PERF-001 vs FR-030 | Resource conflict | Negotiate performance target or processing approach |
| 3 | {description} | ASM-003 vs NFR-USA-002 | Assumption conflict | Confirm browser support policy with stakeholder |

### Areas Needing Exploration

{If nothing needs exploration:}
> All areas have adequate coverage.

{If gaps found, list by urgency:}

**Must Address** (blocking specification completeness)
| Area | Issue | Recommendation |
|------|-------|----------------|
| Security | No security requirements documented | `/business-analyst:add security requirements` |
| {Category} | {Issue} | {Action} |

**Should Address** (reduces specification quality)
| Area | Issue | Recommendation |
|------|-------|----------------|
| FR-003, FR-007, FR-012 | Missing acceptance criteria | Add measurable criteria to these requirements |
| Payment integration | No error handling / SLA defined | Explore failure scenarios and recovery |
| {Entity X, Entity Y} | Referenced in requirements but not in data dictionary | Define data elements |
| FR-015 | Complex workflow without use case | Document actors, flows, and exceptions |

**Consider Addressing** (would improve completeness)
| Area | Issue | Recommendation |
|------|-------|----------------|
| Maintainability | No NFR-MAINT requirements | Consider logging, monitoring, deployment needs |
| Risk coverage | 3 Must-Have FRs have no associated risks | Assess what could go wrong |

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
{Context-aware suggestions based on current state — see Step 4}
```

### Step 4: Suggest Next Steps

Based on the full analysis, recommend actions in priority order:

**If there are conflicts:**
> You have {N} conflicting requirements that need resolution. Want me to walk through them? These should be resolved before generating the SRS.

**If there are "Must Address" exploration gaps:**
> Key areas need exploration: {list}. Run `/business-analyst:add {category}` to fill them, or `/business-analyst:resume` and I'll guide you through.

**If never validated:**
> Run `/business-analyst:validate` for a full quality check.

**If there are "Should Address" gaps:**
> {N} requirements need more detail (missing acceptance criteria, data definitions, etc.). Run `/business-analyst:resume` to work through them.

**If there are TBDs:**
> You have {N} unresolved items. Run `/business-analyst:resume` to work through them.

**If completeness >= 90% and quality >= 90% and no conflicts:**
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
