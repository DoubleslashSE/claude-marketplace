---
description: Run all validations (build, test, static analysis) and generate quality report
---

# Validate .NET Project

Validate: **$ARGUMENTS**

## Validation Steps

### 1. Build Validation
Execute a clean build to catch all compilation errors:
```bash
dotnet build --no-incremental
```

### 2. Test Validation
Run all tests to verify behavior:
```bash
dotnet test --no-build --logger "console;verbosity=detailed"
```

### 3. Static Analysis
Check code quality and formatting:
```bash
dotnet format --verify-no-changes
```

## Quality Gates

| Gate | Pass Condition | Blocking |
|------|----------------|----------|
| Build | 0 errors | Yes |
| Tests | 100% pass rate | Yes |
| Critical Warnings | 0 critical warnings | No |
| Total Warnings | < 10 warnings | No |

## Status Determination

- **PASS**: All blocking gates pass, no critical warnings
- **CONDITIONAL**: Blocking gates pass, some non-critical warnings
- **FAIL**: Any blocking gate fails

## Output Format

Generate a structured validation report:

```markdown
## Validation Report

### Summary
| Metric | Value |
|--------|-------|
| Build Status | PASS/FAIL |
| Test Status | PASS/FAIL (X/Y) |
| Analysis Status | PASS/WARN |
| **Overall** | **PASS/CONDITIONAL/FAIL** |
| **Score** | **X%** |

### Build Results
{Build output and any errors}

### Test Results
{Test results with pass/fail per test}

### Static Analysis
{Warnings and issues found}

### Quality Gates
| Gate | Target | Actual | Status |
|------|--------|--------|--------|
| Build | 0 errors | X | PASS/FAIL |
| Tests | 100% | X% | PASS/FAIL |
| Critical | 0 | X | PASS/FAIL |
| Warnings | <10 | X | PASS/WARN |

### Next Steps
- PASS: Ready to commit
- CONDITIONAL: Review warnings, decide to proceed
- FAIL: Run /dotnet-developer:fix or manually resolve
```

## Usage

```
/dotnet-developer:validate                    # Validate entire solution
/dotnet-developer:validate src/MyApp          # Validate specific project
/dotnet-developer:validate --build-only       # Build check only
```
