# Workflow Reference

Detailed reference for the multi-agent autonomous workflow with nested loop patterns for long-running execution.

---

## Execution Flow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          COMPLETE EXECUTION FLOW                             │
│                                                                              │
│  START                                                                       │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 0: SETUP                                                        │   │
│  │   0.1 Session recovery check                                          │   │
│  │   0.2 Discover platforms (scan Workflows/platforms/)                  │   │
│  │   0.3 Match platform to codebase                                      │   │
│  │   0.4 Load platform configuration                                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 1: ANALYSIS                                                     │   │
│  │   1.1 Pre-analysis clarification ←── ASK QUESTIONS IF NEEDED          │   │
│  │   1.2 Initialize state                                                │   │
│  │   1.3 Invoke analyst → stories                                        │   │
│  │   1.4 Pre-plan clarification ←── ASK QUESTIONS IF NEEDED              │   │
│  │   1.5 Invoke architect → design                                       │   │
│  │   1.6 Gate G1: verify design complete                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 2: STORY EXECUTION (NESTED LOOPS)                               │   │
│  │                                                                        │   │
│  │   ┌─ WHILE incomplete_stories > 0: ────────────────────────────────┐  │   │
│  │   │                                                                 │  │   │
│  │   │   story = get_next_incomplete()                                 │  │   │
│  │   │                                                                 │  │   │
│  │   │   ┌─ WHILE story.status != 'completed' AND iteration < 3: ──┐  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   │   1. Invoke developer(story, failures)                   │  │  │   │
│  │   │   │      └─ If build fails → append error, CONTINUE          │  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   │   2. Invoke tester(story, files)                         │  │  │   │
│  │   │   │      └─ If FAIL → append issues, CONTINUE                │  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   │   3. Invoke reviewer(story, files)                       │  │  │   │
│  │   │   │      └─ If CHANGES_REQUESTED → append, CONTINUE          │  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   │   4. If security_sensitive:                              │  │  │   │
│  │   │   │      Invoke security(story, files)                       │  │  │   │
│  │   │   │      └─ If NEEDS_REMEDIATION → append, CONTINUE          │  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   │   5. Mark story COMPLETED, commit changes                │  │  │   │
│  │   │   │                                                          │  │  │   │
│  │   │   └──────────────────────────────────────────────────────────┘  │  │   │
│  │   │                                                                 │  │   │
│  │   │   If story still incomplete → ESCALATE BLOCKER                  │  │   │
│  │   │                                                                 │  │   │
│  │   └─────────────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 3: COMPLETION                                                   │   │
│  │   3.1 Verify all stories completed                                    │   │
│  │   3.2 Invoke devops (if needed)                                       │   │
│  │   3.3 Create pull request ←── REQUIRED                                │   │
│  │   3.4 Complete workflow state                                         │   │
│  │   3.5 Output WORKFLOW_COMPLETE marker                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│    │                                                                         │
│    ▼                                                                         │
│  END                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Platform Auto-Detection (Phase 0)

### Step 0.2: Discover Available Platforms

```bash
# Scan platforms directory
ls Workflows/platforms/

# For each platform directory, read its detection criteria
# Example: Workflows/platforms/dotnet/platform.json
```

### Step 0.3: Detection Matching

Each `platform.json` contains:

```json
{
  "name": "dotnet",
  "detection": {
    "markers": ["*.sln", "*.csproj"],
    "matchMode": "any",
    "priority": 100,
    "description": "Detected by .sln or .csproj files"
  }
}
```

**Matching logic:**
- `matchMode: "any"` → Platform matches if ANY marker file exists
- `matchMode: "all"` → Platform matches only if ALL marker files exist
- If multiple platforms match → Select highest `priority`

### Step 0.4: Build Platform Context Block

After loading platform.json, create this context block for ALL subagent invocations:

```markdown
## Platform Context

**Platform:** {displayName} (v{version})

### Commands
| Action | Command |
|--------|---------|
| Build | `{commands.build}` |
| Test | `{commands.test}` |
| Lint | `{commands.lint}` |
| Coverage | `{commands.coverage}` |

### Project Structure
{projectStructure.description}

**Layers:**
- **{layer.name}** (`{layer.path}`) - {layer.contains}
  - Dependencies: {layer.dependencies}

### File Patterns
| Type | Pattern |
|------|---------|
| {patternName} | `{patternPath}` |

### Conventions
- **Test naming:** {conventions.testNaming}
- **Commit format:** {conventions.commitFormat}
- **Branch format:** {conventions.branchFormat}

### Anti-Patterns to Avoid
- **{ap.name}:** {ap.reason}

### Quality Thresholds
| Story Size | Coverage |
|------------|----------|
| S | {qualityGates.coverageThresholds.S}% |
| M | {qualityGates.coverageThresholds.M}% |
| L | {qualityGates.coverageThresholds.L}% |
| XL | {qualityGates.coverageThresholds.XL}% |
```

