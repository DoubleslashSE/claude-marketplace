---
description: Execute complete TDD cycle (RED-GREEN-REFACTOR) for implementing a feature with integrated feedback loops
---

# TDD Workflow

Execute the complete TDD cycle for: **$ARGUMENTS**

## TDD Feedback Loop Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TDD WITH FEEDBACK LOOPS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ RED PHASE                                                │   │
│  │  Design Test → Run → Fails for RIGHT reason?             │   │
│  │       ▲                        │                         │   │
│  │       └──── NO: Adjust test ───┘                         │   │
│  │                    YES ↓                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ GREEN PHASE                                              │   │
│  │  Implement → Run → All tests pass?                       │   │
│  │       ▲                    │                             │   │
│  │       └──── NO: Fix impl ──┘                             │   │
│  │                   YES ↓                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ REFACTOR PHASE (with Quality Gate)                       │   │
│  │  Refactor → Review → Score >= 90%?                       │   │
│  │       ▲                    │                             │   │
│  │       └──── NO: Apply ─────┘                             │   │
│  │             feedback                                     │   │
│  │                   YES ↓                                  │   │
│  │                 COMPLETE                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Steps

### Phase 1: RED - Design Tests (with Feedback Loop)

```
Design → Run → Analyze → Adjust (if needed) → Confirm RED
```

1. Analyze the feature requirements
2. Identify test scenarios (happy path, edge cases, errors)
3. Write failing tests following AAA pattern
4. **Run tests and verify they fail**
5. **Feedback Check**: Does it fail for the RIGHT reason?
   - YES → Proceed to GREEN
   - NO → Adjust test and re-run

**Exit Criteria**: Test fails for the correct reason

### Phase 2: GREEN - Implement (with Feedback Loop)

```
Implement → Run → Analyze Failures → Fix → Re-run → Confirm GREEN
```

1. Write minimal code to pass ONE failing test
2. **Run tests**
3. **Feedback Check**: Does test pass?
   - YES → Next test or proceed to REFACTOR
   - NO → Analyze failure feedback, fix implementation, re-run
4. Repeat for each failing test
5. Do NOT optimize yet

**Exit Criteria**: All tests pass (GREEN state)

### Phase 3: REFACTOR - Improve (with Quality Gate)

```
Refactor → Review → Process Feedback → Apply Fixes → Re-review → Quality Gate
```

1. **Run code review** (`/dotnet-tdd:review`)
2. **Receive feedback** with quality scores
3. **Quality Gate Check**:
   - Score >= 90%: PASS → Complete
   - Score 75-89%: CONDITIONAL → User decides
   - Score < 75%: FAIL → Must apply feedback
4. **Process feedback**:
   - Apply suggested refactorings
   - Run tests after EACH change
   - Verify tests stay GREEN
5. **Re-review** until quality gate passes

**Exit Criteria**: Quality score >= 90% AND all tests pass

## Quality Gate Scores

| Category | Target | Weight |
|----------|--------|--------|
| SOLID Compliance | 90% | 30% |
| Clean Code (DRY/KISS/YAGNI) | 90% | 25% |
| Test Quality | 90% | 25% |
| CQS Compliance | 95% | 20% |

## Feedback Processing

### RED Phase Feedback
- Test passes unexpectedly → Strengthen assertions
- Wrong failure type → Adjust test setup
- Missing edge cases → Add more tests

### GREEN Phase Feedback
- Test fails → Analyze error, implement fix
- Multiple failures → Fix one at a time
- Compilation error → Fix syntax/types

### REFACTOR Phase Feedback
- SOLID violations → Apply specific refactorings
- DRY violations → Extract common code
- Test quality issues → Split/rename tests

## Test Naming Convention
```
{MethodUnderTest}_{Scenario}_{ExpectedBehavior}
```

## Commands Available
```bash
# Run all tests
dotnet test

# Run specific test
dotnet test --filter "FullyQualifiedName~{TestName}"

# Run with coverage
dotnet test /p:CollectCoverage=true

# Run code review
/dotnet-tdd:review {path}
```

## Principles to Follow

### TDD
- Tests first, implementation second
- One test at a time
- Refactor only with green tests
- **Iterate until quality gate passes**

### SOLID
- **S**: Single Responsibility
- **O**: Open/Closed
- **L**: Liskov Substitution
- **I**: Interface Segregation
- **D**: Dependency Inversion

### Clean Code
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple
- **YAGNI**: You Aren't Gonna Need It
- **CQS**: Command Query Separation

## Output Expected

Provide a summary after completing the TDD cycle:

```markdown
## TDD Cycle Complete

### RED Phase
- Tests designed: {count}
- Scenarios covered: Happy path, edge cases, errors
- All tests fail for correct reasons: ✅

### GREEN Phase
- Tests passing: {count}/{total}
- Implementation files: {list}
- Iterations to pass: {count}

### REFACTOR Phase
- Review cycles: {count}
- Initial score: {X}%
- Final score: {Y}%
- Refactorings applied: {list}

### Quality Scores
| Category | Score | Status |
|----------|-------|--------|
| SOLID | {X}% | ✅ |
| Clean Code | {X}% | ✅ |
| Test Quality | {X}% | ✅ |
| CQS | {X}% | ✅ |
| **Overall** | {X}% | ✅ PASS |

### Final Test Results
```bash
dotnet test
# {X} tests passed, 0 failed
```
```
