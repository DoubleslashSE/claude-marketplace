---
name: requirements-engineering
description: >-
  Interactively elicit, capture, and maintain software/system requirements as a
  living, traceable repository. Use whenever the user wants to gather, write,
  refine, or organize requirements — including producing or updating an SRS
  (software/system requirements specification), writing ADRs / architecture
  decision records, building a requirements traceability graph (DAG), or keeping a
  decision ledger. Trigger proactively when the working folder already holds
  requirements artifacts (a `requirements/` folder of YAML, `decisions/` ADRs, an
  `srs.md`, or `ledger.md`), or when the user shares documents that are clearly
  specs, RFCs, or feature briefs and wants them structured. Also use for phrases
  like "let's spec this out", "interview me about what we're building", "capture
  these requirements", "write a decision record", or "turn these notes into a spec".
  Not for project management, code review, application code, dependency manifests
  like requirements.txt, or hardware "system requirements" (RAM/CPU).
---

# Requirements Engineering

This skill turns the messy, iterative work of figuring out *what to build* into a
durable, queryable artifact set. The goal is a **living requirements repository**:
every requirement is atomic, uniquely identified, verifiable, and traceable to the
need it came from and the decisions that shaped it. Nothing is captured as prose
that should be captured as structure.

The work is fundamentally **iterative and conversational**. You are not filling in
a form once. You interview the human in focused batches, write artifacts as you go,
and resume from wherever the repository currently stands the next time. Treat the
repository — not the chat — as the source of truth.

## The artifact set

