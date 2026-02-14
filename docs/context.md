# Noventrax VLE/LMS  
## C4 Level 1 – System Context Diagram

---

## 1. Purpose

This diagram presents the **system context** for the Noventrax Virtual Learning Environment (VLE) and Learning Management System (LMS).

It shows:

- The system boundary
- Primary user roles
- External systems the platform depends on
- High-level interactions between actors and the system

This level does **not** show internal technical components (those appear in the Container Diagram).

---

## 2. System Overview

**System Name:** Noventrax VLE/LMS  

**Description:**  
A secure, AI-enhanced digital learning platform that combines:

- Structured course delivery (VLE)
- Course management and assessment (LMS)
- Integrated AI learning assistant
- Governance, audit, and role-based access control

---

## 3. Actors (Users)

- **Student**  
  Access courses, complete lessons, submit assignments, view grades, interact with AI tutor.

- **Instructor**  
  Create and publish courses, upload learning materials, create assessments, grade submissions, monitor learner progress.

- **Admin**  
  Manage users and roles, oversee governance, access audit logs, monitor system health and analytics.

---

## 4. External Systems

- **Identity Provider (e.g., Microsoft Entra ID or JWT Authentication Service)**  
  Handles authentication and token validation.

- **Azure OpenAI**  
  Provides AI-generated tutoring responses.

- **Cloud Storage (e.g., Azure Blob Storage)**  
  Stores learning materials and assignment uploads.

- **Email / Notification Service**  
  Sends enrolment confirmations, password resets, and announcements.

- **Observability Platform (e.g., Azure Application Insights / Azure Monitor)**  
  Collects logs, metrics, traces, and alerts.

---

## 5. C4 Level 1 – System Context Diagram

```mermaid
flowchart LR

  %% Users
  Student([Student])
  Instructor([Instructor])
  Admin([Admin])

  %% System Boundary
  subgraph SYS[Noventrax VLE/LMS]
    VLELMS["AI-Enhanced Learning Platform<br>(VLE + LMS)"]
  end

  %% External Systems
  IdP[(Identity Provider)]
  OpenAI[(Azure OpenAI)]
  Storage[(Cloud Storage)]
  Notify[(Email / Notification Service)]
  Obs[(Observability Platform)]

  %% User Interactions
  Student -->|Access courses,\nsubmit assignments,\nview grades,\nchat with AI tutor| VLELMS
  Instructor -->|Create courses,\nmanage content,\ngrade submissions| VLELMS
  Admin -->|Manage users & roles,\naudit & reporting| VLELMS

  %% System Integrations
  VLELMS -->|Authenticate users /\nvalidate tokens| IdP
  VLELMS -->|Send prompts /\nreceive AI responses| OpenAI
  VLELMS -->|Store & retrieve\nlearning materials| Storage
  VLELMS -->|Send notifications| Notify
  VLELMS -->|Send logs, metrics,\ntraces & alerts| Obs

