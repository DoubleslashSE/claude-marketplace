# Use Case Templates

## Formal Use Case Template

Use this template to document detailed behavioral requirements that user stories alone cannot capture. Use cases are particularly valuable for complex interactions, multi-step workflows, and scenarios with many alternative/exception flows.

### When to Use Use Cases vs User Stories

| Use Cases | User Stories |
|-----------|-------------|
| Complex multi-step interactions | Simple, single-action features |
| Multiple actors or system interactions | Single user perspective |
| Many alternative/exception flows | Happy path is sufficient |
| Regulatory/audit requirements | Agile iteration planning |
| Safety-critical systems | General feature tracking |

## Use Case Template

```markdown
### UC-{XXX}: {Use Case Title}

| Attribute | Value |
|-----------|-------|
| **ID** | UC-{XXX} |
| **Name** | {Descriptive name} |
| **Primary Actor** | {Who initiates this use case} |
| **Secondary Actors** | {Other participants: systems, users, timers} |
| **Scope** | {System / Subsystem} |
| **Level** | {User Goal / Subfunction / Summary} |
| **Priority** | {Must / Should / Could} |
| **Status** | {Proposed / Confirmed / Approved} |
| **Related Requirements** | {FR-XXX, FR-YYY} |

#### Preconditions
1. {Condition that must be true before this use case starts}
2. {e.g., "User is authenticated and has Manager role"}

#### Postconditions (Success)
1. {State of the system after successful completion}
2. {e.g., "Order is saved with status 'Submitted'"}

#### Postconditions (Failure)
1. {State of the system if the use case fails}
2. {e.g., "No order is created; user is notified of error"}

#### Main Success Scenario (Happy Path)
| Step | Actor | Action |
|------|-------|--------|
| 1 | {Actor} | {Action taken} |
| 2 | System | {System response} |
| 3 | {Actor} | {Next action} |
| 4 | System | {System response} |

#### Alternative Flows

**{ALT-1}: {Alternative name}**
- Branches from: Step {N}
- Condition: {When this alternative applies}

| Step | Actor | Action |
|------|-------|--------|
| {N}a.1 | {Actor} | {Alternative action} |
| {N}a.2 | System | {System response} |

- Returns to: Step {M} / Ends use case

#### Exception Flows

**{EXC-1}: {Exception name}**
- Occurs at: Step {N}
- Trigger: {What causes this exception}

| Step | Actor | Action |
|------|-------|--------|
| {N}e.1 | System | {Error detection} |
| {N}e.2 | System | {Error notification to actor} |
| {N}e.3 | {Actor} | {Recovery action} |

- Result: {Returns to step N / Ends use case with failure}

#### Business Rules
- {BR-XXX}: {Business rule applied in this use case}

#### Special Requirements
- {Performance: must complete within X seconds}
- {Security: requires encryption}
- {Audit: must log all actions}

#### Frequency of Use
{How often this use case is expected to occur: e.g., "50 times per day"}

#### Open Issues
- {Unresolved question about this use case}
```

## Use Case Levels

### Summary Level (Cloud)
High-level business processes spanning multiple user goals:
- "Manage customer orders" (includes create, modify, cancel, fulfill)
- "Process monthly billing cycle"

### User Goal Level (Sea)
A single, complete goal a user wants to achieve in one session:
- "Place an order"
- "Generate monthly report"
- "Register new customer"

### Subfunction Level (Fish)
Supporting steps required by user-goal use cases:
- "Validate payment method"
- "Check inventory availability"
- "Send email notification"

## Use Case Diagram Elements

```
[System Boundary]
┌─────────────────────────────────┐
│                                 │
│   (Use Case 1)   (Use Case 2)  │
│        │              │         │
│        │    «include»  │        │
│        └──────┐       │         │
│               ▼       │         │
│         (Shared UC)   │         │
│                       │         │
│   (Use Case 3)───────┘         │
│        │   «extend»             │
│        ▼                        │
│   (Extension UC)                │
│                                 │
└─────────────────────────────────┘
     │              │
  [Actor A]    [Actor B]
```

### Relationships
- **Include**: Use case always includes another (mandatory sub-flow)
- **Extend**: Use case optionally extends another (conditional behavior)
- **Generalization**: Parent/child actor or use case inheritance

## Actor Identification Checklist

- [ ] Who starts/triggers this process?
- [ ] Who provides information to the system?
- [ ] Who receives information from the system?
- [ ] What external systems interact with this feature?
- [ ] Are there time-based triggers (schedulers, cron)?
- [ ] Are there event-based triggers (webhooks, messages)?

## Use Case Writing Guidelines

### DO
- Write in present tense, active voice
- Use actor names consistently (not "the user" one place and "customer" another)
- Number steps sequentially
- Keep each step as a single observable action
- Include system responses (the system is an actor too)
- Document both success and failure postconditions

### DON'T
- Include UI details (say "enters data" not "clicks the blue submit button")
- Include implementation details (say "system stores" not "system INSERTs into database")
- Write overly long scenarios (break into sub-use-cases if > 12 steps)
- Skip alternative and exception flows (these are where most bugs live)
- Assume the happy path is the only path
