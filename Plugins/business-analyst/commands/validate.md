---
description: Validate requirements artifacts for completeness, quality, and consistency. Produces validation report with scores, issues, and recommendations.
---

# Validate Requirements Artifact

Validate: **$ARGUMENTS**

## Validation Overview

This command runs comprehensive validation on requirements artifacts to ensure quality, completeness, and consistency. The validation produces a detailed report with scores, identified issues, and actionable recommendations.

## What Can Be Validated

- **SRS Document**: Full IEEE 830 compliance check
- **Requirements List**: Quality and completeness check
- **Interview Notes**: Information completeness check
- **Analysis Report**: Coverage and accuracy check
- **Traceability Matrix**: Completeness and correctness check

## Validation Checks

### 1. Completeness Validation

**SRS Completeness (IEEE 830)**
```
Section 1: Introduction
  [ ] 1.1 Purpose stated
  [ ] 1.2 Scope defined
  [ ] 1.3 All terms defined
  [ ] 1.4 References listed
  [ ] 1.5 Overview provided

Section 2: Overall Description
  [ ] 2.1 Product perspective
  [ ] 2.2 Functions summarized
  [ ] 2.3 User characteristics
  [ ] 2.4 Constraints
  [ ] 2.5 Assumptions

Section 3: Specific Requirements
  [ ] 3.1 External interfaces
  [ ] 3.2 Functional requirements
  [ ] 3.3 Non-functional requirements

Appendices
  [ ] Glossary
  [ ] Analysis models
  [ ] Traceability matrix
```

### 2. Requirement Quality (SMART)

For each requirement:
| Criterion | Check |
|-----------|-------|
| **S**pecific | Clear and unambiguous? |
| **M**easurable | Quantifiable criteria? |
| **A**chievable | Technically feasible? |
| **R**elevant | Traces to business value? |
| **T**estable | Test cases can be written? |

### 3. Consistency Validation

- No conflicting requirements
- No duplicate requirements
- Consistent terminology
- Consistent formatting
- Valid cross-references

### 4. Traceability Validation

- All requirements trace to business objectives
- No orphan requirements
- Dependencies documented
- Test case mapping exists (or planned)

### 5. Assumption Validation

- All assumptions documented
- Impact if false identified
- Confirmation status tracked

## Validation Report Format

```markdown
# Validation Report

## Summary
| Metric | Value |
|--------|-------|
| Artifact | {Type} |
| Completeness Score | {X}% |
| Quality Score | {X}% |
| Issues Found | {N} |
| Critical Issues | {N} |

## Scores Breakdown

### Completeness: {X}%
| Section | Status | Score |
|---------|--------|-------|
| {Section} | {Complete/Partial/Missing} | {%} |

### Quality: {X}%
| Factor | Score |
|--------|-------|
| SMART Compliance | {%} |
| Traceability | {%} |
| Consistency | {%} |
| Clarity | {%} |

## Issues Found

### Critical (Must Fix)
| ID | Issue | Location | Recommendation |
|----|-------|----------|----------------|
| C1 | {Issue} | {Where} | {Fix} |

### High Priority
| ID | Issue | Location | Recommendation |
|----|-------|----------|----------------|
| H1 | {Issue} | {Where} | {Fix} |

### Medium Priority
| ID | Issue | Location | Recommendation |
|----|-------|----------|----------------|
| M1 | {Issue} | {Where} | {Fix} |

### Low Priority
| ID | Issue | Location | Recommendation |
|----|-------|----------|----------------|
| L1 | {Issue} | {Where} | {Fix} |

## Unconfirmed Assumptions
| ID | Assumption | Impact if False | Status |
|----|------------|-----------------|--------|
| A1 | {Assumption} | {Impact} | Needs confirmation |

## User Confirmation Required
[ ] {Item needing confirmation}

## Status: {PASS / CONDITIONAL PASS / FAIL}

## Recommended Next Steps
1. {Action}
2. {Action}
```

## Scoring Methodology

### Completeness Score
```
Section Weights:
- Introduction: 10%
- Overall Description: 20%
- Functional Requirements: 35%
- Non-Functional Requirements: 25%
- Appendices: 10%

Score = Sum of (Section % Complete * Weight)
```

### Quality Score
```
Factor Weights:
- SMART Compliance: 30%
- Traceability: 25%
- Consistency: 20%
- Clarity: 15%
- Confirmation Status: 10%

Score = Sum of (Factor % Achieved * Weight)
```

### Status Thresholds
| Score | Status |
|-------|--------|
| 90-100% | PASS |
| 75-89% | CONDITIONAL PASS |
| 60-74% | FAIL (revisions needed) |
| Below 60% | FAIL (major rework) |

## Validation Options

