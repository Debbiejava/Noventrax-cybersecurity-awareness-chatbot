# Noventrax VLE/LMS  
## Security Architecture & Threat Model

---

## 1. Purpose

This document defines the security architecture of the Noventrax VLE/LMS and outlines:

- Threat model (STRIDE-based)
- Authentication and authorization model
- Data protection controls
- Logging and audit strategy
- Secure deployment considerations
- Risk mitigation controls

This document supports compliance (GDPR), governance, and secure-by-design implementation.

---

# 2. Security Principles

The system is designed according to the following principles:

- Least privilege
- Zero trust between components
- Defense in depth
- Secure by default configuration
- Data minimisation
- Server-side enforcement of all access controls
- No reliance on client-side validation for security

---

# 3. Authentication & Authorization Model

## 3.1 Authentication (AuthN)

Supported models:

- Microsoft Entra ID (SSO)
- OR JWT-based authentication

Authentication requirements:

- All API endpoints must require valid authentication tokens.
- Tokens must be validated server-side.
- Tokens must expire.
- Refresh tokens (if used) must be securely stored.

---

## 3.2 Authorization (AuthZ)

Authorization is enforced using:

- Role-Based Access Control (RBAC)
- Resource ownership checks

Roles:

- Student
- Instructor
- Admin

Examples:

- A student can only view their own submissions.
- An instructor can only grade submissions for courses they manage.
- Only admins can modify user roles.
- No user can access another user’s chat session.

Authorization is enforced **server-side only**.

---

# 4. Threat Model (STRIDE Analysis)

This section evaluates threats across trust boundaries.

---

## 4.1 Spoofing Identity

Threat:
- Attacker impersonates another user.

Mitigation:
- Strong authentication (SSO or signed JWT).
- Token validation on every request.
- HTTPS enforced.
- Secure session handling.

---

## 4.2 Tampering with Data

Threat:
- Manipulation of grades, enrolments, or submissions.
- Modification of API requests.

Mitigation:
- Parameterised database queries.
- Server-side validation.
- Immutable audit logs.
- Role-based enforcement.
- Input sanitisation.

---

## 4.3 Repudiation

Threat:
- User denies performing an action (e.g., grade change).

Mitigation:
- Audit logging of:
  - Login events
  - Grade changes
  - Role changes
  - Course publishing
- Logs stored securely and retained per policy.

---

## 4.4 Information Disclosure

Threat:
- Cross-user data leakage.
- Exposure of personal data.
- Prompt injection leaking hidden context.

Mitigation:
- Per-user chat session isolation.
- Ownership checks before returning data.
- No global in-memory state.
- Strict access control checks.
- Avoid storing sensitive data in prompts.
- Encrypted storage at rest.
- TLS for all communications.

---

## 4.5 Denial of Service (DoS)

Threat:
- API flooding.
- AI usage abuse.
- Resource exhaustion.

Mitigation:
- API rate limiting.
- Request size limits.
- Per-user usage monitoring.
- Auto-scaling backend.
- Graceful degradation if AI service unavailable.

---

## 4.6 Elevation of Privilege

Threat:
- Student gains instructor/admin privileges.

Mitigation:
- Server-side RBAC enforcement.
- No trust in client-side role indicators.
- Admin-only role assignment endpoints.
- Token claim validation.

---

# 5. AI-Specific Security Controls

## 5.1 Prompt Injection Risk

Threat:
- Malicious user attempts to override system instructions.
- Attempts to extract hidden system prompts or sensitive data.

Mitigation:
- System prompt isolation.
- No exposure of secrets in prompts.
- No inclusion of other users' data in context.
- Sanitised user input.
- Controlled prompt construction.

---

## 5.2 Cross-User Data Leakage

Threat:
- Chat history shared between users.

Mitigation:
- Chat sessions stored per user.
- No global in-memory conversation state.
- Database isolation by user_id.
- Strict ownership validation before retrieval.

---

## 5.3 Model Output Risks

Threat:
- Harmful or unsafe AI responses.

Mitigation:
- Content filtering.
- Moderation layer (if implemented).
- Output sanitisation before rendering.
- Clear disclaimers where appropriate.

---

# 6. Data Protection Controls

## 6.1 Encryption

- HTTPS enforced for all traffic.
- TLS between backend and database.
- Encryption at rest for database and blob storage.
- Secrets stored in Azure Key Vault or secure App Settings.

---

## 6.2 Access Control to Storage

- Blob access restricted via backend.
- No public containers for sensitive content.
- Role-based authorization before generating file access URLs.

---

## 6.3 Data Minimisation

- Only required personal data collected.
- Avoid storing unnecessary personal metadata in chat logs.
- Chat logs subject to retention limits.

---

# 7. Logging & Audit Strategy

The system must log:

- Authentication attempts (success/failure)
- Role assignments and changes
- Course publishing
- Assessment creation
- Grade modifications
- Admin actions
- API errors

Audit logs must:

- Be append-only
- Include timestamp and actor ID
- Be protected from modification
- Be retained per policy

---

# 8. Secure Deployment Controls

- Separate Dev/Test/Prod environments.
- Secrets not committed to source control.
- CI/CD pipeline secured via GitHub Secrets.
- Dependency scanning enabled (Dependabot).
- Minimal container base image.
- Non-root container user (recommended).
- Environment variable validation on startup.

---

# 9. Dependency & Supply Chain Security

Risks:

- Vulnerable third-party packages.
- Malicious package injection.
- Outdated libraries.

Mitigations:

- Version pinning in requirements.txt.
- Automated vulnerability scanning.
- Regular dependency updates.
- Minimal dependency surface.

---

# 10. Incident Response Overview

In case of a security incident:

1. Contain (disable affected feature/service).
2. Preserve logs.
3. Identify root cause.
4. Patch vulnerability.
5. Notify stakeholders (if required by law).
6. Document post-incident review.

---

# 11. Security Responsibilities Matrix

| Area | Responsibility |
|------|---------------|
| Authentication | Backend |
| Authorization | Backend |
| Input validation | Backend |
| Output sanitisation | Backend |
| Rate limiting | Backend |
| Secret management | Infrastructure |
| Role management | Admin |
| Monitoring & alerts | DevOps/Admin |

---

# 12. Future Security Enhancements

- Multi-factor authentication (MFA)
- Advanced AI moderation
- File virus scanning
- Web Application Firewall (WAF)
- Security Information & Event Management (SIEM) integration

---

**Document Version:** v1.0  
**Document Type:** Security Architecture & Threat Model  
**Compliance Alignment:** GDPR-aligned, STRIDE-informed, Secure-by-Design

