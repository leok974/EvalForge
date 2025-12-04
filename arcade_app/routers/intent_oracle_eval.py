# arcade_app/routers/intent_oracle_eval.py

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from arcade_app.config import settings
from arcade_app.auth_helper import get_current_user


router = APIRouter(
    prefix="/api/agents/intent-oracle",
    tags=["agents-intent-oracle"],
)


class IntentOracleEvalRequest(BaseModel):
    """
    Request body for running the Intent Oracle planner evaluation.

    If candidate_path is omitted, we fall back to a default planner file.
    """
    candidate_path: Optional[str] = Field(
        default=None,
        description="Path to candidate planner file containing plan_actions().",
    )


class IntentOracleEvalResponse(BaseModel):
    """
    Normalized response for planner evaluation via the Intent Oracle boss.
    """
    boss_id: str = Field(default="intent_oracle")
    success: bool
    score: Optional[float] = None
    rubric: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None

    # 🔹 New optional UX fields
    integrity_before: Optional[int] = None
    integrity_after: Optional[int] = None
    integrity_delta: Optional[int] = None

    boss_hp_before: Optional[int] = None
    boss_hp_after: Optional[int] = None
    boss_hp_delta: Optional[int] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_candidate_path(candidate_path: Optional[str]) -> str:
    """
    Resolve candidate_path to an absolute path string.

    If None, fall back to scripts/agents/candidate_planner.py

    Raises HTTPException 400 if the path does not exist.
    """
    if candidate_path:
        p = Path(candidate_path)
    else:
        p = Path("scripts/agents/candidate_planner.py")

    # Ensure directory exists if we are going to write a default file (for dev convenience)
    if not p.exists() and p.name == "candidate_planner.py":
         # Create a dummy one if it doesn't exist, just to be safe for the demo
         p.parent.mkdir(parents=True, exist_ok=True)
         with open(p, "w") as f:
            f.write("def plan_actions(goal, tools):\n    return [{'tool': 'none', 'reason': 'Default dummy planner'}]")

    if not p.is_file():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Candidate planner not found at: {p}",
        )
    return str(p.resolve())


def _run_via_subprocess(candidate_path: str) -> IntentOracleEvalResponse:
    """
    Fallback path: run the local CLI script directly (no Antigravity required).

    This calls:
        python scripts/agents/run_intent_oracle_eval.py <candidate_path>

    and expects that script to print a JSON object with
    fields like { boss_id, success, score, rubric, ... }.
    """
    script_path = Path("scripts/agents/run_intent_oracle_eval.py")
    if not script_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Eval script not found at {script_path}. "
                   f"Make sure scripts/agents/run_intent_oracle_eval.py exists.",
        )

    env = os.environ.copy()

    # Where the backend is reachable from the script's point of view
    evalforge_base = settings.public_base_url or "http://localhost:8081"
    env.setdefault("EVALFORGE_BASE_URL", evalforge_base)

    # Token for calling /api/boss/* endpoints
    token = settings.intent_oracle_eval_token
    if not token:
        # Fallback for dev
        if settings.environment == "dev":
            token = "mock-token"
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="INTENT_ORACLE_EVAL_TOKEN is not configured. "
                       "Set this in your .env so the eval script can "
                       "talk to the boss endpoints.",
            )
    env["EVALFORGE_API_TOKEN"] = token

    try:
        # Use sys.executable to ensure we use the same python environment
        import sys
        proc = subprocess.run(
            [sys.executable, str(script_path), candidate_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Local Intent Oracle eval timed out: {exc}",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute local eval script: {exc}",
        ) from exc

    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "").strip()
        # Log stderr for debugging
        print(f"Subprocess failed. Stderr: {proc.stderr}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Local Intent Oracle eval failed (exit {proc.returncode}): {msg[:256]}",
        )

    stdout = proc.stdout.strip()
    if not stdout:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Local eval script produced no output.",
        )

    try:
        payload_json = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Local eval script returned invalid JSON: {exc}",
        ) from exc

    return IntentOracleEvalResponse(
        boss_id=payload_json.get("boss_id", "intent_oracle"),
        success=bool(payload_json.get("success", False)),
        score=payload_json.get("score"),
        rubric=payload_json.get("rubric"),
        raw=payload_json,

        # Optional meta if your eval script returns them
        integrity_before=payload_json.get("integrity_before"),
        integrity_after=payload_json.get("integrity_after"),
        integrity_delta=payload_json.get("integrity_delta"),
        boss_hp_before=payload_json.get("boss_hp_before"),
        boss_hp_after=payload_json.get("boss_hp_after"),
        boss_hp_delta=payload_json.get("boss_hp_delta"),
    )


