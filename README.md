# AI Career Agent — Full-Stack Implementation

A complete AI-powered career guidance platform that matches candidates with jobs, analyzes skill gaps, and provides interview coaching. Built with FastAPI (backend), React + Vite (frontend), PostgreSQL + pgvector, Redis, and Celery workers.

## Project Status

✅ **Complete backend and frontend scaffolds aligned to the implementation guide**
✅ **Core modules:** Auth, Profiles, Jobs, Applications, Matching, Resume Parsing
✅ **Database models and migrations** ready
✅ **API endpoints** for auth, jobs, profiles
✅ **React frontend** with routing, global state (Zustand), API client
✅ **Docker setup** with Compose for local development

🚀 **Ready for:** Setting up a local dev environment, running tests, extending business logic

## Quick Start

### With Docker Compose (Recommended)

```bash
# Copy environment file and customize
cp .env.example .env

# Start all services
docker-compose up

# In another terminal, run migrations
docker-compose exec backend alembic upgrade head

# Open http://localhost:5173 for the frontend
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## Project Structure

```
ai-career-agent/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry
│   │   ├── core/                    # Config, security, dependencies
│   │   ├── api/v1/                  # Route handlers (auth, jobs, profiles)
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic (job matching, resume parsing)
│   │   ├── repositories/            # Database access layer
│   │   ├── jobs/                    # Celery async tasks
│   │   ├── agents/                  # AI orchestrator
│   │   └── db/                      # Database session management
│   ├── tests/                       # Unit & integration tests
│   ├── alembic/                     # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.jsx                 # React app entry
│   │   ├── pages/                   # Page components (Dashboard, Jobs, Login)
│   │   ├── layouts/                 # Reusable layouts
│   │   ├── components/              # Shared UI components
│   │   ├── services/                # API client
│   │   ├── store/                   # Zustand global state (auth)
│   │   └── index.css                # Tailwind global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── docker-compose.yml               # Local dev orchestration
├── .env.example                     # Environment template
├── .gitignore
├── AI_Career_Agent_Implementation_Guide.md  # Full product spec
└── SETUP_GUIDE.md                   # Setup & deployment instructions
```

## Key Features Implemented

### Authentication & Authorization
- User registration and login with JWT tokens
- Password hashing with bcrypt
- Role-based access control (candidate vs admin)

### Job Discovery
- List and search jobs from multiple sources
- Job parsing and normalization
- Fraud risk detection (placeholder)

### Job Matching
- Weighted compatibility scoring (skills, experience, education, location, goals)
- Explanation of match factors and gaps
- Match category ranking (High/Medium/Low)

### Profile Management
- Candidate profile creation and updates
- Career goals and preferences
- Profile completeness tracking

### Resume Management
- Resume upload and storage (placeholder)
- Async resume parsing with Celery
- Extracted skills, education, experience tracking

### Application Tracking
- State machine for applications (Discovered → Applied → Interview → Offer)
- Application history and notes
- Resume version tracking

## API Endpoints

All endpoints are prefixed with `/api/v1`:

```
Authentication
  POST   /auth/register              Register a new account
  POST   /auth/login                 Login and receive JWT

Jobs
  GET    /jobs                       List jobs with pagination
  GET    /jobs/search                Search jobs by title, company, location
  GET    /jobs/{id}                  Get job details
  POST   /jobs/{id}/match            Calculate match score with candidate

Profiles
  GET    /profiles/{id}              Get candidate profile
  POST   /profiles                   Create or update profile

Health
  GET    /health                     Service health check
  GET    /ping                       Simple ping endpoint
```

Interactive documentation available at `http://localhost:8000/docs` (Swagger UI).

## Core Services

### Job Matching Service
Computes a weighted compatibility score based on:
- Skills match (exact + similar)
- Experience level alignment
- Education requirements
- Location preferences
- Career goals alignment
- Project portfolio relevance

### Resume Parser Service
Extracts structured data from resumes (PDF, DOCX, TXT):
- Contact information
- Skills with proficiency tags
- Work experience entries
- Education
- Projects and certifications
- Career summary

