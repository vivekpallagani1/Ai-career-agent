# AI Career Agent — Project Setup & Deployment Guide

This document covers how to set up and run the AI Career Agent project locally or in production.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Running with Docker Compose](#running-with-docker-compose)
3. [Environment Variables](#environment-variables)
4. [Database Migrations](#database-migrations)
5. [API Documentation](#api-documentation)
6. [Deployment](#deployment)

---

## Local Development Setup

### Prerequisites

- **Python 3.11+** with venv
- **Node.js 20+** with npm
- **PostgreSQL 15+** with pgvector extension
- **Redis 7+**
- **Git**

### Backend Setup

```bash
# Create Python virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy .env.example to .env and update)
cp ../.env.example ../.env

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000** with interactive docs at **http://localhost:8000/docs**.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run dev
```

The frontend will be available at **http://localhost:5173**.

### Redis & PostgreSQL Setup (Local)

#### Option A: Install natively

**PostgreSQL:**
```bash
# macOS (using Homebrew)
brew install postgresql@15 pgvector
brew services start postgresql@15
createdb career_agent
psql career_agent -c "CREATE EXTENSION pgvector;"

# Ubuntu/Debian
sudo apt-get install postgresql-15 postgresql-15-pgvector
sudo systemctl start postgresql
createdb career_agent
psql career_agent -c "CREATE EXTENSION pgvector;"

# Windows
# Download and install from https://www.postgresql.org/download/windows/
# Use pgAdmin to create the database and enable pgvector
```

**Redis:**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# Windows
# Download from https://github.com/microsoftarchive/redis/releases
```

#### Option B: Docker containers (recommended)

```bash
# PostgreSQL + pgvector
docker run -d \
  --name postgres_career \
  -e POSTGRES_DB=career_agent \
  -e POSTGRES_PASSWORD=pass \
  -p 5432:5432 \
  pgvector/pgvector:pg15

# Redis
docker run -d \
  --name redis_career \
  -p 6379:6379 \
  redis:7-alpine
```

---

## Running with Docker Compose

The simplest way to run the entire stack:

```bash
# Copy and update environment file
cp .env.example .env
nano .env  # edit with your config

# Start all services (PostgreSQL, Redis, Backend, Worker, Frontend)
docker-compose up

# Run migrations (in a new terminal)
docker-compose exec backend alembic upgrade head

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
```

Services will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

---

## Environment Variables

Create a `.env` file in the project root. Required variables:

```env
# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/career_agent

# Redis (for caching and Celery queue)
REDIS_URL=redis://redis:6379/0

# JWT (generate a secure key: openssl rand -hex 32)
JWT_SECRET=your-secret-key-here
JWT_EXPIRY_MINUTES=60

# LLM Integration (optional, for AI features)
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Object Storage (optional, for resume uploads)
OBJECT_STORAGE_BUCKET=career-agent-storage
OBJECT_STORAGE_KEY=your-aws-key
OBJECT_STORAGE_SECRET=your-aws-secret

# Environment
ENVIRONMENT=development  # or production
```

---

## Database Migrations

Using **Alembic** for database versioning:

```bash
cd backend

# Create a new migration (after changing models)
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback to previous migration
alembic downgrade -1

# Show current migration version
alembic current

# View migration history
alembic history
```

Migrations are stored in `backend/alembic/versions/`.

---

## API Documentation

Once the backend is running, interactive API docs are available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

```
POST   /api/v1/auth/register          Register a new user
POST   /api/v1/auth/login             Login and get JWT token
GET    /api/v1/jobs                   List jobs
GET    /api/v1/jobs/search            Search jobs
GET    /api/v1/jobs/{id}              Get job details
POST   /api/v1/jobs/{id}/match        Calculate match score
GET    /api/v1/profiles/{id}          Get user profile
POST   /api/v1/profiles               Create/update profile
GET    /api/v1/health                 Health check
```

---

## Deployment

### Docker Build

```bash
# Build frontend image
cd frontend
docker build -t career-agent-frontend:latest .

# Build backend image
cd ../backend
docker build -t career-agent-backend:latest .
```

### AWS Deployment (ECS + RDS)

1. **Create RDS PostgreSQL instance** with pgvector extension
2. **Create ElastiCache Redis** cluster
3. **Create ECR repositories** for frontend and backend
4. **Push images to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com
   docker tag career-agent-backend:latest [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/career-agent-backend:latest
   docker push [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/career-agent-backend:latest
   ```
5. **Create ECS Task Definitions** for backend and Celery worker
6. **Create ECS Services** and ALB for load balancing
7. **Deploy frontend to S3 + CloudFront** CDN

### Vercel (Frontend Only)

```bash
cd frontend
vercel deploy --prod
```

### Railway / Render (Full Stack)

1. Connect your GitHub repo
2. Create services for PostgreSQL, Redis, Backend, Worker, Frontend
3. Set environment variables in the platform UI
4. Deploy!

---

## Monitoring & Logging

- **Backend logs:** `docker-compose logs backend`
- **Worker logs:** `docker-compose logs worker`
- **Frontend errors:** Browser DevTools Console
- **Database:** Use pgAdmin or DBeaver for SQL debugging
- **Redis:** Use `redis-cli monitor` for queue inspection

---

## Troubleshooting

### "Module not found" errors

```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### Database connection errors

Verify `DATABASE_URL` in `.env` and check PostgreSQL is running:

```bash
psql -c "SELECT 1"  # Quick connection test
```

### CORS errors

Frontend and backend must use matching origins. For local dev:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

---

## Next Steps

After setup:
1. Complete the onboarding flow on the frontend
2. Upload a resume to test extraction
3. Run a job search to test matching
4. Review job details and match scores
5. Prepare and submit an application

For more details, see [AI_Career_Agent_Implementation_Guide.md](AI_Career_Agent_Implementation_Guide.md).
