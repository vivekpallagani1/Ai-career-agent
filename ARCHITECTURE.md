# AI Career Agent — Technical Architecture

This document describes the system design, component relationships, and data flows.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                    React + Vite Frontend                     │
│  (Dashboard, Jobs, Resume Manager, Interview Prep)          │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/WebSocket (REST API)
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Routes (/api/v1)                                │  │
│  │  • Auth (register, login)                           │  │
│  │  • Jobs (list, search, match)                       │  │
│  │  • Profiles (create, read, update)                  │  │
│  │  • Applications (track, update)                     │  │
│  │  • Resumes (upload, extract)                        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Services (Business Logic)                           │  │
│  │  • JobMatchingService                               │  │
│  │  • ResumeParserService                              │  │
│  │  • FraudDetectionService                            │  │
│  │  • CareerIntelligenceService                        │  │
│  │  • AgentOrchestrator                                │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Data Layer                                          │  │
│  │  • SQLAlchemy ORM                                   │  │
│  │  • Repositories (UserRepo, JobRepo, etc.)           │  │
│  └──────────────────────────────────────────────────────┘  │
└──────┬──────────────────────┬─────────────────────┬────────┘
       │                      │                     │
       │                      │                     │
┌──────▼────────┐   ┌────────▼────────┐   ┌──────▼───────┐
│  PostgreSQL   │   │     Redis       │   │   Celery     │
│  + pgvector   │   │   Cache/Queue   │   │    Worker    │
│               │   │                 │   │   (Async)    │
│ • users       │   │ • Session cache │   │              │
│ • jobs        │   │ • Task queue    │   │ • Parse      │
│ • resumes     │   │ • Rate limits   │   │   Resume     │
│ • profiles    │   │ • Results cache │   │ • Extract    │
│ • apps        │   │                 │   │   Jobs       │
└───────────────┘   └─────────────────┘   └──────────────┘
```

## Component Descriptions

### Frontend (React + Vite)

**Architecture:**
- **Single Page Application (SPA)** with client-side routing
- **Component-based** UI with reusable components
- **Global state** management via Zustand (auth store)
- **Data fetching** via TanStack Query (caching, background sync)
- **Styling** with Tailwind CSS + utility classes

**Key Modules:**

1. **Pages** (`src/pages/`)
   - `LoginPage.tsx` — Authentication UI
   - `Dashboard.tsx` — Career overview and stats
   - `JobsPage.tsx` — Job discovery and search
   - Future: `ResumeManager.tsx`, `ApplicationTracker.tsx`, `CareerRoadmap.tsx`

2. **Layouts** (`src/layouts/`)
   - `AppLayout.tsx` — Authenticated app container with sidebar
   - `AuthLayout.tsx` — Login/register page wrapper

3. **Services** (`src/services/`)
   - `api.ts` — HTTP client with axios, JWT token injection, auth error handling

4. **Store** (`src/store/`)
   - `auth.ts` — Zustand store for user authentication state

5. **Hooks** (`src/hooks/`)
   - `useAsync.ts` — Reusable hook for async operations

**Data Flow:**
```
User Action → React Component → API Call (axios) 
  → Backend Endpoint → Response → Zustand Store Update 
  → Component Re-render → UI Update
```

### Backend (FastAPI)

**Architecture:**
- **Layered Design** with clear separation of concerns
- **Async/Await** for high concurrency
- **Middleware** for CORS, request logging, error handling
- **Dependency Injection** via FastAPI's `Depends()`
- **Type Safety** with Pydantic schemas and SQLAlchemy models

**Layer Structure:**

```
API Routes (handlers)
  ↓ (request validation via Pydantic schemas)
Services (business logic)
  ↓ (orchestrate operations, call multiple repos)
Repositories (data access)
  ↓ (translate domain models to/from DB)
SQLAlchemy Models (database layer)
  ↓
