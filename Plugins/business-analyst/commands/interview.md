---
description: Start interactive requirements gathering interview session. Uses structured templates with adaptive follow-ups based on stakeholder responses.
---

# Requirements Interview Session

Start requirements gathering interview for: **$ARGUMENTS**

## Interview Overview

This command initiates a focused interview session to gather requirements from stakeholders. The interview combines structured question templates with adaptive follow-up based on your responses.

## Interview Categories

Select a focus area or let me guide you through a comprehensive interview:

### 1. Stakeholder Identification
- Who are the users, owners, and maintainers?
- What are their roles and interests?
- Who makes decisions?

### 2. Scope Definition
- What problem are we solving?
- What's in and out of scope?
- What are the boundaries?

### 3. Functional Requirements
- What must the system do?
- What are the key user workflows?
- What business rules apply?

### 4. Non-Functional Requirements
- Performance expectations
- Security requirements
- Reliability needs
- Usability standards

### 5. Constraints
- Technical limitations
- Budget and timeline
- Regulatory compliance

### 6. Integrations
- External systems
- Data flows
- APIs and protocols

## Interview Process

### Opening
I'll start by understanding your context:
- Your role in relation to the system
- Your main objectives
- Areas you're most concerned about

### Main Questions
Based on the focus area, I'll ask targeted questions:
- Open-ended questions for context
- Specific questions for details
- Scenario-based questions for edge cases

### Adaptive Follow-Ups
Based on your answers, I'll probe deeper:
- "Can you give me an example?"
- "What happens if [edge case]?"
- "Who else is involved?"

### Confirmation
After each section, I'll summarize and confirm:
- "Let me make sure I understood correctly..."
- "Is there anything I missed?"

## Project Persistence

**All interview results are automatically saved** to `.business-analyst/` if a project exists.

- New requirements are appended to the appropriate requirement files with next available IDs
- Interview Q&A is logged to `interview-log.md` with timestamps
- Assumptions are added to `requirements/assumptions.md`
- TBD items are tracked in `project.json`
- Session summary is appended to `changelog.md`

If no project exists, the interview will offer to create one.

## Interview Output

At the end of the interview, you'll receive:

1. **Interview Summary**
   - Key findings
   - Requirements identified
   - Open questions

2. **Requirements List**
   - Organized by category
   - With preliminary priorities
   - Linked to interview context
   - Saved to `.business-analyst/` project

3. **Assumptions Log**
   - Assumptions made during interview
   - Items needing confirmation

4. **Follow-Up Actions**
   - Additional interviews needed
   - Information to gather
   - Decisions to make

## Interview Tips

For the best results:
- Be specific with examples when possible
- Share real scenarios you've encountered
- Mention pain points and frustrations
- Think about edge cases and exceptions
- Don't worry about technical details - I'll translate to requirements

## Starting the Interview

To begin, tell me:
1. What topic or area would you like to focus on?
2. What is your role (user, business owner, technical lead, etc.)?
3. How much time do you have for this session?

Or simply describe what you need, and I'll guide the conversation from there.

---

## Quick Start Options

**Comprehensive Interview**: Cover all categories systematically
```
/business-analyst:interview comprehensive
```

**Focused Interview**: Specific topic
```
/business-analyst:interview functional requirements
/business-analyst:interview performance requirements
/business-analyst:interview security requirements
```

**Role-Based Interview**: From specific perspective
```
/business-analyst:interview as business owner
/business-analyst:interview as end user
/business-analyst:interview as technical lead
```
