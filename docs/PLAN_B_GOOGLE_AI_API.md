# Plan B Configuration - Google AI API Fallback

This configuration provides a fallback to Google AI API (Gemini API) if Vertex AI has issues.

## When to Use Plan B

Switch to Plan B if experiencing:
- Vertex AI regional outages
- IAM permission issues that can't be quickly resolved
- Project quota/billing issues with Vertex AI
- Model unavailability in your region

## Setup Instructions

### 1. Get Google AI API Key

```bash
# Visit: https://aistudio.google.com/app/apikey
# Generate an API key
```

### 2. Store API Key Securely

**Local Development (.env.local):**
```bash
# DO NOT commit this to git!
GOOGLE_API_KEY=your-api-key-here
```

**Cloud Run (Secret Manager):**
```bash
# Create secret
echo -n "your-api-key-here" | gcloud secrets create google-api-key \
  --data-file=- \
  --project=evalforge-1063529378

# Grant access to Cloud Run service
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=evalforge-1063529378
```

### 3. Deployment Configuration

**Update manual_deploy.ps1 to support Plan B:**

Add to environment variables section:
```powershell
# Plan B: Switch between Vertex AI and Google AI API
$useVertexAI = $true  # Set to $false to use Google AI API

if ($useVertexAI) {
    $envVars = @(
        "GENAI_PROVIDER=vertex",
        "GOOGLE_CLOUD_PROJECT=$ProjectId",
        "VERTEX_LOCATION=$Region",
        "GENAI_MODEL=gemini-1.5-flash-002",
        "GOOGLE_GENAI_USE_VERTEXAI=true",
        "GOOGLE_CLOUD_LOCATION=$Region"
    ) -join ","
} else {
    # Plan B: Google AI API
    $envVars = @(
        "GENAI_PROVIDER=google",
        "GENAI_MODEL=gemini-1.5-flash-002"
    ) -join ","
    
    # Add secret for API key
    $secretArgs = "--set-secrets=GOOGLE_API_KEY=google-api-key:latest"
}
```

### 4. Quick Switch Commands

**Switch to Plan B (Google AI API):**
```bash
gcloud run services update evalforge-agents \
  --region=us-central1 \
  --set-env-vars="GENAI_PROVIDER=google,GENAI_MODEL=gemini-1.5-flash-002" \
  --set-secrets="GOOGLE_API_KEY=google-api-key:latest" \
  --remove-env-vars="GOOGLE_GENAI_USE_VERTEXAI,GOOGLE_CLOUD_PROJECT,VERTEX_LOCATION,GOOGLE_CLOUD_LOCATION"
```

**Switch back to Vertex AI:**
```bash
gcloud run services update evalforge-agents \
  --region=us-central1 \
  --set-env-vars="GENAI_PROVIDER=vertex,GOOGLE_CLOUD_PROJECT=evalforge-1063529378,VERTEX_LOCATION=us-central1,GENAI_MODEL=gemini-1.5-flash-002,GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_LOCATION=us-central1" \
  --remove-secrets="GOOGLE_API_KEY"
```

## Code Changes (Already Implemented)

The code in `arcade_app/agent.py` already supports both providers:

```python
# The code checks GENAI_PROVIDER and adapts accordingly
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"  # Only set when provider=vertex
```

## Testing Plan B

### Local Test:
```powershell
cd D:\EvalForge
$env:GENAI_PROVIDER="google"
$env:GOOGLE_API_KEY="your-api-key-here"
$env:GENAI_MODEL="gemini-1.5-flash-002"
D:/EvalForge/.venv/Scripts/adk.exe web . --port 19000
```

### Verify in Logs:
```
[startup] provider=google project=None region=us-central1 model=gemini-1.5-flash-002
```

## Comparison

| Feature | Vertex AI (Primary) | Google AI API (Plan B) |
|---------|-------------------|----------------------|
| Authentication | ADC (no keys needed) | API Key required |
| Cost | Pay-per-use, enterprise | Pay-per-use, standard |
| Rate Limits | Higher for enterprise | Standard limits |
| Availability | Regional | Global |
| IAM Integration | Full Cloud IAM | API Key only |
| Audit Logs | Full Cloud Logging | Limited |
| Best For | Production, team use | Backup, quick fixes |

## Monitoring Plan B

If using Plan B, monitor for:
- API key expiration warnings
- Rate limit errors (429)
- Quota exceeded errors

## Security Notes

⚠️ **IMPORTANT:**
- Never commit API keys to git
- Rotate API keys regularly
- Use Secret Manager in production
- Monitor API key usage
- Restrict API key by IP/referrer if possible

## Rollback Plan

If Plan B causes issues:
1. Use quick switch command to revert to Vertex AI
2. Check Cloud Run logs for errors
3. Verify environment variables are correct
4. Confirm ADC is working (for Vertex AI)

## Cost Comparison

Both options use the same pricing tier for Gemini 1.5 Flash, but:
- **Vertex AI**: Better for high-volume, team scenarios
- **Google AI API**: Good for development and backup

Check current pricing: https://ai.google.dev/pricing
