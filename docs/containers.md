# Noventrax VLE/LMS  
## C4 Level 2 – Container Diagram

---

## 1. Purpose

This diagram shows the **major runtime containers** that make up the Noventrax VLE/LMS and how they communicate.

At this level we describe:

- The main application building blocks (frontend, backend, data stores)
- Responsibilities of each container
- High-level communication paths and protocols
- External service integrations (Identity, Azure OpenAI)

This level does **not** show detailed internal components/classes (that appears in C4 Level 3).

---

## 2. Containers (Inside the System)

### 2.1 Web Frontend (Azure Static Web Apps)
- Hosts the user interface for Students, Instructors, and Admins.
- Provides navigation for Courses, Lessons, Assessments, Grades, and AI Tutor.
- Sends API requests to the backend over HTTPS.

### 2.2 Backend API (FastAPI on Azure Container Apps or Azure App Service)
- Provides REST API endpoints for:
  - Authentication/authorization enforcement
  - Course, enrolment, content metadata
  - Assessments, submissions, grading
  - Progress tracking
  - AI tutor orchestration
  - Feedback collection
- Must be **stateless** (no global in-memory user state).

### 2.3 Relational Database (Azure Database for PostgreSQL)
- Stores LMS core data:
  - Users, roles, permissions
  - Courses, modules, lessons
  - Enrolments, progress
  - Assessments, submissions, grades
  - Chat sessions/messages (if persisted here)
  - Feedback, audit logs

### 2.4 Object Storage (Azure Blob Storage)
- Stores learning content and uploads:
  - PDFs, slides, videos (or links)
  - Assignment uploads (if file-based)
- Backend manages access control to blobs (no public sensitive blobs).

### 2.5 Session / Cache Store (Optional: Azure Redis Cache)
- Stores:
  - Auth/session optimisation (optional)
  - Per-user chat session state (optional)
  - Rate-limit counters (optional)
- Used to support horizontal scaling and performance.

---

## 3. External Systems (Outside the System)

### 3.1 Identity Provider (Microsoft Entra ID or JWT Auth Service)
- Handles login and token issuance/validation.
- Enables SSO (if Entra ID) or internal auth (if JWT).

### 3.2 Azure OpenAI
- Generates AI tutor responses.
- Receives prompts from backend and returns responses.

### 3.3 Observability (Application Insights / Azure Monitor)
- Collects:
  - Logs (API requests, errors, audit events)
  - Metrics (latency, error rate, throughput)
  - Traces (request correlation across dependencies)

### 3.4 Email / Notification Service (Optional)
- Sends announcements, enrolment confirmations, password resets.

---

## 4. C4 Level 2 – Container Diagram

```mermaid
flowchart LR

  subgraph SYS["Noventrax VLE/LMS"]
    FE["Web Frontend<br>(Azure Static Web Apps)"]
    API["Backend API<br>(FastAPI on Azure Container Apps/App Service)"]
    DB[("Relational Database<br>(Azure PostgreSQL)")]
    BLOB[("Object Storage<br>(Azure Blob Storage)")]
    REDIS[("Session/Cache Store<br>(Optional: Azure Redis Cache)")]
  end

  IdP[("Identity Provider<br>(Entra ID / JWT Auth)")]
  OpenAI[("Azure OpenAI")]
  Obs[("Observability<br>(App Insights / Azure Monitor)")]
  Notify[("Email / Notification Service")]

  FE -->|"HTTPS: REST/JSON"| API
  API -->|"SQL over TLS"| DB
  API -->|"Blob SDK over TLS"| BLOB
  API -->|"Cache/session ops"| REDIS

  API -->|"Authenticate / validate tokens"| IdP
  API -->|"Prompts / AI responses"| OpenAI
  API -->|"Logs, metrics, traces"| Obs
  API -->|"Send notifications"| Notify

