---
description: Auto-fix validation issues (build errors, test failures, analyzer warnings)
---

# Fix Validation Issues

Fix issues from: **$ARGUMENTS**

## Fix Process

### Step 1: Identify Issues
Parse validation output to extract:
- Build errors (file, line, code, message)
- Test failures (test name, failure reason)
- Analyzer warnings (code, location, message)

### Step 2: Categorize by Fixability

| Category | Auto-Fixable | Method |
|----------|--------------|--------|
| Format violations | Yes | `dotnet format` |
| Simple analyzer warnings | Yes | `dotnet format analyzers` |
| Build errors | Partial | Code analysis and edit |
| Test failures | No | Analyze and guide |
| Complex warnings | Partial | Code edit or suppress |

### Step 3: Apply Fixes

**Auto-fixes:**
```bash
# Fix formatting
dotnet format

# Fix specific analyzers
dotnet format analyzers --diagnostics CA1062 IDE0044
```

**Code fixes applied directly:**
- Add null checks (CA1062)
- Make fields readonly (IDE0044)
- Add using statements (CS0246)
- Fix dispose patterns (CA2000)

### Step 4: Re-validate
```bash
dotnet build --no-incremental
dotnet test --no-build
dotnet format --verify-no-changes
```

## Output Format

```markdown
## Fix Report

### Summary
| Metric | Value |
|--------|-------|
| Issues Found | X |
| Auto-Fixed | X |
| Manually Fixed | X |
| Remaining | X |
| Success Rate | X% |

### Fixes Applied
| Issue | Location | Fix |
|-------|----------|-----|
| CA1062 | Service.cs:23 | Added null check |
| IDE0044 | Model.cs:15 | Made field readonly |

### Remaining Issues
| Issue | Location | Guidance |
|-------|----------|----------|
| CS0103 | File.cs:45 | Check variable scope |

### Re-validation Results
| Gate | Before | After |
|------|--------|-------|
| Build | FAIL | PASS |
| Tests | 95% | 100% |
| Warnings | 15 | 3 |

### Next Steps
{Guidance based on remaining issues}
```

## Fix Strategies

### Build Errors
- CS0103: Check spelling, add using
- CS0246: Add package/project reference
- CS1061: Fix member name or interface

### Test Failures
- Assertion: Check expected vs actual
- Exception: Verify exception handling
- Null: Check setup and mocks

### Analyzer Warnings
- CA1062: Add ArgumentNullException.ThrowIfNull
- CA2000: Use 'using' statement
- IDE0044: Add 'readonly' modifier

## Usage

```
/dotnet-developer:fix                # Fix issues from last validation
/dotnet-developer:fix --auto-only    # Apply only auto-fixes
/dotnet-developer:fix --report X     # Fix issues from specific report
```
