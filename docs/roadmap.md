# Noventrax VLE/LMS  
## Product Roadmap & Delivery Plan

---

## 1. Purpose

This roadmap defines the phased development plan for Noventrax VLE/LMS.

It ensures:

- Controlled scope growth
- Governance-first implementation
- Security built into every phase
- Clear MVP boundary
- Measurable delivery milestones

The roadmap is structured into execution phases.

---

# 2. Delivery Strategy

The product will be delivered in progressive maturity stages:

Phase 0 → Architecture & Controls  
Phase 1 → Secure MVP LMS Core  
Phase 2 → Assessment & Governance Hardening  
Phase 3 → AI Tutor Maturity & Analytics  
Phase 4 → Enterprise Readiness & Scaling  

Each phase must complete:

- Functional implementation
- RBAC enforcement
- Audit coverage
- Testing
- Documentation updates

---

# 3. Phase 0 — Architecture & Governance Foundation (Completed)

Deliverables:

- Context diagram
- Container diagram
- ERD
- Data flow diagram
- Sequence diagrams
- State machines
- RBAC matrix
- Governance framework
- Threat model
- Audit logging architecture
- Framework-as-code design

Outcome:
- Clear system boundary
- Defined data model
- Defined access model
- Defined security posture

Status: Complete

---

# 4. Phase 1 — Secure MVP (Core LMS)

## Goal
Replace prototype chatbot platform with secure, persistent LMS core.

## Scope

### 4.1 Authentication & Authorization
- JWT validation middleware
- Role-based access control enforcement
- Ownership validation
- Deny-by-default policy

### 4.2 Database Integration
- PostgreSQL integration
- Replace in-memory storage:
  - conversation history
  - feedback store
- Implement:
  - users
  - courses
  - enrolments
  - lessons
  - chat sessions/messages

### 4.3 Course Lifecycle
- Instructor create/edit course
- Publish/unpublish (optional)
- Enrolment creation
- Enrolment access control

### 4.4 Basic AI Tutor Isolation
- Per-user chat session storage
- No cross-user memory
- Chat persistence in DB

### 4.5 Security Baseline
- Server-side rate limiting
- Request size limits
- Safe error handling
- Audit logging on:
  - course publish
  - enrolment creation
  - role changes

### 4.6 Testing
- Unit tests for RBAC
- Integration tests for enrolment access
- Cross-user data access tests

Outcome:
- Secure LMS foundation
- Persistent storage
- No in-memory shared state
- Governance baseline enforced

---

# 5. Phase 2 — Assessment & Academic Governance

## Goal
Introduce assessments and grading with audit integrity.

## Scope

### 5.1 Assessment Management
- Create assessment
- Define open/due date
- State-based enforcement

### 5.2 Submission Workflow
- File upload to Blob
- Submission record creation
- Late submission handling
- Resubmission policy

### 5.3 Grading
- Grade creation
- Grade update (append-only)
- Release grades
- Audit log required for:
  - grade creation
  - grade modification
  - grade override

### 5.4 Governance Controls
- Enforce state machines
- Lock submissions when closed
- Prevent unauthorized grade changes

### 5.5 Reporting
- Basic instructor dashboard
- Basic admin overview

Outcome:
- Academic integrity preserved
- Fully auditable grading system
- Policy-aligned workflows

---

# 6. Phase 3 — AI Tutor Maturity

## Goal
Enhance AI tutor safely and responsibly.

## Scope

### 6.1 Contextual AI
- Course-scoped context
- Lesson-aware prompts
- Avoid personal data leakage

### 6.2 AI Observability
- Log AI latency
- Monitor usage spikes
- Track token consumption (optional)

### 6.3 Abuse Protection
- AI rate limiting
- Input filtering improvements
- Session expiration policy

### 6.4 AI Governance Controls
- Admin visibility of usage metadata
- Clear AI usage policy display

Outcome:
- Mature AI tutor
- Controlled risk exposure
- Transparent AI governance

---

# 7. Phase 4 — Enterprise & Operational Readiness

## Goal
Prepare platform for institutional use.

## Scope

### 7.1 Infrastructure Hardening
- Infrastructure as Code
- Azure Policy enforcement
- Private networking where feasible
- Backup and restore procedures

### 7.2 Monitoring & Alerting
- Security alert thresholds
- Operational dashboards
- Incident response playbook integration

### 7.3 Data Governance
- Automated retention jobs
- GDPR export/delete workflows
- Access review workflow

### 7.4 Performance & Scaling
- Load testing
- Autoscaling configuration
- DB indexing optimization
- Blob lifecycle rules

Outcome:
- Production-grade platform
- Governance maturity
- Institutional readiness

---

# 8. Feature Flags & Safe Rollout

All high-risk features should be:

- Feature-flagged
- Tested in staging
- Observed via metrics
- Gradually enabled

Especially:
- Grade modifications
- AI enhancements
- Admin data access features

---

# 9. Acceptance Criteria Per Phase

Each phase must meet:

- All endpoints authenticated
- RBAC enforced
- Audit events logged
- No cross-user data leakage
- Tests passing
- Documentation updated
- Threat model reviewed

No phase is complete without governance validation.

---

# 10. Version Milestones

| Version | Description |
|----------|------------|
| v0.1 | Prototype AI tutor (existing) |
| v1.0 | Secure LMS MVP (Phase 1 complete) |
| v1.5 | Assessment + Grading governance (Phase 2 complete) |
| v2.0 | AI maturity + analytics |
| v3.0 | Enterprise-ready platform |

---

# 11. Scope Control Rules

To prevent uncontrolled growth:

- No feature without RBAC mapping.
- No feature without state definition.
- No feature without audit requirement assessment.
- No feature without threat review.
- No direct DB access from frontend.

---

# 12. Continuous Review

Roadmap must be reviewed:

- At end of each phase
- After incidents
- Before major architecture changes

---

**Document Version:** v1.0  
**Document Type:** Product Roadmap  
**Focus:** Secure phased delivery
