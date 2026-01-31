# Quest QA Dashboard

The Quest QA Dashboard is a dev tool for monitoring quest content health and running on-demand integrity checks.

## What It Is

The dashboard provides:
- **Health Monitoring**: Real-time view of quest status across all worlds/tracks
- **Integrity Checks**: On-demand validation that ensures:
  - **Starter code FAILS** (as expected for learner challenges)
  - **Solution code PASSES** (proving the quest is solvable)
- **Smoke Test Results**: Visual display of the latest CI smoke test artifacts

**Why "Integrity" Matters**: A quest has integrity when the starter code correctly represents the challenge (should fail) and the solution code proves it's solvable (should pass). This invariant prevents "broken quests" from shipping.

## How to Use

### Accessing the Dashboard

Navigate to:
```
http://localhost:3000/dev/qa
```

**Note**: Currently dev-only. Future versions may add production admin gating.

### Dashboard Components

#### Overview Cards
- **Total Quests**: Count of all quests in DB
- **Healthy**: Quests where latest integrity check passed
- **Unhealthy**: Quests where latest integrity check failed
- **Unknown**: Quests never tested via dashboard

#### Filters
- **Search**: Filter by quest title or slug
- **World**: Filter by world (Foundry, Prism, Synapse, etc.)
- **Status**: Filter by health status (healthy/unhealthy/unknown)

#### Quest Grid
Each row shows:
- Quest title + slug
- World/track
- Language
- Health status badge
- Last run timestamp
- **Integrity** button (runs starter + solution)

### Running an Integrity Check

1. Click **"Integrity"** button on any quest row
2. Status changes to **"Running..."** with spinner
3. Dashboard polls for updates every 1 second
4. Results modal appears when finished

### Results Modal

The modal displays:
- **Status**: PASSED (green ✓) or FAILED (red ✕)
- **Duration**: Execution time in milliseconds
- **Issues** (if failed): List of what went wrong
  - "Starter code PASSED but should FAIL"
  - "Solution code FAILED but should PASS"
- **Output Logs**: Captured stdout/stderr (sanitized)
- **Raw Result JSON**: Expandable for debugging

## API Contracts

### `GET /api/qa/summary`

Returns global health metrics.

**Response:**
```json
{
  "generated_at": "2026-01-31T12:00:00Z",
  "tracks": [
    {
      "world_id": "foundry",
      "track_id": "beginner",
      "quests_total": 10,
      "healthy": 8,
      "unhealthy": 2,
      "unknown": 0
    }
  ],
  "global": {
    "quests_total": 100,
    "healthy": 85,
    "unhealthy": 10,
    "unknown": 5
  }
}
```

### `GET /api/qa/quests`

Returns list of quests with health status.

**Query Params:**
- `world_id` (optional)
- `track_id` (optional)
- `language` (optional)
- `status` (optional): healthy/unhealthy/unknown
- `q` (optional): search query

**Response:**
```json
{
  "quests": [
    {
      "slug": "quest-py-hello",
      "title": "Hello World",
      "world_id": "foundry",
      "track_id": "beginner",
      "language": "python",
      "health_status": "healthy",
      "last_run_at": "2026-01-31T11:00:00Z",
      "last_run_variant": "integrity"
    }
  ]
}
```

### `POST /api/qa/run`

Triggers an on-demand QA test run.

**Request Body:**
```json
{
  "quest_id": "quest-py-hello",
  "variant": "integrity"
}
```

**Variants:**
- `starter`: Run starter code only
- `solution`: Run solution code only
- `integrity`: Run both + assert invariants

**Response:**
```json
{
  "run_id": "qarun_abc123",
  "status": "queued"
}
```

### `GET /api/qa/runs/{run_id}`

Get status and results of a QA run (polling endpoint).

**Response:**
```json
{
  "id": "qarun_abc123",
  "quest_slug": "quest-py-hello",
  "variant": "integrity",
  "status": "finished",
  "duration_ms": 1234,
  "result": {
    "passed": true,
    "issues": []
  },
  "logs": "Test output...",
  "diagnostics": {},
  "test_summary": {},
  "created_at": "2026-01-31T12:00:00Z"
}
```

**Status Values:**
- `queued`: Waiting to execute
- `running`: Currently executing
- `finished`: Completed successfully
- `failed`: Execution error

### `GET /api/qa/artifacts/{filename}`

Serves allowlisted smoke test artifact files.

**Allowed Files:**
- `smoke-content-failures.json`
- `smoke-content-failures.md`

**Security**: Path traversal attempts (`../`, etc.) are blocked.

## Troubleshooting

### Run Stuck in "Running" State

**Symptom**: Integrity button shows "Running..." indefinitely.

