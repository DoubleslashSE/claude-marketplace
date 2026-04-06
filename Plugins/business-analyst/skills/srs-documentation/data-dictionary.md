# Data Dictionary Template

## Overview

A data dictionary defines every data element referenced in the specification. While the glossary defines terms, the data dictionary defines the structure, format, valid values, and business rules for each piece of data the system handles. This is essential for developers to implement correctly.

## Data Dictionary Template

```markdown
# Data Dictionary

## {Domain Entity / Feature Area}

### DE-{XXX}: {Data Element Name}

| Attribute | Value |
|-----------|-------|
| **ID** | DE-{XXX} |
| **Name** | {Business name} |
| **Alias(es)** | {Other names used for this element} |
| **Definition** | {Clear business definition} |
| **Data Type** | {String / Integer / Decimal / Boolean / Date / Enum / Object} |
| **Format** | {Pattern or structure, e.g., "YYYY-MM-DD", "XXX-XXXX"} |
| **Length / Size** | {Min and max, e.g., "1-100 characters", "2 decimal places"} |
| **Valid Values / Range** | {Enumerated values or numeric range} |
| **Default Value** | {Default if not provided, or "None - Required"} |
| **Required** | {Yes / No / Conditional (explain)} |
| **Unique** | {Yes / No / Scoped (explain scope)} |
| **Source** | {Where this data originates} |
| **Owner** | {Who is responsible for data quality} |
| **Related Requirements** | {FR-XXX, NFR-YYY} |
| **Related Entities** | {Entity.attribute references} |
| **Sensitivity** | {Public / Internal / Confidential / Restricted / PII / PHI / PCI} |
| **Encryption Required** | {At rest / In transit / Both / None} |
| **Retention Period** | {Duration or policy reference} |

**Validation Rules**:
- {Rule 1: e.g., "Must be a valid email format (RFC 5322)"}
- {Rule 2: e.g., "Cannot be a date in the future"}

**Business Rules**:
- {Rule 1: e.g., "Discount cannot exceed 50% of item price"}
- {Rule 2: e.g., "Status can only be changed by users with Manager role"}

**Derivation / Calculation**:
- {If computed: formula or logic, e.g., "Total = Sum(LineItem.Amount) + Tax - Discount"}

**Notes**:
- {Additional context}
```

## Data Element Categories

### Identity Data
| Element | Type | Format | Example |
|---------|------|--------|---------|
| User ID | UUID | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | 550e8400-e29b-41d4-a716-446655440000 |
| Email | String | RFC 5322 | user@example.com |
| Phone | String | E.164 | +14155552671 |

### Financial Data
| Element | Type | Format | Precision |
|---------|------|--------|-----------|
| Currency Amount | Decimal | {amount} | 2 decimal places |
| Currency Code | String | ISO 4217 (3 chars) | USD, EUR, SEK |
| Tax Rate | Decimal | Percentage | 4 decimal places |
| Account Number | String | Varies by type | Masked in display |

### Temporal Data
| Element | Type | Format | Timezone |
|---------|------|--------|----------|
| Date | Date | YYYY-MM-DD (ISO 8601) | N/A |
| Timestamp | DateTime | ISO 8601 with TZ | Store as UTC |
| Duration | Interval | ISO 8601 duration | P1Y2M3DT4H5M6S |

### Status / State Data
| Element | Type | Valid Values | Transitions |
|---------|------|-------------|-------------|
| Order Status | Enum | Draft, Submitted, Approved, Shipped, Delivered, Cancelled | See state diagram |
| User Status | Enum | Active, Inactive, Suspended, Deleted | See lifecycle rules |

## Sensitive Data Classification

| Classification | Description | Handling Requirements |
|----------------|-------------|----------------------|
| **Public** | Freely available | No special handling |
| **Internal** | Internal business use | Access control required |
| **Confidential** | Business-sensitive | Encryption + access control |
| **Restricted** | Highly sensitive | Encryption + audit + MFA |
| **PII** | Personally identifiable | GDPR/privacy controls |
| **PHI** | Protected health info | HIPAA controls |
| **PCI** | Payment card data | PCI-DSS controls |

## Data Relationship Documentation

```markdown
## Entity Relationship: {Entity A} to {Entity B}

| Attribute | Value |
|-----------|-------|
| Relationship Type | {1:1 / 1:N / N:N} |
| Cardinality | {Entity A (min..max) : Entity B (min..max)} |
| Required | {Is the relationship mandatory?} |
| Cascade Rules | {On delete: cascade / set null / restrict / no action} |
| Ordering | {Is ordering significant? By what field?} |
| Business Rule | {e.g., "Customer must have at least one address"} |
```

## Integration with SRS

The data dictionary should be referenced from:
- **Section 3.1** (External Interface Requirements) - data exchanged at interfaces
- **Section 3.2** (Functional Requirements) - data inputs/outputs per requirement
- **Appendix A** (Glossary) - cross-reference business terms
- **Appendix B** (Analysis Models) - ERD entities reference data dictionary

Include the full data dictionary as **Appendix E: Data Dictionary** in the SRS.

## Data Dictionary Questions for Stakeholders

1. "What does this field represent in business terms?"
2. "What values are valid for this field?"
3. "Is this field always required, or only in certain contexts?"
4. "Who is allowed to see/modify this data?"
5. "How long must this data be kept?"
6. "Is this data sensitive or regulated?"
7. "Where does this data come from originally?"
8. "How is this value calculated/derived?"
9. "What happens if this value is missing or invalid?"
10. "Does this field have different meanings in different contexts?"
