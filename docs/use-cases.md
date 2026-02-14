# Noventrax VLE/LMS  
## Use Case Specification

---
## 1. Purpose

This document defines the functional use cases of the Noventrax VLE/LMS.

It describes:

- Primary actors
- System interactions
- Core learning workflows
- Administrative workflows
- AI tutor integration use cases

This document helps prevent scope creep and ensures alignment between product goals and implementation.

---
# 2. Actors

| Actor | Description |
|--------|------------|
| Student | Learner consuming course content and completing assessments |
| Instructor | Course creator and assessor |
| Admin | Platform administrator responsible for governance and oversight |

---
# 3. High-Level Use Case Diagram

```mermaid
flowchart LR

  Student[Student]
  Instructor[Instructor]
  Admin[Admin]

  subgraph System["Noventrax VLE/LMS"]
    UC1["Authenticate"]
    UC2["Browse Courses"]
    UC3["Enrol in Course"]
    UC4["Access Lessons"]
    UC5["Submit Assessment"]
    UC6["View Grades"]
    UC7["Chat with AI Tutor"]
    UC8["Create / Edit Course"]
    UC9["Publish Course"]
    UC10["Grade Submission"]
    UC11["Manage Users & Roles"]
    UC12["View Audit Logs"]
  end

  Student --> UC1
  Student --> UC2
  Student --> UC3
  Student --> UC4
  Student --> UC5
  Student --> UC6
  Student --> UC7

  Instructor --> UC1
  Instructor --> UC8
  Instructor --> UC9
  Instructor --> UC10
  Instructor --> UC7

  Admin --> UC1
  Admin --> UC11
  Admin --> UC12
