---
description: Add new requirements to an existing business analysis project. Reads from files, inline input, or interactive Q&A. Merges with existing requirements, detects duplicates, and updates project state.
---

# Add Requirements

Add requirements to project: **$ARGUMENTS**

## Overview

This command adds new requirements to an existing `.business-analyst/` project. Use it when you have new requirements to incorporate — from a file, pasted inline, or gathered through conversation.

**This is the command for incremental work.** Come back days or weeks later, add what's new, and the plugin merges it with everything already gathered.

## Input Modes

### Mode 1: From File
```bash
/business-analyst:add ./new-requirements.md
/business-analyst:add ./sprint-3-features.md ./compliance-reqs.md
```

### Mode 2: Inline / Conversational
```bash
/business-analyst:add
```
Then describe or paste requirements in the conversation.

### Mode 3: Targeted Category
```bash
/business-analyst:add security requirements
/business-analyst:add performance requirements
/business-analyst:add integrations
```
Starts a focused interview for that specific category.

## Process

### Step 1: Load Existing Project

1. Locate `.business-analyst/` directory
2. Read `project.json` for current state and counters
3. Read existing requirements to check for duplicates
4. If no project exists: "No project found. Start with `/business-analyst:analyze`, `/business-analyst:review`, or `/business-analyst:greenfield` first."

**Show brief status:**
> "Loaded project **{name}**. Currently has {N} functional, {N} non-functional requirements. Adding new ones..."

### Step 2: Parse New Input

**If from file:**
1. Read the file(s)
2. Extract and classify requirements (same as `/business-analyst:review` Step 1)
3. Present what was found:
   > "Found {N} new items in your file:
   > - {N} functional requirements
   > - {N} non-functional requirements
   > - {N} other items"

**If inline/conversational:**
1. Ask: "What requirements would you like to add? You can describe them in any format — bullet points, paragraphs, user stories, or just tell me what you need."
2. Parse the user's input into requirement candidates

**If targeted category:**
1. Load the domain-specific and category-specific question templates
2. Run a focused interview session for that category
3. Generate requirements from the answers

### Step 3: Duplicate Check

For each new requirement, compare against existing:

1. Look for similar descriptions, key terms, and intent
2. If a likely duplicate is found:
   > "This looks similar to an existing requirement:
   > - **Existing FR-005**: {description}
   > - **New**: {description}
   >
   > Should I: (a) skip the new one, (b) keep both, (c) update the existing one, or (d) merge them?"

3. If not a duplicate: proceed to assign ID

### Step 4: Assign IDs and Classify

For each new requirement:

1. **Classify**: Functional / NFR (which subcategory) / Constraint / Assumption
2. **Assign ID**: Use next available from `project.json` counters
3. **Set priority**: Ask user or default to "Proposed"
4. **Set status**: "Proposed" (new items start as proposed)
5. **Tag session**: Mark with today's date and session info

### Step 5: Quality Quick-Check

For each new requirement, do a quick SMART check:
- If vague: suggest improvement immediately
  > "'{requirement}' is a bit vague. Can you tell me:
  > - What specific metric would you use?
  > - What's an acceptable threshold?"
- If missing acceptance criteria: ask for them
- If no clear business justification: ask "Why is this needed?"

The user can say "skip" to add as-is and refine later.

### Step 6: Save and Report

1. **Append** new requirements to the appropriate files in `.business-analyst/requirements/`
2. **Update** `project.json` counters and session log
3. **Append** to `changelog.md`
4. **Update** `interview-log.md` if questions were asked
5. **Present summary:**

```markdown
## Session Summary

### Added ({N} new requirements)
| ID | Description | Priority | Status |
|----|-------------|----------|--------|
| FR-013 | {title} | Should | Proposed |
| FR-014 | {title} | Must | Proposed |
| NFR-SEC-004 | {title} | Must | Proposed |

### Updated ({N} existing requirements)
| ID | Change |
|----|--------|
| FR-005 | Updated acceptance criteria |

### Skipped ({N} duplicates)
| New | Matched Existing | Reason |
|-----|-----------------|--------|
| {desc} | FR-003 | Duplicate |

### Current Project Totals
| Category | Before | After |
|----------|--------|-------|
| Functional | {N} | {N} |
| Non-Functional | {N} | {N} |
| Total | {N} | {N} |

### Recommended Next Steps
- Run `/business-analyst:validate` to check completeness
- Run `/business-analyst:status` to see overall progress
- Run `/business-analyst:generate-srs` when ready for a draft
```

## Handling Large Additions

If the user provides a large file with many requirements:

1. Parse all at once
2. Present a summary for confirmation before saving:
   > "I've extracted {N} requirements from your file. Here's a preview of the first 5:
   > 1. FR-013: {title}
   > 2. FR-014: {title}
   > ...
   > Should I add all {N}, or would you like to review them one by one?"

3. Offer batch or individual review

## Usage Examples

```bash
# Add from a file
/business-analyst:add ./new-features.md

# Add from multiple files
/business-analyst:add ./sprint-4.md ./compliance-update.md

# Start interactive addition (no file)
/business-analyst:add

# Add specific category via focused interview
/business-analyst:add security requirements
/business-analyst:add performance requirements
/business-analyst:add integration requirements

# Add with context
/business-analyst:add --context "Requirements from client meeting on April 5"
```