PostgreSQL Database
```

**Key Modules:**

1. **API Routes** (`app/api/v1/endpoints/`)
   - `auth.py` — Register, login, logout
   - `jobs.py` — List, search, get job, calculate match
   - `profiles.py` — Get, create, update candidate profile
   - `applications.py` (future) — Track and manage applications
   - `resumes.py` (future) — Upload and extract resumes
   - `health.py` — Health check endpoint

2. **Services** (`app/services/`)
   - `job_matching.py` — Weighted score calculation
   - `resume_parser.py` — Extract data from resumes
   - `fraud_detection.py` (future) — Risk scoring
   - `career_intelligence.py` (future) — Analytics and insights

3. **Repositories** (`app/repositories/`)
   - `user_repository.py` — User CRUD operations
   - `job_repository.py` — Job queries and search
   - `profile_repository.py` — Candidate profile operations
   - More as needed per domain

4. **Models** (`app/models/`)
   - `user.py` — User account model
   - `profile.py` — Candidate profile model
   - `job.py` — Job listing model
   - `resume.py` — Resume document model
   - `application.py` — Job application model

5. **Schemas** (`app/schemas/`)
   - Pydantic models for request/response validation
   - Separate request (UserRegisterRequest) and response (UserResponse) schemas
   - Field validation, examples, documentation

6. **Core** (`app/core/`)
   - `config.py` — Settings from environment variables
   - `security.py` — JWT token handling, password hashing
   - `dependencies.py` — Dependency injection setup (e.g., `get_db`)

7. **Jobs/Queue** (`app/jobs/`)
   - `celery_app.py` — Celery configuration
   - `tasks.py` — Async background tasks
   - Example: `process_job_feed()`, `parse_resume_async()`

8. **Agents** (`app/agents/`)
   - `orchestrator.py` — Routes actions to correct agent or service
   - Example: User toggles "auto-discover jobs" → orchestrator queues Celery task

### Database (PostgreSQL + pgvector)

**Schema:**

```sql
users
├── id (PK)
├── email (UNIQUE)
├── hashed_password
├── name
└── role (candidate | admin)

candidate_profiles
├── id (PK)
├── user_id (FK → users.id)
├── location
├── phone
├── bio
├── profile_completeness (0-100)
├── target_roles (JSON)
├── preferred_locations (JSON)
├── min_salary
├── max_salary
└── experience_level

jobs
├── id (PK)
├── external_id (UNIQUE) — from job board API
├── title
├── company
├── location
├── salary_min, salary_max
├── description (FULL TEXT indexed)
├── employment_type
├── seniority_level
├── parsed_data (JSON) — extracted skills, requirements
├── source (LinkedIn, Indeed, etc.)
├── posted_at
└── fraud_score (0-100)

resumes
├── id (PK)
├── user_id (FK)
├── filename
├── file_path
├── is_primary
├── status (pending | processing | ready | failed)
├── extracted_data (JSON) — skills, experience, education
└── created_at

applications
├── id (PK)
├── user_id (FK)
├── job_id (FK)
├── status (saved | preparing | applied | screening | interview | offer | rejected)
├── resume_used (FK → resumes.id)
├── match_score (0-100)
├── notes
├── created_at
└── updated_at
```

**Indexing Strategy:**
- Primary keys (id)
- Foreign keys (user_id, job_id)
- Unique constraints (email, external_id)
- Search indexes (title, company, description in jobs)
- pgvector embedding index on job descriptions (future)

### Caching & Queue (Redis)

**Cache:**
- Session tokens (short-lived, ~1 hour)
- Job match scores (avoid recomputation)
- User profile data (sync across services)
- Rate limiting buckets

**Queue (Celery):**
- Resume parsing (CPU-intensive, async)
- Job discovery ingestion (scheduled, bulk)
- Fraud analysis (expensive ML model)
- Email notifications
- Report generation

Example task flow:
```
1. User uploads resume
2. Route handler enqueues `parse_resume_async(resume_id)` task
3. Celery worker picks up task from Redis queue
4. Worker calls ResumeParserService
5. Updates resume.status to 'ready' + extracted_data
6. Frontend polls or webhooks receive update
7. UI displays extracted skills, education, etc.
```

### Async Task Worker (Celery)

**Configuration:**
- `BROKER_URL` = Redis (task queue)
- `RESULT_BACKEND` = Redis (task results cache)
- Workers run independently, scale horizontally
- Task routing via queue names

**Typical Tasks:**
```python
@celery_app.task
def parse_resume_async(resume_id: int):
    # Fetch from DB, call service, update DB
    pass

@celery_app.task
def ingest_jobs_from_source(source: str):
    # Query job API, normalize, deduplicate, insert
    pass

@celery_app.task
def calculate_fraud_scores_batch(job_ids: list[int]):
    # Run ML model, update fraud_score column
    pass
```

## Data Flow Examples

### Authentication Flow

```
1. User enters email/password in LoginPage
2. Frontend calls api.login(email, password)
3. API POST /auth/login with UserLoginRequest payload
4. Backend handler:
   - Validates schema
   - Queries UserRepository.get_by_email()
   - Verifies password with verify_password()
   - Creates JWT token via create_access_token()
   - Returns {access_token, user}
5. Frontend stores token in localStorage
6. Subsequent API calls inject token in Authorization header
7. Backend middleware verifies token in request
```

### Job Matching Flow

```
1. User browses jobs, clicks "View Details & Match"
2. Frontend calls api.calculateJobMatch(jobId)
3. POST /jobs/{id}/match triggered
4. Backend handler:
   - Extracts user_id from JWT token
   - Gets job from JobRepository
   - Gets candidate profile from ProfileRepository
   - Calls JobMatchingService.score_candidate_job()
     - Compares skills (exact + fuzzy matching)
     - Analyzes experience level alignment
     - Checks education requirements
     - Scores location match
     - Weights all factors
   - Returns JobMatchScoreResponse
