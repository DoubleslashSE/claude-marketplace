# Multi-Agent Autonomous Workflow

This project implements Anthropic's best practices for long-running autonomous agents using Claude Code's extension system (subagents, skills, hooks, and commands).

## Quick Commands

```bash
# Workflow Management
/workflow [goal]                              # Start full autonomous workflow
/status                                       # Check current progress
/implement [story]                            # Implement single story
/review [files]                               # Run code review

# State Management
python .claude/hooks/state.py status          # View workflow state
python .claude/hooks/state.py recover         # Session recovery info
python .claude/hooks/state.py progress        # Recent progress log

# Development
dotnet build                                  # Build solution
dotnet test                                   # Run all tests
dotnet test --filter "FullyQualifiedName~TestName"  # Run specific test
```

## Session Recovery Protocol

Run these at the START of every session per Anthropic best practices:

```bash
pwd                                           # Verify working directory
python .claude/hooks/state.py recover         # Get recovery context
python .claude/hooks/state.py progress --lines 15  # Recent progress
git log --oneline -5                          # Recent commits
git status                                    # Uncommitted changes
```

## Architecture

**Clean Architecture with CQRS pattern:**

```
src/
├── Core/           # Domain entities, interfaces (zero dependencies)
├── Application/    # Commands, Queries, Handlers, Validators
├── Infrastructure/ # EF Core, external services
└── Api/            # Controllers, DTOs, middleware

tests/
├── Core.Tests/
├── Application.Tests/
└── Integration.Tests/
```

**Dependency Rule:** Dependencies flow inward only. Core has no external dependencies.

## Conventions

### Naming
- **Tests:** `{MethodName}_{Scenario}_{ExpectedResult}`
- **Commands:** `{Action}{Entity}Command` (e.g., `CreateAuctionCommand`)
- **Queries:** `{Action}{Entity}Query` (e.g., `GetAuctionByIdQuery`)
- **Handlers:** `{Command/Query}Handler`

### Git
- **Branches:** `feature/S{n}-{short-description}`
- **Commits:** `type: description` where type is feat/fix/refactor/test/docs/chore
- **Message format:**
  ```
  type: short description

  - Detail 1
  - Detail 2

  Generated with [Claude Code](https://claude.com/claude-code)
  ```

### Code Style
- Use `CancellationToken` in all async methods
- Use `AsNoTracking()` for read-only queries
- Validate at boundaries (commands, API input)
- No `async void` except event handlers
- No string concatenation for SQL

## Workflow Integration

This project uses a multi-agent autonomous workflow with specialized subagents:

| Agent | Purpose | When Invoked |
|-------|---------|--------------|
| analyst | Break goals into testable user stories | Phase 1 |
| architect | Technical design decisions | Phase 1 |
| developer | TDD implementation | Phase 2 |
| tester | Verify acceptance criteria | Phase 2 |
| reviewer | Code quality review | Phase 2 |
| security | Security audit (sensitive stories) | Phase 2 |
| devops | Infrastructure & deployment | Phase 3 |

### Story Lifecycle

```
pending → in_progress → testing → review → verified → completed
              ↑                              │
              └──────── (on failure) ────────┘
```

Stories must pass ALL verification checks before completion:
- `testsPass` - All tests pass
- `coverageMet` - Coverage threshold met (S=70%, M=80%, L=85%, XL=90%)
- `reviewApproved` - Code review approved
- `securityCleared` - Security review passed (if security-sensitive)

## Safety Hooks

The following operations are protected by `.claude/hooks/safety.py`:

**Auto-blocked:** `rm -rf /`, `DROP DATABASE`, `force push`, destructive commands
**Requires confirmation:** `git push`, `dotnet ef database update`, deployments
**Protected files:** `.env`, `credentials.json`, `secrets.json`

## Known Issues & Quirks

- EF Core migrations require `dotnet ef` CLI tool installed
- Test coverage reports need `coverlet` collector
- Some integration tests require local database connection

## Environment Setup

Run the initialization script before starting work:

```bash
./.claude/init.sh
```

Or manually:
```bash
dotnet restore
dotnet build
dotnet test
```

## Lessons Learned

See `.claude/lessons-learned.md` for accumulated insights from previous workflow runs.

## References

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
