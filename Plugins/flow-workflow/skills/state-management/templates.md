# State File Templates

## FLOW.md Template (Project-Level)

```markdown
# Flow Project State

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Project Type**: [detected type or "Not detected"]

## Vision

[High-level project vision statement - set during initialization or first item]

## Backlog

| ID | Name | Status | Priority | Progress |
|----|------|--------|----------|----------|
| ITEM-001 | [Title] | EXECUTE | P1 | 60% |
| ITEM-002 | [Title] | DISCUSS | P2 | 25% |
| ITEM-003 | [Title] | BACKLOG | P3 | 0% |

**Summary**: 1 executing, 1 discussing, 1 in backlog, 0 done

## Active Item

**Current**: ITEM-001
**Title**: [Work item title]
**Phase**: EXECUTE (task 3/5)
**Started**: [TIMESTAMP]

## Capabilities Cache

**Last Scanned**: [TIMESTAMP]

| Capability | Matched Plugin | Agent/Command | Confidence |
|------------|----------------|---------------|------------|
| requirements-gathering | business-analyst | stakeholder-interviewer | High |
| tdd-implementation | dotnet-tdd | implementer | High |
| code-review | dotnet-tdd | reviewer | High |
| codebase-analysis | business-analyst | codebase-analyzer | Medium |
| brainstorming | workshop-facilitator | brainstorm | High |
| infrastructure | - | (use default) | - |

**Default Agents** (when no plugin matches):
- requirements-gathering → flow-workflow:defaults/interviewer
- codebase-analysis → flow-workflow:defaults/researcher
- code-implementation → flow-workflow:defaults/executor
- code-review → flow-workflow:validator

## Context Monitor

- Coordinator usage: [X]%
- Auto-spawn threshold: 50%
- Fresh agents spawned this session: [N]

## Quick Commands

- `/flow:go` - Continue from current state
- `/flow:status` - Show detailed status
- `/flow:start [name]` - Create/switch to item
- `/flow:backlog` - List all items
- `/flow:quick "task"` - Direct execution (no state)
```

## ITEM-XXX.md Template (Per-Item)

```markdown
# ITEM-001: [Work Item Title]

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Phase: EXECUTE (task 3/5)

**Phase Progress**: 60%
**Current Task**: TASK-003 - Implement validation logic

### Phase History

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| DISCUSS | [TS] | [TS] | 15m |
| PLAN | [TS] | [TS] | 10m |
| EXECUTE | [TS] | - | - |

## Decisions

### DEC-001: Authentication Method
**Made**: [TIMESTAMP]
**Phase**: DISCUSS
**Decision**: Use OAuth2 with Google/GitHub providers
**Rationale**: User preference for social login, reduces password management burden
**Alternatives Rejected**:
- Email/password: User didn't want to manage passwords
- Magic links: Requires email service setup

### DEC-002: Token Storage
**Made**: [TIMESTAMP]
**Phase**: DISCUSS
**Decision**: JWT stored in httpOnly cookies
**Rationale**: Better security than localStorage, CSRF protection via SameSite

## Requirements

### Functional

**FR-001**: User can authenticate via Google OAuth
- Priority: MUST
- Status: IMPLEMENTING
- Acceptance: User clicks "Sign in with Google" and is authenticated

**FR-002**: User can authenticate via GitHub OAuth
- Priority: MUST
- Status: PENDING
- Acceptance: User clicks "Sign in with GitHub" and is authenticated

**FR-003**: Session persists across browser refresh
- Priority: MUST
- Status: PENDING
- Acceptance: User remains logged in after page reload

### Non-Functional

**NFR-001**: Authentication completes in under 3 seconds
- Category: Performance
- Status: PENDING

## Tasks

<task id="TASK-001" status="completed">
  <name>Set up OAuth providers configuration</name>
  <description>Configure Google and GitHub OAuth credentials</description>
  <files>
    <file action="create">src/config/oauth.ts</file>
    <file action="modify">src/config/index.ts</file>
  </files>
  <actions>
    <action>Create OAuth configuration structure</action>
    <action>Add environment variable mappings</action>
  </actions>
  <verify>
    <step>npm run build</step>
    <step>Config exports correctly</step>
  </verify>
  <done>
    <criterion>OAuth config is importable</criterion>
  </done>
  <commit>feat(auth): add OAuth provider configuration</commit>
</task>

<task id="TASK-002" status="completed">
  <name>Create AuthService base class</name>
  <description>Implement core authentication service</description>
  <files>
    <file action="create">src/services/AuthService.ts</file>
  </files>
  <actions>
    <action>Create AuthService class</action>
    <action>Add login/logout methods</action>
    <action>Add token management</action>
  </actions>
  <verify>
    <step>npm test -- AuthService</step>
  </verify>
  <done>
    <criterion>AuthService tests pass</criterion>
  </done>
  <commit>feat(auth): implement AuthService with login/logout</commit>
</task>

<task id="TASK-003" status="in_progress">
  <name>Implement validation logic</name>
  <description>Add token validation and refresh</description>
  <files>
    <file action="modify">src/services/AuthService.ts</file>
  </files>
  <actions>
    <action>Add token validation</action>
    <action>Add token refresh logic</action>
  </actions>
  <verify>
    <step>npm test -- AuthService</step>
  </verify>
  <done>
    <criterion>Validation tests pass</criterion>
  </done>
  <commit>feat(auth): add token validation and refresh</commit>
</task>

<task id="TASK-004" status="pending">
  <name>Add Google OAuth integration</name>
  <depends>TASK-003</depends>
  ...
</task>

<task id="TASK-005" status="pending">
  <name>Add GitHub OAuth integration</name>
  <depends>TASK-003</depends>
  ...
</task>

### Task Progress

```
[====================----------] 60% (3/5 tasks)
TASK-001 ✓ → TASK-002 ✓ → TASK-003 ● → TASK-004 ○ → TASK-005 ○
```

## Checkpoint

**Timestamp**: [TIMESTAMP]
**Phase**: EXECUTE
**Task**: TASK-003 (in_progress)
**Context**: 32%

**Completed**:
- [x] OAuth configuration created
- [x] AuthService base implemented
- [x] Started validation logic

**Next Action**: Complete token validation in TASK-003, then run verification

**Resume Command**: `/flow:go` will continue from TASK-003

## Blockers

[No active blockers]

## Notes

- User prefers minimal UI during auth flow
- Consider rate limiting after MVP
```

## Minimal ITEM-XXX.md (For New Items)

```markdown
# ITEM-001: [Title]

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Phase: DISCUSS (0%)

Starting requirements exploration.

## Decisions

[No decisions yet - beginning DISCUSS phase]

## Requirements

[To be gathered during DISCUSS phase]

## Tasks

[To be created during PLAN phase]

## Checkpoint

**Timestamp**: [TIMESTAMP]
**Phase**: DISCUSS
**Progress**: 0%
**Next Action**: Begin requirements exploration with interviewer
```

## Quick Mode ITEM-XXX.md

```markdown
# ITEM-001: [Task Description]

**Created**: [TIMESTAMP]
**Mode**: QUICK

## Phase: EXECUTE (0%)

**Task**: [task description]

## Quick Tasks

<task id="TASK-001" status="pending">
  <name>[task name]</name>
  <files>
    <file action="[action]">[path]</file>
  </files>
  <actions>
    <action>[action]</action>
  </actions>
  <verify>
    <step>[verification]</step>
  </verify>
  <commit>[commit message]</commit>
</task>

## Checkpoint

**Phase**: EXECUTE
**Task**: TASK-001
**Next**: Execute task and verify
```
