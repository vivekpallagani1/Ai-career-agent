# Railway Deployment - Step by Step Guide

Your GitHub repository is live at: https://github.com/vivekpallagani1/Ai-career-agent

Now let's deploy it to Railway for a live running server!

## Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click "Sign up with GitHub"
3. Authorize Railway to access your GitHub account
4. Choose a free account

## Step 2: Connect Your Repository

1. After signing in, click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize Railway to access your repositories
4. Find and select `Ai-career-agent` repository

## Step 3: Railway Auto-Configuration

Railway will:
- 🔍 Detect `docker-compose.yml`
- 🐳 Build Docker images
- 📦 Create services for: PostgreSQL, Redis, Backend, Worker, Frontend
- 🌐 Generate public URLs

## Step 4: Add Environment Variables

Railway needs environment variables from your `.env` file:

1. In Railway dashboard, go to your project
2. Click "Variables" in the left menu
3. Add these variables:

```
DATABASE_URL=postgresql://user:pass@postgres:5432/career_agent
POSTGRES_DB=career_agent
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
REDIS_URL=redis://redis:6379
SECRET_KEY=your-super-secret-key-change-this-in-production
ENVIRONMENT=production
DEBUG=False
```

## Step 5: Deploy!

1. Railway should auto-deploy on connection
2. Watch the build logs in the Dashboard
3. Wait for all services to be "Running" (usually 3-5 minutes)

## Step 6: Access Your Live App

Once deployed, Railway gives you URLs:

```
Frontend:  https://aicareeragent-frontend-production-xxxx.up.railway.app
Backend:   https://aicareeragent-backend-production-xxxx.up.railway.app
API Docs:  https://aicareeragent-backend-production-xxxx.up.railway.app/docs
```

## Step 7: Test Your Deployment

```bash
# Check API health
curl https://your-backend-url/api/v1/health

# Or open in browser
https://your-backend-url/docs
```

Try:
1. Opening frontend URL
2. Creating an account
3. Browsing job listings
4. Checking backend API documentation

## Troubleshooting

### Logs Won't Show
- Click on each service (backend, frontend, worker, postgres, redis)
- Check individual service logs

### Build Failed
- Check for environment variable errors
- Ensure all required variables are set
- Review backend/requirements.txt for Python issues

### Services Won't Start
- Check PostgreSQL and Redis status
- Verify environment variables have correct values
- Look for database connection errors in logs

### Database Migrations Failed
- SSH into backend service: Click terminal icon
- Run: `alembic upgrade head`

## Auto-Deployment

After deployment:
```bash
# Make changes locally
git add .
git commit -m "Your update"
git push origin master

# Railway auto-deploys! No manual steps needed.
```

## Monitor Your App

Railway dashboard shows:
- ✅ Real-time logs for each service
- 📊 CPU and Memory usage
- 🔄 Deployment history
- ⚠️ Errors and warnings

## Support

- Railway Docs: https://docs.railway.app
- GitHub Issues: Report bugs in your repo
- Railway Community: https://discord.gg/railway

---

## Quick Checklist

- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Added environment variables
- [ ] Deployment complete (all services running)
- [ ] Tested frontend URL
- [ ] Tested backend API docs
- [ ] Made a test account on the app
- [ ] Verified job matching works

**Congratulations! Your app is now live!** 🎉

