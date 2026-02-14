# Noventrax VLE/LMS  
## Sequence Diagrams (Critical Flows)

---

## 1. Purpose

This document captures **time-ordered interactions** between actors, the frontend, backend, and dependent services for the most critical VLE/LMS workflows.

Sequence diagrams help ensure:

- Correct ordering of steps
- Clear responsibilities across containers
- Consistent security enforcement (AuthN/AuthZ)
- Reliable data persistence (no in-memory shared state)
- Predictable error handling and audit logging

---

## 2. Notation

Participants used across diagrams:

- **User**: Student / Instructor / Admin
- **UI**: Web Frontend (Azure Static Web Apps)
- **API**: Backend API (FastAPI)
- **IdP**: Identity Provider (Entra ID / JWT Auth)
- **DB**: PostgreSQL
- **BLOB**: Blob Storage
- **OpenAI**: Azure OpenAI
- **Obs**: Observability (App Insights / Monitor)

---

# 3. Sequence Diagram 1 — Login (Authentication)

```mermaid
sequenceDiagram
  autonumber
  actor User as User (Student/Instructor/Admin)
  participant UI as Web Frontend (SWA)
  participant IdP as Identity Provider
  participant API as Backend API (FastAPI)

  User->>UI: Open app / Click Sign in
  UI->>IdP: Redirect / Auth request
  IdP-->>UI: Token / Claims
  UI->>API: API request with token
  API->>IdP: Validate token
  IdP-->>API: Token valid + claims
  API-->>UI: Authorized response
  UI-->>User: User is signed in


# Sequence diagram 2 - student enrolment in a course

```mermaid
sequenceDiagram
  autonumber
  actor Student as Student
  participant UI as Web Frontend (SWA)
  participant API as Backend API (FastAPI)
  participant IdP as Identity Provider
  participant DB as PostgreSQL
  participant Obs as Observability

  Student->>UI: Click Enrol on Course
  UI->>API: POST /enrolments (token, course_id)
  API->>IdP: Validate token + role
  IdP-->>API: Valid + role=Student
  API->>DB: Check course status=Published
  DB-->>API: Published
  API->>DB: Check existing enrolment(user_id, course_id)
  DB-->>API: Not enrolled
  API->>DB: Create enrolment(status=Active)
  DB-->>API: Enrolment created
  API->>Obs: Log event (enrolment_created)
  API-->>UI: 201 Created + enrolment details
  UI-->>Student: Access granted to course

# Sequence diagram 3 - Lesson Access + Progress Update
```mermaid
sequenceDiagram
  autonumber
  actor Student as Student
  participant UI as Web Frontend (SWA)
  participant API as Backend API (FastAPI)
  participant IdP as Identity Provider
  participant DB as PostgreSQL
  participant BLOB as Blob Storage

  Student->>UI: Open lesson
  UI->>API: GET /lessons/{id} (token)
  API->>IdP: Validate token
  IdP-->>API: Valid
  API->>DB: Authorize access (enrolment check)
  DB-->>API: Enrolled
  API->>DB: Fetch lesson metadata + content references
  DB-->>API: Lesson metadata
  API->>BLOB: Fetch file link / read content (if file)
  BLOB-->>API: Content/URL
  API-->>UI: Lesson content payload
  UI-->>Student: Render lesson

  Student->>UI: Mark lesson complete
  UI->>API: POST /progress (lesson_id, completed=true)
  API->>IdP: Validate token
  IdP-->>API: Valid
  API->>DB: Verify enrolment still Active
  DB-->>API: Active
  API->>DB: Upsert lesson_progress(completed_at)
  DB-->>API: Updated
  API-->>UI: 200 OK


# Sequence diagram 4 - Assignment Submission
```mermaid
sequenceDiagram
  autonumber
  actor Student as Student
  participant UI as Web Frontend (SWA)
  participant API as Backend API (FastAPI)
  participant IdP as Identity Provider
  participant DB as PostgreSQL
  participant BLOB as Blob Storage
  participant Obs as Observability

  Student->>UI: Upload assignment file + submit
  UI->>API: POST /submissions (token, assessment_id, metadata)
  API->>IdP: Validate token + role
  IdP-->>API: Valid + role=Student
  API->>DB: Authorize (enrolment + assessment open)
  DB-->>API: Authorized
  API->>BLOB: Store file (private container)
  BLOB-->>API: blob_path
  API->>DB: Create submission record(blob_path, status=Submitted)
  DB-->>API: Submission created
  API->>Obs: Log event (submission_created)
  API-->>UI: 201 Created + submission ID
  UI-->>Student: Submission confirmation

# Sequence Diagram 5 - Instructor Grading + Audit logging
```mermaid
sequenceDiagram
  autonumber
  actor Instructor as Instructor
  participant UI as Web Frontend (SWA)
  participant API as Backend API (FastAPI)
  participant IdP as Identity Provider
  participant DB as PostgreSQL
  participant Obs as Observability
  participant Notify as Notification Service

  Instructor->>UI: Open submission + enter grade
  UI->>API: POST /grades (token, submission_id, score, feedback)
  API->>IdP: Validate token + role
  IdP-->>API: Valid + role=Instructor
  API->>DB: Authorize instructor for course
  DB-->>API: Authorized
  API->>DB: Create new grade record (append-only)
  DB-->>API: Grade saved
  API->>DB: Write audit log (grade_changed)
  DB-->>API: Audit saved
  API->>Obs: Log event (grade_created)
  API->>Notify: Notify student (optional)
  Notify-->>API: Accepted
  API-->>UI: 200 OK
  UI-->>Instructor: Grade published

# Sequence diagram 6 - AI Tutor chat (per-user session isolation)
```mermaid
sequenceDiagram
  autonumber
  actor Student as Student
  participant UI as Web Frontend (SWA)
  participant API as Backend API (FastAPI)
  participant IdP as Identity Provider
  participant DB as PostgreSQL
  participant OpenAI as Azure OpenAI
  participant Obs as Observability

  Student->>UI: Send chat message
  UI->>API: POST /chat (token, message, session_id?)
  API->>IdP: Validate token
  IdP-->>API: Valid + user_id
  API->>DB: Load chat session (must belong to user_id)
  DB-->>API: Session ok (or create new)
  API->>DB: Persist user message (chat_messages)
  DB-->>API: Saved
  API->>OpenAI: Send prompt (user context only)
  OpenAI-->>API: AI response
  API->>DB: Persist assistant response
  DB-->>API: Saved
  API->>Obs: Log AI latency + request metrics
  API-->>UI: Reply text
  UI-->>Student: Render AI response

## Failure & Degradation Patterns (Applies to All Flows)

If IdP fails: return 401/503 with clear message; do not process requests.

If DB fails: return safe error; prevent partial writes; log incident.

If Blob Storage fails: block uploads/downloads; keep system stable.

If Azure OpenAI fails: return fallback response; keep LMS functional.

