# Requirement schema reference

Each requirement is a single YAML file in `requirements/reqs/`, named after its `id`
(e.g. `SW-FUN-001.yaml`). The validator (`scripts/validate_requirements.py`) enforces
the structural rules below; the JSON Schema in `assets/requirement.schema.json` is the
machine-checkable version.

## Fields

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Unique, immutable, never reused. Typed prefix + zero-padded number. See ID scheme below. |
| `title` | yes | Short imperative noun phrase. Human label, not the obligation itself. |
| `type` | yes | `stakeholder` \| `system` \| `functional` \| `nonfunctional` \| `interface` \| `constraint` |
| `statement` | yes | The actual obligation. Use "shall" for binding requirements. One obligation only. |
| `rationale` | recommended | Why this exists. Saves future readers from re-litigating it. |
| `priority` | yes | MoSCoW: `must` \| `should` \| `could` \| `wont` |
| `status` | yes | `proposed` \| `accepted` \| `implemented` \| `verified` \| `deprecated` |
| `source` | recommended | Where it came from — interview, stakeholder, source doc, regulation. |
| `derived_from` | conditional | List of parent requirement IDs (edges up the DAG). Required for every non-`stakeholder` requirement. |
| `depends_on` | optional | List of sibling requirement IDs this one needs to function. |
| `verification` | conditional | Required for `functional` and `nonfunctional`. Object with `method` and `criterion`. |
| `decisions` | optional | List of ADR IDs (e.g. `ADR-0003`) that shaped this requirement. |
| `conflicts_with` | optional | List of requirement IDs known to be in tension. Forces the conflict to be visible and resolved. |
| `tags` | optional | Free-form labels for slicing the set. |

### `verification` object

```yaml
verification:
  method: test            # test | analysis | inspection | demonstration
  criterion: >-
    A concrete, observable pass/fail condition. Numbers, not adjectives.
```

The four methods follow standard practice: **test** (execute and measure),
**analysis** (calculation/modelling), **inspection** (examine the artifact), and
**demonstration** (operate and observe). If you can't pick a method, the requirement
isn't verifiable yet — that's a finding to raise, not a field to skip.

## ID scheme

`<PREFIX>-<NNN>` where the prefix encodes the layer/type so the graph reads top-down:

- `STK-###` — stakeholder requirement / need (top of the graph, no parent)
- `SYS-###` — system requirement (derived from stakeholder needs)
- `SW-FUN-###` — software functional requirement
- `SW-NFR-###` — software nonfunctional requirement (quality attributes)
- `IF-###` — interface requirement
- `CON-###` — constraint

IDs are immutable once assigned. When a requirement dies, set `status: deprecated` —
never delete the file and never recycle the number, because the ledger and other
artifacts still point at it.

## The DAG (derivation + dependency graph)

The graph emerges from links, not hand-drawing:

- `derived_from` edges flow **up** the abstraction ladder: a `SW-FUN` derives from a
  `SYS` requirement, which derives from a `STK` need. This answers "why does this
  exist?" and "what higher need do we violate if we cut it?"
- `depends_on` edges flow **across** at the same level: requirement A needs B to be
  meaningful or implementable.

The combined graph must be **acyclic** — nothing may, through any chain, derive from
or depend on itself. The validator fails on cycles because a cycle means the
abstraction hierarchy is broken (two requirements each justifying the other is a sign
they should be merged, re-parented, or one reframed).

`stakeholder` requirements are the roots and legitimately have no `derived_from`.
Any other type with no parent is an **orphan** — usually a sign a need wasn't
captured. The validator warns on orphans so you can either add the missing parent or
reclassify.

## Example

```yaml
id: SW-NFR-002
title: Job list load time
type: nonfunctional
statement: >-
  The system shall render the technician's job list within 2 seconds at the
  95th percentile under a load of 500 concurrent users.
rationale: Technicians check the list dozens of times per shift on mobile data.
priority: should
status: proposed
source: Interview 2026-06-18, field ops manager
derived_from: [SYS-004]
depends_on: [SW-FUN-001]
verification:
  method: test
  criterion: >-
    Load test at 500 concurrent users; p95 render time of the job list endpoint
    is under 2000 ms across a 10-minute run.
decisions: [ADR-0002]
tags: [performance, mobile]
```
