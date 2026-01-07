---
description: Execute business analysis for a new project. Focuses on stakeholder interviews, scope definition, and requirements gathering from scratch.
---

# Greenfield Project Analysis

Execute new project analysis for: **$ARGUMENTS**

## Objective Context

**IMPORTANT**: Parse the arguments for an objective/context statement that explains the driving purpose. Look for patterns like:
- `--objective "..."` or `-o "..."`
- `--context "..."` or `-c "..."`
- Natural language after project name: `MyApp - need mobile-first e-commerce`
- Quoted context: `CustomerPortal "replace legacy desktop app"`

If an objective is provided, store it as the **Analysis Objective** and use it to:
1. **Shape vision discussions** - Orient around the stated goal
2. **Focus requirements** - Prioritize requirements that serve the objective
3. **Guide stakeholder questions** - Ask questions relevant to the purpose
4. **Align outputs** - Ensure all documentation supports the objective

**Analysis Objective**: {extracted from arguments, or gathered during Phase 1}

## Greenfield Overview

This command is optimized for new projects where there is no existing codebase. The focus is on gathering requirements from stakeholders, defining scope, and documenting the vision for the new system.

**When an objective is provided**, it becomes the north star for the entire analysis.

## Greenfield Workflow

### Phase 1: Vision and Context (15 min)

**Business Context**
1. What business problem are we solving?
2. Who is the target audience?
3. What is the competitive landscape?
4. What differentiates this solution?

**Success Criteria**
1. How will we measure success?
2. What are the key performance indicators (KPIs)?
3. What does the MVP look like?

### Phase 2: Stakeholder Identification (10 min)

**Key Questions**
1. Who will use this system?
2. Who will make decisions about features?
3. Who controls the budget?
4. Who will maintain the system?
5. Are there external stakeholders (customers, partners, regulators)?

**Stakeholder Mapping**
For each stakeholder:
- Role and responsibilities
- Interest level (High/Medium/Low)
- Influence level (High/Medium/Low)
- Key concerns

### Phase 3: Scope Definition (15 min)

**Boundaries**
1. What is explicitly IN scope for this project?
2. What is explicitly OUT of scope?
3. What are the system boundaries?
4. What integrations are required?

**MVP vs Future**
1. What features are essential for launch?
2. What can be deferred to future phases?
3. What is the rollout strategy?

### Phase 4: Functional Requirements (30 min)

**Core Functionality**
For each feature area:
1. What must users be able to do?
2. What is the typical workflow?
3. What are the business rules?
4. What data is involved?

**User Stories Format**
```
As a [role]
I want [capability]
So that [business value]

Acceptance Criteria:
- Given [context]
- When [action]
- Then [outcome]
```

### Phase 5: Non-Functional Requirements (20 min)

**FURPS+ Categories**

**Performance**
- Expected user load
- Response time requirements
- Data volume expectations

**Security**
- Authentication requirements
- Authorization model
- Data protection needs
- Compliance requirements

**Reliability**
- Availability requirements
- Disaster recovery needs
- Backup requirements

**Usability**
- User skill level
- Accessibility needs
- Multi-language support

**Supportability**
- Monitoring requirements
- Logging needs
- Maintenance considerations

### Phase 6: Constraints and Assumptions (10 min)

**Constraints**
- Budget limitations
- Timeline constraints
- Technology requirements/restrictions
- Resource limitations
- Regulatory requirements

**Assumptions**
- User capabilities assumed
- Infrastructure assumptions
- Third-party availability
- Business conditions assumed

### Phase 7: Prioritization (15 min)

**MoSCoW Method**
Categorize all requirements:
- **Must Have**: Non-negotiable for launch
- **Should Have**: Important but not critical
- **Could Have**: Nice to have
- **Won't Have**: Future consideration

### Phase 8: Validation and Documentation (20 min)

**Validation Checkpoint**
1. Review all gathered requirements
2. Confirm priorities with stakeholder
3. Verify assumptions
4. Identify gaps

**Documentation**
1. Generate requirements inventory
2. Create traceability matrix
3. Produce SRS document draft

## User Checkpoints

I will pause for your confirmation at:

1. **After Vision/Context**: "Is this understanding of the problem correct?"
2. **After Stakeholders**: "Have I identified all key stakeholders?"
3. **After Scope**: "Are these boundaries accurate?"
4. **After Functional Requirements**: "Have I captured the core functionality?"
5. **After Priorities**: "Does this prioritization look right?"
6. **Before Documentation**: "Ready to generate the SRS?"

## Expected Outputs

1. **Stakeholder Register**
   - Complete list with roles and interests

2. **Scope Document**
   - In/out of scope items
   - MVP definition
   - Future phases outline

3. **Requirements Inventory**
   - Functional requirements (user stories)
   - Non-functional requirements
   - Constraints and assumptions

4. **Prioritized Backlog**
   - MoSCoW categorized requirements

5. **SRS Document**
   - IEEE 830 compliant specification

6. **Validation Report**
   - Quality and completeness assessment

## Getting Started

Let's begin the greenfield analysis!

**If an objective was provided in the arguments**, acknowledge it:
> "I see you're building this for: **{objective}**. I'll focus my analysis accordingly."

Then gather remaining context.

**If no objective was provided**, ask:
1. What is the name of the project?
2. In 2-3 sentences, what problem does it solve?
3. **What is the primary driver?** Examples:
   - "Replacing a legacy system"
   - "New market opportunity"
   - "Customer request"
   - "Internal efficiency improvement"
4. Who is the primary target user?

## Usage Examples

```bash
# Basic usage (will gather objective during Phase 1)
/business-analyst:greenfield MyNewApp

# With objective
/business-analyst:greenfield CustomerPortal --objective "Replace legacy desktop app with web-based solution"
/business-analyst:greenfield MobileApp -o "Capture millennial market segment"

# Natural language
/business-analyst:greenfield TimeTracker - internal tool to replace spreadsheets
```
