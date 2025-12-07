### `test_quest_agent_smoke.py` — Quest Agent SSE Smoke Test

**Purpose**

End-to-end smoke test for the Quest Agent pipeline. Verifies that the agent can
serve a request over SSE and produce a response without requiring a live
Vertex AI connection.

**What it covers**

- **SSE plumbing**
  - Hits `GET /apps/arcade_app/users/{user}/sessions/{sid}/query/stream`.
  - Asserts a 200 OK and at least one SSE `data:` event.
- **Quest retrieval**
  - Ensures the current `IN_PROGRESS` quest is fetched from the database.
  - Caught and fixed a bug in `order_index` handling while wiring this up.
- **LLM integration (mocked)**
  - Mocks the full `vertexai` import surface:
    - `vertexai`
    - `vertexai.generative_models`
    - `vertexai.language_models`
    - `vertexai.preview`
    - `vertexai.vision_models`
  - Patches `sys.modules` so deep imports in agent code resolve cleanly.
  - Confirms the agent can call into the mocked LLM client without raising
    `ImportError` or `AttributeError`.
- **Agent logic**
  - Patches `arcade_app.agent.TRACKS` so the agent can locate the requested
    track and associated quest.
  - Verifies the agent transitions from “quest identified” → “call LLM” and
    emits the mocked text.

**Assertions**

- Response status: `200 OK`.
- SSE stream yields a message that includes the string
  `"Hello from Smoke Test Agent"` (mocked LLM output).
- No `UnicodeEncodeError`, `ImportError`, or `AttributeError` during import
  or streaming.

**Notes**

- This test runs entirely against mocks and does **not** require Vertex AI or
  external network access.
- It is intentionally loose on content; it only cares that the loop is alive
  and producing *some* text.
