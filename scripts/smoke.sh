#!/usr/bin/env bash
# scripts/smoke.sh - Cloud Run smoke tests (bash/mac/Cloud Shell)
set -euo pipefail

mkdir -p logs

BASE=$(gcloud run services describe evalforge-agents --region us-central1 --format='value(status.url)')

{
  echo "BASE=$BASE"
  echo "→ discovery"
  curl -sf "$BASE/list-apps?relative_path=arcade_app" >/dev/null
  echo "✓ discovery passed"
  
  echo "→ session"
  curl -sf -X POST -H 'Content-Length: 0' "$BASE/apps/arcade_app/users/user/sessions" >/dev/null
  echo "✓ session passed"
  
  echo "→ grep model env in service spec"
  gcloud run services describe evalforge-agents --region us-central1 --format='value(spec.template.spec.containers[0].env)' | grep -q 'gemini-1.5-flash-002'
  echo "✓ model env verified"
  
  echo ""
  echo "✓ cloud smoke passed"
} | tee logs/smoke.cloud.log
