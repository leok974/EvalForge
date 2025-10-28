# EvalForge - Testing & Deployment Guide

## ✅ Local Setup Complete

### What's Working
- ✅ Real Vitest exercise with debounce implementation
- ✅ 100% test coverage (2 tests passing)
- ✅ Multi-agent system (Judge → Coach)
- ✅ Automatic grading based on test results + coverage
- ✅ ADK Web UI running on http://127.0.0.1:9000

## 🧪 Testing the System

### Option 1: Test via ADK UI (http://127.0.0.1:9000)

1. Select **ArcadeOrchestrator** agent
2. Send a message like: "Run the debounce quest tests"
3. The Judge agent will:
   - Execute `run_tests` with command: `scripts/run_vitest.sh debounce`
   - Parse the coverage JSON
   - Call `grade_submission` with results
   - Return verdict (PASS/PARTIAL/FAIL)
4. The Coach agent will suggest next quests

### Option 2: Test via Python directly

```powershell
cd d:\EvalForge
D:/EvalForge/.venv/Scripts/python.exe -c "from arcade_app.agent import run_tests, grade_submission; result = run_tests('bash scripts/run_vitest.sh debounce', ['exercises/js/coverage/coverage-final.json']); print('Verdict:', grade_submission(result, {}))"
```

Expected output:
```
Verdict: PASS: solid fundamentals (100% coverage); unlock next quest.
```

### Option 3: Test the runner script directly

```powershell
bash scripts/run_vitest.sh debounce
```

Expected: Tests pass and creates `exercises/js/coverage/coverage-final.json`

## 📊 Coverage Grading Logic

- **PASS**: Tests pass + ≥80% coverage
- **PARTIAL (high)**: Tests pass + 60-79% coverage
- **PARTIAL (low)**: Tests pass + <60% coverage  
- **FAIL**: Tests fail (regardless of coverage)

## 🚀 Cloud Run Deployment

### Prerequisites
1. Google Cloud Project with billing enabled
2. APIs enabled: Cloud Run, Artifact Registry, Cloud Build

### Deploy Commands

```powershell
# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:GOOGLE_CLOUD_LOCATION="us-central1"

# Deploy (from repo root)
D:/EvalForge/.venv/Scripts/python.exe -m google.adk.cli deploy cloud_run `
  --project=$env:GOOGLE_CLOUD_PROJECT `
  --region=$env:GOOGLE_CLOUD_LOCATION `
  --service_name=evalforge-agents `
  --app_name=evalforge `
  --with_ui `
  arcade_app
```

The deployment will:
- Build a container image
- Push to Artifact Registry
- Deploy to Cloud Run
- Return a public URL (e.g., https://evalforge-agents-xxx-uc.a.run.app)

## 📁 Project Structure

```
d:\EvalForge/
├── arcade_app/
│   ├── __init__.py           # Package init
│   └── agent.py              # Multi-agent system (Judge + Coach)
├── exercises/
│   └── js/
│       ├── src/
│       │   └── debounce.ts   # Implementation
│       ├── test/
│       │   └── debounce.test.ts  # Vitest tests
│       ├── coverage/         # Generated coverage reports
│       ├── package.json      # Node dependencies
│       └── vitest.config.ts  # Vitest configuration
├── scripts/
│   ├── run_vitest.sh         # Vitest runner (bash)
│   └── run_pytest.sh         # Pytest runner stub
├── seed/
│   ├── skilltree.json        # Skill tree data
│   └── quests/
│       ├── js_debounce_B.json   # Quest config
│       ├── js_retry_I.json      # Future quest
│       └── ops_csp_I.json       # Future quest
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
└── README.md                 # Main documentation
```

## 🔧 Troubleshooting

### "No agents found" in ADK UI
1. Run from repo root: `cd d:\EvalForge`
2. Always pass module: `adk web arcade_app`
3. Activate venv: `.\.venv\Scripts\Activate.ps1`
4. Verify agent exists:
   ```powershell
   python -c "from arcade_app.agent import root_agent; print(root_agent.name)"
   # Expected: ArcadeOrchestrator
   ```

### Tests fail or coverage not found
1. Ensure Node.js is installed
2. Install dependencies: `cd exercises/js; npm install`
3. Run tests manually: `npm test`
4. Check coverage file: `Test-Path exercises/js/coverage/coverage-final.json`

### Port already in use
Use a different port: `adk web arcade_app --port 9001`

## 🎯 Next Steps (Fast Wins)

### 1. Add Retry Quest
```powershell
# Create exercises/js/src/retry.ts
# Create exercises/js/test/retry.test.ts
# Update scripts/run_vitest.sh to support "retry" target
# Test: bash scripts/run_vitest.sh retry
```

### 2. Enhance Grading
- Add mutation testing (Stryker)
- Check for edge cases (negative numbers, empty arrays, etc.)
- Validate code style/lint rules

### 3. Add More Quests
- CSP Nonce with Playwright (ops_csp_I.json)
- API design quests
- Database query optimization
- RAG implementation challenges

### 4. Build Quest API (Optional)
Add a FastAPI service to serve:
- `GET /api/skilltree` → Returns seed/skilltree.json
- `GET /api/quests` → Returns all quest configs
- `POST /api/evaluate` → Runs Judge agent on submitted code

## 📝 Key Files to Customize

1. **arcade_app/agent.py**: 
   - Modify `grade_submission` for your grading logic
   - Add more tools (code review, mutation testing, etc.)
   - Adjust Coach suggestions

2. **seed/quests/*.json**:
   - Add more quest configurations
   - Update rubrics and time limits
   - Point to different test runners

3. **scripts/run_*.sh**:
   - Wire to your actual test infrastructure
   - Add support for different test frameworks
   - Collect more artifacts (mutation reports, etc.)

## 🌐 Production Considerations

- [ ] Set up proper authentication (OAuth, API keys)
- [ ] Add rate limiting
- [ ] Configure monitoring/logging
- [ ] Set up CI/CD pipeline
- [ ] Add database for quest results/user progress
- [ ] Implement quest unlocking logic
- [ ] Add user management
