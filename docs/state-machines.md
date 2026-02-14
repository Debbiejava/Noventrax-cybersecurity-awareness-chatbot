# Noventrax VLE/LMS  
## State Machine Diagrams (Core Lifecycles)

---

## 1. Purpose

This document defines the key **state machines** (lifecycles) required for correct VLE/LMS behaviour.

State machines reduce ambiguity in implementation by clarifying:

- Allowed states
- Valid transitions
- Who can trigger transitions
- What must be logged/audited
- What happens in edge cases (late submissions, regrades, withdrawals)

All diagrams use GitHub-compatible Mermaid syntax.

---

# 2. State Machine 1 — Course Lifecycle

A course moves from drafting to publication and eventually archival.

**Actors**
- Instructor: creates/updates/publishes/archives courses
- Admin: can override (optional)

**Audit**
- Log: publish, archive, restore events

```mermaid
stateDiagram-v2
  [*] --> Draft

  Draft --> Published: Publish
  Published --> Draft: Unpublish (optional)
  Published --> Archived: Archive
  Archived --> Published: Restore (optional)

  Draft --> Archived: Archive (optional)
  Archived --> [*]
```

# 3. State Machine 2 - Enrolment lifecycle

Tracks a student's enrolment status in a course
Actors

- Student: self-enrol (if enabled), withdraw
- Instructor/Admin: enrol student, mark completion, withdraw

Audit
- Log: enrolment created, withdrawn, completed

```mermaid
stateDiagram-v2
  [*] --> Active: Enrol

  Active --> Completed: Mark complete
  Active --> Withdrawn: Withdraw
  Active --> Suspended: Suspend (optional)

  Suspended --> Active: Reinstate (optional)
  Completed --> [*]
  Withdrawn --> [*]
```
Notes

- “Suspended” is optional (useful for policy enforcement).
- Access control checks should ensure only enrolled students in Active state can access learning materials and submit assessments.

# 4. State Machine 3 - Lesson progress lifecycle
Tracks completion for an individual lesson per enrolment.
Actors
- student : marks complete
- System: auto-complete

```mermaid
stateDiagram-v2
  [*] --> NotStarted
  NotStarted --> InProgress: Open lesson
  InProgress --> Completed: Mark complete
  Completed --> InProgress: Reopen (optional)
  Completed --> [*]

```
Notes
- "Reopen" can be allowed if you want flexible learning, but progress should not be deleted silently (keep timestamps)

# 5. State Machine 4 - Assessment availability lifecycle
Determines whether an assessment can accept submissions.
Actors
- Instructor/Admin: schedules assessment windows
```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Scheduled: Set open/due dates
  Draft --> Open: Publish now (no schedule)

  Scheduled --> Open: Open time reached
  Open --> Closed: Due time reached
  Closed --> Archived: Archive (optional)

  Draft --> Archived: Archive (optional)
  Archived --> [*]
```

# 6. State Machine 5 - Submission lifecycle (Quiz/Assignment)
Captures submissions and resubmissions, including late handling.
Actors
- Student: submit/resubmit
- Instructor/Admin: allow resubmission (policy-based)
Audit
- Log: initial submit, resubmit, late flag changes

```mermaid
stateDiagram-v2
  [*] --> NotSubmitted

  NotSubmitted --> Submitted: Submit
  Submitted --> Resubmitted: Resubmit (allowed)
  Submitted --> LateSubmitted: Submit after due date
  Resubmitted --> LateSubmitted: Resubmit after due date

  LateSubmitted --> Graded: Grade
  Submitted --> Graded: Grade
  Resubmitted --> Graded: Grade

  Graded --> RegradeRequested: Appeal (optional)
  RegradeRequested --> Graded: Regrade complete

  Graded --> [*]

```

# 7. State Machine 6 — Grading Lifecycle (Governance Focus)

Ensures grade changes are traceable and auditable.
Actors
- Instructor: grade/regrade
- Admin: override (optional)
Audit
- Log: grade created, grade updated, override reason

```mermaid
stateDiagram-v2
  [*] --> NotGraded
  NotGraded --> DraftGrade: Create grade (optional)
  DraftGrade --> FinalGrade: Publish grade
  NotGraded --> FinalGrade: Grade (direct)

  FinalGrade --> Regraded: Update grade
  Regraded --> FinalGrade: Confirm updated grade

  FinalGrade --> Overridden: Admin override (optional)
  Overridden --> FinalGrade: Confirm override

  FinalGrade --> [*]

```

# 8. State Machine 7 — AI Tutor Chat Session Lifecycle

Manages chat sessions per user and per course context.

Actors
- Student/Instructor: create/use sessions
- System: expire sessions (optional)

```mermaid
stateDiagram-v2
  [*] --> Active
  Active --> Active: Add message
  Active --> Closed: User ends session (optional)
  Active --> Expired: Inactivity timeout (optional)

  Closed --> [*]
  Expired --> [*]
```


# 9. Policy Hooks (Where rules must be enforced)

- Course state controls catalogue visibility (only Published visible to students).

- Enrolment state controls access (only Active can access content and submit).

- Assessment state controls submissions (only Open accepts submissions).

- Submission state controls grading and resubmissions.

- Grade lifecycle controls governance and audit logging.

- Chat session lifecycle controls retention and privacy.