### Full Validation
Complete validation of all aspects.
```
/business-analyst:validate all
```

### Quick Validation
Essential checks only (faster).
```
/business-analyst:validate quick
```

### Specific Checks
Run specific validation only.
```
/business-analyst:validate completeness
/business-analyst:validate quality
/business-analyst:validate consistency
/business-analyst:validate traceability
```

### Validate Specific Artifact
```
/business-analyst:validate SRS
/business-analyst:validate requirements-list
/business-analyst:validate {file-path}
```

## Interactive Validation

After validation, I will:

1. **Present Summary**: "The validation found {N} issues."
2. **Offer Details**: "Would you like to see the full report?"
3. **Confirm Assumptions**: "Can you verify these {N} assumptions?"
4. **Suggest Fixes**: "Here's how to address the critical issues."
5. **Offer Re-validation**: "After fixes, shall I validate again?"

## Feedback Loop Integration

### Feeding Back to Business Analyst

The validation doesn't just report issues - it generates structured feedback that is fed back to improve the requirements. This creates a continuous improvement cycle.

### Feedback Output Format

After validation, generate actionable feedback:

```markdown
## Validation Feedback for Requirements Improvement

### Immediate Corrections Required
| Issue ID | Current State | Required Change | How to Fix |
|----------|---------------|-----------------|------------|
| FB-001 | FR-023 is vague | Add metrics | Ask: "What response time is acceptable?" |
| FB-002 | NFR-SEC missing | Add auth requirements | Use NFR-SEC template |

### Specific Rewrites
BEFORE: "The system should be user-friendly"
AFTER: "The system shall achieve SUS score >= 80"
REASON: Not measurable → Now has specific metric

### Questions to Ask Stakeholder
1. [For NFR-PERF-001] "What is the expected concurrent user count?"
2. [For NFR-SEC-001] "What authentication method is preferred?"
3. [For ASM-001] "Can we assume modern browser support only?"

### Assumptions to Confirm
| Assumption | Impact if Wrong | Question |
|------------|-----------------|----------|
| Modern browsers | Need legacy support | "Confirm browser support?" |
| 99.9% uptime | Higher availability | "Is 99.9% acceptable?" |

### Templates for Missing Requirements
[Provide templates for any missing requirement types]

### Conflict Resolutions Needed
[List conflicts with resolution options]
```

### Feedback Processing Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEEDBACK IMPROVEMENT CYCLE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VALIDATE ──▶ GENERATE FEEDBACK ──▶ PROCESS FEEDBACK            │
│      ▲                                    │                     │
│      │                                    ▼                     │
│      │                           ┌────────────────┐             │
│      │                           │ Apply Fixes:   │             │
│      │                           │ - Rewrite reqs │             │
│      │                           │ - Add missing  │             │
│      │                           │ - Ask questions│             │
│      │                           │ - Resolve      │             │
│      │                           │   conflicts    │             │
│      │                           └────────────────┘             │
│      │                                    │                     │
│      └────────────────────────────────────┘                     │
│                    RE-VALIDATE                                  │
│                                                                 │
│  Continue until: Score >= 90% OR User approves                  │
└─────────────────────────────────────────────────────────────────┘
```

### Improvement Tracking

Track progress across validation cycles:

```markdown
| Cycle | Completeness | Quality | Issues | Status |
|-------|--------------|---------|--------|--------|
| 1     | 65%          | 70%     | 15     | FAIL   |
| 2     | 82%          | 85%     | 6      | COND   |
| 3     | 95%          | 92%     | 2      | PASS   |
```

## Continuous Improvement

The validator helps maintain quality by:
- Identifying issues early
- **Feeding back actionable improvements to the business analyst**
- **Generating targeted stakeholder questions**
- **Providing specific rewrites for vague requirements**
- Tracking progress over iterations
- Ensuring stakeholder confirmation
- Maintaining documentation standards

## Project Persistence

### Loading from Saved Project
If a `.business-analyst/` directory exists, the validator automatically reads all persisted requirements, risks, data dictionary, and traceability from it. This is the preferred mode — it validates the full accumulated state of the project.

### Saving Validation Results
After validation:
1. Update `validation-history.md` with the new validation run (date, scores, issue count)
2. Update `project.json` validation section (lastRun, completeness, quality, status, openIssues)
3. Append validation summary to `changelog.md`

This means `/business-analyst:status` will always show the latest validation scores.

## Getting Started

What would you like me to validate?

1. **Saved project** — If `.business-analyst/` exists, I'll validate everything in it
2. A requirements list we've been building in this conversation
3. A specific file or document you can point me to

Or just say "validate" and I'll check the saved project state, or everything we've discussed if no project exists.

After validation, I will generate structured feedback that can be directly processed to improve the requirements.