Everything lives in a `requirements/` working tree (create it in the user's folder
if it doesn't exist; adapt to an existing layout if one is already there):

```
requirements/
├── srs.md                # Human-readable spec, generated/maintained from the YAML. 29148 structure.
├── reqs/                 # One YAML file per requirement, named <ID>.yaml. The source of truth.
│   ├── STK-001.yaml
│   ├── SYS-001.yaml
│   └── SW-FUN-001.yaml
├── decisions/            # ADRs in MADR format, named NNNN-kebab-title.md
│   └── 0001-use-postgres.md
├── ledger.md             # Append-only audit log of every material change.
└── traceability.mmd      # Generated Mermaid DAG of the derivation/dependency graph.
```

Why this shape: the YAML in `reqs/` is structured so the graph and the SRS can both
be **generated and validated** rather than hand-maintained and drifting. The ledger
gives an audit trail standards bodies and reviewers expect. The ADRs capture the
*why* behind choices that requirements alone don't explain.

## Workflow

### Step 0 — Orient before asking anything

Look at the working folder first. Read `scripts/validate_requirements.py`'s output
or just list the tree. Determine which situation you're in:

- **Greenfield** — no artifacts yet. You'll establish scope, then interview from the
  top of the graph (stakeholder needs) downward.
- **Existing repository** — `requirements/` already has content. Load it, run the
  validator to see open gaps and conflicts, and resume. Summarize the current state
  back to the user ("You have 23 requirements; 4 are unverifiable, 2 have no parent,
  1 dependency cycle") before asking what they want to work on.
- **Source documents to ingest** — the user dropped in a spec, RFC, brief, or notes.
  Read them, extract candidate requirements into the schema, flag what's ambiguous
  or missing, *then* interview to fill the gaps. Don't silently invent details.

Tell the user which situation you detected and what you propose to do next. Then go.

### Step 1 — Interview in focused batches

This is the core skill. Read `references/interview-playbook.md` for the question
banks organized by area (scope & goals, stakeholders, functional capabilities, data,
interfaces & integrations, quality attributes, constraints, assumptions, acceptance,
risks).

How to run it:

- Ask **2–4 related questions at a time** from one area, so the human can hold the
  context and answer well. A wall of 30 questions gets shallow answers.
- Be **adaptive**: when an answer is clear, move on; when an answer reveals ambiguity,
  risk, or a hidden assumption, drill into that one thread before broadening again.
  Following the interesting thread is where real requirements get found.
- Reflect answers back as **draft requirement statements** ("So: *The system shall
  notify the assigned technician within 5 minutes of a job being created.* Is the
  5-minute bound real, or a placeholder?"). This surfaces vagueness immediately and
  is how you turn opinions into verifiable requirements.
- Capture decisions and their rationale as they come up — if the human chooses
  between real alternatives for an architecturally significant reason, that's an ADR
  (see Step 4), not just a requirement.

Don't interrogate endlessly. After each batch, **write the artifacts** (Step 2),
then continue. The human should see the repository growing, not just answer questions
into a void.

### Step 2 — Write requirements as structured YAML

Each requirement is one file in `reqs/`. Read `references/requirement-schema.md` for
the full field reference and `assets/requirement.schema.json` for the validated
schema. The essentials:

```yaml
id: SW-FUN-001                 # unique, typed prefix (see schema)
title: Notify technician on job creation
type: functional               # functional | nonfunctional | constraint | interface | stakeholder | system
statement: >-
  The system shall notify the assigned technician within 5 minutes of a job
  being created.
rationale: Technicians miss SLA windows when notifications are delayed.
priority: must                 # must | should | could | wont (MoSCoW)
status: proposed               # proposed | accepted | implemented | verified | deprecated
source: Interview 2026-06-18, ops lead
derived_from: [SYS-004]        # parent requirement(s) — edges UP the DAG
depends_on: []                 # sibling requirements this one needs — edges across the DAG
verification:
  method: test                 # test | analysis | inspection | demonstration
  criterion: >-
    Create a job; assert a notification is delivered to the assignee in <5 min.
decisions: []                  # ADR ids that shaped this requirement
tags: [notifications, sla]
```

The rules that make requirements *good* (and that the validator enforces):

- **Atomic** — one testable obligation per requirement. "The system shall do X and Y"
  is two requirements. Splitting is what makes traceability and verification possible.
- **Verifiable** — if you can't state how you'd confirm it's met, it's a goal, not a
  requirement. Every functional and nonfunctional requirement needs a `verification`
  block. "Fast", "user-friendly", "robust" must become measurable fit criteria.
- **Uniquely identified** — IDs never change once assigned and never get reused, even
  after deprecation. Other artifacts and the ledger point at them.
- **Traceable** — `derived_from` links a requirement to the higher-level need it
  satisfies. This is what builds the DAG and lets you answer "why does this exist?"
  and "what breaks if we drop this?"

### Step 3 — Maintain the traceability DAG

The graph is implicit in the `derived_from` and `depends_on` links — you don't draw
it by hand. After writing or changing requirements, run the validator:

```bash
python scripts/validate_requirements.py requirements/reqs --mermaid requirements/traceability.mmd
```

It checks ID uniqueness and format, flags dangling links, **detects cycles** (the
graph must stay acyclic — a requirement can't ultimately derive from itself),
warns about orphans (non-stakeholder requirements with no parent) and unverifiable
requirements, and regenerates the Mermaid graph. Surface its findings to the user;
don't just run it silently. A clean validation run is a quality gate before you
consider an area "done".

### Step 4 — Record decisions as ADRs

When the human makes an architecturally significant choice — one that's costly to
reverse, constrains future work, or picks among real alternatives for a real reason —
capture it as an ADR in `decisions/`, numbered sequentially. Use the MADR 4.0.0
format in `references/adr-format.md` (template in `assets/adr-template.md`). Link the
ADR from the requirements it affects via their `decisions` field, and link back from
the ADR to those requirement IDs. The ADR explains the *why* that the requirement
statement deliberately leaves out.

### Step 5 — Append to the ledger

Every material change — new requirement, status change, deprecation, accepted ADR —
gets one line appended to `ledger.md` (never edit or delete past entries; that's the
point of a ledger):

```
| 2026-06-18 | added    | SW-FUN-001 | New: notify technician on job creation | Interview w/ ops lead |
| 2026-06-18 | accepted | ADR-0001   | Chose PostgreSQL over DynamoDB         | See decisions/0001    |
```

### Step 6 — Generate / refresh the SRS

The `srs.md` is the readable rollup, organized per ISO/IEC/IEEE 29148 (Introduction →
Overall Description → Specific Requirements → Verification). It's generated *from* the
YAML, not authored independently, so it never drifts. Read
`references/srs-structure.md` for the section guide and `assets/srs-template.md` for
the skeleton. Regenerate it when the user wants a document to share, or at the end of
a working session.

### Step 7 — Close the session

End by summarizing what changed, what the validator says, and the open threads worth
picking up next time (unanswered questions, unverifiable requirements, areas not yet
covered). Because the repository is the source of truth, the next session — yours or
a colleague's — can resume cleanly from Step 0.

## A note on judgment

Standards give you structure, not substance. The value you add is pushing vague
wishes into atomic, verifiable, traceable statements and noticing what the human
*hasn't* said — the unstated assumption, the missing error case, the quality
attribute nobody mentioned, the requirement with no way to test it. Be the diligent
interviewer who keeps asking "how would we know this is met?" without becoming a
bureaucrat who buries a small project in ceremony. Scale the rigor to the project.
                                                                                                             