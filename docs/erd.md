# Noventrax VLE/LMS  
## ERD – Entity Relationship Diagram (Domain Model)

---

## 1. Purpose

This ERD defines the **core data model** for the Noventrax VLE/LMS, including:

- Users and role-based access control (RBAC)
- Course structure (courses → modules → lessons)
- Enrolment and progress tracking
- Assessments, submissions, grading, and feedback
- AI tutor sessions and messages
- Audit logging for governance

This ERD is implementation-agnostic and can be mapped directly to a relational database such as **PostgreSQL**.

---

## 2. Core Entities

### 2.1 Identity & Access (RBAC)
- **users**: platform users
- **roles**: student/instructor/admin
- **user_roles**: many-to-many mapping of users to roles (supports multi-role users)

### 2.2 Learning Structure
- **courses**: learning units owned by instructors
- **course_instructors**: many-to-many mapping for multiple instructors per course
- **modules**: course sections
- **lessons**: learning items inside modules
- **content_items**: lesson materials (text, link, file reference)

### 2.3 Enrolment & Progress
- **enrolments**: joins students to courses + status
- **lesson_progress**: tracks completion of lessons per student

### 2.4 Assessments & Grading
- **assessments**: quizzes/assignments attached to courses
- **questions**: quiz questions
- **submissions**: student submissions (quiz answers or assignment uploads)
- **grades**: grading records + feedback notes (audit-friendly)

### 2.5 AI Tutor
- **chat_sessions**: per-user sessions (optionally tied to course/module)
- **chat_messages**: messages belonging to a chat session

### 2.6 Governance
- **feedback**: product feedback (rating/comment/page URL)
- **audit_logs**: immutable trail of key actions (role changes, grade changes, etc.)

---

## 3. ER Diagram (Mermaid)

> Paste this in GitHub to render the ERD diagram.

```mermaid
erDiagram

  USERS ||--o{ USER_ROLES : has
  ROLES ||--o{ USER_ROLES : assigned

  USERS ||--o{ COURSE_INSTRUCTORS : teaches
  COURSES ||--o{ COURSE_INSTRUCTORS : managed_by

  COURSES ||--o{ MODULES : contains
  MODULES ||--o{ LESSONS : contains
  LESSONS ||--o{ CONTENT_ITEMS : includes

  USERS ||--o{ ENROLMENTS : enrolls
  COURSES ||--o{ ENROLMENTS : has

  ENROLMENTS ||--o{ LESSON_PROGRESS : tracks
  LESSONS ||--o{ LESSON_PROGRESS : completion_of

  COURSES ||--o{ ASSESSMENTS : has
  ASSESSMENTS ||--o{ QUESTIONS : includes
  ASSESSMENTS ||--o{ SUBMISSIONS : receives
  USERS ||--o{ SUBMISSIONS : submits

  SUBMISSIONS ||--o{ GRADES : graded_as
  USERS ||--o{ GRADES : graded_by

  USERS ||--o{ CHAT_SESSIONS : starts
  CHAT_SESSIONS ||--o{ CHAT_MESSAGES : contains
  COURSES ||--o{ CHAT_SESSIONS : context_for

  USERS ||--o{ FEEDBACK : provides

  USERS ||--o{ AUDIT_LOGS : triggers

  USERS {
    uuid id PK
    string full_name
    string email UK
    string password_hash "nullable if SSO"
    boolean is_active
    datetime created_at
    datetime updated_at
  }

  ROLES {
    int id PK
    string name UK "Student|Instructor|Admin"
    string description
  }

  USER_ROLES {
    uuid user_id FK
    int role_id FK
    datetime assigned_at
  }

  COURSES {
    uuid id PK
    string title
    string description
    string status "Draft|Published|Archived"
    datetime created_at
    datetime updated_at
  }

  COURSE_INSTRUCTORS {
    uuid course_id FK
    uuid user_id FK
    datetime added_at
  }

  MODULES {
    uuid id PK
    uuid course_id FK
    string title
    int sort_order
  }

  LESSONS {
    uuid id PK
    uuid module_id FK
    string title
    string lesson_type "Reading|Video|Lab|Discussion"
    int sort_order
  }

  CONTENT_ITEMS {
    uuid id PK
    uuid lesson_id FK
    string content_type "Text|Link|File"
    string title
    string body_text "nullable"
    string url "nullable"
    string blob_path "nullable"
  }

  ENROLMENTS {
    uuid id PK
    uuid user_id FK
    uuid course_id FK
    string status "Active|Completed|Withdrawn"
    datetime enrolled_at
    datetime completed_at "nullable"
  }

  LESSON_PROGRESS {
    uuid id PK
    uuid enrolment_id FK
    uuid lesson_id FK
    boolean is_completed
    datetime completed_at "nullable"
  }

  ASSESSMENTS {
    uuid id PK
    uuid course_id FK
    string title
    string assessment_type "Quiz|Assignment"
    datetime open_at "nullable"
    datetime due_at "nullable"
    int max_score
  }

  QUESTIONS {
    uuid id PK
    uuid assessment_id FK
    string question_type "MCQ|ShortAnswer"
    string prompt
    string options_json "nullable"
    string correct_answer "nullable"
    int points
  }

  SUBMISSIONS {
    uuid id PK
    uuid assessment_id FK
    uuid user_id FK
    string submission_type "QuizAnswers|FileUpload|Text"
    string answers_json "nullable"
    string text_answer "nullable"
    string file_blob_path "nullable"
    datetime submitted_at
    string status "Submitted|Resubmitted|Late"
  }

  GRADES {
    uuid id PK
    uuid submission_id FK
    uuid graded_by_user_id FK
    int score
    string feedback_text "nullable"
    datetime graded_at
    boolean is_final
  }

  CHAT_SESSIONS {
    uuid id PK
    uuid user_id FK
    uuid course_id FK "nullable"
    string title "nullable"
    datetime created_at
    datetime updated_at
  }

  CHAT_MESSAGES {
    uuid id PK
    uuid session_id FK
    string role "system|user|assistant"
    string content
    datetime created_at
  }

  FEEDBACK {
    uuid id PK
    uuid user_id FK "nullable if anonymous"
    int rating "nullable"
    string comment
    string page_url "nullable"
    datetime created_at
  }

  AUDIT_LOGS {
    uuid id PK
    uuid actor_user_id FK
    string action
    string target_type "User|Course|Grade|Assessment|Content"
    uuid target_id "nullable"
    string metadata_json "nullable"
    datetime created_at
  }