**Causes:**
1. Docker runner not available
2. Quest execution timeout (default: 5s)
3. Backend crash during execution

**Fix:**
1. Check backend logs: `docker compose logs backend`
2. Verify Docker socket mounted: `docker compose exec backend docker ps`
3. Check `qa_runs` table: `SELECT * FROM qa_runs WHERE status = 'running' ORDER BY created_at DESC;`
4. Manually mark as failed if stuck:
   ```sql
   UPDATE qa_runs SET status = 'failed', result_json = '{"error": "timeout"}' WHERE id = 'qarun_...';
   ```

### "Docker Not Available" Error

**Symptom**: Run fails with "docker: command not found" or similar.

**Fix:**
Ensure Docker socket is mounted in `docker-compose.yml`:
```yaml
services:
  backend:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Unix
      - //./pipe/docker_desktop:/var/run/docker.sock  # Windows
```

Restart backend: `docker compose restart backend`

### "Quest Not Found" Error

**Symptom**: Clicking Integrity returns 404 or "Quest not found".

**Causes:**
1. Quest not seeded into DB
2. Quest slug mismatch

**Fix:**
1. Re-run seeding: `python scripts/seed_all.py`
2. Verify quest exists: `SELECT slug FROM questdefinition WHERE slug = 'quest-...'`
3. Check quest JSON for slug typos

### Frontend Shows "Failed to Load QA Data"

**Symptom**: Dashboard displays error message on load.

**Causes:**
1. Backend not running
2. Proxy misconfiguration
3. CORS issue

**Fix:**
1. Verify backend: `curl http://localhost:8092/api/qa/summary`
2. Check Vite proxy in `vite.config.ts`:
   ```ts
   server: {
     proxy: {
       '/api': 'http://127.0.0.1:8092'  // Must use 127.0.0.1, not localhost
     }
   }
   ```
3. Check browser console for CORS errors
4. Restart dev server: `npm run dev`

### Modal Shows No Logs or Empty Result

**Symptom**: Results modal opens but logs/result fields are empty.

**Causes:**
1. Quest has no solution code configured
2. Runner output capture failed
3. Logs sanitization removed everything

**Fix:**
1. Check quest's `smoke` config in JSON:
   ```json
   "smoke": {
     "solution_code": "...",
     "solution_workspace_files": [...]
   }
   ```
2. Check `qa_runs` table for raw result: `SELECT result_json, logs_sanitized FROM qa_runs WHERE id = '...'`
3. If logs are cut off, increase limit in `qa_runner.py`:
   ```python
   qa_run.logs_sanitized = result.get("stdout", "")[:10000]  # Increase from 5000
   ```

## Security & Redaction

### Log Sanitization

All logs displayed in the dashboard are sanitized via:
- Character limit (5000 chars)
- Sensitive pattern redaction (if configured)
- ANSI color code stripping (future)

### Hidden Test Output

If a quest uses `hidden_tests`, the dashboard:
- **Does NOT** show hidden test details in logs
- Shows aggregate pass/fail only
- Redacts specific assertion failures

This prevents leaking solutions.

### Access Control

**Current (Phase 8.0):**
- Dashboard is **dev-only** (available at `/dev/qa`)
- No authentication required in local development

**Future (Phase 8.1+):**
- Production deployment will require admin role
- Route will move to `/admin/qa` with RBAC checks
- API endpoints will validate JWT claims

## Tips & Best Practices

### When to Run Integrity Checks

- After authoring a new quest
- After modifying starter/solution code
- Before committing quest changes
- When CI smoke tests report failures

### Interpreting Results

**Healthy Quest:**
- Starter fails (expected)
- Solution passes (proves solvability)
- Green badge, no issues

**Unhealthy Quest:**
- Starter passes (too easy / broken)
- Solution fails (unsolvable / buggy)
- Red badge, issues listed

**Unknown Quest:**
- Never tested via dashboard
- May still be healthy (e.g., CI tested it)
- Gray badge

### Combining with CLI Tools

Dashboard complements CLI workflows:

1. **Author** with CLI: `python scripts/quest_new.py`
2. **Validate** with CLI: `python scripts/dev_validate_all.py --only-slug quest-...`
3. **Monitor** with Dashboard: Visual health check
4. **Debug** with Dashboard: View logs + issues inline

### Performance Notes

- Integrity checks run **one at a time** (no parallel execution yet)
- Polling interval: 1000ms
- Recommended max concurrent runs: 3-5

## Related Documentation

- [Quest Authoring Guide](./QUEST_AUTHORING.md) - How to create quests
- [Content Integrity CI](./.github/workflows/content-integrity.yml) - Automated smoke tests
- [QA Runner Service](../arcade_app/services/qa_runner.py) - Implementation details
