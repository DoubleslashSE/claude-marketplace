# ADR format reference (MADR 4.0.0)

Architecture Decision Records capture *why* a choice was made — the context, the
options considered, and the consequences accepted. They live in `requirements/decisions/`
named `NNNN-kebab-case-title.md`, numbered sequentially from `0001`. The template is in
`assets/adr-template.md`.

## When to write one

Write an ADR when a decision is **architecturally significant**: costly to reverse,
constrains future work, picks among genuine alternatives, or future readers will ask
"why did we do it this way?" Choosing a database, an auth model, a sync-vs-async
boundary, a third-party integration, a data-retention policy — these earn ADRs.
Picking a variable name does not. When in doubt: if a reasonable engineer six months
from now would be confused or want to relitigate it, record it.

Don't edit accepted ADRs to change the decision. ADRs are immutable history; if you
reverse a decision, write a new ADR that supersedes the old one (set the old one's
status to `superseded by ADR-NNNN`).

## Structure (MADR 4.0.0)

```markdown
# {short title of the decision}

- Status: {proposed | accepted | rejected | deprecated | superseded by ADR-NNNN}
- Date: {YYYY-MM-DD}
- Decision-makers: {who decided}
- Affected requirements: {REQ ids this decision shapes}

## Context and Problem Statement

Two or three sentences framing the problem and forces at play. Phrase it so the
decision feels necessary, ideally as a question.

## Decision Drivers

- {driver 1 — a force, concern, or constraint that the decision must respect}
- {driver 2}

## Considered Options

- {option 1}
- {option 2}
- {option 3}

## Decision Outcome

Chosen option: "{option}", because {justification — tie back to the drivers}.

### Consequences

- Good, because {benefit}
- Bad, because {cost or risk now accepted}
- Neutral, because {tradeoff}

### Confirmation

How we'll confirm the decision is implemented as intended (review, test, fitness
function, etc.).

## Pros and Cons of the Options

### {option 1}

- Good, because {…}
- Bad, because {…}

### {option 2}

- Good, because {…}
- Bad, because {…}

## More Information

Links, related ADRs, requirements affected, evidence, or revisit conditions.
```

The mandatory core is the title, status/date, **Context and Problem Statement**,
**Considered Options**, and **Decision Outcome**. The rest is valuable but can be
trimmed for a lightweight decision — keep the options and the reasoning, because an
ADR with only the chosen option (no alternatives) doesn't actually record a decision,
it records an assertion.

## Linking to requirements

An ADR and the requirements it shapes point at each other: list the requirement IDs
under "Affected requirements" in the ADR, and add the ADR's id to those requirements'
`decisions` field. This keeps the *what* (requirement) and the *why* (decision)
connected without duplicating one inside the other.
