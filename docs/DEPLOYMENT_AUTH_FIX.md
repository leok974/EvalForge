# Production Deployment - Auth Fix

## Status: ✅ DEPLOYED

**Date:** 2026-01-12  
**Project:** evalforge-480016 (105491344850)  
**Service URL:** https://evalforge-agents-105491344850.us-central1.run.app

## What Was Fixed

The `/api/auth/login` endpoint was returning 500 errors because GitHub OAuth credentials were not configured in Cloud Run.

## Changes Made

### 1. Updated `.env.prod`
Added GitHub OAuth credentials:
```bash
GITHUB_CLIENT_ID=Ov23lifICLbZB03xXhf8
GITHUB_CLIENT_SECRET=5abafbf9b7ab393cf8300cfe2521377bce1fd978
```

### 2. Deployed to Cloud Run
```powershell
gcloud run services update evalforge-agents \
  --project=evalforge-480016 \
  --region=us-central1 \
  --update-env-vars="GITHUB_CLIENT_ID=Ov23lifICLbZB03xXhf8,GITHUB_CLIENT_SECRET=***,SECRET_KEY=***,EVALFORGE_AUTH_MODE=github"
```

**Revision:** evalforge-agents-00006-6gd  
**Status:** Serving 100% traffic

## GitHub OAuth App Configuration

**IMPORTANT:** Update your GitHub OAuth App with the new callback URL:

1. Go to: https://github.com/settings/developers
2. Find: "EvalForge Production" (or your OAuth app)
3. Update **Authorization callback URL** to:
   ```
   https://evalforge-agents-105491344850.us-central1.run.app/api/auth/github/callback
   ```

## Testing

Test the auth endpoint:
```powershell
curl https://evalforge-agents-105491344850.us-central1.run.app/api/auth/login
```

Expected response:
```json
{
  "url": "https://github.com/login/oauth/authorize?client_id=Ov23lifICLbZB03xXhf8&scope=read:user"
}
```

## Next Steps

1. ✅ OAuth credentials deployed
2. ⏳ Update GitHub OAuth callback URL (see above)
3. ⏳ Test full auth flow in browser
4. ⏳ Update any hardcoded URLs in frontend if needed
