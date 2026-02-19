
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
        
        failure_class = self._detect_failed_state(req.terminal_output_text or "")
        
        if effective_mode == "explain":
            sys_prompt = coach_prompts.EXPLAIN_SYSTEM_PROMPT
            model_id = MODEL_FAST # Explain is usually easier
        else:
            sys_prompt = coach_prompts.DEBUG_SYSTEM_PROMPT
            model_id = MODEL_FAST # Start fast
            
            # INJECT AUTHORITATIVE HINT
        if failure_class:
            logger.info(f"Coach Pre-Parser caught failure: {failure_class}")
            # SYSTEM ERROR SHORT-CIRCUIT
            # If we know the runner failed, do NOT ask the LLM. It will hallucinate.
            return self._mock_fallback(
                req, 
                f"System Error Detected: {failure_class}. The runner failed to execute your code because of an environment or file path issue. Check the logs."
            )
            
        # C2. Config Error Short-Circuit
        config_err = self._detect_config_error(req.runner_result)
        if config_err:
            logger.info(f"Coach caught CONFIG error: {config_err}")
            return self._mock_fallback(
                req, 
                f"Quest Configuration Error: {config_err}\n\nThis is an issue with the quest definition, not your code.\nHint: python arcade_app/force_seed_standard.py --validate-only"
            )

        # 3. Call Gemini

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
                    
                    # Content safety check
                    if "diff --git" in parsed.summary_md or "+++" in parsed.summary_md:
                         logger.warning("Coach: Guardrail detected diff markers in summary. Redacting.")
                         parsed.summary_md = "(Summary redacted regarding code patch due to student mode protections)"
                         parsed.safety.blocked = True
                         parsed.safety.solution_leak_risk = "high"
                
                # Evidence Guardrail
                if failure_class and not parsed.evidence:
                    # If we detected a failure but model gave no evidence, force it
                     logger.warning("Coach: Model failed to cite evidence for detected system failure.")
                     parsed.evidence = ["(System detected error but Coach failed to cite specific log line)"]
                     parsed.confidence = 0.5

                return parsed
            else:
                return self._mock_fallback(req, "Model returned empty response.")

        except Exception as e:
            logger.error(f"Gemini Call Failed: {e}")
            return self._mock_fallback(req, f"AI Provider Error: {str(e)}")

    def _detect_failed_state(self, terminal_text: str) -> Optional[str]:
        """Detects common system/runner failures from terminal output."""
        if not terminal_text:
            return None
            
        # 1. Workspace Missing (Errno 2)
        if "No such file or directory" in terminal_text and ("can't open file" in terminal_text or "[Errno 2]" in terminal_text):
            return "WORKSPACE_MISSING"
            
        # 2. Dependency Missing
        if "ModuleNotFoundError" in terminal_text or "ImportError" in terminal_text:
            return "DEPENDENCY_MISSING"
            
        # 3. Syntax Error (Before code runs)
        if "SyntaxError:" in terminal_text:
            return "SYNTAX_ERROR"
            
        return None

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

    def _detect_config_error(self, runner_result: Optional[Dict[str, Any]]) -> Optional[str]:
        """Scans runner result for CONFIG_INVALID_OBJECTIVES."""
        if not runner_result:
            return None
            
        # Strategy: Look for specific ID or Kind in the result structure
        # Structure varies (might be raw list wrapped in dict, or dict of results)
        
        candidates = []
        if isinstance(runner_result, dict):
            # Check for direct keys
            if runner_result.get("id") == "CONFIG_INVALID_OBJECTIVES" or runner_result.get("kind") == "config":
                return runner_result.get("actual") or runner_result.get("detail")
            
            # Check 'objectives' list
            if "objectives" in runner_result and isinstance(runner_result["objectives"], list):
                candidates.extend(runner_result["objectives"])
            
            # Check if values are results (dict of dicts - less likely but possible)
            for v in runner_result.values():
                if isinstance(v, dict) or isinstance(v, list):
                    if isinstance(v, list):
                        candidates.extend(v)
                    else:
                        candidates.append(v)

        for c in candidates:
            if isinstance(c, dict):
                if c.get("id") == "CONFIG_INVALID_OBJECTIVES" or c.get("kind") == "config":
                    return c.get("actual") or c.get("detail") or "Invalid Quest Configuration"
                    
        return None

# Global Instance
coach_service = CoachService()
