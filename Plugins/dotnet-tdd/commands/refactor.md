---
description: REFACTOR phase - Improve code design while keeping tests green
---

# REFACTOR Phase - Improve Design

Improve the code design for: **$ARGUMENTS**

## Your Task

1. **Identify Improvements**
   - Code smells
   - Principle violations
   - Duplication
   - Complexity

2. **Apply Refactorings**
   - One change at a time
   - Run tests after each change
   - Keep tests GREEN

3. **Verify Quality**
   - All tests still pass
   - Code is cleaner
   - Principles followed

## Principles Checklist

### SOLID
- [ ] **S**ingle Responsibility - One reason to change
- [ ] **O**pen/Closed - Extensible without modification
- [ ] **L**iskov Substitution - Subtypes substitutable
- [ ] **I**nterface Segregation - Specific interfaces
- [ ] **D**ependency Inversion - Depend on abstractions

### Clean Code
- [ ] **DRY** - No duplication
- [ ] **KISS** - Simple solutions
- [ ] **YAGNI** - No unused code
- [ ] **CQS** - Separated commands/queries

## Common Refactorings

| Refactoring | When to Apply |
|-------------|---------------|
| Extract Method | Long methods, repeated code |
| Rename | Unclear naming |
| Extract Interface | Concrete dependencies |
| Replace Conditional | Switch statements |
| Extract Class | Mixed responsibilities |

## REFACTOR Rules

1. **Tests stay GREEN** - Never break tests
2. **Small steps** - One change at a time
3. **Run tests often** - After every change
4. **Commit frequently** - Preserve progress

## Commands

```bash
# Run tests
dotnet test

# Format code
dotnet format

# Check coverage
dotnet test /p:CollectCoverage=true
```

## Quality Gate Integration

### Refactoring with Quality Gate Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              REFACTOR PHASE WITH QUALITY GATE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ Identify │───▶│  Apply   │───▶│   Run    │                  │
│  │  Smells  │    │ Refactor │    │  Tests   │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│                                        │                        │
│                                        ▼                        │
│                                  Tests Pass?                    │
│                                   │      │                      │
│                                  NO      YES                    │
│                                   │       │                     │
│                            ┌──────┘       ▼                     │
│                            │       ┌──────────┐                 │
│                      Revert &      │  Review  │                 │
│                      Retry         │(/review) │                 │
│                                    └──────────┘                 │
│                                         │                       │
│                                         ▼                       │
│                                  Score >= 90%?                  │
│                                   │       │                     │
│                                  NO       YES                   │
│                                   │        │                    │
│                                   ▼        ▼                    │
│                             Process    COMPLETE                 │
│                             Feedback                            │
│                                   │                             │
│                                   └────────▶ Apply More ────┐   │
│                                              Refactorings   │   │
│                                                    │        │   │
│                                                    └────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Quality Gate Thresholds

| Category | Target | Weight |
|----------|--------|--------|
| SOLID Compliance | 90% | 30% |
| Clean Code (DRY/KISS/YAGNI) | 90% | 25% |
| Test Quality | 90% | 25% |
| CQS Compliance | 95% | 20% |

### Quality Gate Actions

| Score | Status | Action |
|-------|--------|--------|
| 90-100% | PASS | Refactoring complete |
| 75-89% | CONDITIONAL | User decides to continue or accept |
| Below 75% | FAIL | Must continue refactoring |

## Feedback Loop Process

### 1. Initial Refactoring
```bash
# Run tests first
dotnet test

# Apply refactoring
# (make code changes)

# Verify tests still pass
dotnet test
```

### 2. Request Review
```bash
# Run code review to get quality scores
/dotnet-tdd:review {path}
```

### 3. Process Feedback
When review feedback is received:

```markdown
## Feedback Processing

### Review Scores Received
| Category | Score | Status |
|----------|-------|--------|
| SOLID | {X}% | {PASS/FAIL} |
| Clean Code | {X}% | {PASS/FAIL} |
| Test Quality | {X}% | {PASS/FAIL} |
| CQS | {X}% | {PASS/FAIL} |

### Issues to Address
| Issue ID | Principle | File:Line | Required Fix |
|----------|-----------|-----------|--------------|
| FIX-001 | {Principle} | {Location} | {Change} |

### Applying Fixes
For each issue:
1. Read the feedback carefully
2. Apply the suggested refactoring
3. Run tests: `dotnet test`
4. Mark issue as resolved
```

### 4. Re-Review
After applying fixes, request another review:
```bash
/dotnet-tdd:review {path}
```

### 5. Iterate Until Pass
Continue the cycle until:
- All quality scores >= 90%
- All tests pass

## Progress Tracking

Track refactoring progress across iterations:

```markdown
## Refactoring Progress

### Iteration History
| Cycle | SOLID | Clean | Tests | CQS | Overall | Status |
|-------|-------|-------|-------|-----|---------|--------|
| 1 | 60% | 70% | 75% | 80% | 68% | FAIL |
| 2 | 80% | 85% | 85% | 90% | 84% | CONDITIONAL |
| 3 | 95% | 92% | 95% | 100% | 94% | PASS |

### Refactorings Applied
- Cycle 1→2: Extracted 2 interfaces, removed duplication
- Cycle 2→3: Split god class, improved test naming

### Final Test Results
```bash
dotnet test
# All tests pass
```
```

## Output Required

Provide:
1. Identified code smells/violations
2. Refactorings applied (before/after)
3. Test results showing GREEN
4. Quality gate status with scores
5. Summary of improvements

### Complete Output Format

```markdown
## REFACTOR Phase Complete

### Code Smells Identified
- {Smell 1}: {Location}
- {Smell 2}: {Location}

### Refactorings Applied

#### Refactoring 1: {Type}
**Before** ({file}:{line}):
```csharp
{original code}
```

**After**:
```csharp
{refactored code}
```

### Test Results
```bash
dotnet test
# {X} tests passed, 0 failed
```

### Quality Gate
| Category | Score | Status |
|----------|-------|--------|
| SOLID | {X}% | ✅ |
| Clean Code | {X}% | ✅ |
| Test Quality | {X}% | ✅ |
| CQS | {X}% | ✅ |
| **Overall** | {X}% | ✅ PASS |

### Summary
- Review cycles: {count}
- Refactorings applied: {count}
- Quality improvement: {initial}% → {final}%
```
