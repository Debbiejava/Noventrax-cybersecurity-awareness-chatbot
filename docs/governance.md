# Noventrax VLE/LMS  
## Governance, Privacy & Compliance Framework

---

## 1. Purpose

This document defines the governance framework for the Noventrax VLE/LMS.

It outlines:

- Data protection principles
- Retention and deletion policies
- GDPR alignment
- Audit and accountability model
- AI governance controls
- Incident response and reporting
- Access review and oversight mechanisms

This document supports compliance readiness and responsible platform operation.

---

# 2. Governance Principles

The platform operates under the following governance principles:

- Lawfulness, fairness, and transparency
- Purpose limitation
- Data minimisation
- Accuracy
- Storage limitation
- Integrity and confidentiality
- Accountability

These principles align with UK GDPR and general data protection best practices.

---

# 3. Data Protection Framework

---

## 3.1 Lawful Basis for Processing

| Data Category | Purpose | Lawful Basis |
|---------------|----------|--------------|
| User identity data | Authentication & access control | Contract / Legitimate interest |
| Course enrolment data | Learning delivery | Contract |
| Assessment & grading data | Academic evaluation | Contract / Institutional obligation |
| Chat transcripts | Learning support | Legitimate interest |
| Feedback | Service improvement | Legitimate interest |
| Audit logs | Security & governance | Legal obligation / Legitimate interest |

---

## 3.2 Data Minimisation

The system collects only data required to:

- Authenticate users
- Deliver learning content
- Track progress
- Evaluate assessments
- Maintain governance records

The system must avoid:

- Storing unnecessary personal identifiers in chat prompts
- Embedding sensitive data into AI context

---

# 4. Data Retention Policy

Retention periods must be clearly defined and documented.

| Data Type | Retention Period | Notes |
|-----------|------------------|-------|
| User accounts | While active | Deleted/anonymised upon request where lawful |
| Academic records | Per institutional policy | May require long-term retention |
| Submissions | Per academic policy | May align with grade retention |
| Grades | Long-term academic record | Must remain auditable |
| Chat transcripts | Defined period (e.g., 6–12 months) | Subject to review |
| Feedback | 12–24 months | Anonymise where possible |
| Audit logs | Minimum 12–24 months | Cannot be silently modified |

Retention enforcement must be automated where feasible.

---

# 5. Data Subject Rights (GDPR Alignment)

Users must have the ability to:

- Access their personal data
- Request correction of inaccurate data
- Request deletion (subject to academic/legal constraints)
- Request data portability
- Be informed of data usage

Deletion requests must consider:

- Academic record obligations
- Legal retention requirements
- Audit integrity requirements

Where deletion is not possible, data should be anonymised where feasible.

---

# 6. AI Governance

The AI tutor introduces additional governance responsibilities.

---

## 6.1 AI Usage Policy

The AI assistant is intended for:

- Learning support
- Clarification of course topics
- Supplementary educational guidance

It must not be used for:

- Automated grading decisions (unless explicitly approved)
- Disciplinary actions
- Automated academic sanctions

---

## 6.2 AI Data Handling Controls

- No cross-user chat data sharing.
- Chat sessions isolated by user_id.
- Avoid sending sensitive personal data to AI service.
- Log AI interactions (metadata only, not prompt secrets).
- Monitor AI usage patterns for abuse.

---

## 6.3 AI Risk Mitigation

Risks include:

- Prompt injection
- Hallucinated responses
- Inappropriate content
- Over-reliance by learners

Mitigations:

- Input sanitisation
- Output filtering (where applicable)
- Clear disclaimer that AI is assistive, not authoritative
- Logging and monitoring AI usage

---

# 7. Access Reviews & Oversight

Periodic reviews must be conducted for:

- Role assignments (Student / Instructor / Admin)
- Admin privileges
- Instructor-course assignments
- Database access
- Blob storage access
- Azure resource permissions

Access review cadence: Quarterly (recommended).

---

# 8. Audit & Accountability

The system must log:

- Role changes
- Course publishing
- Enrolment modifications
- Grade changes
- Admin actions
- Sensitive data access (e.g., chat transcript review by admin)

Audit logs must:

- Be append-only
- Include timestamp and actor ID
- Be tamper-resistant
- Be retained per policy

---

# 9. Incident Response Governance

In the event of:

- Data breach
- Unauthorized access
- Service outage
- AI misuse

The following steps must occur:

1. Immediate containment.
2. Root cause investigation.
3. Log preservation.
4. Impact assessment.
5. Stakeholder notification (if required by law).
6. Remediation and patch.
7. Post-incident review documentation.

If personal data is compromised, regulatory notification timelines must be followed.

---

# 10. Monitoring & Reporting

The platform must monitor:

- Failed login attempts
- Elevated privilege changes
- Unusual grading patterns
- High AI usage spikes
- Storage anomalies

Reports should be available to administrators and reviewed periodically.

---

# 11. Third-Party & Vendor Governance

External dependencies include:

- Azure OpenAI
- Azure hosting services
- Identity provider

Governance requirements:

- Review vendor compliance documentation.
- Monitor service-level agreements (SLAs).
- Ensure data residency compliance (region selection).
- Maintain vendor risk assessment documentation.

---

# 12. Governance Review & Updates

This governance framework must be:

- Reviewed annually (minimum)
- Updated after major feature changes
- Updated after security incidents
- Version-controlled in the repository

---

**Document Version:** v1.0  
**Document Type:** Governance & Compliance Framework  
**Focus:** GDPR alignment, AI governance, audit accountability
