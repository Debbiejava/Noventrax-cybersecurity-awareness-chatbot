# Noventrax VLE/LMS  
## Deployment Architecture & Operational Model

---

## 1. Purpose

This document defines the deployment architecture, infrastructure components, CI/CD model, environment strategy, scaling approach, and disaster recovery planning for the Noventrax VLE/LMS.

This document aligns with:

- Azure-based hosting
- Secure-by-design principles
- High availability goals
- GDPR and governance requirements

---

# 2. High-Level Deployment Architecture

The Noventrax VLE/LMS is deployed on Microsoft Azure using a cloud-native architecture.

---

## 2.1 Core Infrastructure Components

### Frontend
- **Azure Static Web Apps**
- Hosts the SPA (HTML/CSS/JS or future framework)
- Global CDN-backed delivery
- Automatic HTTPS

### Backend API
- **Azure Container Apps** (Recommended)  
  OR  
- Azure App Service (if standardised)

Runs:
- FastAPI application
- Gunicorn + Uvicorn worker
- Stateless design (no in-memory session persistence)

### Database
- **Azure Database for PostgreSQL**
- Stores LMS core data
- Encrypted at rest
- Automated backups enabled

### Object Storage
- **Azure Blob Storage**
- Stores:
  - Course materials
  - Assignment uploads
- Private containers only

### Session/Cache (Optional)
- **Azure Redis Cache**
- Used for:
  - Session optimisation
  - Rate limiting counters
  - Chat state caching

### AI Service
- **Azure OpenAI**
- Provides AI tutor functionality

### Observability
- **Azure Application Insights**
- Azure Monitor
- Log Analytics Workspace

---

# 3. Deployment Diagram (Mermaid)

```mermaid
flowchart LR

  GitHub[(GitHub Repository)]

  subgraph CI_CD["CI/CD Pipeline"]
    Actions[GitHub Actions]
  end

  subgraph Azure["Microsoft Azure"]
    SWA["Static Web Apps"]
    API["Container Apps / App Service"]
    DB[("Azure PostgreSQL")]
    BLOB[("Azure Blob Storage")]
    REDIS[("Azure Redis (Optional)")]
    OPENAI[("Azure OpenAI")]
    MONITOR[("App Insights / Monitor")]
  end

  GitHub --> Actions
  Actions --> SWA
  Actions --> API

  SWA -->|HTTPS| API
  API --> DB
  API --> BLOB
  API --> REDIS
  API --> OPENAI
  API --> MONITOR

