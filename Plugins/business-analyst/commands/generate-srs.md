---
description: Generate IEEE 830 compliant Software Requirements Specification document from gathered requirements.
---

# Generate SRS Document

Generate Software Requirements Specification for: **$ARGUMENTS**

## SRS Generation Overview

This command compiles all gathered requirements, analysis findings, and stakeholder information into a formal IEEE 830 compliant Software Requirements Specification document.

## Input Sources

### From Saved Project (preferred)
If a `.business-analyst/` directory exists, the SRS is generated from all persisted state:
- `requirements/functional.md` → Section 3.2
- `requirements/non-functional.md` → Section 3.3
- `requirements/constraints.md` → Section 2.4, 3.4
- `requirements/assumptions.md` → Section 2.5
- `requirements/use-cases.md` → Section 3.2 (detailed flows)
- `stakeholders.md` → Section 2.3
- `risk-register.md` → Appendix D
- `data-dictionary.md` → Appendix E
- `traceability.md` → Appendix C
- `project.json` → Document metadata, version, counters

This means you can gather requirements over days or weeks using `/add`, `/review`, `/resume`, etc., then run `/generate-srs` at any point to produce the full document from everything accumulated so far.

### From Conversation Context
If no `.business-analyst/` project exists, the SRS is compiled from whatever requirements have been gathered in the current conversation.

## Prerequisites

Before generating the SRS, ensure you have:
- [ ] Stakeholder information identified
- [ ] Scope defined
- [ ] Functional requirements gathered
- [ ] Non-functional requirements documented
- [ ] Constraints and assumptions listed
- [ ] Priorities assigned

If any of these are missing, I'll help gather them or note them as TBD in the document.

## Document Structure

The SRS will follow IEEE 830 standard:

```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Definitions, Acronyms, Abbreviations
   1.4 References
   1.5 Overview

2. Overall Description
   2.1 Product Perspective
   2.2 Product Functions
   2.3 User Characteristics
   2.4 Constraints
   2.5 Assumptions and Dependencies

3. Specific Requirements
   3.1 External Interface Requirements
   3.2 Functional Requirements
   3.3 Non-Functional Requirements
   3.4 Design Constraints
   3.5 Software System Attributes

4. Appendices
   A. Glossary
   B. Analysis Models
   C. Requirements Traceability Matrix
```

## Generation Process

### Step 1: Information Gathering

I will:
1. Review all previous conversation context
2. Read any existing requirements documents
3. Compile stakeholder information
4. Gather all documented requirements

### Step 2: Document Compilation

For each section:
1. Populate with gathered information
2. Format according to IEEE 830 standards
3. Assign requirement IDs
4. Cross-reference related items

### Step 3: Quality Review

Before finalizing:
1. Check all sections are populated
2. Verify consistent terminology
3. Ensure unique requirement IDs
4. Validate cross-references
5. Mark any TBD items

### Step 4: Traceability Matrix

Create mappings:
- Business objectives to requirements
- Requirements to each other (dependencies)
- Requirements to stakeholders

### Step 5: Output Generation

Produce the final document in markdown format.

## Output Options

### Full SRS Document
Complete IEEE 830 compliant document with all sections.
```
/business-analyst:generate-srs full
```

### Executive Summary
Condensed overview for stakeholder review.
```
/business-analyst:generate-srs summary
```

### Requirements Only
Just the requirements section without IEEE structure.
```
/business-analyst:generate-srs requirements-only
```

### Specific Sections
Generate specific sections only.
```
/business-analyst:generate-srs functional
/business-analyst:generate-srs non-functional
/business-analyst:generate-srs appendices
```

## Customization

### Project Information
Please provide (or confirm):
- Project name
- Version number
- Author name
- Date

### Requirement ID Prefix
Default format: `FR-001`, `NFR-PERF-001`
Custom prefix: `/business-analyst:generate-srs prefix=REQ`

### Priority Scheme
Default: MoSCoW (Must/Should/Could/Won't)
Alternative: `/business-analyst:generate-srs priority=P1-P4`

## Document Metadata

The generated document will include:

```markdown
# Software Requirements Specification

## {Project Name}

| Field | Value |
|-------|-------|
| Document Version | {X.X} |
| Date | {YYYY-MM-DD} |
| Author | {Name} |
| Status | Draft |

## Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | {Date} | {Author} | Initial draft |
```

## Handling Incomplete Information

When information is missing:

1. **Mark as TBD**: Section will note "To Be Determined"
2. **Create Action Item**: Flag for follow-up
3. **Document Assumption**: If reasonable assumption can be made
4. **Skip Section**: Only if truly not applicable

I will inform you of any TBD items at the end.

## Post-Generation

After generating the SRS:

1. **Review Summary**: Overview of what was generated
2. **TBD Items**: List of items needing completion
3. **Validation Offer**: Option to run validator for quality check
4. **Next Steps**: Recommended actions

## User Checkpoints

Before generating, I'll confirm:
1. "I have the following information. Is it complete?"
2. "There are {N} TBD items. Proceed or provide more info?"
3. "Ready to generate the SRS document?"

After generating:
1. "The SRS has been generated. Would you like me to run validation?"
2. "There are {N} items marked TBD. Should I help complete them?"

## Getting Started

Let me check what information we have available:
1. Have requirements been gathered in this conversation?
2. Is there an existing requirements document to incorporate?
3. What project name should I use?
4. What format would you prefer (full/summary/requirements-only)?