def _run_via_antigravity(candidate_path: str) -> IntentOracleEvalResponse:
    """
    Preferred path (when configured): call Antigravity subagent intent-oracle-evaluator.

    Expects Antigravity to respond with:
        {
          "status": "completed",
          "output": { boss_id, success, score, rubric, ... }
        }
    """
    ag_base = settings.antigravity_base_url
    ag_token = settings.antigravity_api_token
    if not ag_base or not ag_token:
        # Should never be called if env is not configured; guard anyway.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Antigravity is not configured (ANTIGRAVITY_BASE_URL / ANTIGRAVITY_API_TOKEN).",
        )

    evalforge_base = settings.public_base_url or "http://localhost:8081"
    evalforge_token = settings.intent_oracle_eval_token
    if not evalforge_token:
         if settings.environment == "dev":
            evalforge_token = "mock-token"
         else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="INTENT_ORACLE_EVAL_TOKEN is not configured.",
            )

    # Build subagent request payload
    inputs: Dict[str, Any] = {
        "BASE_URL": evalforge_base,
        "API_TOKEN": evalforge_token,
        "CANDIDATE_PATH": candidate_path,
    }

    ag_url = ag_base.rstrip("/") + "/api/subagents/run"
    req_payload: Dict[str, Any] = {
        "subagent": "intent-oracle-evaluator",
        "mode": "sync",
        "inputs": inputs,
    }

    try:
        resp = httpx.post(
            ag_url,
            json=req_payload,
            headers={"Authorization": f"Bearer {ag_token}"},
            timeout=90.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to contact Antigravity at {ag_url}: {exc}",
        ) from exc

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Antigravity returned {resp.status_code}: {resp.text[:256]}",
        )

    try:
        job = resp.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Antigravity response was not valid JSON: {exc}",
        ) from exc

    status_value = job.get("status")
    if status_value != "completed":
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Antigravity job did not complete successfully (status={status_value}).",
        )

    output = job.get("output") or {}

    return IntentOracleEvalResponse(
        boss_id=output.get("boss_id", "intent_oracle"),
        success=bool(output.get("success", False)),
        score=output.get("score"),
        rubric=output.get("rubric"),
        raw=output,

        integrity_before=output.get("integrity_before"),
        integrity_after=output.get("integrity_after"),
        integrity_delta=output.get("integrity_delta"),
        boss_hp_before=output.get("boss_hp_before"),
        boss_hp_after=output.get("boss_hp_after"),
        boss_hp_delta=output.get("boss_hp_delta"),
    )


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.post("/eval", response_model=IntentOracleEvalResponse)
def eval_intent_oracle(
    payload: IntentOracleEvalRequest,
    user=Depends(get_current_user),
) -> IntentOracleEvalResponse:
    """
    Run the Intent Oracle boss evaluation for a planner implementation.

    Behavior:
    - If ANTIGRAVITY_BASE_URL + ANTIGRAVITY_API_TOKEN are set:
        -> use Antigravity subagent (intent-oracle-evaluator).
    - Otherwise:
        -> fall back to running the local eval script via subprocess.
    """
    candidate_path = _resolve_candidate_path(payload.candidate_path)

    # If Antigravity is configured, use it
    if settings.antigravity_base_url and settings.antigravity_api_token:
        return _run_via_antigravity(candidate_path)

    # Fallback: local script
    return _run_via_subprocess(candidate_path)


# --- History Endpoint ---

class IntentOracleEvalRun(BaseModel):
    id: str
    timestamp: datetime
    success: bool
    score: Optional[float] = None
    candidate_path: Optional[str] = None
    source: Optional[str] = None  # subagent name, "manual"/"auto", etc.
    raw: Optional[Dict[str, Any]] = None


class IntentOracleEvalHistoryResponse(BaseModel):
    runs: List[IntentOracleEvalRun]