---

## Clarifying Questions (Phase 1)

### Pre-Analysis Clarification Template

```markdown
## Clarification Needed

Before I begin analysis, I need to clarify a few things about: **{goal}**

### Questions:

1. **Scope:** {specific question about boundaries}
   - Option A: {description}
   - Option B: {description}

2. **Constraints:** {question about technical constraints}

3. **Priority:** {question about what matters most}

---

Please answer these questions, or respond with "proceed with your best judgment" to continue autonomously.
```

### Pre-Plan Clarification Template

```markdown
## Design Clarification

I've broken down the goal into these stories:

| ID | Title | Size | Security |
|----|-------|------|----------|
| S1 | {title} | {size} | {yes/no} |
| S2 | {title} | {size} | {yes/no} |

### Questions:

1. **Priority order:** Should I implement in this order, or would you prefer a different sequence?

2. **Technical preferences:**
   - Any specific patterns or libraries to use?
   - Any patterns or libraries to avoid?

3. **Existing code concerns:**
   - Any files or modules I should be careful modifying?
   - Any known technical debt to be aware of?

---

Say "proceed" to continue with my proposed approach, or provide specific guidance.
```

---

## Subagent Invocation Patterns

**IMPORTANT:** Every subagent invocation MUST include the Platform Context block.

### Analyst (Phase 1.3)

```markdown
## Task for Analyst Subagent

{PLATFORM CONTEXT BLOCK}

**Goal:** {User's goal description}

### Requirements:
1. Break down the goal into discrete user stories
2. Define clear, testable acceptance criteria for each story
3. Estimate size (S/M/L/XL) based on platform conventions
4. Flag security-sensitive stories (auth, payments, user data)
5. Identify dependencies between stories
6. Recommend implementation order

### Output Format:
Return a structured list of stories with:
- Title
- User story format (As a... I want... So that...)
- Acceptance criteria (testable)
- Size estimate
- Security flag
- Dependencies
```

### Architect (Phase 1.5)

```markdown
## Task for Architect Subagent

{PLATFORM CONTEXT BLOCK}

**Stories from Analyst:**
{List of stories with acceptance criteria}

### Requirements:
1. Design component structure following platform.projectStructure
2. Use file patterns from platform.patterns
3. Document key architectural decisions with rationale
4. Identify file changes per story
5. Flag technical risks and mitigations
6. Ensure design avoids platform.antiPatterns

### Output Format:
Return technical design per story with:
- Component structure
- File changes with purposes
- Key decisions with rationale
- Technical risks
```

### Developer (Phase 2 - with Retry Context)

```markdown
## Task for Developer Subagent

{PLATFORM CONTEXT BLOCK}

**Story:** {story.id} - {story.title}

**Acceptance Criteria:**
- AC1: {criterion}
- AC2: {criterion}

**Technical Design:**
{Relevant design from architect for this story}

---

**Iteration:** {n}/3
**Previous Failures:** {list or "First attempt"}
**Fix Instructions:** {specific guidance or "None - initial implementation"}

---

### Requirements:
1. Follow TDD: RED → GREEN → REFACTOR
2. Use `{platform.commands.build}` to build
3. Use `{platform.commands.test}` to test
4. Follow `{platform.conventions.testNaming}` for test names
5. Place files according to `platform.patterns`
6. Avoid `platform.antiPatterns`
7. Commit with `{platform.conventions.commitFormat}`

### Output Format:
- Implementation log with test results
- Files changed with descriptions
- Build status: PASS/FAIL
- Test status: X passing, Y failing
```

### Tester (Phase 2 - Verification)

