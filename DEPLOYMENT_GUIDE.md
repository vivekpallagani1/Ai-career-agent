# Deployment Guide - AI Career Agent

This guide will help you deploy your AI Career Agent to GitHub and then to a live server.

## Step 1: Push to GitHub

### Option A: Using Personal Access Token (Recommended)

1. **Create a Personal Access Token on GitHub:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `write:packages`, `read:packages`
   - Copy the token (you'll use it below)

2. **Add GitHub Remote and Push:**

```bash
cd "d:\ai career agent"

# Add GitHub remote
git remote add origin https://github.com/vivekpallagani1/Ai-career-agent.git

# Rename branch to main (optional but recommended)
git branch -M main

# Push to GitHub (when prompted for password, use your Personal Access Token)
git push -u origin main
```

### Option B: Using SSH Keys

If you have SSH keys set up:

```bash
git remote add origin git@github.com:vivekpallagani1/Ai-career-agent.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Live Server

### Recommended: Railway (Easiest for Docker Apps)

Railway automatically deploys from GitHub with excellent Docker support.

#### Setup Steps:

1. **Go to https://railway.app and sign up**
2. **Connect your GitHub repository:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select the `Ai-career-agent` repository

3. **Configure Environment Variables:**
   - Railway will detect docker-compose.yml
   - Add these environment variables in Railway dashboard:
     ```
     DATABASE_URL=postgresql://user:pass@postgres:5432/career_agent
     REDIS_URL=redis://redis:6379
     ENVIRONMENT=production
     SECRET_KEY=your-secret-key-here
     ```

4. **Railway will automatically:**
   - Build Docker images
   - Start services
   - Provide public URLs

#### Access Your App:
- **Frontend:** `https://your-railway-app.up.railway.app`
- **Backend API:** `https://your-railway-api.up.railway.app`
- **API Docs:** `https://your-railway-api.up.railway.app/docs`

---

### Alternative: Render.com

1. **Go to https://render.com and sign up**
2. **Create New → Web Service**
3. **Connect GitHub repository**
4. **Configure:**
   - Build Command: `docker-compose build`
   - Start Command: `docker-compose up`
   - Add environment variables from `.env`

---

### Alternative: AWS ECS (More Complex but Powerful)

For AWS deployment, you'll need:
- AWS Account (free tier available)
- AWS ECR (Elastic Container Registry) for Docker images
- AWS RDS for PostgreSQL
- AWS ElastiCache for Redis
- AWS ECS for orchestration

Create file `.github/workflows/deploy-aws.yml` for CI/CD pipeline.

---

## Step 3: Monitor and Manage

### View Logs:
```bash
# For Railway/Render - available in dashboard

# For local Docker:
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f worker
```

### Update and Redeploy:
```bash
# Make changes locally
# Commit and push to GitHub
git add .
git commit -m "Your update message"
git push origin main

# Railway/Render will auto-deploy!
```

---

## Troubleshooting

### Database Migration Issues:
```bash
# After deployment, run migrations
docker-compose exec backend alembic upgrade head
```

### Environment Variables Not Working:
- Ensure all variables from `.env` are set in deployment platform
- Check that variable names match those referenced in `backend/app/core/config.py`

### Port/Connection Issues:
- Railway/Render handle port mapping automatically
- Ensure `docker-compose.yml` has correct service dependencies

---

## Next Steps

1. ✅ Create GitHub repository (follow Step 1 above)
2. ✅ Push your code to GitHub
3. ✅ Sign up for Railway/Render
4. ✅ Connect your GitHub repository to Railway
5. ✅ Set environment variables
6. ✅ Deploy!
7. ✅ Visit your live app URL

**Total time to live deployment: ~15-20 minutes**

---

## Quick Commands Reference

```bash
# View git status
git status

# View remote configuration
git remote -v

# View commit history
git log --oneline

# Add changes and commit
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

