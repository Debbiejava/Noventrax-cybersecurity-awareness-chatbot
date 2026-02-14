# Noventrax VLE/LMS  
## Architecture Overview

---

## 1. Purpose

This document provides a single entry point to the Noventrax VLE/LMS architecture. It summarises:

- What the system is
- The major architectural decisions
- Where to find each diagram and design document
- How the platform will evolve from the current prototype to a full VLE/LMS

---

## 2. System Summary

**Noventrax VLE/LMS** is a secure, AI-enhanced learning platform that combines:

- **VLE** capabilities: learning delivery (content access, learning pathways, engagement support)
- **LMS** capabilities: course management, enrolments, assessments, grading, and progress tracking
- **AI Tutor**: embedded learning assistant for cybersecurity and related learning modules

---

## 3. Current Prototype Status (What Exists Today)

The current build includes:

- Static web frontend (chat UI + learning module buttons + feedback modal)
- FastAPI backend (chat endpoint, feedback endpoint, health endpoint)
- Azure OpenAI integration for AI tutoring responses
- Basic client-side safety checks (validation/sanitisation)

Key limitations of the prototype:

- No authentication / RBAC
- No persistent database
- No persistent chat sessions (global in-memory state is not production-safe)
- No LMS core features (courses, enrolments, assessments, grades)

---

## 4. Target System Capabilities (VLE/LMS)

The target system adds:

- Authentication and role-based access control (Student/Instructor/Admin)
- Course catalogue and course structure (Course → Module → Lesson)
- Enrolment management
- Content delivery (including file uploads)
- Assessment engine (quizzes + assignments)
- Submissions and grading
- Progress tracking and basic analytics
- Governance features (audit logs, retention, incident response readiness)
- AI tutor integrated into course context (per-user session isolation)

---

## 5. Architectural Decisions (High-Level)

### 5.1 Hosting Model
- Frontend: Azure Static Web Apps
- Backend API: Azure Container Apps (recommended) or Azure App Service (standardise to one)
- AI: Azure OpenAI

### 5.2 Persistence Model (Required for VLE/LMS)
- Relational DB: Azure PostgreSQL (users, roles, courses, enrolments, grades, chat logs, audits)
- Object Storage: Azure Blob Storage (course materials, assignment uploads)
- Optional cache/session: Azure Redis (rate limiting counters, session optimisation)

### 5.3 Stateless Backend Requirement
The backend must be stateless to support scaling. No in-memory shared user session state is permitted in production.

### 5.4 Security Baseline
- Authentication and RBAC enforced server-side
- Per-user data isolation (especially chat sessions and messages)
- Audit logs for grade changes, role changes, admin actions
- Observability and monitoring with alerts
- GDPR-aligned privacy controls (retention/deletion/export)

---

## 6. Documentation Map (Where Everything Lives)

### Core architecture diagrams and designs
- **System Context (C4 L1):** `docs/context.md`
- **Container Diagram (C4 L2):** `docs/containers.md`
- **Entity Relationship Diagram (ERD):** `docs/erd.md`
- **Data Flow Diagram (DFD):** `docs/data-flow.md`
- **Security Architecture (STRIDE-informed):** `docs/security.md`
- **Deployment Architecture:** `docs/deployment.md`

### Additional diagrams and specs (generated next)
- **Use cases + use-case diagram:** `docs/use-case.md`
- **Sequence diagrams (critical flows):** `docs/sequence.md`
- **State machine diagrams:** `docs/state-machines.md`
- **RBAC matrix:** `docs/rbac.md`
- **Audit & logging flow:** `docs/audit-logging.md`
- **Threat model diagram:** `docs/threat-model.md`
- **Governance policy pack:** `docs/governance.md`
- **Delivery roadmap:** `docs/roadmap.md`
- **API interface spec (optional):** `docs/api-spec.md`

---

## 7. Architecture at a Glance (Quick View)

```mermaid
flowchart LR

  Student[Student] --> UI["Web Frontend<br>(Azure Static Web Apps)"]
  Instructor[Instructor] --> UI
  Admin[Admin] --> UI

  UI -->|"HTTPS API Calls"| API["Backend API<br>(FastAPI)"]

  API --> DB[("PostgreSQL<br>(LMS Data)")]
  API --> BLOB[("Blob Storage<br>(Files/Uploads)")]
  API --> REDIS[("Redis (Optional)<br>(Sessions/Rate Limits)")]
  API --> OpenAI[("Azure OpenAI<br>(AI Tutor)")]
  API --> IdP[("Identity Provider<br>(Entra ID / JWT Auth)")]
  API --> Obs[("App Insights / Monitor<br>(Logs & Metrics)")]
