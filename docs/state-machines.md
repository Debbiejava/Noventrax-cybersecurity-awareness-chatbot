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