5. Frontend displays match score with breakdown
6. Optional: Cache result in Redis for 24 hours
```

### Resume Parsing Flow

```
1. User uploads resume file on Resume Manager page
2. Frontend calls api.uploadResume(file)
3. Multipart form handler:
   - Saves file to object storage (S3 or local)
   - Creates Resume DB record (status='pending')
   - Enqueues parse_resume_async(resume_id) task to Celery
   - Returns {resume_id, status: 'processing'}
4. Frontend polls GET /resumes/{id} for status updates
5. Celery worker:
   - Fetches resume from storage
   - Calls ResumeParserService.parse()
   - Extracts skills, education, experience, projects
   - Updates Resume.extracted_data (JSON)
   - Updates Resume.status = 'ready'
   - Triggers notification (optional)
6. Frontend receives 'ready' status, displays extracted data
7. User can edit and approve extracted fields
8. Approved data syncs to CandidateProfile
```

## Authentication & Security

**JWT Token Flow:**

1. User logs in → Backend creates JWT with `{sub: email, user_id: id, exp: tomorrow}`
2. Token signed with `JWT_SECRET` (HS256)
3. Frontend stores in localStorage
4. Each request includes `Authorization: Bearer <token>`
5. Backend middleware decodes and validates token
6. If invalid/expired → 401 Unauthorized

**Password Security:**

1. Registration: plaintext → hash with bcrypt → store hash
2. Login: plaintext → hash → compare with stored hash
3. Never store plaintext passwords

**API Authorization:**

- All protected routes check JWT token
- Extract `user_id` from token
- Verify user owns the resource (profile, application, etc.)
- Admin routes check `role == 'admin'`

## Scalability Considerations

### Horizontal Scaling

**Frontend:**
- Deploy to CDN (Vercel, Netlify, CloudFront)
- Static assets cached at edge
- API requests go to backend via API Gateway

**Backend:**
- Stateless FastAPI servers behind load balancer
- Scale workers up/down based on CPU/memory
- Session/auth state in Redis, not memory

**Database:**
- Read replicas for analytics queries
- Connection pooling (PgBouncer)
- Partitioning large tables (jobs, applications)
- Full-text search indexes

**Cache & Queue:**
- Redis Cluster for high availability
- Multiple Celery workers for task processing
- Dead-letter queue for failed tasks

### Performance Optimization

1. **Caching:**
   - Job matches cached 24 hours
   - User profiles cached after fetch
   - Invalidate on update

2. **Pagination:**
   - Jobs API: limit=20, offset=0 by default
   - Cursor-based pagination for large datasets

3. **Async Processing:**
   - Resume parsing → background task
   - Job ingestion → scheduled Celery task
   - Notifications → queued, not blocking

4. **Indexing:**
   - Database indexes on foreign keys, search columns
   - pgvector embeddings for semantic search

5. **API Design:**
   - Only fetch required fields
   - Combine related queries (avoid N+1)
   - Rate limiting (via Redis)

## Monitoring & Observability

**Logging:**
- FastAPI middleware logs all requests/responses
- Service layer logs business logic errors
- Celery worker logs task execution

**Metrics:**
- API response times (latency)
- Error rates by endpoint
- Queue depth (pending tasks)
- Database query times
- Cache hit/miss rates

**Health Checks:**
- `GET /api/v1/health` returns service status
- Checks database connectivity
- Checks Redis connectivity
- Checks Celery worker availability

**Error Tracking:**
- Log exceptions with full stack traces
- Send critical errors to monitoring tool (Sentry, etc.)
- Alert on >5% error rate

## Deployment Architecture

```
┌────────────────────────────────────┐
│        GitHub / Git Repo           │
└─────────────────┬──────────────────┘
                  │
        ┌─────────▼─────────┐
        │  CI/CD Pipeline   │
        │ (GitHub Actions)  │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼────┐  ┌────▼────┐
│ Build  │  │  Test   │  │ Docker  │
│ Frontend│  │ Backend │  │ Build   │
└───┬────┘  └────┬────┘  └────┬────┘
    │           │           │
┌───▼───────────▼───────────▼──┐
│      Push to Registry         │
│   (ECR, Docker Hub)           │
└────────────┬──────────────────┘
             │
    ┌────────▼────────┐
    │   Deploy         │
    │  (AWS ECS, K8s)  │
    └─────────────────┘
```

---

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for deployment instructions.