@router.get("/eval/history", response_model=IntentOracleEvalHistoryResponse)
def eval_intent_oracle_history(
    limit: int = 5,
    user=Depends(get_current_user),
) -> IntentOracleEvalHistoryResponse:
    """
    Return a recent history of Intent Oracle planner eval runs.

    This proxies Antigravity's runs API, filtered to the intent-oracle-evaluator subagent.
    """
    ag_base = settings.antigravity_base_url
    ag_token = settings.antigravity_api_token
    if not ag_base or not ag_token:
        # Fallback for dev/demo if Antigravity not configured
        # We could return local history if we were tracking it, but for now just empty
        return IntentOracleEvalHistoryResponse(runs=[])

    ag_url = ag_base.rstrip("/") + "/api/subagents/runs"

    try:
        resp = httpx.get(
            ag_url,
            params={
                "subagent": "intent-oracle-evaluator",
                "limit": limit,
            },
            headers={"Authorization": f"Bearer {ag_token}"},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to contact Antigravity at {ag_url}: {exc}",
        ) from exc

    if resp.status_code != 200:
        # Be graceful if history fails
        return IntentOracleEvalHistoryResponse(runs=[])

    try:
        runs_raw = resp.json()
    except json.JSONDecodeError:
        return IntentOracleEvalHistoryResponse(runs=[])

    if not isinstance(runs_raw, list):
        return IntentOracleEvalHistoryResponse(runs=[])

    runs: List[IntentOracleEvalRun] = []
    for item in runs_raw:
        output = item.get("output") or {}
        inputs = item.get("inputs") or {}
        created = item.get("created_at") or item.get("started_at") or None
        try:
            ts = datetime.fromisoformat(created.replace("Z", "+00:00")) if created else datetime.utcnow()
        except Exception:
            ts = datetime.utcnow()

        runs.append(
            IntentOracleEvalRun(
                id=str(item.get("id")),
                timestamp=ts,
                success=bool(output.get("success", False)),
                score=output.get("score"),
                candidate_path=inputs.get("CANDIDATE_PATH"),
                source=item.get("subagent", "intent-oracle-evaluator"),
                raw=item,
            )
        )

    return IntentOracleEvalHistoryResponse(runs=runs)


# --- Auto-Eval Endpoint ---

class IntentOracleAutoEvalRequest(BaseModel):
    repo_url: str = Field(..., description="Git repo URL containing planner source/generator.")
    branch: Optional[str] = Field(
        default=None,
        description="Optional branch name to checkout.",
    )
    planner_rel_path: Optional[str] = Field(
        default="scripts/agents/candidate_planner.py",
        description="Relative path inside the repo to the candidate planner.",
    )
    planner_generator: Optional[str] = Field(
        default="",
        description=(
            "Optional shell command to generate the planner file. "
            "May contain {PLANNER_REL_PATH} placeholder."
        ),
    )


@router.post("/auto-eval", response_model=IntentOracleEvalResponse)
def eval_intent_oracle_auto(
    payload: IntentOracleAutoEvalRequest,
    user=Depends(get_current_user),
) -> IntentOracleEvalResponse:
    """
    Use Antigravity to clone a repo, optionally generate a planner, and run
    the Intent Oracle boss evaluation in a single shot.
    """
    ag_base = settings.antigravity_base_url
    ag_token = settings.antigravity_api_token
    if not ag_base or not ag_token:
        # No fallback for auto-eval yet (requires cloning logic locally which we moved to subagent)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Auto-eval requires Antigravity configuration.",
        )

    evalforge_base = settings.public_base_url or "http://localhost:8081"
    evalforge_token = settings.intent_oracle_eval_token
    if not evalforge_token:
        if settings.environment == "dev":
            evalforge_token = "mock-token"
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="INTENT_ORACLE_EVAL_TOKEN is not configured.",
            )

    inputs: Dict[str, Any] = {
        "BASE_URL": evalforge_base,
        "API_TOKEN": evalforge_token,
        "REPO_URL": payload.repo_url,
        "BRANCH": payload.branch or "",
        "PLANNER_REL_PATH": payload.planner_rel_path or "scripts/agents/candidate_planner.py",
        "PLANNER_GENERATOR": payload.planner_generator or "",
    }

    ag_url = ag_base.rstrip("/") + "/api/subagents/run"
    req_payload = {
        "subagent": "intent-oracle-auto-evaluator",
        "mode": "sync",
        "inputs": inputs,
    }

    try:
        resp = httpx.post(
            ag_url,
            json=req_payload,
            headers={"Authorization": f"Bearer {ag_token}"},
            timeout=180.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to contact Antigravity at {ag_url}: {exc}",
        ) from exc

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Antigravity returned {resp.status_code}: {resp.text[:256]}",
        )

    try:
        job = resp.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Antigravity response was not valid JSON: {exc}",
        ) from exc

    status_value = job.get("status")
    if status_value != "completed":
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Antigravity auto-eval job did not complete successfully (status={status_value}).",
        )

    output = job.get("output") or {}
    return IntentOracleEvalResponse(
        boss_id=output.get("boss_id", "intent_oracle"),
        success=bool(output.get("success", False)),
        score=output.get("score"),
        rubric=output.get("rubric"),
        raw=output,
    )
