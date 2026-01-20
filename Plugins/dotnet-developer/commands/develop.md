---
description: Full development workflow with integrated validation - implement, validate, fix loop
---

# Develop Feature

Develop: **$ARGUMENTS**

## Development Workflow

```
┌──────────────┐
│  Understand  │  Read requirements, explore codebase
└──────────────┘
       │
       ▼
┌──────────────┐
│  Implement   │  Write code following patterns
└──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Validate   │────▶│   Report     │
│ Build/Test/  │     │   Results    │
│   Analyze    │     │              │
└──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
  ┌─────────┐         ┌──────────┐
  │  PASS?  │───NO───▶│   Fix    │
  └─────────┘         │  Issues  │
       │              └──────────┘
       │                    │
      YES                   │
       │                    │
       ▼                    │
┌──────────────┐           │
│   Ready to   │◀──────────┘
│    Commit    │
└──────────────┘
```

## Phase 1: Understand

1. **Read the task requirements**
2. **Explore the codebase** to find:
   - Affected files and components
   - Existing patterns to follow
   - Related tests
3. **Plan the implementation approach**

## Phase 2: Implement

1. **Follow existing patterns** in the codebase
2. **Make small, incremental changes**
3. **Build frequently** to catch errors early

### Code Standards
- Naming: PascalCase classes, camelCase params, _camelCase fields
- Structure: Fields → Constructor → Public → Private
- Async: Use async suffix, await properly
- Errors: Guard clauses, specific exceptions

## Phase 3: Validate

Run full validation:
```bash
dotnet build --no-incremental
dotnet test --no-build
dotnet format --verify-no-changes
```

### Quality Gates
| Gate | Requirement |
|------|-------------|
| Build | 0 errors |
| Tests | 100% pass |
| Analysis | No critical warnings |

## Phase 4: Fix (if needed)

If validation fails:
1. Fix build errors first (blocking)
2. Fix test failures second
3. Address warnings last

Use auto-fixes where possible:
```bash
dotnet format
dotnet format analyzers
```

## Phase 5: Complete

When all gates pass:
- Summarize changes
- List modified files
- Confirm ready to commit

## Output Format

```markdown
## Development Summary

### Task
{What was requested}

### Changes Made
| File | Change | Description |
|------|--------|-------------|
| path/File.cs | Modified | {Brief} |
| path/New.cs | Added | {Brief} |

### Key Changes
1. {Main change 1}
2. {Main change 2}

### Validation Results
| Gate | Status |
|------|--------|
| Build | PASS |
| Tests | PASS (X/Y) |
| Analysis | PASS (X warnings) |

### Ready to Commit
Yes/No
```

## Usage

```
/dotnet-developer:develop Add user authentication endpoint
/dotnet-developer:develop Fix null reference in OrderService
/dotnet-developer:develop Refactor payment processing
```
