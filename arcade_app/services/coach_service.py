
import os
import logging
from typing import Optional, Dict, Any

# Internal
from arcade_app.schemas.coach_schemas import (
    CoachRequest, CoachResponse, 
    SafetyAssessment, UnifiedDiff, 
    Hypothesis, NextStep
)
from arcade_app.services import coach_prompts

# External (Google Gen AI SDK - Python)
# Requires: pip install google-genai
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

logger = logging.getLogger(__name__)

# --- Configuration ---
# Models
MODEL_FAST = os.getenv("EF_GEMINI_MODEL_FAST", "gemini-2.0-flash-001") # Fallback to 2.0 Flash if 3 not avail
MODEL_DEEP = os.getenv("EF_GEMINI_MODEL_DEEP", "gemini-2.0-pro-exp") # Fallback to 2.0 Pro if 3 not avail

# Auth
API_KEY = os.getenv("GEMINI_API_KEY")

class CoachService:
    def __init__(self):
        self.enabled = os.getenv("EF_COACH_ENABLED", "0") == "1"
        self.client = None
        
        if self.enabled:
            if not API_KEY:
                logger.warning("EF_COACH_ENABLED=1 but GEMINI_API_KEY is missing.")
            elif not HAS_GENAI:
                logger.warning("EF_COACH_ENABLED=1 but google-genai package is missing.")
            else:
                try:
                    self.client = genai.Client(api_key=API_KEY)
                    logger.info(f"CoachService initialized with models: Fast={MODEL_FAST}, Deep={MODEL_DEEP}")
                except Exception as e:
                    logger.error(f"Failed to init Gemini Client: {e}")

    async def process_request(self, req: CoachRequest) -> CoachResponse:
        """
        Main entrypoint.
        1. Determines mode (Auto -> Explain/Debug).
        2. Selects model.
        3. Calls Gemini.
        4. Enforces guardrails.
        """
        if not self.client:
            return self._mock_fallback(req, "Coach service is disabled or misconfigured.")

        # 1. Resolve Mode
        effective_mode = req.mode
        if effective_mode == "auto":
            # Heuristic: If tests failed or failing_tests_text populated -> DEBUG
            # Else -> EXPLAIN
            has_failures = False
            if req.failing_tests_text and len(req.failing_tests_text.strip()) > 10:
                has_failures = True
            
            if req.runner_result:
                 # Check generic runner result indicators if standardized
                 pass 
                 
            effective_mode = "debug" if has_failures else "explain"

        # 2. Prepare Prompt & Schema
        user_prompt = coach_prompts.build_user_prompt(req.model_dump())
        
        if effective_mode == "explain":
            sys_prompt = coach_prompts.EXPLAIN_SYSTEM_PROMPT
            model_id = MODEL_FAST # Explain is usually easier
        else:
            sys_prompt = coach_prompts.DEBUG_SYSTEM_PROMPT
            model_id = MODEL_FAST # Start fast, could escalate to DEEP if we had retry logic (simplifying for now)

        # 3. Call Gemini
        try:
            logger.info(f"Coach Calling Gemini ({model_id}) Mode={effective_mode}")
            
            # Using structured output (Pydantic)
            response = self.client.models.generate_content(
                model=model_id,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    response_mime_type="application/json",
                    response_schema=CoachResponse,
                    temperature=0.2
                )
            )
            
            parsed: CoachResponse = response.parsed
            
            # 4. Enforce Guardrails
            if parsed:
                # Force mode match (in case model hallucinated wrong mode string)
                parsed.mode = effective_mode 
                
                # Student Mode Safety
                if req.student_mode:
                    if parsed.patch is not None:
                        logger.warning("Coach: Guardrail intercepted a patch in student mode. Stripping it.")
                        parsed.patch = None
                    
                    # Content safety check (simple keyword heuristic)
                    if "diff --git" in parsed.summary_md or "+++" in parsed.summary_md:
                         logger.warning("Coach: Guardrail detected diff markers in summary. Redacting.")
                         parsed.summary_md = "(Summary redacted regarding code patch due to student mode protections)"
                         parsed.safety.blocked = True
                         parsed.safety.solution_leak_risk = "high"

                return parsed
            else:
                return self._mock_fallback(req, "Model returned empty response.")

        except Exception as e:
            logger.error(f"Gemini Call Failed: {e}")
            return self._mock_fallback(req, f"AI Provider Error: {str(e)}")

    def _mock_fallback(self, req: CoachRequest, reason: str) -> CoachResponse:
        """Returns a valid schema response when AI fails or is disabled."""
        mode = "debug" if req.mode == "auto" or req.mode == "debug" else "explain"
        
        return CoachResponse(
            mode=mode,
            summary_md=f"**Coach Service Unavailable**: {reason}",
            hypotheses=[Hypothesis(title="Service Error", evidence=[reason])],
            next_steps=[NextStep(label="Check configuration", action="read", target="logs")],
            patch=None,
            confidence=0.0,
            safety=SafetyAssessment(solution_leak_risk="low", blocked=False)
        )

# Global Instance
coach_service = CoachService()
