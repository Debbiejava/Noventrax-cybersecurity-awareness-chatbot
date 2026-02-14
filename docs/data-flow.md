# Noventrax VLE/LMS  
## Data Flow Diagram (DFD) – Privacy-by-Design

---

## 1. Purpose

This document describes the **end-to-end data flows** in the Noventrax VLE/LMS, focusing on:

- Where data originates
- How it is processed
- Where it is stored
- Who can access it
- Trust boundaries and privacy considerations

This DFD supports governance, GDPR alignment, and secure-by-design implementation.

---

## 2. Key Data Types

- **Identity data:** name, email, role, tokens/claims
- **Learning data:** courses, enrolments, lesson progress
- **Assessment data:** submissions, quiz answers, grades, feedback
- **AI tutor data:** chat sessions/messages, course context references
- **Governance data:** audit logs, product feedback, security logs
- **Content data:** uploaded learning materials and assignment files

---

## 3. Trust Boundaries (High-Level)

- **Boundary A:** User Device/Browser ↔ Public Internet ↔ Web/API endpoints  
- **Boundary B:** Backend API ↔ Data stores (DB/Blob/Redis)  
- **Boundary C:** Backend API ↔ External services (Identity Provider, Azure OpenAI, Notifications)  
- **Boundary D:** Admin/Operators ↔ Observability/Monitoring (restricted access)

---

## 4. Data Flow Diagram (Mermaid)

> Notes:
> - This is a **logical** DFD (privacy + governance focus), not a network diagram.
> - All flows must use TLS (HTTPS) in implementation.

```mermaid
flowchart LR

  %% Actors
  Student[Student]
  Instructor[Instructor]
  Admin[Admin]

  %% Client / UI
  UI["Web Frontend<br>(Browser / Azure Static Web Apps)"]

  %% Core processing
  API["Backend API<br>(FastAPI)"]

  %% Data stores
  DB[("Relational DB<br>(PostgreSQL)")]
  BLOB[("Object Storage<br>(Blob Storage)")]
  REDIS[("Session/Cache Store<br>(Optional Redis)")]

  %% External services
  IdP[("Identity Provider<br>(Entra ID / JWT Auth)")]
  OpenAI[("Azure OpenAI")]
  Notify[("Email / Notification Service")]
  Obs[("Observability<br>(App Insights / Monitor)")]

  %% ----------------------------
  %% Authentication & Authorization
  %% ----------------------------
  Student -->|"Login / Access request"| UI
  Instructor -->|"Login / Authoring actions"| UI
  Admin -->|"Admin access"| UI

  UI -->|"Auth request"| IdP
  IdP -->|"Token / Claims"| UI
  UI -->|"HTTPS API calls<br>(Token attached)"| API
  API -->|"Validate token / claims"| IdP

  %% ----------------------------
  %% Course & Enrolment Data Flows
  %% ----------------------------
  API -->|"Read/write:<br>Users, Roles, Courses, Enrolments"| DB
  API -->|"Write/read:<br>Lesson progress updates"| DB

  %% ----------------------------
  %% Content Delivery & File Uploads
  %% ----------------------------
  Instructor -->|"Upload course materials"| UI
  UI -->|"Upload request"| API
  API -->|"Store files"| BLOB
  API -->|"Store metadata<br>(title, blob path, access rules)"| DB

  Student -->|"Access lesson content"| UI
  UI -->|"Request content metadata"| API
  API -->|"Authorize access<br>(enrolment check)"| DB
  API -->|"Fetch file / generate access path"| BLOB
  API -->|"Serve content link/response"| UI

  %% ----------------------------
  %% Assessments, Submissions, Grading
  %% ----------------------------
  Student -->|"Submit quiz/assignment"| UI
  UI -->|"Submission request"| API
  API -->|"Store submission record"| DB
  API -->|"Store uploaded file (if any)"| BLOB

  Instructor -->|"Grade submission"| UI
  UI -->|"Grade update request"| API
  API -->|"Write grade + feedback"| DB
  API -->|"Write audit event<br>(grade change)"| DB

  %% ----------------------------
  %% AI Tutor Flow (Per-user Isolation)
  %% ----------------------------
  Student -->|"Ask AI tutor question"| UI
  UI -->|"Chat message"| API
  API -->|"Read user/session context"| REDIS
  API -->|"Persist chat session/messages"| DB
  API -->|"Send prompt (no other users' data)"| OpenAI
  OpenAI -->|"AI response"| API
  API -->|"Persist AI response"| DB
  API -->|"Return response"| UI
  API -->|"Update session cache"| REDIS

  %% ----------------------------
  %% Feedback & Governance
  %% ----------------------------
  Student -->|"Submit product feedback"| UI
  UI -->|"Feedback request"| API
  API -->|"Store feedback"| DB

  %% ----------------------------
  %% Logging & Observability
  %% ----------------------------
  API -->|"Logs, metrics, traces"| Obs
  Admin -->|"Review reports / alerts"| Obs

  %% Notifications (optional)
  API -->|"Send notifications<br>(announcements, resets)"| Notify

