# .NET Developer Plugin for Claude Code

A general-purpose .NET development workflow plugin with automated validation through build, test, and static analysis quality gates.

## Features

- **Development Workflow**: Implement features, fix bugs, refactor code
- **Automated Validation**: Build, test, and static analysis checks
- **Quality Gates**: Pass/fail criteria before committing
- **Fix Assistance**: Auto-fix common issues and guide manual fixes

## Comparison with dotnet-tdd

| Aspect | dotnet-developer | dotnet-tdd |
|--------|------------------|------------|
| Focus | General development | Test-first (TDD) |
| Validation | Build/Test/Lint | SOLID/DRY/KISS compliance |
| AI Review | No | Yes |
| Workflow | Implement → Validate | RED → GREEN → REFACTOR |

Use **dotnet-developer** for standard development workflows. Use **dotnet-tdd** when practicing strict test-driven development.

## Installation

```bash
claude --plugin-dir ./Plugins/dotnet-developer
```

## Commands

| Command | Description |
|---------|-------------|
| `/dotnet-developer:validate` | Run build, test, and static analysis |
| `/dotnet-developer:fix` | Auto-fix validation issues |
| `/dotnet-developer:develop {task}` | Full workflow with validation |
| `/dotnet-developer:build` | Quick build check only |

## Skills

### dotnet-build
Build configuration and error handling:
- Build commands and options
- Multi-project solutions
- Common error resolutions
- Package restoration

### dotnet-test
Test execution and diagnostics:
- Test filtering
- Code coverage
- Parallel execution
- CI/CD integration

### static-analysis
Code quality and linting:
- Built-in .NET analyzers
- EditorConfig configuration
- StyleCop, Roslynator
- dotnet format

### development-workflow
General development patterns:
- Feature implementation
- Bug fixing
- Refactoring
- .NET patterns and practices

## Agents

| Agent | Role |
|-------|------|
| `developer` | Implements features, fixes, refactoring |
| `validator` | Executes build/test/analysis gates |
| `fixer` | Auto-fixes and guides manual fixes |

## Quality Gates

| Gate | Pass Condition | Blocking |
|------|----------------|----------|
| Build | 0 errors | Yes |
| Tests | 100% pass rate | Yes |
| Critical Warnings | 0 | No |
| Total Warnings | < 10 | No |

### Status

- **PASS**: All blocking gates pass, no critical warnings
- **CONDITIONAL**: Blocking gates pass, some warnings exist
- **FAIL**: Any blocking gate fails

## Workflow

```
┌──────────────┐
│  Understand  │
└──────────────┘
       │
       ▼
┌──────────────┐
│  Implement   │
└──────────────┘
       │
       ▼
┌──────────────┐
│   Validate   │──── FAIL ───▶ Fix ──┐
└──────────────┘                     │
       │                             │
      PASS                           │
       │                             │
       ▼                             │
┌──────────────┐                     │
│ Ready to     │◀────────────────────┘
│ Commit       │
└──────────────┘
```

## Usage Examples

```bash
# Validate before committing
/dotnet-developer:validate

# Fix validation issues
/dotnet-developer:fix

# Implement a feature with validation
/dotnet-developer:develop Add user authentication endpoint

# Quick build check
/dotnet-developer:build
```

## Best Practice: Validate Before Commit

Always run validation before committing:

```bash
# Full validation
dotnet build --no-incremental && \
dotnet test --no-build && \
dotnet format --verify-no-changes

# Or use the command
/dotnet-developer:validate
```

## Directory Structure

```
dotnet-developer/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── developer.md
│   ├── validator.md
│   └── fixer.md
├── commands/
│   ├── develop.md
│   ├── validate.md
│   ├── fix.md
│   └── build.md
├── hooks/
│   └── hooks.json
├── skills/
│   ├── dotnet-build/
│   │   ├── SKILL.md
│   │   └── common-errors.md
│   ├── dotnet-test/
│   │   ├── SKILL.md
│   │   └── test-filtering.md
│   ├── static-analysis/
│   │   ├── SKILL.md
│   │   └── analyzers.md
│   └── development-workflow/
│       ├── SKILL.md
│       └── patterns.md
└── README.md
```

## License

MIT
