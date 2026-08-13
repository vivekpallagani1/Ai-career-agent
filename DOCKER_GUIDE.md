# Docker Compose Startup Guide

This guide walks you through starting the AI Career Agent using Docker Compose.

## Quick Start (30 seconds)

### Windows (PowerShell)
```powershell
cd d:\ai career agent
.\docker-start.bat
```

### macOS / Linux (Bash)
```bash
cd ~/path/to/ai-career-agent
bash docker-start.sh
```

## Manual Start (If scripts don't work)

```bash
# Navigate to project root
cd ai-career-agent

# Copy environment file
cp .env.example .env
# On Windows: copy .env.example .env

# Start all services in background
docker-compose up -d

# Wait 10 seconds for services to initialize
sleep 10

# Run database migrations
docker-compose exec backend alembic upgrade head
```

## What Gets Started

When you run Docker Compose, these 5 services start:

```
┌─────────────────────────────────────────────────────────┐
│ PostgreSQL 15 + pgvector                                │
│ Port: 5432                                              │
│ Database: career_agent                                  │
│ Username: user, Password: pass                          │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ Redis 7 (Cache & Task Queue)                            │
│ Port: 6379                                              │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ FastAPI Backend (http://localhost:8000)                 │
│ • API endpoints                                         │
│ • Health check                                          │
│ • Swagger UI: /docs, ReDoc: /redoc                      │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ Celery Worker                                           │
│ • Async background tasks                               │
│ • Resume parsing                                        │
│ • Job ingestion                                         │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ React Frontend (http://localhost:5173)                  │
│ • Vite dev server with hot reload                       │
│ • Login, Dashboard, Job Discovery pages                 │
│ • Connected to backend API                              │
└─────────────────────────────────────────────────────────┘
```

## Monitoring Services

### View Real-Time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f worker
docker-compose logs -f postgres
```

### Check Service Status

```bash
docker-compose ps
```

Output:
```
NAME                COMMAND                  STATUS
postgres            postgres -c ...          Up (healthy)
redis               redis-server             Up
backend             uvicorn app.main:app     Up
worker              celery -A app.jobs ...   Up
frontend            npm run dev              Up
```

### Stop Services

```bash
# Stop but keep data
docker-compose stop

# Stop and remove containers (data persists)
docker-compose down

# Remove everything including volumes (DELETES DATA)
docker-compose down -v
```

## Testing the Setup

### 1. Frontend (React App)
```
Open: http://localhost:5173
Expected: AI Career Agent landing page with "Get Started" button
```

### 2. Backend API
```bash
# Health check
curl http://localhost:8000/health
# Response: {"status":"ok","app":"AI Career Agent","environment":"development"}

# API Docs (interactive)
Open: http://localhost:8000/docs
# Try: POST /api/v1/auth/register with email, password, name
```

### 3. Database
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U user -d career_agent

# Inside psql:
\dt                 # List tables
SELECT * FROM users;  # View users table
\q                  # Exit
```

### 4. Redis
```bash
# Monitor Redis
docker-compose exec redis redis-cli monitor

# Or check keys
docker-compose exec redis redis-cli KEYS "*"
```

## Common Workflows

### Register a New User

1. Open http://localhost:5173
2. Click "Create Your Free Account"
3. Enter email, password, name
4. Click "Create account"
5. Redirected to Dashboard

### List Jobs

1. Click "Jobs" in sidebar
2. See mock job listings
3. Click "View Details & Match" on any job
4. View match score calculation

### Check Logs While Developing

```bash
# Terminal 1: Watch backend logs
docker-compose logs -f backend

# Terminal 2: Watch frontend build errors
docker-compose logs -f frontend

# Terminal 3: Interact with the app
# Open http://localhost:5173 and test features
```

### Restart a Service

```bash
# Restart backend after code changes
docker-compose restart backend

# Restart frontend
docker-compose restart frontend
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose down
docker-compose up --build -d

# Check disk space
docker system df
```

### "Port already in use"
```bash
# Find what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr ":8000"  # Windows

# Edit docker-compose.yml to use different port:
# backend:
#   ports:
#     - "8001:8000"  # Use 8001 instead
```

### Database migrations fail
```bash
# Check migrations
docker-compose exec backend alembic current

# Manually upgrade
docker-compose exec backend alembic upgrade head

# View migration history
docker-compose exec backend alembic history
```

### Frontend not updating after code changes
```bash
# Vite should auto-reload, but if not:
docker-compose restart frontend

# Or clear browser cache (Ctrl+Shift+Delete)
```

## Performance Tips

### On M1/M2 Mac
Docker for Mac on Apple Silicon can be slow. Options:
1. Use Rosetta emulation (check Docker Desktop settings)
2. Use OrbStack instead of Docker Desktop (faster alternative)

### Reduce Memory Usage
Edit `docker-compose.yml` to limit resources:
```yaml
services:
  backend:
    mem_limit: 512m
    memswap_limit: 512m
```

### Speed Up Image Pulls
First run may take 5-10 minutes to download images. Subsequent runs are instant.

## Next Steps

1. ✅ All services running
2. ✅ Frontend accessible at http://localhost:5173
3. ✅ Backend API at http://localhost:8000
4. 🔄 Now you can:
   - Register and test the login flow
   - Browse and search jobs
   - Test API endpoints via Swagger UI
   - Modify backend code and watch auto-reload
   - Modify frontend code and see instant updates
   - Check logs to debug issues

## Getting Help

- **Setup Issues?** → See [PREREQUISITES.md](PREREQUISITES.md)
- **What to do next?** → See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **System design?** → See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Contributing?** → See [CONTRIBUTING.md](CONTRIBUTING.md)
- **API Reference?** → http://localhost:8000/docs (Swagger UI)

---

**Estimated Time:**
- First run: 3-5 minutes (downloading images)
- Subsequent runs: 30 seconds
- Total until ready: 5-10 minutes

🚀 **Happy coding!**
