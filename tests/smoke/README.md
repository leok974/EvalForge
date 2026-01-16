# Smoke Tests

Smoke tests ensure core functionality works end-to-end. These are fast, lightweight tests that run in CI on every commit.

## What We Test

- ✅ Health endpoints (`/health`, `/healthz`)
- ✅ Version endpoint (`/version`)
- ✅ Universe data availability and structure
- ✅ Quest endpoints for all worlds (Python, TypeScript, Java)
- ✅ Database readiness

## Running Locally

```powershell
# Ensure test database is set up
$env:DATABASE_URL = "postgresql+asyncpg://evalforge_app:evalforge_dev@127.0.0.1:5435/evalforge"
$env:PYTHONPATH = "D:\EvalForge"

# Run smoke tests
pytest tests/smoke/ -v

# Run specific test
pytest tests/smoke/test_api_smoke.py::test_universe_endpoint -v
```

## Running in CI

These tests run automatically in GitHub Actions via `.github/workflows/smoke-test.yml`.

The workflow:
1. Starts a PostgreSQL service container
2. Initializes the database schema
3. Seeds universe data
4. Runs the smoke test suite

## What Failures Mean

| Test | Failure Indicates |
|------|-------------------|
| `test_health_endpoint` | FastAPI app not starting |
| `test_universe_endpoint` | Missing seeded data or broken universe route |
| `test_quests_endpoint_*` | Missing quests or broken quest route |
| `test_ready_endpoint` | Database connection issues |

## Adding New Smoke Tests

Keep smoke tests:
- **Fast**: < 1 second per test
- **Critical**: Only test essential functionality
- **Independent**: No shared state between tests
- **Clear**: Obvious what broke when they fail

Example:
```python
@pytest.mark.asyncio
async def test_new_feature():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/new-feature")
        assert response.status_code == 200
        assert response.json()["feature"] == "working"
```
