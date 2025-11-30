Write-Host "🧪 Running Backend Tests..." -ForegroundColor Cyan
python -m pytest tests/backend/

Write-Host "🧪 Running Frontend Tests..." -ForegroundColor Cyan
cd apps/web
npm run test -- run
cd ../..

# Optional: Run E2E (Requires server running)
# Write-Host "🧪 Running E2E Tests..." -ForegroundColor Cyan
# npx playwright test