### Fraud Detection Service
Rule-based + ML scoring to identify suspicious jobs:
- Domain reputation checks
- Upfront payment requests
- Unverifiable companies
- Suspicious URLs
- Seniority/salary mismatches

### Career Intelligence Service
Generates insights and recommendations:
- Skill gap analysis vs market demand
- Learning roadmap generation
- Application → Interview → Offer conversion rates
- Career progression paths

## Database Schema

Primary tables (see `backend/alembic/versions/001_initial.py`):

- **users** — User accounts with email, password, role
- **candidate_profiles** — Career goals, skills, preferences
- **jobs** — Job listings with parsed data and fraud scores
- **resumes** — Uploaded resumes with extraction status
- **applications** — Job applications with status tracking

Uses **PostgreSQL** with **pgvector** extension for semantic search of job descriptions.

## Technology Stack

**Backend:**
- FastAPI 0.115+ (async Python web framework)
- SQLAlchemy 2.0+ (ORM)
- Pydantic (data validation)
- PostgreSQL 15+ (relational database)
- pgvector (semantic search)
- Redis 7+ (caching & queue)
- Celery 5.4+ (async task worker)
- JWT (authentication)
- Pytest (testing)

**Frontend:**
- React 18+ (UI library)
- Vite 5+ (build tool)
- TailwindCSS 3+ (styling)
- React Router 6+ (navigation)
- TanStack Query 5+ (data fetching & caching)
- Zustand (global state management)
- Axios (HTTP client)

**DevOps:**
- Docker & Docker Compose (containerization)
- Alembic (database migrations)

## Environment Setup

Copy `.env.example` to `.env` and customize:

```env
# Database connection (PostgreSQL + pgvector)
DATABASE_URL=postgresql://user:pass@localhost:5432/career_agent
REDIS_URL=redis://localhost:6379/0

# JWT authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRY_MINUTES=60

# LLM Integration (for AI features)
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o-mini

# Object storage (for resume uploads)
OBJECT_STORAGE_BUCKET=career-agent-storage

# Environment
ENVIRONMENT=development
```

## Running Tests

**Backend:**
```bash
cd backend
pytest tests/ -v
```

**Frontend:**
```bash
cd frontend
npm run test  # (add test script to package.json)
```

## Deployment

### Docker Compose (Local & Staging)
See `docker-compose.yml` — starts all services with one command.

### Production Deployment
- **AWS:** ECR + ECS + RDS + ElastiCache + ALB
- **Vercel:** Frontend only (with backend on AWS/Railway/Render)
- **Railway, Render, Heroku:** One-click deployment from GitHub

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed deployment instructions.

## Documentation

- **[AI_Career_Agent_Implementation_Guide.md](AI_Career_Agent_Implementation_Guide.md)** — Complete product specification with all features, requirements, and UI designs
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** — Local development, Docker, migrations, deployment
- **API Docs:** http://localhost:8000/docs (Swagger UI)

## Development Workflow

1. **Create a feature branch:** `git checkout -b feature/your-feature`
2. **Make changes** to backend or frontend
3. **Test locally:**
   - Backend: `pytest` or call endpoints via Swagger
   - Frontend: `npm run dev` and test in browser
4. **Commit with clear messages:** `git commit -m "feat: add job matching"`
5. **Push and open a PR** for review

## Next Steps

1. ✅ Complete backend scaffolding
2. ✅ Complete frontend app structure
3. 🔄 **Implement core features:**
   - [ ] Resume parsing (integrate with LLM or PDF library)
   - [ ] Job intelligence (parse JD into structured fields)
   - [ ] Fraud detection rules & ML model
   - [ ] Matching algorithm refinement
   - [ ] Interview prep chatbot
   - [ ] Career analytics dashboard
4. 🔄 **Full-stack integration tests**
5. 🔄 **Deploy to production environment**

## Contributing

Contributions are welcome! Please:
1. Follow PEP 8 (Python) and Prettier (JavaScript) style guides
2. Add tests for new features
3. Update documentation
4. Keep commit messages clear and concise

## License

MIT License — See LICENSE file for details.

---

**Questions?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) or open an issue on GitHub.

