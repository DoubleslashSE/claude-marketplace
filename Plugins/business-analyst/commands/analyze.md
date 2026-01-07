---
description: Execute complete business analysis workflow. Auto-detects greenfield vs brownfield and runs appropriate analysis combining codebase analysis, stakeholder interviews, and documentation.
---

# Business Analysis Workflow

Execute comprehensive business analysis for: **$ARGUMENTS**

## Objective Context

**IMPORTANT**: Parse the arguments for an objective/context statement that explains WHY this analysis is being done. Look for patterns like:
- `--objective "..."` or `-o "..."`
- `--context "..."` or `-c "..."`
- `--reason "..."` or `-r "..."`
- Natural language after path/name: `./src - refactoring for testability`
- Quoted context: `MyProject "adding real-time features"`

If an objective is provided, store it as the **Analysis Objective** and use it to:
1. **Focus the entire workflow** - Every phase should align with this objective
2. **Prioritize relevant areas** - Spend more time on aspects that matter for the goal
3. **Shape stakeholder questions** - Ask questions oriented toward the objective
4. **Guide recommendations** - All outputs should help achieve the stated goal

**Analysis Objective**: {extracted from arguments, or ask during context assessment}

## Workflow Overview

This command orchestrates the complete business analysis process, automatically detecting whether this is a greenfield (new) or brownfield (existing) project and adapting the workflow accordingly.

**When an objective is provided**, acknowledge it immediately and let it drive the analysis focus throughout all phases.

## Auto-Detection Logic

**Greenfield indicators:**
- No existing codebase provided
- User mentions "new project", "from scratch", "greenfield"
- No path to existing code specified

**Brownfield indicators:**
- Path to existing codebase provided
- User mentions "existing", "legacy", "current system", "brownfield"
- References to current functionality

## Workflow Steps

### Phase 1: Context Assessment

1. **Determine Project Type**
   - Ask: "Is this a new project (greenfield) or does it involve an existing system (brownfield)?"
   - If brownfield, identify the codebase location

2. **Identify Stakeholders**
   - Ask: "Who are the key stakeholders for this project?"
   - Categories: Users, Business Owners, Technical Team, External parties

3. **Define Objectives**
   - Ask: "What are the main business objectives?"
   - Ask: "How will success be measured?"

### Phase 2: Requirements Gathering

**For Greenfield Projects:**
1. Conduct stakeholder interviews (structured + adaptive)
2. Define scope boundaries
3. Gather functional requirements
4. Gather non-functional requirements (FURPS+)
5. Document constraints and assumptions

**For Brownfield Projects:**
1. Analyze existing codebase
   - Extract domain models
   - Identify business rules
   - Map integrations
2. Conduct stakeholder interviews for:
   - Pain points with current system
   - Desired changes/enhancements
   - New requirements
3. Document as-is capabilities
4. Identify gaps and technical debt

### Phase 3: Analysis and Prioritization

1. **Classify Requirements**
   - Functional vs Non-functional
   - New vs Changed vs Removed (brownfield)

2. **Prioritize Using MoSCoW**
   - Must Have: Critical for success
   - Should Have: Important but not critical
   - Could Have: Nice to have
   - Won't Have: Out of scope

3. **Create Traceability**
   - Link requirements to business objectives
   - Identify dependencies between requirements

### Phase 4: Validation and Feedback Loop

