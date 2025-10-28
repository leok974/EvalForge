# EvalForge Quick Reference Card

## 🚀 Common Commands

### Deploy
```powershell
./manual_deploy.ps1              # Full deployment with guards
```

### Rollback
```powershell
./fast_rollback.ps1              # Interactive rollback
./fast_rollback.ps1 -DryRun      # Preview only
```

### Test
```powershell
python tests/test_env_model.py   # Model config test
```

### Monitor
```bash
# View errors
gcloud logging read 'resource.type="cloud_run_revision" AND severity>=ERROR' --limit=10

# Check model
gcloud run services describe evalforge-agents --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)" | grep GENAI_MODEL
```

## 🔥 Emergency Procedures

### Service Down
1. Check revision traffic: `gcloud run services describe evalforge-agents --region us-central1`
2. Rollback: `./fast_rollback.ps1`
3. Switch to Plan B: See `docs/PLAN_B_GOOGLE_AI_API.md`

### 404 Model Error
1. Verify env vars: Check `GENAI_MODEL=gemini-1.5-flash-002`
2. Pin traffic to latest: `gcloud run services update-traffic evalforge-agents --region=us-central1 --to-latest`
3. Redeploy if needed: `./manual_deploy.ps1`

### 403 Permission Error
1. Check IAM: Service account needs `roles/aiplatform.user`
2. Verify API enabled: `gcloud services list --enabled | grep aiplatform`
3. Check ADC: `gcloud auth application-default print-access-token`

## 📊 Health Checks

```bash
# Get service URL
BASE=$(gcloud run services describe evalforge-agents --region us-central1 --format='value(status.url)')

# Test endpoints
curl -sf "$BASE/list-apps?relative_path=arcade_app" && echo "✓ discovery"
curl -sf -X POST -H "Content-Length: 0" "$BASE/apps/arcade_app/users/user/sessions" && echo "✓ session"
```

## 🔧 Configuration

### Environment Variables (Locked)
- `GENAI_PROVIDER=vertex`
- `GOOGLE_CLOUD_PROJECT=evalforge-1063529378`
- `VERTEX_LOCATION=us-central1`
- `GENAI_MODEL=gemini-1.5-flash-002`

### Files to Know
- `manual_deploy.ps1` - Main deployment script
- `fast_rollback.ps1` - Emergency rollback
- `tests/test_env_model.py` - Guardrail test
- `docs/TROUBLESHOOTING.md` - Detailed solutions

## 📱 Quick Links
- **Cloud Run:** https://console.cloud.google.com/run
- **Logs:** https://console.cloud.google.com/logs
- **Service:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app
- **Dev UI:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/
