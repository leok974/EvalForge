# AI Trainer Arcade (ADK + Cloud Run)

> 🔒 **This repo is EvalForge only.**  
> If you are about to scaffold **TasteOS**, use a separate folder: `D:\TasteOS`  
> See [.vscode/README_EVALFORGE_CONTRACT.md](.vscode/README_EVALFORGE_CONTRACT.md) for details.

Multi-agent trainer (Judge + Coach) built with **Google's ADK** and deployable to **Cloud Run** in one command. Ships with a **real Vitest exercise** and working test runners.

## ✅ Status: Fully Functional & Deployed

- ✅ Multi-agent system (Judge → Coach)
- ✅ Real JavaScript debounce exercise with Vitest
- ✅ 100% test coverage with automatic grading
- ✅ Working on Windows (PowerShell) and Linux (Bash)
- ✅ **DEPLOYED to Cloud Run with Vertex AI**

**🌐 Live Production:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/

## Quick start (local)

```powershell
# Windows PowerShell
cd d:\EvalForge
D:/EvalForge/.venv/Scripts/python.exe -m google.adk.cli web arcade_app --port 9000

# Or activate venv first:
.\.venv\Scripts\Activate.ps1
adk web arcade_app --port 9000
```

```bash
# Linux/Mac
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start local ADK UI or API server
adk web arcade_app         # local web UI
# or
adk api_server arcade_app  # local REST API
```

**Access at: http://127.0.0.1:9000**

## Test the system

### Via ADK UI
1. Open http://127.0.0.1:9000
2. Select **ArcadeOrchestrator** agent
3. Message: "Run the debounce quest and evaluate it"

### Via Command Line
```powershell
# Windows
pwsh -File scripts/run_vitest.ps1 debounce

# Linux/Mac
bash scripts/run_vitest.sh debounce
```

Expected: 2 tests pass, 100% coverage ✅

## 🚀 Deploy to Cloud Run (Windows)

### Quick Deploy (Recommended)

```powershell
cd D:\EvalForge
.\manual_deploy.ps1
```

The script will:
1. ✅ Copy application files
2. ✅ Generate Dockerfile with module mode + Vertex AI config
3. ✅ Deploy to Cloud Run with environment variables
4. ✅ Return your service URL

**Result:** Your agent will be live at `https://evalforge-agents-<id>.run.app`

### Manual Deploy Commands

```powershell
# Update existing service with env vars
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --project=YOUR-PROJECT-ID `
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID,GOOGLE_CLOUD_LOCATION=us-central1,EVALFORGE_MODEL=gemini-1.5-flash"
```

### Linux/Mac Deployment

```bash
# Auth & project
gcloud auth login
gcloud config set project YOUR_PROJECT
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT
export GOOGLE_CLOUD_LOCATION=us-central1

# Deploy with ADK (Note: Windows has a bug, use manual_deploy.ps1 instead)
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=evalforge-agents \
  --app_name=evalforge \
  --with_ui \
  arcade_app
```

**📚 Deployment Docs:**
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Complete deployment guide
- **[CLOUD_RUN_CONFIG.md](CLOUD_RUN_CONFIG.md)**: Configuration reference
- **[DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md)**: What's deployed and working
- **[DEPLOY_ISSUE.md](DEPLOY_ISSUE.md)**: Windows gcloud bug workaround

## What's included

- **ADK multi-agent system**: Orchestrator → Judge → Coach
- **Real exercise**: JavaScript debounce with TypeScript + Vitest
- **Automatic grading**: Coverage-based (PASS ≥80%, PARTIAL 60-79%, FAIL <60%)
- **Error journaling**: Automatic capture of all test runs for quest generation
- **Tools**: 
  - `run_tests`: Executes test runners (Vitest/Pytest)
  - `grade_submission`: Parses coverage and returns verdict
  - `suggest_next_quests`: Recommends follow-up challenges
- **Seeds**: Skill Tree + 3 quest specs (1 working, 2 ready to implement)
- **Runners**: PowerShell (Windows) and Bash (Linux/Mac)
- **Makefile**: Handy targets for setup/run/deploy
- **VS Code Tasks**: One-click testing with automatic error logging

## Project structure

```
exercises/js/               # Real JavaScript exercise
  ├── src/debounce.ts       # Implementation (100% coverage)
  ├── test/debounce.test.ts # Vitest tests (2 passing)
  └── coverage/             # Auto-generated coverage reports

arcade_app/                 # Multi-agent system
  └── agent.py              # Judge + Coach + Orchestrator

scripts/
  ├── run_vitest.ps1        # PowerShell runner
  └── run_vitest.sh         # Bash runner

seed/
  ├── skilltree.json        # Skill tree data
  └── quests/               # Quest configurations
```

## Next steps

1. **Test locally**: Open http://127.0.0.1:9000 and try the debounce quest ✅
2. **Add Retry quest**: Implement `exercises/js/src/retry.ts` with tests
3. **Deploy to Cloud Run**: Use commands in deployment section for production
4. **Enhance grading**: Add mutation testing, style checks, complexity analysis
5. **(Optional)** Build Quest API with FastAPI to serve `/api/skilltree` & `/api/quests`

## 📚 Documentation

- **[DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md)**: ✅ Live deployment status and access URLs
- **[CLOUD_RUN_CONFIG.md](CLOUD_RUN_CONFIG.md)**: Complete Cloud Run configuration reference
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Full deployment guide with prerequisites
- **[DEPLOY_ISSUE.md](DEPLOY_ISSUE.md)**: Windows gcloud bug documentation
- **[START_SERVER.md](START_SERVER.md)**: Local development server guide
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)**: What's built and verification checklist
- **[TESTING_DEPLOYMENT.md](TESTING_DEPLOYMENT.md)**: Detailed testing guide
- **[ERROR_JOURNALING.md](ERROR_JOURNALING.md)**: Automatic error capture system
- **[ERROR_JOURNALING_QUICKSTART.md](ERROR_JOURNALING_QUICKSTART.md)**: Quick start guide
