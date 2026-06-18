# Interview playbook

Question banks for eliciting requirements, organized by area. These are prompts for
*you* — don't read them at the human like a checklist. Pull 2–4 relevant questions,
ask conversationally, follow the interesting threads, and reflect answers back as
draft requirement statements so vagueness surfaces immediately.

Work roughly top-down (scope → stakeholders → capabilities → qualities → constraints),
but jump around when an answer opens a thread worth chasing. The richest requirements
come from the follow-up question, not the first one.

## 1. Scope & goals (start here)

- What problem does this system solve, and for whom? What happens today without it?
- What does success look like in 6–12 months? How would you measure it?
- What is explicitly **out of scope** for this version? (Naming non-goals prevents scope creep and is itself a requirement.)
- What's the one capability that, if missing, makes the whole thing pointless?

## 2. Stakeholders & users

- Who are the distinct user roles? What's each one trying to accomplish?
- Who is affected but not a direct user (approvers, auditors, downstream systems, regulators)?
- Whose sign-off is needed, and what do they care about most?
- Are there users with accessibility, language, or device constraints?

## 3. Functional capabilities

- Walk me through the main workflow end to end. Where does it start and end?
- For each step: who triggers it, what's the input, what's the expected output?
- What are the alternative and error paths? What should happen when something goes wrong, times out, or arrives malformed?
- What state does the system remember between sessions? Who can change it?
- What's permitted vs forbidden — and who decides? (authorization rules)

## 4. Data

- What are the core entities and how do they relate?
- Where does data come from, how often, in what volume, and how clean is it?
- What's the retention policy? Anything that must be deleted, or must never be deleted?
- Any data that's sensitive, regulated, or personally identifying?
- What's the source of truth when two systems disagree?

## 5. Interfaces & integrations

- What external systems, APIs, or services does this talk to? In which direction?
- What are the contracts — formats, protocols, auth, rate limits, SLAs of those systems?
- What happens when a dependency is down or slow? (Drives availability/degradation requirements.)
- Any hardware, sensors, or physical interfaces?

## 6. Quality attributes (the ones people forget)

Probe each — they're where "user-friendly" turns into something testable:

- **Performance**: response time, throughput, under what load, at which percentile?
- **Scale**: how many users/records/requests now, and in 2 years?
- **Availability**: acceptable downtime? Maintenance windows? RPO/RTO if it fails?
- **Security**: authentication, authorization, encryption, audit, threat model?
- **Privacy/compliance**: GDPR, HIPAA, SOC2, industry rules?
- **Usability**: who learns it how fast? Accessibility standards (e.g. WCAG)?
- **Reliability**: failure modes, recovery, data integrity guarantees?
- **Maintainability/operability**: who runs it, how is it monitored, deployed, rolled back?
- **Portability**: which platforms, browsers, devices, regions?

For each that matters, push to a number: "fast" → "p95 under 500 ms"; "secure" →
"all PII encrypted at rest and in transit, access logged."

## 7. Constraints

- Mandated technologies, platforms, vendors, or languages? Why — preference or hard constraint?
- Budget, timeline, or team-size limits that shape what's feasible?
- Legal, regulatory, contractual, or organizational policy constraints?
- Existing systems this must coexist with or migrate from?

## 8. Assumptions & dependencies

- What are we assuming to be true that, if false, breaks the plan?
- What do we depend on others to deliver, and by when?
- What's uncertain right now that we're proceeding on anyway? (Flag for revisit.)

## 9. Acceptance & verification

- For each requirement: how would we *prove* it's met? Who signs off?
- What's the definition of done for the whole release?
- Are there acceptance tests, demos, or audits the system must pass?

## 10. Risks

- What's most likely to go wrong, and what's the impact if it does?
- Where is the team least confident? What would you want to prototype first?
- Are there decisions being deferred that will be expensive to change later? (Candidates for an ADR now or soon.)

## Turning answers into requirements

After a batch, convert answers into the schema (`references/requirement-schema.md`):

1. Split compound answers into **atomic** requirements — one obligation each.
2. Phrase each as a binding **statement** ("The system shall …").
3. Attach a **verification** method and concrete criterion — if you can't, say so and
   ask the question that would make it verifiable.
4. Link **derived_from** to the higher-level need it serves, building the DAG.
5. Note any **conflict** with an existing requirement explicitly rather than letting
   two contradictory requirements coexist silently.
6. If an answer was really a *decision among alternatives*, capture an ADR too.
