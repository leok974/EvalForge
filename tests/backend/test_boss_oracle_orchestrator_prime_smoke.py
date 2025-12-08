import pytest

@pytest.mark.asyncio
async def test_oracle_orchestrator_prime_boss_judge_smoke(client, db_session):
    """
    Smoke test: ensure Oracle Orchestrator Prime boss QA returns a valid BossEvalResult.
    """
    import os
    os.environ["EVALFORGE_MOCK_GRADING"] = "1"

    from arcade_app.models import BossDefinition
    
    # Seed the boss
    boss_slug = "boss-oracle-orchestrator-prime"
    boss_def = BossDefinition(
        id=boss_slug,
        name="Oracle Orchestrator Prime",
        rubric=boss_slug,
        world_id="world-agents",
        track_id="oracle-senior-orchestrator",
        difficulty="legendary",
        max_hp=100
    )
    db_session.add(boss_def)
    await db_session.commit()

    payload = {
        "world_slug": "world-agents",
        "boss_id": boss_slug,
        "mode": "smoke",
        "submission_markdown": """# Agentic Orchestrator Blueprint – Oracle Orchestrator Prime

## Use Case & Requirements
We are designing a multi-agent assistant that helps engineers debug production issues
by searching logs, querying metrics, and proposing remediation steps.
The system must be safe, observable, and able to improve over time.

## Agent Graph & Roles
- Planner Agent: reads the user problem, proposes a plan, and decomposes into steps.
- Tools Router: decides which tool-capable agent should handle each step.
- Logs Agent: specialized in log search and summarization with a limited tool set.
- Metrics Agent: queries metrics and explains anomalies.
- Fix Draft Agent: proposes remediation steps with explicit 'DO / DO NOT' sections.
- Safety Guard Agent: reviews actions and outputs against policy before they reach the user.
- Evaluator Agent: scores completed runs and suggests improvements.

State:
- A central Run State holds the user request, plan, step results, and decisions.
- Each agent reads/writes specific fields; the orchestrator enforces boundaries.

## Tool Contracts & IO
Each tool is defined with a typed contract:
- `search_logs(query: string, window: TimeRange) -> LogSummary`
- `query_metric(name: string, window: TimeRange) -> MetricSummary`
- `open_ticket(summary: string, details: string) -> TicketRef`

Contracts:
- Inputs/outputs have JSON schemas with explicit field names and types.
- Errors: all tools return structured error objects, not raw exceptions.
- Timeouts and retries: tools enforce time limits; the orchestrator handles retries with backoff.
- Only the Tools Router can invoke tools directly; worker agents must request tool calls via intents.

## Policy & Guardrails
- Global safety policy is enforced by the Safety Guard Agent.
- Safety Guard checks:
  - No direct destructive actions (e.g., executing shell commands) are allowed in this system.
  - No PII is logged or echoed back.
  - Remediation suggestions are written as 'proposed steps', not auto-applied changes.
- Per-agent prompts include role-specific constraints (e.g., Logs Agent cannot open tickets).
- Denials:
  - If a proposed action violates policy, the Safety Guard blocks it,
    adds a policy_violation entry to run state, and returns a safe explanation to the user.

## Observability & Run State
- Each run has a unique run_id.
- For every agent step, we log:
  - run_id, agent_name, step_index, inputs (redacted), outputs (redacted), tool calls, and timing.
- We emit traces that show the full decision tree of the run.
- Run state is persisted with a compact summary and links to logs/traces.

## Evaluation & Improvement Loop
- Metrics:
  - Task success rate (did the user accept the proposed explanation/remediation?).
  - Tool error rate and timeouts.
  - Policy violation rate.
- We sample a subset of runs weekly for human review and label correctness and safety.
- Evaluator Agent:
  - Uses metrics and annotated runs to suggest prompt/policy tweaks.
  - Proposals are reviewed by humans before applying.

## Rollout & Risk Management
- Start with read-only tools only (logs and metrics); ticket creation is gated behind a flag.
- Introduce agents gradually (planner + logs first, then metrics, then fix-draft).
- Monitor metrics and policy violations; rollback to a simpler single-agent fallback if needed.
"""
    }

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    assert resp.status_code == 200

    data = resp.json()

    # Validate WorldBossQAReport structure
    assert "results" in data
    assert len(data["results"]) >= 1
    
    result = data["results"][0]
    assert result["boss_slug"] == "boss-oracle-orchestrator-prime"
    assert result["rubric_id"] == "boss-oracle-orchestrator-prime"

    # Score & integrity
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 8

    assert isinstance(result["grade"], str)
    assert result["grade"] in ["S", "A", "B", "C", "F", "MISSING"]

    crit = {c["id"]: c for c in result.get("criteria", [])}

    for key in [
        "architecture_and_roles",
        "tooling_and_contracts",
        "guardrails_and_policy",
        "observability_and_eval_loop"
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(result.get("strengths", []), list)
    assert isinstance(result.get("improvements", []), list)
