# SRS structure reference (ISO/IEC/IEEE 29148:2018)

The `srs.md` is the readable rollup of the requirements repository, organized per
ISO/IEC/IEEE 29148 (the standard that succeeds IEEE 830). It is **generated from the
YAML in `reqs/`**, not authored separately — so requirement statements, IDs, and
verification criteria in the SRS always match the source of truth. The skeleton is in
`assets/srs-template.md`.

29148 distinguishes three document levels; pick the one that fits, or layer them:

- **StRS** — Stakeholder Requirements Specification: what stakeholders need.
- **SyRS** — System Requirements Specification: system-level requirements.
- **SRS** — Software Requirements Specification: software-level detail for design and test.

For most projects a single SRS that traces up to stakeholder needs is enough; the
`derived_from` links in the YAML already encode the level relationships.

## Section structure

```
1. Introduction
   1.1 Purpose                  — what this document specifies and for whom
   1.2 Scope                    — name the system, what it does and does not do
   1.3 Definitions, acronyms    — glossary; expand domain terms
   1.4 References               — source docs, standards, related specs
   1.5 Overview                 — how the rest of the document is organized

2. Overall Description
   2.1 Product perspective      — context, neighbouring systems, where this fits
   2.2 Product functions        — summary of major capabilities (the "what", not detail)
   2.3 User characteristics     — the roles and their relevant traits
   2.4 Constraints              — CON-* requirements: mandated tech, regulation, etc.
   2.5 Assumptions & dependencies — what's assumed true; what we rely on others for

3. Specific Requirements        — the detailed, verifiable requirements
   3.1 Functional requirements  — SW-FUN-* grouped by feature/capability
   3.2 External interfaces      — IF-*: user, hardware, software, comms interfaces
   3.3 Nonfunctional requirements — SW-NFR-* by quality attribute (performance,
                                    security, usability, reliability, …)
   3.4 Other constraints        — anything not covered above

4. Verification                 — for each requirement, the method and criterion by
                                  which it will be confirmed (pull from each req's
                                  `verification` block; a traceability table works well)

Appendix: Traceability          — the requirement DAG (embed traceability.mmd) and/or
                                  a table mapping stakeholder need → system → software
                                  requirement, so coverage is auditable both ways.
```

## Generation guidance

- Group requirements in §3 by capability/quality attribute, listing each with its ID,
  statement, priority, and status. Keep the ID visible — it's the anchor everything
  else references.
- §4 is where 29148's emphasis on verification shows: every requirement should appear
  with how it will be verified. A table (ID | statement | method | criterion) is
  readable and exposes any requirement still lacking verification.
- Embed or link `traceability.mmd` so a reader can see the derivation graph.
- Note the generation date and the validator status ("0 errors, 2 warnings") so a
  reader knows the document reflects a validated state of the repository.
- Order and grouping can be adapted to the project's information-management policy —
  29148 allows flexibility in arrangement as long as the normative content is present.
