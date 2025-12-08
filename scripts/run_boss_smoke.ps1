Write-Host "🧪 Running boss smoke tests..." -ForegroundColor Cyan
python -m pytest -q tests/backend -k "boss and smoke" --ignore=tests/backend/test_boss_triggers.py
