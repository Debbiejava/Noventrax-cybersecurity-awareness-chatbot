# Noventrax VLE/LMS  
## RBAC (Role-Based Access Control) Matrix

---

## 1. Purpose

This document defines the **Role-Based Access Control (RBAC)** rules for the Noventrax VLE/LMS.

It provides:

- A clear permission matrix for Students, Instructors, and Admins
- Ownership constraints (e.g., “only for courses you teach”)
- Audit logging expectations for sensitive actions

RBAC must be enforced **server-side** by the Backend API.

---

## 2. Roles

| Role | Description |
|------|-------------|
| Student | Learner consuming content and completing assessments |
| Instructor | Course creator and assessor |
| Admin | Platform administrator responsible for governance and oversight |

---

## 3. Core RBAC Rules

### 3.1 General Enforcement Rules
- All protected endpoints require authentication.
- Authorization uses:
  - **Role checks** (Student/Instructor/Admin)
  - **Ownership checks** (resource belongs to user)
  - **Course assignment checks** (instructor assigned to course)
- No reliance on client-side restrictions.

### 3.2 Ownership & Scope Constraints
- Students can only access:
  - Courses they are enrolled in
  - Their own submissions and grades
  - Their own chat sessions/messages
- Instructors can only access:
  - Courses they created or are assigned to
  - Submissions for their courses
  - Grades for their courses
- Admin can access:
  - All system data (governance needs), but must be audited

---

## 4. RBAC Permission Matrix

Legend:
- ✅ Allowed
- ❌ Not allowed
- ⚠️ Allowed with constraints (ownership / course assignment / policy)

### 4.1 Identity & Profile

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| Sign in / authenticate | ✅ | ✅ | ✅ | Via IdP/JWT |
| View own profile | ✅ | ✅ | ✅ | Own data only |
| Update own profile | ✅ | ✅ | ✅ | Limited fields |
| View other user profiles | ❌ | ⚠️ | ✅ | Instructor: only enrolled students in their courses (optional) |
| Assign / change roles | ❌ | ❌ | ✅ | Must log to audit |

---

### 4.2 Course Catalogue & Enrolment

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| Browse published courses | ✅ | ✅ | ✅ | Students see Published only |
| Create course | ❌ | ✅ | ✅ | Admin optional |
| Edit course | ❌ | ⚠️ | ✅ | Instructor: only own/assigned courses |
| Publish/unpublish course | ❌ | ⚠️ | ✅ | Must audit |
| Archive course | ❌ | ⚠️ | ✅ | Must audit |
| Self-enrol in course | ⚠️ | ❌ | ✅ | If self-enrol enabled |
| Enrol student manually | ❌ | ⚠️ | ✅ | Instructor: only own/assigned courses |
| Withdraw enrolment | ✅ | ❌ | ✅ | Student can withdraw self |
| View enrolments | ⚠️ | ⚠️ | ✅ | Student: own; Instructor: own courses |

---

### 4.3 Content Delivery (Lessons & Materials)

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| View lessons/content | ⚠️ | ⚠️ | ✅ | Must be enrolled / assigned |
| Create modules/lessons | ❌ | ⚠️ | ✅ | Instructor: own/assigned course |
| Upload learning materials | ❌ | ⚠️ | ✅ | Stored in Blob, metadata in DB |
| Delete learning materials | ❌ | ⚠️ | ✅ | Must audit |
| Update lesson progress | ⚠️ | ❌ | ✅ | Student: own progress only |

---

### 4.4 Assessments & Submissions

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| View assessments | ⚠️ | ⚠️ | ✅ | Student: enrolled only |
| Create assessment | ❌ | ⚠️ | ✅ | Instructor: own courses |
| Edit assessment | ❌ | ⚠️ | ✅ | Must audit if published |
| Submit quiz/assignment | ⚠️ | ❌ | ✅ | Student: enrolled, assessment open |
| View submissions | ⚠️ | ⚠️ | ✅ | Student: own; Instructor: course submissions |
| Allow resubmission | ❌ | ⚠️ | ✅ | Policy-driven; must audit |

---

### 4.5 Grading & Feedback (High Risk)

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| Grade submission | ❌ | ⚠️ | ✅ | Instructor: assigned course only |
| View grades | ⚠️ | ⚠️ | ✅ | Student: own; Instructor: course grades |
| Modify grade after publish | ❌ | ⚠️ | ✅ | Append-only grading strongly recommended |
| Release grades to students | ❌ | ⚠️ | ✅ | Must audit |
| Add feedback comments | ❌ | ⚠️ | ✅ | Stored with grade; audit if changed |

---

### 4.6 AI Tutor (Chat)

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| Start chat session | ✅ | ✅ | ✅ | Per-user |
| View own chat history | ✅ | ✅ | ✅ | Own only |
| View other users’ chats | ❌ | ❌ | ⚠️ | Admin only if governance requires; must be audited |
| Delete chat session | ⚠️ | ⚠️ | ✅ | Subject to retention policy |
| Submit feedback | ✅ | ✅ | ✅ | Stored in DB |

---

### 4.7 Governance, Audit, and Monitoring

| Action | Student | Instructor | Admin | Notes |
|--------|---------|------------|-------|------|
| View audit logs | ❌ | ❌ | ✅ | Restricted |
| Export reports | ❌ | ⚠️ | ✅ | Instructor: own course reports only |
| View platform health metrics | ❌ | ❌ | ✅ | Restricted |
| Configure system settings | ❌ | ❌ | ✅ | Must audit |
| Data export for GDPR | ⚠️ | ⚠️ | ✅ | Users export own data; admin exports require policy |

---

## 5. Audit Logging Requirements (RBAC-Linked)

The following actions must always generate audit logs:

- Role changes
- Course publish/unpublish/archive
- Enrolment changes made by staff
- Assessment modifications after publishing
- Grade creation and grade modification
- Admin access to sensitive user data (including chat transcripts)
- Deletion of content, submissions, or grades (if allowed)

---

## 6. Implementation Notes

### Server-side authorization checks must include:
- Role validation (claims-based)
- Course assignment checks for instructors
- Enrolment checks for students
- Ownership checks on:
  - submissions
  - grades
  - chat sessions/messages
- Deny-by-default policy

---

**Document Version:** v1.0  
**Document Type:** RBAC Policy & Permission Matrix  
**Focus:** Authorization correctness and governance alignment
