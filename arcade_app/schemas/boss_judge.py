"""
Boss Judge Result Schema - Strict validation with fail-closed enforcement.

Phase 8.x: Ensures boss judge responses are machine-parseable and valid.
Invalid responses → attempt fails with E_JUDGE_SCHEMA error code.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import json
import re


class RubricRow(BaseModel):
    """Single rubric criterion evaluation."""
    model_config = ConfigDict(extra="forbid")
    
    criterion: str
    score: int = Field(ge=0, le=100)
    evidence: List[str] = Field(default_factory=list)


class BossJudgeResult(BaseModel):
    """
    Boss judge evaluation result - strict schema.
    
    All fields required. Extra fields rejected.
    This is the NEW schema for Phase 8.x (fail-closed).
    """
    model_config = ConfigDict(extra="forbid")
    
    pass_: bool = Field(alias="pass")
    score: int = Field(ge=0, le=100)
    rubric_breakdown: List[RubricRow]
    blocking_issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    model_id: str
    prompt_version: str
    judged_at: str  # ISO8601


def parse_boss_judge_result(raw_text: str, model_id: str, prompt_version: str) -> BossJudgeResult:
    """
    Parse and validate boss judge response.
    
    FAIL-CLOSED: If JSON invalid or schema invalid, raises ValueError.
    Caller should catch and mark attempt as failed with E_JUDGE_SCHEMA.
    
    Args:
        raw_text: Raw LLM response text
        model_id: Model ID used for judging (for metadata)
        prompt_version: Prompt version used (for metadata)
    
    Returns:
        Validated BossJudgeResult
    
    Raises:
        ValueError: If JSON parse fails or schema validation fails
    """
    from datetime import datetime
    
    # Extract JSON (strict, no heuristics)
    try:
        # Try to parse as pure JSON first
        data = json.loads(raw_text.strip())
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        match = re.search(r'```json\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON parse failed (from code block): {e}")
        else:
            # Try to find any JSON object in the text
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                except json.JSONDecodeError as e:
                    raise ValueError(f"JSON parse failed (from text extraction): {e}")
            else:
                raise ValueError("No valid JSON found in response")
    
    # Add metadata if not present
    if "model_id" not in data:
        data["model_id"] = model_id
    if "prompt_version" not in data:
        data["prompt_version"] = prompt_version
    if "judged_at" not in data:
        data["judged_at"] = datetime.utcnow().isoformat()
    
    # Validate schema (strict, extra fields rejected)
    try:
        return BossJudgeResult.model_validate(data)
    except Exception as e:
        raise ValueError(f"Schema validation failed: {e}")
