# Risk Register Template

## Overview

Every specification should include a risk register that identifies, assesses, and plans mitigation for risks tied to requirements. Risks that are not captured in the specification become surprises during implementation.

## Risk Register Template

```markdown
# Risk Register

## Risk Summary

| Total Risks | Critical | High | Medium | Low |
|-------------|----------|------|--------|-----|
| {N} | {N} | {N} | {N} | {N} |

## Risk Entries

### RISK-{XXX}: {Risk Title}

| Attribute | Value |
|-----------|-------|
| **ID** | RISK-{XXX} |
| **Category** | {Technical / Business / Regulatory / Operational / External} |
| **Related Requirements** | {FR-XXX, NFR-YYY} |
| **Description** | {Clear statement of what could go wrong} |
| **Likelihood** | {1-5: Rare / Unlikely / Possible / Likely / Almost Certain} |
| **Impact** | {1-5: Negligible / Minor / Moderate / Major / Severe} |
| **Risk Score** | {Likelihood x Impact} |
| **Risk Level** | {Critical / High / Medium / Low} |
| **Owner** | {Person responsible for monitoring/mitigating} |
| **Status** | {Open / Mitigating / Accepted / Closed} |

**Trigger Conditions**:
- {What signals that this risk is materializing}

**Mitigation Strategy**:
- {Preventive actions to reduce likelihood}
- {Contingent actions to reduce impact}

**Contingency Plan**:
- {What to do if this risk materializes despite mitigation}

**Impact on Requirements**:
- {Which requirements are affected and how}
```

## Risk Assessment Matrix

```
                    IMPACT
              1     2     3     4     5
         ┌─────┬─────┬─────┬─────┬─────┐
    5    │  5  │ 10  │ 15  │ 20  │ 25  │  Almost Certain
         ├─────┼─────┼─────┼─────┼─────┤
    4    │  4  │  8  │ 12  │ 16  │ 20  │  Likely
L        ├─────┼─────┼─────┼─────┼─────┤
I   3    │  3  │  6  │  9  │ 12  │ 15  │  Possible
K        ├─────┼─────┼─────┼─────┼─────┤
E   2    │  2  │  4  │  6  │  8  │ 10  │  Unlikely
L        ├─────┼─────┼─────┼─────┼─────┤
I   1    │  1  │  2  │  3  │  4  │  5  │  Rare
H        └─────┴─────┴─────┴─────┴─────┘
O
O   Score:  1-4  = Low
D           5-9  = Medium
            10-16 = High
            17-25 = Critical
```

## Risk Categories

### Technical Risks
- Technology immaturity or instability
- Integration complexity with external systems
- Performance bottlenecks under load
- Data migration failures or data loss
- Security vulnerabilities
- Scalability limitations

### Business Risks
- Changing business requirements mid-project
- Stakeholder availability for decisions
- Budget constraints limiting scope
- Market timing pressure
- Competitive changes invalidating requirements

### Regulatory Risks
- New regulations enacted during development
- Compliance interpretation uncertainty
- Audit failures
- Data residency violations
- Privacy regulation changes

### Operational Risks
- Team skill gaps for chosen technology
- Key person dependency
- Third-party vendor reliability
- Deployment environment constraints
- Support and maintenance capacity

### External Risks
- Third-party API deprecation or breaking changes
- Vendor pricing changes
- Open-source license changes
- Network/infrastructure outages
- Force majeure events

## Common Requirement-Level Risks

When documenting requirements, watch for these risk indicators:

| Requirement Pattern | Risk | Mitigation |
|--------------------|------|------------|
| "System shall integrate with {external}" | External dependency failure | Circuit breaker, fallback, SLA |
| "Real-time processing of..." | Performance under load | Load testing, capacity planning |
| "Must comply with {regulation}" | Compliance interpretation | Legal review, compliance audit |
| "Users shall upload..." | Malicious content, size limits | Validation, scanning, quotas |
| "System shall migrate data from..." | Data loss, corruption | Dry-run migration, rollback plan |
| "Available 99.99%..." | Downtime exceeding SLA | Redundancy, failover, monitoring |
| "Support N concurrent users" | Scalability limits | Load testing, auto-scaling design |
| Single vendor/technology dependency | Vendor lock-in | Abstraction layers, multi-vendor eval |

## Risk Identification Questions

Ask stakeholders:

1. "What could go wrong with this requirement?"
2. "What are you most worried about?"
3. "What has gone wrong on similar projects?"
4. "What external dependencies concern you?"
5. "What happens if {dependency} is unavailable?"
6. "What's the worst case if this requirement isn't met?"
7. "Are there any regulatory changes on the horizon?"
8. "What assumptions are we making that could prove false?"

## Integration with SRS

The risk register should be included as an appendix in the SRS document (Appendix D or E) and cross-referenced from:

- **Section 2.5** (Assumptions and Dependencies) - risks from assumptions
- **Section 3.3** (Non-Functional Requirements) - risks to quality attributes
- **Section 3.4** (Design Constraints) - risks from constraints
- **Traceability Matrix** - risk-to-requirement mapping