```markdown
## Task for Tester Subagent

{PLATFORM CONTEXT BLOCK}

**Story:** {story.id} - {story.title}

**Acceptance Criteria:**
- AC1: {criterion}
- AC2: {criterion}

**Implementation Summary:** {from developer}
**Files Changed:** {list from developer}

---

### Requirements:
1. Run tests using `{platform.commands.test}`
2. Check coverage using `{platform.commands.coverage}`
3. Verify coverage meets threshold for story size {size}
4. Verify each acceptance criterion has tests
5. Follow `{platform.conventions.testNaming}` for new tests
6. Return PASS or FAIL with specific issues

### Output Format:
- Verdict: PASS or FAIL
- Acceptance criteria status (each one)
- Coverage analysis vs threshold ({threshold}% required)
- Issues found (if FAIL): specific file:line references
```

### Reviewer (Phase 2 - Code Review)

```markdown
## Task for Reviewer Subagent

{PLATFORM CONTEXT BLOCK}

**Story:** {story.id} - {story.title}
**Files Changed:** {list of files}
**Implementation Summary:** {brief description}

---

### Requirements:
1. Verify files follow `platform.patterns` locations
2. Check architecture compliance per `platform.projectStructure`
3. Verify naming follows `platform.conventions`
4. Scan for `platform.antiPatterns` violations
5. Check code quality and maintainability
6. Return APPROVED or CHANGES_REQUESTED

### Output Format:
- Verdict: APPROVED or CHANGES_REQUESTED
- Architecture compliance: PASS/FAIL
- Anti-pattern violations found (if any)
- Code quality findings
- Required changes (if any): specific file:line with fix
```

### Security (Phase 2 - If Flagged)

```markdown
## Task for Security Subagent

{PLATFORM CONTEXT BLOCK}

**Story:** {story.id} - {story.title}
**Files Changed:** {list of security-sensitive files}
**Security Concerns:** {specific areas to review}

---

### Requirements:
1. Check OWASP Top 10 compliance
2. Review authentication/authorization logic
3. Check input validation and output encoding
4. Verify secure data handling
5. Check for security-related `platform.antiPatterns`
6. Return SECURE or NEEDS_REMEDIATION

### Output Format:
- Verdict: SECURE or NEEDS_REMEDIATION
- OWASP checklist results
- Vulnerabilities found (if any): CWE reference, file:line, fix
```

### DevOps (Phase 3)

```markdown
## Task for DevOps Subagent

{PLATFORM CONTEXT BLOCK}

**Implemented Features:**
{Summary of all completed stories}

**Files Changed:**
{Full list of changed files}

---

### Requirements:
1. Create/update CI/CD configuration using `platform.commands`
2. Update deployment configuration if needed
3. Ensure all environment variables documented
4. Verify security checklist
5. Document deployment steps

### Output Format:
- Infrastructure changes made
- CI/CD configuration
- Environment variables needed
- Deployment steps
- Rollback plan
```

---

## Loop Control Patterns

### Inner Loop: Story Iteration

```python
MAX_RETRIES = 3

def execute_story(story):
    iteration = 0
    previous_failures = []

    while story.status != 'completed' and iteration < MAX_RETRIES:
        iteration += 1

        # Build retry context for developer
        retry_context = {
            'iteration': iteration,
            'max_retries': MAX_RETRIES,
            'previous_failures': previous_failures,
            'files_changed': get_story_files(story)
        }

        # DEVELOP
        dev_result = invoke_developer(story, retry_context)
        if dev_result.build_failed:
            previous_failures.append({
                'phase': 'build',
                'error': dev_result.error,
                'files': dev_result.files
            })
            continue  # RETRY from developer

        # TEST
        test_result = invoke_tester(story, dev_result.files)
        if test_result.verdict == 'FAIL':
            previous_failures.append({
                'phase': 'test',
                'issues': test_result.issues,
                'coverage': test_result.coverage
            })
            continue  # RETRY from developer

        # REVIEW
        review_result = invoke_reviewer(story, dev_result.files)
        if review_result.verdict == 'CHANGES_REQUESTED':
            previous_failures.append({
                'phase': 'review',
                'changes': review_result.required_changes
            })
            continue  # RETRY from developer

        # SECURITY (if needed)
        if story.is_security_sensitive:
            security_result = invoke_security(story, dev_result.files)
            if security_result.verdict == 'NEEDS_REMEDIATION':
                previous_failures.append({
                    'phase': 'security',
                    'vulnerabilities': security_result.vulnerabilities
                })
                continue  # RETRY from developer

        # SUCCESS - story complete
        story.status = 'completed'
        commit_story(story)
        return True

    # Max retries exceeded
    escalate_blocker(story, previous_failures)
    return False
```

