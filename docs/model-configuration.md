# Model Configuration

EvalForge supports three LLM modes:

1. **Vertex AI (production / real grading)**
2. **Local model (developer experimentation)**
3. **Mock grading (no external LLM calls, deterministic for demos & tests)**

All modes are controlled via environment variables.

---

## 1. Vertex AI (recommended for real grading)

**Required env vars:**

- `EVALFORGE_MOCK_GRADING=0`
- `GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>`
- `GOOGLE_CLOUD_LOCATION=us-central1`
- `EVALFORGE_MODEL_VERSION=gemini-2.5-flash`

> **Important:** Use the **stable model name** `gemini-2.5-flash` (without `-001`) in `us-central1`.  
> Old names like `gemini-2.5-flash-001`, `gemini-3.0-flash-001`, or `gemini-1.5-flash-001` will return **404 Not Found**.

### Quickstart (.env example)

```env
EVALFORGE_MOCK_GRADING=0
GOOGLE_CLOUD_PROJECT=my-evalforge-project
GOOGLE_CLOUD_LOCATION=us-central1
EVALFORGE_MODEL_VERSION=gemini-2.5-flash
```

Then start the server (example):

```bash
# Using the startup script (Recommended)
./scripts/start_evalforge.ps1

# Or manually
python -m uvicorn arcade_app.agent:app --host 0.0.0.0 --port 8092
```

---

## 2. Local model mode (for offline / cheap dev)

*Currently, the code is optimized for Vertex AI. To use a local model, you would need to adapt `grading_helper.py` and `coach_helper.py` to use a local provider.*

---

## 3. Mock grading mode (no external LLM calls)

Use this for **demos, tests, and when Vertex isn’t configured**.

```env
EVALFORGE_MOCK_GRADING=1
# Provider/model vars can be left as-is; they’re ignored in mock mode.
```

In this mode, the judge / coach use deterministic, rule-based scoring so the UI works even without network access.

---

## 4. Troubleshooting 404s and common issues

### 404 Not Found from Vertex AI

Check:

1. **Model name**

   * ✅ `gemini-2.5-flash`
   * ❌ `gemini-2.5-flash-001`, `gemini-3.0-flash-001`, `gemini-1.5-flash-001`

2. **Location**

   * Use `GOOGLE_CLOUD_LOCATION=us-central1` for `gemini-2.5-flash`.
   * If you later use preview models that require `global`, make sure the location matches.

3. **Project / auth**

   * `GOOGLE_CLOUD_PROJECT` set correctly.
   * ADC / service account has Vertex AI permissions.

### Verifying configuration

1. Run the app.
2. Hit the Dev UI (e.g. `http://localhost:8092`).
3. Create a session and type `start` → **RUN**.
   If the response is helpful and non-deterministic, you’re on real LLM mode.
   If logs show “mock grading enabled”, you’re in mock mode.
