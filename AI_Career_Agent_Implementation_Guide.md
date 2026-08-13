# AI Career Agent — Full Implementation Guide (Scratch → Deployment)

This is the complete build guide: environment setup, detailed requirements, every screen with its UI elements, database, build sequence, and deployment.

---

# PART A — ENVIRONMENT SETUP (From Scratch)

## A1. Install Prerequisites

| Tool | Purpose | Version |
|---|---|---|
| Python | Backend | 3.11+ |
| Node.js | Frontend | 20+ |
| PostgreSQL | Database (+ pgvector extension) | 15+ |
| Redis | Cache/Queue | 7+ |
| Docker & Docker Compose | Containerization | latest |
| Git | Version control | latest |

## A2. Initialize the Repository

```bash
mkdir ai-career-agent && cd ai-career-agent
git init
mkdir -p frontend backend ai infrastructure docs tests scripts
touch README.md .env.example docker-compose.yml .gitignore
```

`.gitignore` should exclude: `.env`, `node_modules/`, `__pycache__/`, `*.pyc`, `venv/`, `dist/`, `.DS_Store`.

## A3. Backend Skeleton

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings \
            psycopg2-binary redis celery python-multipart python-jose passlib \
            bcrypt pytest httpx
```

```
backend/
├── app/
│   ├── main.py
│   ├── core/          # config, security, dependencies
│   ├── models/         # SQLAlchemy models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── api/v1/          # route files per module
│   ├── services/        # business logic
│   ├── repositories/    # DB access layer
│   ├── agents/           # AI agent classes
│   ├── ai/               # LLM client, prompt loader, embeddings
│   ├── jobs/              # Celery tasks
│   └── fraud/, matching/, applications/, career/
├── tests/
├── alembic/
└── requirements.txt
```

## A4. Frontend Skeleton

```bash
cd ../frontend
npm create vite@latest . -- --template react-ts
npm install tailwindcss @tanstack/react-query react-router-dom recharts axios zustand
npx tailwindcss init -p
```

```
frontend/src/
├── pages/            # one folder per screen (see Part C)
├── components/       # shared UI components
├── layouts/           # AppLayout, AuthLayout
├── hooks/
├── services/           # API client per module
├── store/               # Zustand/global state
└── types/
```

## A5. Docker Compose (local dev)

Services to define: `frontend`, `backend`, `worker` (Celery), `postgres` (with pgvector), `redis`. Backend and worker share the same image; worker overrides the container command to run `celery -A app.jobs.celery_app worker`.

## A6. Environment Variables (`.env.example`)

```
DATABASE_URL=postgresql://user:pass@postgres:5432/career_agent
REDIS_URL=redis://redis:6379/0
JWT_SECRET=
JWT_EXPIRY_MINUTES=60
LLM_API_KEY=
LLM_MODEL=
EMBEDDING_MODEL=
OBJECT_STORAGE_BUCKET=
OBJECT_STORAGE_KEY=
OBJECT_STORAGE_SECRET=
ENVIRONMENT=development
```

---

# PART B — DETAILED REQUIREMENTS

## B1. Functional Requirements (by module)

### FR-Auth (Module 1)
- FR-01 Register with email/password (or OAuth), email verification
- FR-02 Login/logout with JWT session
- FR-03 Forgot/reset password via emailed token
- FR-04 Edit account settings (email, password, notification prefs)
- FR-05 Role-based access (candidate vs admin)

### FR-Profile (Module 2)
- FR-10 Create/edit candidate profile: name, contact, location
- FR-11 Manage education entries (degree, institution, year)
- FR-12 Manage skills list (technical + tools), tagged by proficiency
- FR-13 Manage experience entries (company, role, duration, description)
- FR-14 Manage projects (title, description, tech stack, link)
- FR-15 Set target roles, preferred locations, salary range
- FR-16 View profile completeness percentage

### FR-Resume (Module 3)
- FR-20 Upload resume (PDF/DOCX/TXT, max size enforced)
- FR-21 Parse resume asynchronously; show processing status
- FR-22 Extract skills, education, experience, projects, certifications
- FR-23 Let user review and correct extracted fields before saving
- FR-24 Support multiple resume versions per user
- FR-25 Generate structured career profile from parsed data

### FR-JobDiscovery (Module 4)
- FR-30 Ingest jobs from configured connectors on a schedule
- FR-31 Normalize job data into a common schema
- FR-32 Deduplicate jobs via fingerprint (company+title+location+description similarity)
- FR-33 Store job with source, posted date, connector health metadata

### FR-JobIntelligence (Module 5)
- FR-40 Parse job description into structured fields (title, required/preferred skills, experience, education, location, salary, employment type)
- FR-41 Classify job seniority level

### FR-Matching (Module 6)
- FR-50 Compute weighted compatibility score (skills/experience/education/location/goals/projects/preferences)
- FR-51 Show explanation: matched skills, missing skills, match category (High/Medium/Low)
- FR-52 Rank job list by score with filters (location, role, match %, fraud risk)

### FR-Fraud (Module 7)
- FR-60 Run rule-based checks (personal-email domain, upfront-payment request, unverifiable company, suspicious URL)
- FR-61 Combine rules + ML into a 0–100 risk score
- FR-62 Present risk band (Low/Medium/High) with itemized reasons, never an absolute "scam" verdict

### FR-Application (Module 8)
- FR-70 Generate tailored resume from master resume + JD (no fabricated content)
- FR-71 Generate cover letter using profile + JD + company
- FR-72 Assist with application-question answers
- FR-73 Enforce automation policy per source: `AUTOMATION_ALLOWED / ASSISTED / MANUAL_REQUIRED / BLOCKED`
- FR-74 Require explicit consent before any auto-submission

### FR-Tracker (Module 9)
- FR-80 Save/apply/track jobs through state machine (Discovered→Saved→Matched→Preparing→Ready→Submitted→Under Review→Interview→Offer/Rejected/Withdrawn/Expired)
- FR-81 Kanban board view of applications
- FR-82 Manual status update + notes
- FR-83 Application history log per job

### FR-Career (Module 10)
- FR-90 Analyze skill frequency across target-role job market
- FR-91 Identify missing high-value skills, ranked by priority
- FR-92 Generate a learning roadmap (weekly plan)
- FR-93 Show career analytics (application→interview→offer conversion rates)

### FR-Interview (Module 11)
- FR-100 Generate interview questions (technical, behavioral, resume-based, company-specific) once an application reaches Interview state
- FR-101 Run mock interview flow (question → candidate answer → AI feedback)
- FR-102 Store interview history and feedback

### FR-Agent (Module 12)
- FR-110 Scheduler triggers periodic job discovery + analysis per user preferences
- FR-111 Orchestrator routes tasks to the correct agent
- FR-112 Permission system: user toggles which actions the agent may perform autonomously vs requires approval
- FR-113 Notification on new high-match job, status changes, skill-gap updates

## B2. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Normal API calls respond quickly; long AI/job tasks run asynchronously via queue |
| Scalability | Stateless backend workers, horizontal scaling of Celery workers |
| Security | HTTPS, JWT auth, RBAC, hashed passwords, input validation, rate limiting, audit logs |
| Reliability | Retry with exponential backoff for external calls; queue-based processing; graceful degradation on AI/job-source failure |
| Explainability | Every match score and fraud score must show reasoning, not just a number |
| Privacy | User can export/delete profile, resumes, and application history |
| Auditability | All sensitive actions (resume upload, AI generation, application submission) are logged |
| Cost control | Cache AI analysis per job so it isn't recomputed for every user |

---

# PART C — UI / SCREENS (Detailed)

For each screen: purpose, and every UI element with what it does.

### C1. Landing / Marketing Page
- Purpose: explain the product to a new visitor, drive signup.
- Elements: hero headline + subtext, "Get Started" CTA button, feature highlight cards (Resume Intelligence, Job Matching, Fraud Detection, Career Coaching), testimonials/placeholder section, footer with links.

### C2. Register / Login
- Purpose: account creation and authentication.
- Elements: email input, password input (with strength meter on register), confirm-password field (register only), "Forgot password?" link, submit button, OAuth buttons (optional), toggle link between login/register, inline validation error text.

### C3. Onboarding Wizard (first login)
- Purpose: capture initial profile fast so the system has something to work with immediately.
- Elements: step indicator (1/4, 2/4...), Step 1: basic info (name, location, phone); Step 2: resume upload dropzone; Step 3: target roles multi-select + preferred locations chips; Step 4: salary range slider + experience level radio buttons; "Skip for now" and "Continue" buttons.

### C4. Main Dashboard
- Purpose: at-a-glance career status.
- Elements: top stat cards — Career Readiness % (progress ring), Profile Completeness % (progress bar), New Jobs count, High Match count, Applications count, Interviews count, Offers count; "Recommended Jobs" horizontal scroll of job cards; "Recent Activity" feed list; sidebar nav (Dashboard, Jobs, Applications, Resume, Interviews, Career, Analytics, Settings).

### C5. Resume Manager
- Purpose: upload/manage resumes and review AI-extracted data.
- Elements: file upload dropzone (drag-and-drop + browse button), list of uploaded resumes with status badge (Processing/Ready/Failed), "Set as primary" toggle per resume, extracted-data review panel with editable fields grouped by section (Education, Skills as removable chips, Experience entry cards, Projects entry cards, Certifications list), "Save Corrections" button, version history dropdown.

### C6. Job Feed / Search
- Purpose: browse and filter discovered jobs.
- Elements: search bar, filter sidebar (location dropdown, role type checkboxes, match-score slider, fraud-risk filter, date-posted filter, employment type), sort dropdown (Best Match / Newest / Salary), job card grid — each card: title, company, location pin icon, salary range, match % badge (color-coded), fraud-risk badge (Low/Medium/High, color-coded), matched-skill chips, "View Details" and "Prepare Application" buttons, pagination or infinite scroll.

### C7. Job Detail Page
- Purpose: full analysis of one job.
- Elements: header (title, company, location, employment type, posted date, source link), full JD text panel, Match Analysis panel (overall %, breakdown bars per factor: skill/experience/education/location/goal match, matched-skill checklist, missing-skill checklist), Fraud Analysis panel (risk score gauge, itemized warning list with icons, disclaimer text), action buttons: "Save," "Generate Tailored Resume," "Generate Cover Letter," "Mark as Applied."

### C8. Application Preparation Screen
- Purpose: generate and review tailored materials before submitting.
- Elements: side-by-side view — original master resume vs. AI-tailored resume (diff-highlighted), edit-in-place text areas, cover-letter draft panel with regenerate button, application-question assistant (question list + AI-suggested answers, editable), automation-status banner showing policy (Automated / Assisted / Manual Required / Blocked) with explanation, consent checkbox before any auto-submit, "Submit" / "Mark as Manually Applied" buttons.

### C9. Application Tracker (Kanban + List toggle)
- Purpose: manage application pipeline.
- Elements: view toggle (Kanban/List), Kanban columns (Saved, Preparing, Applied, Screening, Interview, Offer, Rejected) with draggable cards, each card shows company, role, match %, applied date; List view as sortable table with columns (Company, Role, Applied Date, Match Score, Fraud Risk, Resume Version, Status, Next Action); filter by status/date; card click opens detail drawer with status-change dropdown and notes field.

### C10. Career Intelligence — Skill Gap
- Purpose: show market-demand skill gaps.
- Elements: bar chart of skill frequency across target-role job market, "Your Skills" vs "Market Demand" comparison table, missing-skill list ranked by priority with badges (Priority 1/2/3), "Add to Learning Plan" button per skill.

### C11. Career Roadmap
- Purpose: actionable learning plan.
- Elements: timeline/week-by-week cards (Week 1, Week 2...) each listing a skill/topic + suggested resources, progress checkboxes, "Regenerate Roadmap" button, link-out cards to external courses.

### C12. Interview Preparation
- Purpose: practice for a specific application.
- Elements: job selector dropdown (only jobs in Interview state), question category tabs (Technical / Behavioral / Resume-based / Company), question list with expandable AI-suggested answer guide, "Start Mock Interview" button, mock-interview chat UI (question → text/voice answer input → AI feedback panel with score and suggestions), session history list.

### C13. Career Analytics
- Purpose: performance overview.
- Elements: funnel chart (Applications → Interviews → Offers), conversion-rate stat cards, line chart of applications-over-time, insight callout box (AI-generated text insight, e.g. "roles requiring Power BI have a higher response rate"), export-report button.

### C14. Settings
- Purpose: account, privacy, and agent permissions.
- Elements: tabs — Profile (edit basic info), Security (change password, sessions), Notifications (toggle switches per channel/event), Privacy (data export button, delete-account button, delete-specific-data buttons), Agent Permissions (checklist of autonomous actions with allow/require-approval toggle: Discover Jobs, Analyze Jobs, Generate Resume, Generate Cover Letter, Submit Applications, Send Communications).

### C15. Admin Dashboard (internal)
- Purpose: operate the platform.
- Elements: user table with search/filter, job-source connector health table (status, last sync, jobs discovered, error count), fraud-report review queue, AI usage/cost chart (tokens, requests, cost by feature), system error log viewer, no direct access to private resume content.

---

# PART D — DATABASE (Quick Reference)

Core tables: `users, profiles, resumes, skills, education, experience, projects, jobs, companies, applications, interviews, offers, fraud_assessments, match_scores, career_goals, learning_recommendations, agent_tasks, audit_logs`.

Relationships:
```
users → profiles → (skills, education, experience, projects)
users → resumes
users → applications → jobs → companies, match_scores, fraud_assessments
```

Use Alembic migrations from day one; never hand-edit schema in prod.

---

# PART E — BUILD SEQUENCE (Sprint-by-Sprint)

1. **Foundation** — repo, Docker, CI, Postgres+pgvector, Redis, Auth (C2), base layout/nav
2. **Profile + Resume** — C3, C5, resume parser service, career profile generation
3. **Job Discovery** — connectors, normalization, dedup, Celery scheduled ingestion
4. **Job Intelligence + Matching** — JD parser, matching engine, C6, C7 (match panel)
5. **Fraud Detection** — rules engine → ML later, C7 (fraud panel)
6. **Application Intelligence** — resume tailoring, cover letter, C8
7. **Application Tracker** — state machine, C9
8. **Career Intelligence** — skill gap, roadmap, C10, C11
9. **Interview Agent** — C12
10. **Analytics + Notifications** — C13, notification engine
11. **Autonomous Agent + Permissions** — scheduler, orchestrator, C14 permissions tab
12. **Admin, Security Hardening, Testing** — C15, pen-test pass, load test
13. **Deployment + Monitoring** — see Part F
14. **Docs + polish**

---

# PART F — DEPLOYMENT

## F1. Containerize
Build separate Docker images: `frontend` (static build served via Nginx or Vercel), `backend` (FastAPI + Uvicorn/Gunicorn), `worker` (same image, Celery command).

## F2. CI/CD Pipeline (GitHub Actions)
```
push → lint → unit tests → integration tests → security scan
→ build images → push to registry → deploy staging → smoke test
→ manual approval → deploy production
```

## F3. Hosting Options
- **Simple/cheap:** Railway, Render, or Fly.io for backend+worker+Postgres+Redis; Vercel/Netlify for frontend.
- **Production-grade:** AWS/GCP/Azure — ECS/Cloud Run for backend & workers, managed Postgres (RDS/Cloud SQL) with pgvector, managed Redis (ElastiCache), S3/GCS for object storage, CloudFront/CDN for frontend.

## F4. Environment Promotion
`development → staging → production`. Staging mirrors production config with test data; run full E2E + load test there before promoting.

## F5. Production Checklist
- HTTPS enforced, secrets in a vault/secret manager (never in repo)
- Database backups + point-in-time recovery enabled
- Health-check endpoints wired to load balancer
- Structured logging + error tracking (e.g. Sentry) + uptime monitoring
- Rate limiting on public endpoints and AI-calling endpoints
- Rollback plan (keep last N deployable images tagged)

## F6. Post-Launch Monitoring
Track: API latency/error rate, AI token cost per feature, job-connector failure rate, queue backlog, DB CPU/connections, fraud false-positive reports, match-quality feedback.

---

# What To Do Next
Start at Part A (environment) → Sprint 1 in Part E. Each sprint pulls its screens from Part C and its requirements from Part B, so you always know exactly what to build and why before writing code.
