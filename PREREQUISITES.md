# Prerequisites Checklist

Before starting Docker Compose, ensure you have the following installed:

## Required

- [ ] **Docker Desktop** (includes Docker + Docker Compose)
  - Download: https://www.docker.com/products/docker-desktop
  - Windows: Install .exe, run `docker --version` in PowerShell
  - macOS: Install .dmg or use Homebrew: `brew install docker`
  - Linux: `sudo apt-get install docker.io docker-compose`

- [ ] **Git** (to clone the repo)
  - Windows: https://git-scm.com/download/win
  - macOS: `brew install git` or https://git-scm.com/download/mac
  - Linux: `sudo apt-get install git`

## Hardware Requirements

- [ ] **CPU**: 2+ cores
- [ ] **RAM**: 4+ GB available (Docker Desktop uses 2-4 GB)
- [ ] **Disk Space**: 5+ GB free (for images and containers)
- [ ] **Internet**: Stable connection (for pulling Docker images)

## Verify Installation

Open a terminal and run:

```bash
docker --version
docker-compose --version
git --version
```

All three should show version numbers without errors.

## Firewall & Network

- [ ] **Port 5173** is not in use (frontend)
- [ ] **Port 8000** is not in use (backend)
- [ ] **Port 5432** is not in use (PostgreSQL)
- [ ] **Port 6379** is not in use (Redis)

Check on Windows:
```powershell
netstat -ano | findstr ":5173"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":5432"
netstat -ano | findstr ":6379"
```

If any are in use, either stop that service or modify the ports in `docker-compose.yml`.

## Next Steps

1. ✅ Ensure all prerequisites are met
2. ✅ Clone the repository or navigate to the project folder
3. ✅ Run `./docker-start.sh` (macOS/Linux) or `docker-start.bat` (Windows)
4. ✅ Wait for all services to start (2-3 minutes)
5. ✅ Open http://localhost:5173 in your browser
6. ✅ Start developing!

## Troubleshooting

### "Docker daemon is not running"
- Windows: Open Docker Desktop from Start menu
- macOS: Click Docker icon in menu bar
- Linux: Run `sudo systemctl start docker`

### "Permission denied" (Linux)
```bash
sudo usermod -aG docker $USER
# Then log out and log back in
```

### "Port already in use"
Edit `docker-compose.yml` and change the port mappings:
```yaml
services:
  frontend:
    ports:
      - "5174:5173"  # Use 5174 instead of 5173
```

### Services won't start
Check logs: `docker-compose logs -f`

---

For more help, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
