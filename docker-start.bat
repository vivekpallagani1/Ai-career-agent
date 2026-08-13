@echo off
REM AI Career Agent — Docker Compose Quick Start (Windows)
REM Run this script from the project root directory

echo.
echo 🚀 AI Career Agent — Docker Compose Setup
echo ===========================================
echo.

REM Step 1: Check prerequisites
echo ✓ Checking prerequisites...

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not installed.
    echo    Download from: https://www.docker.com/products/docker-desktop
    exit /b 1
)

where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose is not installed.
    echo    It comes with Docker Desktop. Please install Docker Desktop.
    exit /b 1
)

for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VERSION=%%i
for /f "tokens=*" %%i in ('docker-compose --version') do set COMPOSE_VERSION=%%i

echo ✅ %DOCKER_VERSION%
echo ✅ %COMPOSE_VERSION%
echo.

REM Step 2: Prepare environment
echo ✓ Preparing environment...

if not exist .env (
    echo    Creating .env from .env.example...
    copy .env.example .env
    echo    ⚠️  Edit .env with your configuration before proceeding.
) else (
    echo    .env already exists
)

echo.

REM Step 3: Start services
echo ✓ Starting services with Docker Compose...
echo    (This may take 2-3 minutes on first run)
echo.

docker-compose up -d

echo.
echo ✅ Services started!
echo.

REM Step 4: Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10

REM Step 5: Run migrations
echo ✓ Running database migrations...
docker-compose exec backend alembic upgrade head

echo.
echo 🎉 Setup complete!
echo.
echo 📍 Service URLs:
echo    Frontend:     http://localhost:5173
echo    Backend API:  http://localhost:8000
echo    API Docs:     http://localhost:8000/docs
echo    ReDoc:        http://localhost:8000/redoc
echo.
echo 🧪 Test the setup:
echo    1. Open http://localhost:5173 in your browser
echo    2. Click 'Log In' or 'Create Your Free Account'
echo    3. Browse the Job Discovery page
echo.
echo 📋 Useful commands:
echo    View logs:        docker-compose logs -f
echo    Stop services:    docker-compose down
echo    Restart services: docker-compose restart
echo    Shell into backend: docker-compose exec backend bash
echo.
pause
