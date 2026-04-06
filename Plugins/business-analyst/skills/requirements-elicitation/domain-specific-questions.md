# Domain-Specific Question Templates

## Overview

Standard question templates miss critical domain-specific requirements. Use these supplemental questions when the project falls within a recognized domain. Always ask the domain identification question first, then apply the relevant template.

## Domain Identification

Ask early in the interview:
> "What industry or domain does this project serve? For example: healthcare, financial services, e-commerce, SaaS/B2B, government, education, logistics, IoT, or media/entertainment."

## Healthcare / Health IT

### Regulatory & Compliance
1. Does this system handle Protected Health Information (PHI)?
2. What HIPAA requirements apply (Privacy Rule, Security Rule, Breach Notification)?
3. Is HL7 FHIR or other interoperability standard required?
4. Are there FDA regulations (if medical device software)?
5. Do you need a BAA (Business Associate Agreement) with cloud providers?

### Clinical Workflow
1. What clinical workflows does this system support or integrate with?
2. Does this interact with EHR/EMR systems? Which ones (Epic, Cerner, etc.)?
3. Are there clinical decision support requirements?
4. What audit trail requirements exist for clinical actions?
5. How are patient consent and authorization managed?

### Data Requirements
1. What de-identification or anonymization is required for research data?
2. What are the data retention requirements for medical records?
3. Is there a minimum necessary standard for data access?

## Financial Services / Fintech

### Regulatory & Compliance
1. What financial regulations apply (PCI-DSS, SOX, PSD2, MiFID II, AML/KYC)?
2. Is PCI-DSS compliance required? At what SAQ level?
3. What anti-money laundering (AML) screening is needed?
4. What Know Your Customer (KYC) verification is required?
5. Are there reporting requirements to regulators?

### Transaction Processing
1. What transaction volumes and TPS are expected?
2. What are the requirements for transaction atomicity and consistency?
3. How are failed/partial transactions handled (rollback, compensation)?
4. What reconciliation processes are needed?
5. What are the settlement and clearing requirements?

### Security
1. What fraud detection mechanisms are needed?
2. How are payment credentials tokenized and stored?
3. What multi-factor authentication is required for financial operations?
4. What are the requirements for transaction signing or non-repudiation?

## E-Commerce / Retail

### Product & Catalog
1. How many SKUs/products will the system manage?
2. Are there product variants (size, color, configuration)?
3. What product search and filtering capabilities are needed?
4. Is multi-currency or multi-language support required?
5. How are product images and media managed?

### Order & Fulfillment
1. What order statuses and lifecycle states exist?
2. What shipping/fulfillment integrations are needed?
3. How are returns, refunds, and exchanges handled?
4. What inventory management approach (real-time, periodic sync)?
5. Are there pre-order or backorder capabilities needed?

### Pricing & Promotions
1. What pricing models apply (fixed, dynamic, tiered, subscription)?
2. What types of promotions/discounts are needed?
3. How are taxes calculated (by jurisdiction)?
4. What loyalty or rewards programs exist?

## SaaS / B2B Platform

### Multi-Tenancy
1. Is multi-tenant architecture required?
2. What tenant isolation level is needed (shared DB, schema-per-tenant, DB-per-tenant)?
3. Can tenants customize branding, workflows, or data fields?
4. What are the tenant onboarding/offboarding requirements?
5. How is tenant-level data export handled?

### Subscription & Billing
1. What billing models apply (per-seat, usage-based, tiered, flat)?
2. What subscription lifecycle events exist (trial, upgrade, downgrade, cancel)?
3. What payment gateway integrations are needed?
4. How are invoices generated and delivered?
5. What dunning (failed payment retry) process is needed?

### API & Integration
1. Do you need a public API for customers/partners?
2. What API authentication model (API keys, OAuth2)?
3. What rate limiting and usage quotas apply?
4. Is webhook support needed for event notifications?
5. What API versioning strategy is required?

## Government / Public Sector

### Compliance & Standards
1. What government standards apply (FedRAMP, FISMA, Section 508)?
2. What data sovereignty requirements exist (data must stay in-country)?
3. What accessibility standards (WCAG 2.1 AA, Section 508)?
4. Are there procurement-specific requirements?
5. What records retention and FOIA requirements apply?

### Security
1. What security clearance levels are involved?
2. Is NIST 800-53 or equivalent framework compliance required?
3. What are the incident reporting requirements?
4. Are air-gapped or disconnected operation modes needed?

## Education / EdTech

### Student Data
1. Does FERPA (or local equivalent) apply?
2. Does COPPA apply (users under 13)?
3. What student data privacy requirements exist?
4. How are parental consent mechanisms handled?

### Learning Management
1. Is LTI (Learning Tools Interoperability) integration needed?
2. What SCORM/xAPI compliance is required?
3. What assessment and grading models are used?
4. How is academic integrity enforced?

## Logistics / Supply Chain

### Tracking & Visibility
1. What real-time tracking capabilities are needed?
2. What geolocation/GPS integration is required?
3. What barcode/RFID/IoT sensor integrations exist?
4. What supply chain visibility across partners is needed?

### Operations
1. What route optimization requirements exist?
2. How are delivery windows and SLAs managed?
3. What warehouse management integrations are needed?
4. How are customs and cross-border requirements handled?

## IoT / Embedded Systems

### Device Management
1. How many devices will the system support?
2. What device provisioning and registration flow is needed?
3. How are firmware updates delivered (OTA)?
4. What device health monitoring is required?

### Data & Connectivity
1. What communication protocols (MQTT, CoAP, HTTP, BLE)?
2. What edge computing vs cloud processing split?
3. How is offline/intermittent connectivity handled?
4. What data ingestion rates and storage volumes are expected?

### Security
1. How are device credentials and certificates managed?
2. What device attestation/integrity verification is needed?
3. How is unauthorized device access prevented?

## Applying Domain Questions

When using these templates:

1. **Identify the domain** during stakeholder identification phase
2. **Select relevant sections** - not all questions apply to every project
3. **Adapt question depth** based on stakeholder's role (technical vs business)
4. **Cross-reference with NFR gathering** - many domain questions map to NFRs
5. **Document regulatory requirements as constraints** (CON-REG-XXX)
6. **Flag compliance requirements early** - they often constrain architecture
