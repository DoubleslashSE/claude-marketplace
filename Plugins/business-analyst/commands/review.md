---
description: Review an existing requirements document (.md or other format). Reads the document, validates it, identifies gaps and ambiguities, and conducts an interactive Q&A session to improve it before generating a complete SRS.
---

# Review Existing Requirements

Review and improve requirements from: **$ARGUMENTS**

## Overview

This command takes an existing requirements document as input, analyzes it thoroughly, and works with you interactively to fill gaps, resolve ambiguities, and produce a complete, validated specification.

**This is the right command when you already have requirements written down** (in markdown, text, or any format) and want to turn them into a rigorous, complete specification.

## Input Handling

### Accepted Input Sources
1. **File path**: `/business-analyst:review ./docs/requirements.md`
2. **Multiple files**: `/business-analyst:review ./docs/requirements.md ./docs/nfr.md`
3. **Directory**: `/business-analyst:review ./docs/requirements/` (reads all .md files)
4. **Inline**: If no file path provided, prompt: "Please paste or describe your existing requirements."

### Step 1: Read and Parse the Document

1. Read the provided file(s) using the Read tool
2. Identify the structure and format used (formal SRS, bullet list, user stories, mixed, etc.)
3. Extract all identifiable requirements, grouping by type:
   - Functional requirements
   - Non-functional requirements
   - Constraints
   - Assumptions
   - Business rules
   - User stories / use cases
4. Note any existing categorization, IDs, or prioritization the author used

**Present initial findings:**
> "I've read your requirements document. Here's what I found:
> - {N} functional requirements identified
> - {N} non-functional requirements identified
> - {N} constraints/assumptions
> - {N} items I couldn't clearly classify
>
> The document appears to be in {format} format. Let me now analyze it for completeness and quality."

### Step 2: Gap Analysis

Run a structured analysis against what a complete specification needs:

#### Completeness Check
| Area | Status | Notes |
|------|--------|-------|
| Stakeholders identified | {Yes/No/Partial} | {Details} |
| Scope defined (in/out) | {Yes/No/Partial} | {Details} |
| Functional requirements | {Yes/No/Partial} | {N found, estimated N missing} |
| Non-functional requirements | {Yes/No/Partial} | {Which FURPS+ categories covered} |
| Business rules | {Yes/No/Partial} | {Details} |
| Constraints | {Yes/No/Partial} | {Details} |
| Assumptions | {Yes/No/Partial} | {Details} |
| Integrations | {Yes/No/Partial} | {Details} |
| Data requirements | {Yes/No/Partial} | {Details} |
| UI/UX requirements | {Yes/No/Partial} | {Details} |
| Risk considerations | {Yes/No/Partial} | {Details} |
| Acceptance criteria | {Yes/No/Partial} | {Per requirement} |

#### Quality Check (per requirement)
For each requirement found, assess:
- **Specific**: Is it clear and unambiguous?
- **Measurable**: Are there quantifiable acceptance criteria?
- **Testable**: Can test cases be written for it?
- **Traceable**: Is there a business justification?

Flag any that use vague language:
- "fast", "user-friendly", "intuitive", "scalable", "flexible"
- "should be easy to", "must handle large amounts"
- "as needed", "various", "etc.", "and so on"

#### Missing FURPS+ Categories
Check which non-functional categories are absent:
- [ ] **Performance**: Response times, throughput, capacity
- [ ] **Security**: Authentication, authorization, data protection
- [ ] **Reliability**: Availability, recovery, fault tolerance
- [ ] **Usability**: Accessibility, learnability, error handling
- [ ] **Supportability**: Maintainability, monitoring, logging
- [ ] **Constraints**: Technical, regulatory, business

### Step 3: Interactive Q&A Session

**This is the core of the review command.** Present findings and work through gaps interactively.