This phase implements an iterative improvement cycle until requirements meet quality standards.

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION FEEDBACK LOOP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │  Validate  │───▶│  Generate  │───▶│   Apply    │            │
│  │Requirements│    │  Feedback  │    │Corrections │            │
│  └────────────┘    └────────────┘    └────────────┘            │
│        ▲                                    │                   │
│        │                                    │                   │
│        │           ┌────────────┐           │                   │
│        └───────────│ Re-validate│◀──────────┘                   │
│                    │  (if needed)│                              │
│                    └────────────┘                               │
│                                                                 │
│  EXIT CONDITION: Score >= 90% or User approves                  │
└─────────────────────────────────────────────────────────────────┘
```

**Cycle Steps:**

1. **Run Validator**
   - Check completeness against IEEE 830
   - Check quality (SMART criteria)
   - Identify gaps and issues
   - Generate feedback report

2. **Process Feedback**
   - Receive structured feedback from validator
   - Prioritize corrections (Critical → High → Medium → Low)
   - Identify questions to ask stakeholders

3. **Apply Corrections**
   - Rewrite ambiguous requirements
   - Add missing requirements using templates
   - Resolve conflicts with stakeholder input
   - Fill traceability gaps

4. **Gather Missing Information**
   - Ask stakeholder questions generated from feedback
   - Confirm assumptions flagged by validator
   - Update requirements with new information

5. **Re-validate**
   - Submit improved requirements
   - Track improvement metrics
   - Repeat until PASS status or user approval

**Quality Gates:**
- **PASS** (90%+): Proceed to documentation
- **CONDITIONAL PASS** (75-89%): User decides to proceed or iterate
- **FAIL** (<75%): Must iterate and improve

### Phase 5: Stakeholder Confirmation

1. **Present Findings Summary**
   - Requirements count by category
   - Validation scores achieved
   - Key assumptions needing confirmation

2. **Confirm Requirements**
   - Walk through critical requirements
   - Validate priorities are correct
   - Verify business value alignment

3. **Final Assumption Review**
   - List all assumptions
   - Get explicit confirmation or correction
   - Document stakeholder decisions

### Phase 6: Documentation

1. **Generate SRS Document**
   - IEEE 830 compliant format
   - Include all gathered requirements
   - Add traceability matrix
   - Include appendices
   - Mark confirmation status

2. **Final Validation Report**
   - Final completeness score
   - Final quality score
   - Iteration history
   - Stakeholder sign-offs

## User Checkpoints

The workflow will pause for user confirmation at these points:

1. After context assessment: "Is this understanding correct?"
2. After codebase analysis (brownfield): "Do these findings match your understanding?"
3. After requirements gathering: "Have I captured all key requirements?"
4. After prioritization: "Does this prioritization look right?"
5. Before SRS generation: "Ready to generate the SRS document?"

## Expected Outputs

At the end of this workflow, you will have:

1. **Stakeholder Register**
   - List of all stakeholders with roles and interests

2. **Requirements Inventory**
   - Comprehensive list of functional requirements
   - Non-functional requirements (FURPS+)
   - Constraints and assumptions

3. **Codebase Analysis Report** (brownfield only)
   - Domain model documentation
   - Business rules inventory
   - Integration map

4. **Traceability Matrix**
   - Business objectives to requirements mapping
   - Requirement dependencies

5. **SRS Document**
   - IEEE 830 compliant specification
   - Ready for stakeholder approval

6. **Validation Report**
   - Quality and completeness scores
   - Issues and recommendations

## Commands for Detailed Work

If you need more focused analysis, use these commands:
- `/business-analyst:greenfield` - Dedicated greenfield workflow
- `/business-analyst:brownfield` - Dedicated brownfield workflow
- `/business-analyst:interview` - Focused interview session
- `/business-analyst:generate-srs` - SRS generation only
- `/business-analyst:validate` - Validation only

## Getting Started

**If an objective was provided in the arguments**, acknowledge it:
> "I see you want to analyze this for: **{objective}**. I'll focus my analysis accordingly."

Then gather remaining context as needed.

**If no objective was provided**, begin with:

1. What is the name/description of the project?
2. Is this a new project or does it involve an existing system?
3. **What is driving this analysis?** (the "why")
   - Refactoring for maintainability/testability?
   - Adding a major new feature?
   - Migration or modernization?
   - Security/compliance audit?
   - Performance optimization?
   - General understanding before changes?
4. Who are the key stakeholders?
5. What are the primary business objectives?

## Usage Examples

```bash
# Basic usage (will ask for objective)
/business-analyst:analyze MyProject

# With explicit objective
/business-analyst:analyze ./src --objective "Refactor payment module for PCI compliance"
/business-analyst:analyze CustomerPortal -o "Add real-time notifications feature"

# Natural language
/business-analyst:analyze ./legacy-api - modernize to REST standards
```
