# GitHub Setup Instructions

Follow these steps to create a Personal Access Token and push your AI Career Agent to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - Repository name: `Ai-career-agent`
   - Description: `AI-powered career management platform with job matching and resume analysis`
   - Visibility: Public (or Private if preferred)
3. Click "Create repository"
4. **Copy the repository URL** - You'll need it in the next steps

## Step 2: Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Fill in:
   - Token name: `AI Career Agent Deployment`
   - Expiration: 90 days (or as needed)
4. Select scopes (check these boxes):
   - ✅ `repo` (all)
   - ✅ `write:packages`
   - ✅ `read:packages`
5. Click "Generate token"
6. **Copy the token immediately** - You won't be able to see it again!
7. Save it somewhere safe (you'll paste it when pushing)

## Step 3: Push Code to GitHub

Run these commands in PowerShell (from your project directory):

```powershell
cd "d:\ai career agent"

# Add GitHub remote (replace YOUR_REPO_URL with the URL from Step 1)
git remote add origin https://github.com/vivekpallagani1/Ai-career-agent.git

# Verify remote was added
git remote -v

# Push to GitHub
git push -u origin master

# When prompted for password:
# - Username: vivekpallagani1
# - Password: Paste your Personal Access Token (not your GitHub password!)
```

## Common Issues & Solutions

### Issue: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/vivekpallagani1/Ai-career-agent.git
```

### Issue: "Authentication failed"
- Verify you're using the Personal Access Token (not your password)
- Make sure the token hasn't expired
- Check that you copied it correctly

### Issue: "Permission denied (publickey)"
- You're using SSH but don't have SSH keys configured
- Use HTTPS method above instead

## Verify Push Was Successful

1. Go to https://github.com/vivekpallagani1/Ai-career-agent
2. You should see all your files and folders
3. Check the commit message shows "Initial commit: AI Career Agent..."

## Next Steps After Successful Push

1. ✅ GitHub repository is now live
2. Go to DEPLOYMENT_GUIDE.md to deploy to a live server
3. Recommended: Use Railway (easiest for Docker apps)
   - Go to https://railway.app
   - Connect your GitHub repository
   - Railway will auto-deploy on every push!

---

## Optional: Setup SSH Keys for Future Pushes (Advanced)

For more secure authentication, you can use SSH keys:

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter for all prompts to use defaults
# Then add the key to SSH agent:
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Display the public key to copy:
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

Then:
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Use SSH URLs for pushing: `git@github.com:vivekpallagani1/Ai-career-agent.git`