### Middle Loop: All Stories

```python
def execute_all_stories():
    while True:
        incomplete = get_incomplete_stories()
        if not incomplete:
            break  # All done!

        story = incomplete[0]  # Next story
        success = execute_story(story)

        if not success:
            # Story blocked - check if we should continue
            if should_skip_blocked():
                continue
            else:
                return False  # Workflow blocked

        # Progress checkpoint every 3 stories
        completed_count = get_completed_count()
        if completed_count % 3 == 0:
            generate_progress_report()

    return True  # All stories complete
```

---

## State Commands Reference

```bash
# === INITIALIZATION ===
python .claude/core/state.py init "Goal description"

# === SESSION RECOVERY ===
python .claude/core/state.py recover
python .claude/core/state.py status

# === STORY MANAGEMENT ===
python .claude/core/state.py add-story "Title" --size M
python .claude/core/state.py add-story "Title" --size L --security

# === STATUS UPDATES ===
python .claude/core/state.py update-story S1 pending
python .claude/core/state.py update-story S1 in_progress
python .claude/core/state.py update-story S1 testing
python .claude/core/state.py update-story S1 review
python .claude/core/state.py update-story S1 completed

# === VERIFICATION CHECKS ===
python .claude/core/state.py verify S1 testsPass --passed
python .claude/core/state.py verify S1 testsPass --failed --details "3 tests failing"
python .claude/core/state.py verify S1 coverageMet --passed --details "87%"
python .claude/core/state.py verify S1 reviewApproved --passed
python .claude/core/state.py verify S1 securityCleared --passed

# === PROGRESS ===
python .claude/core/state.py status
python .claude/core/state.py progress --lines 20

# === COMPLETION ===
python .claude/core/state.py complete
```

---

## Pull Request Creation

### PR Command

```bash
gh pr create --title "[Feature] {Goal Summary}" --body "$(cat <<'EOF'
## Summary
{1-2 sentence description}

## Stories Implemented
| ID | Title | Iterations |
|----|-------|------------|
| S1 | {title} | {n} |
| S2 | {title} | {n} |

## Key Changes
- {change 1}
- {change 2}
- {change 3}

## Testing
- **Tests:** {total} tests, all passing
- **Coverage:** Meets thresholds (S: 70%, M: 80%, L: 85%, XL: 90%)

## Verification
- [x] All acceptance criteria verified by tester agent
- [x] Code review approved by reviewer agent
- [x] Security review passed (if applicable)
- [x] Build and lint pass

## Workflow Metrics
- **Total Runtime:** {hours}h {minutes}m
- **Stories Completed:** {n}/{total}
- **Total Iterations:** {sum of all story iterations}

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### PR Troubleshooting

| Issue | Solution |
|-------|----------|
| `gh: command not found` | Install: https://cli.github.com/ |
| `not authenticated` | Run: `gh auth login` |
| `no remote configured` | Run: `git remote add origin <url>` |
| `branch doesn't exist on remote` | Run: `git push -u origin HEAD` first |

---

## Completion Marker

When workflow is complete, output this exact marker:

```markdown
## WORKFLOW_COMPLETE

**Goal:** {original goal}
**Status:** SUCCESS
**PR:** {pr_url}
**Runtime:** {total elapsed time}
**Stories:** {completed}/{total}
**Iterations:** {total iterations across all stories}

All stories verified. Pull request created. Workflow complete.
```

This marker signals that the workflow has finished successfully.

---

## Error Handling

### Escalation Triggers

| Condition | Action |
|-----------|--------|
| 3 failed iterations on story | Stop story, log blocker, ask user |
| Security vulnerability found | Immediate escalation |
| Build environment broken | Log and escalate |
| External dependency unavailable | Log and escalate |
| Unclear requirements | Ask clarifying question |

### Blocker Log Format

```markdown
## BLOCKER: {story.id}

**Story:** {title}
**Attempts:** 3/3

### Failure History:
1. **Iteration 1:** {phase} - {error summary}
2. **Iteration 2:** {phase} - {error summary}
3. **Iteration 3:** {phase} - {error summary}

### Root Cause Analysis:
{Analysis of why iterations failed}

### Recommended Action:
{Suggestion for user}

---
User intervention required. Respond with guidance or "skip" to continue with other stories.
```
