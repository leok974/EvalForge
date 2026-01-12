# Authentication Setup Guide

## The Problem
Your deployment was missing GitHub OAuth credentials, causing `/api/auth/login` to return 500 errors.

## The Fix
The deployment script now checks for and includes authentication secrets.

## Setup Instructions

### Step 1: Create GitHub OAuth App
1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: EvalForge
   - **Homepage URL**: `https://evalforge-agents-XXXXXXXXX.run.app` (your Cloud Run URL)
   - **Authorization callback URL**: `https://evalforge-agents-XXXXXXXXX.run.app/api/auth/github/callback`
4. Save the **Client ID** and generate a **Client Secret**

### Step 2: Generate Secret Key
```powershell
# Generate a random 32-character secret key
-join ((48..57) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Step 3: Create `.env.prod` File
Copy `.env.prod.example` to `.env.prod` and fill in your secrets:

```bash
GITHUB_CLIENT_ID=Iv1.abc123...
GITHUB_CLIENT_SECRET=ghp_xyz789...
SECRET_KEY=a1b2c3d4e5f6...
```

**⚠️ IMPORTANT:** Add `.env.prod` to `.gitignore` (already done)

### Step 4: Load Secrets
```powershell
# Option A: Use the helper script
./scripts/set_auth_secrets.ps1

# Option B: Set manually
$env:GITHUB_CLIENT_ID = "your_client_id"
$env:GITHUB_CLIENT_SECRET = "your_client_secret"
$env:SECRET_KEY = "your_secret_key"
```

### Step 5: Deploy
```powershell
./manual_deploy.ps1
```

The script will:
- ✓ Check for auth secrets
- ✓ Warn if missing (allows mock auth fallback)
- ✓ Include them in the Cloud Run deployment
- ✓ Mask secrets in the output

## Quick Fix (Current Deployment)
If you want to fix the currently deployed service immediately:

```powershell
gcloud run services update evalforge-agents `
  --project=evalforge `
  --region=us-central1 `
  --set-env-vars="GITHUB_CLIENT_ID=$env:GITHUB_CLIENT_ID,GITHUB_CLIENT_SECRET=$env:GITHUB_CLIENT_SECRET,SECRET_KEY=$env:SECRET_KEY,EVALFORGE_AUTH_MODE=github"
```

## Mock Auth Fallback
If you don't have GitHub OAuth yet, the deployment will use mock auth automatically:
- Default user: "mock_user" 
- Auto-login on page load
- No real authentication (dev only)
