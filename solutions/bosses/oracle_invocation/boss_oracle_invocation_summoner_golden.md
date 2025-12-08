# Boss: Oracle Invocation Summoner – Golden Invocation Blueprint

Scenario: Research Assistant Agent for a single product team.  
Goal: Answer questions about code, architecture, and incident behavior using:

- `repo_search(query)`
- `doc_search(query)`
- `metrics_query(query)`

---

## Scenario

Engineers ask questions like:

- “Why did latency spike on /api/search after the last deploy?”
- “Where is the retry policy configured for our payment client?”
- “Summarize how the alerts are wired for the checkout flow.”

Constraints:

- The agent has no direct DB or shell access.
- It **must** use the three tools for anything repo/infra-specific.
- It should not hallucinate code or dashboards that do not exist.

---

## Tools

### repo_search(query)

- **Purpose:** Find relevant code snippets, configs, or tests in the repo.
- **Input:** Natural language query (file/function/config-oriented).
- **Output:** A list of snippets with:
  - file path,
  - line range,
  - excerpt,
  - optional metadata (e.g., symbol names).

### doc_search(query)

- **Purpose:** Fetch design docs, ADRs, and runbooks.
- **Input:** Natural language query (architecture or process-oriented).
- **Output:** A list of documents/sections with:
  - title,
  - section heading,
  - excerpt,
  - URL.

### metrics_query(query)

- **Purpose:** Retrieve high-level metrics and alerts.
- **Input:** A structured query string describing:
  - metric or alert name,
  - time window,
  - filter (e.g., endpoint=/api/search).
- **Output:** A small JSON payload with:
  - current value,
  - historical comparison,
  - any active alerts.

All tools:

- Are **idempotent** (safe to retry).
- Can return empty results; the agent must handle this explicitly.

---

## Orchestrator Flow

### Step 0 – Normalize User Intent

1. Parse the user message into a small **intent record**:

   - `question_type` (e.g., `debug_incident`, `explain_code`, `design_overview`).
   - `subjects` (e.g., endpoints, services, features).
   - `time_hints` (e.g., “after last deploy”, “in the last week”).

2. If the question is ambiguous, propose **clarifying questions** instead of guessing.

### Step 1 – Plan

Generate a short, explicit plan before any tool calls:

- Example for: “Why is latency up on /api/search after the last deploy?”

  1. Use `metrics_query` to confirm the latency spike and time window.
  2. Use `repo_search` to find handler and related code for `/api/search`.
  3. Use `doc_search` for any incident/runbook related to search latency.
  4. Correlate metrics, code changes, and docs into a hypothesis + next steps.

The plan is:

- **Visible** in logs (stored as JSON),
- **Editable** via configuration (prompt template).

### Step 2 – Execute Plan with Tools

For each plan step:

1. Decide if a tool is actually needed:

   - If the question concerns specific endpoints, services, or deploys → **must** use at least `metrics_query` and `repo_search`.
   - For pure conceptual questions (e.g., “What is a circuit breaker?”) → can answer from model knowledge, but still prefer `doc_search` if relevant.

2. Execute the matching tool:

   - Call `metrics_query` with a structured query including:
     - endpoint,
     - time window inferred from the deploy hint (e.g., last 24h).
   - Call `repo_search` using endpoint/service names as keywords.
   - Call `doc_search` for “incident runbook”, “search latency”, etc.

3. Summarize each tool result in **internal notes**:

   - Highlight key metrics (before vs after),
   - Highlight code locations and suspected bottlenecks,
   - Highlight relevant runbook sections.

### Step 3 – Synthesize Answer

Using the plan, notes, and tool outputs:

- Construct an answer with:
  - What changed,
  - Evidence from metrics,
  - Evidence from code/config,
  - Links to relevant docs,
  - Suggested next steps.

If data is incomplete:

- Explain what was missing,
- Suggest follow-up queries or manual checks.

---

## Guardrails & Grounding

- **Mandatory grounding rules:**
  - If the user asks about:
    - specific endpoints,
    - specific services,
    - latency/errors/throughput,
    - “after last deploy”
  - → the agent **must** call `metrics_query` before making claims about system behavior.

- **Repo & docs:**
  - Any question about code location or configuration must use `repo_search`.
  - Any question about architecture, alerts, or SLOs should prefer `doc_search`.

- **Tool failures:**
  - On tool error or empty result:
    - retry at most once with a refined query,
    - then report what was missing (“metrics for /api/search not found for last 24h”),
    - avoid guessing.

- **Uncertainty:**
  - When evidence is weak, the agent must:
    - flag hypotheses as hypotheses,
    - propose concrete next checks instead of asserting causes.

---

## Observability & Debugging

### Logging

For each request, emit structured logs:

- `request_id`
- `user_question`
- `intent_record`
- `plan` (steps)
- `tool_calls` (tool, input, truncated output summary)
- `final_answer_summary` (short text)

Logs are JSON lines, safe to feed into ELK/Grafana.

### Metrics

Emit counters:

- `agent_requests_total{question_type=...}`
- `agent_tool_calls_total{tool=...}`
- `agent_grounded_responses_total`
- `agent_grounding_rate` (derived: grounded / total)
- `agent_tool_error_total{tool=...}`

### Config & Prompts

Separate into:

- `prompts/intent_classifier.md`
- `prompts/planner.md`
- `prompts/executor.md`
- `config/tools.yaml`

This allows:

- prompt updates without code changes,
- per-environment tool configs,
- clear diffable changes in Git.

---

## Example Walkthrough

User: “Latency on /api/search has been spiky since yesterday’s deploy. What’s going on?”

1. **Intent:**
   - `question_type = "debug_incident"`
   - `subjects = ["/api/search"]`
   - `time_hints = ["since yesterday's deploy"]`

2. **Plan:**
   - Step 1: `metrics_query` for p95 latency on `/api/search` last 24h.
   - Step 2: `repo_search` for `/api/search` handler and related middleware.
   - Step 3: `doc_search` for “search latency” runbooks.
   - Step 4: Synthesize findings and suggest next steps.

3. **Execution:**
   - metrics: spike at the time of deploy, correlated with increased DB latency.
   - repo: new cache layer added in `search_service.py`.
   - docs: runbook mentions cache misconfiguration as common cause.

4. **Answer (synthesized):**
   - Summarize these 3 inputs,
   - Propose checking cache keys/TTL and DB indexes,
   - Link to the runbook section.

This path is what the boss expects as a “2/2” performance across all dimensions.