#### 3a: Present Summary
> "Here's my analysis of your requirements document:
>
> **Strengths:**
> - {What's well-covered}
>
> **Gaps Found:** ({N} total)
> - {Critical gaps}
> - {Missing categories}
> - {Vague requirements needing clarification}
>
> **I have {N} questions to ask you.** I'll work through them by priority — critical gaps first, then quality improvements. We can stop at any point and I'll generate the SRS with what we have.
>
> Ready to begin?"

#### 3b: Question Rounds

Work through questions in priority order:

**Round 1: Critical Gaps** (missing entire categories)
- Ask about missing stakeholders, scope boundaries, security, etc.
- Use domain-specific questions if a domain was identified
- One topic at a time, confirm understanding before moving on

**Round 2: Ambiguous Requirements** (vague or unmeasurable)
For each flagged requirement, ask for specifics:
> "Your requirement says '{vague text}'. Can you help me make this more specific?
> For example:
> - What metric would you use to measure this?
> - What's an acceptable threshold?
> - Can you give me a concrete scenario?"

**Round 3: Missing Details** (requirements that exist but lack depth)
- Missing acceptance criteria
- Missing business justification
- Missing priority
- Missing error/edge case handling

**Round 4: Assumptions and Risks**
- Confirm assumptions discovered in the document
- Ask about risks: "What could go wrong with {requirement}?"
- Identify external dependencies

#### 3c: Adaptive Behavior

- **If the user says "skip"**: Mark item as TBD, move to next
- **If the user says "not sure"**: Document as assumption, flag for later
- **If the user provides partial info**: Capture what's given, note what's still needed
- **If the user says "that's enough"**: Stop Q&A, proceed to generation with what we have
- **If the user provides a detailed answer**: Extract multiple requirements from a single answer when appropriate

### Step 4: Consolidation

After Q&A, consolidate everything:

1. **Merge original requirements** with new information gathered
2. **Assign IDs** to all requirements (FR-XXX, NFR-XXX, etc.)
3. **Assign priorities** (confirm with user if not already set)
4. **Build traceability** from business objectives to requirements
5. **Classify data elements** for the data dictionary
6. **Document risks** identified during review
7. **Build RACI matrix** if stakeholders were identified

### Step 5: Validation

Run the full validation suite on the consolidated requirements:
- Completeness score
- Quality score (SMART compliance)
- Consistency check
- Traceability check

If score < 90%, present remaining gaps and offer another Q&A round.

### Step 6: SRS Generation

Generate the complete SRS document including:
- All IEEE 830 sections
- Requirements from original document + Q&A session
- Risk register
- Data dictionary (for data elements identified)
- Acceptance test strategy
- RACI matrix (if stakeholders identified)
- Traceability matrix
- TBD items clearly marked

## User Checkpoints

1. **After initial read**: "Here's what I found in your document. Does this look right?"
2. **After gap analysis**: "Here are the gaps. Ready to work through questions?"
3. **After each Q&A round**: "Good progress. Want to continue to {next round} or generate with what we have?"
4. **After consolidation**: "Here's the consolidated view. Anything to adjust?"
5. **Before SRS generation**: "Ready to generate the full SRS?"

## Handling Different Input Quality

### Well-Structured Input (has IDs, categories, acceptance criteria)
- Skip classification step
- Focus on gap analysis and missing categories
- Q&A is shorter, focused on gaps

### Rough Notes / Bullet Points
- Spend more time on classification
- Help structure requirements from raw ideas
- Q&A is longer, more discovery-oriented

### User Stories Only
- Good starting point for functional requirements
- Will need significant NFR gathering
- May need use case modeling for complex flows

### Mixed Format / Informal
- Extract requirements from narrative text
- Confirm interpretation with user
- Restructure into consistent format

## Expected Outputs

1. **Review Report**
   - Original document analysis
   - Gaps identified and addressed
   - Questions asked and answers received
   - Items still marked TBD

2. **Complete SRS Document**
   - IEEE 830 compliant
   - Merges original requirements with Q&A findings
   - All appendices (risk, data dictionary, test strategy, RACI)

3. **Validation Report**
   - Quality and completeness scores
   - Remaining issues (if any)

## Project Persistence

**All work is automatically saved** to a `.business-analyst/` directory.

- At start: initialize or load existing `.business-analyst/` project
- After Q&A: save all requirements, changelog, interview log
- At end: save final state, inform user about `/business-analyst:resume` and `/business-analyst:add`

This means you can run `/business-analyst:review` today, then `/business-analyst:add` tomorrow with new requirements, and everything merges together.

## Usage Examples

```bash
# Review a single requirements file
/business-analyst:review ./docs/requirements.md

# Review multiple files
/business-analyst:review ./docs/functional-reqs.md ./docs/nfr.md

# Review a directory of requirement docs
/business-analyst:review ./specs/

# Review with a stated objective
/business-analyst:review ./requirements.md --objective "Preparing for development sprint planning"

# No file - will prompt for inline input
/business-analyst:review
```
