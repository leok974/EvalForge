"""
Grading helper for evaluating user debugging submissions.
Uses Vertex AI to act as a structured evaluator.
"""
import os
import json
import hashlib
from typing import Dict, Any
import vertexai
from vertexai.generative_models import GenerativeModel

from .session_state import session_store

# Shared configuration - matches agent.py
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")


def grade_submission(
    session_id: str,
    code_snippet: str,
    explanation_text: str | None,
    vertex_client: Any = None  # type: ignore[name-defined]
) -> Dict[str, Any]:
    """
    Grade a user's debugging submission using a structured rubric.
    
    Rubric:
    - coverage (0-5): Did they identify and address the real bug?
    - correctness (0-5): Would their fix actually work?
    - clarity (0-5): Did they explain clearly what they did?
    - comment (str): Short coaching feedback
    
    Args:
        session_id: Current session identifier
        code_snippet: User's submitted code
        explanation_text: User's explanation (can be None)
        vertex_client: Optional Vertex AI client (unused, for API compatibility)
    
    Returns:
        Dictionary with:
            - grade: Dict with coverage, correctness, clarity, comment
            - input_hash: SHA1 hash of submission for deduplication
    """
    # Get current session state for context
    state = session_store.get(session_id)
    
    # Build grading prompt with rubric
    prompt = f"""You are "Judge", an evaluator for a coding bootcamp.

Grade the user's latest debugging attempt using this rubric:

**Rubric:**
- coverage (0-5): Did they try to fix the right thing / address the real bug?
- correctness (0-5): Would their fix actually work?
- clarity (0-5): Did they explain what they did in a way another engineer could follow?
- comment (short): What should they do next to improve?

**Context from previous turn:**
- Known problem: {state.debug_problem or "none"}
- Suggested next step: {state.debug_next_step or "none"}
- Language: {state.language_hint or "unknown"}

**User's code submission:**
```
{code_snippet}
```

**User's explanation:**
{explanation_text or "(no explanation provided)"}

**Your task:**
Grade this submission. Return ONLY a JSON object with this exact structure:

{{
  "coverage": <integer 0-5>,
  "correctness": <integer 0-5>,
  "clarity": <integer 0-5>,
  "comment": "<short feedback string, max 1-2 sentences>"
}}

Return ONLY valid JSON. Do not include any other text, markdown formatting, or code blocks.
"""

    try:
        # Initialize Vertex AI if not already done
        vertexai.init(project=VERTEX_PROJECT_NUMBER, location=VERTEX_REGION)
        
        # Create model instance
        model = GenerativeModel(VERTEX_MODEL_ID)
        
        # Generate response
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Try to parse JSON from response
        # Handle common formatting issues (markdown code blocks, etc.)
        json_text = result_text
        
        # Remove markdown code blocks if present
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()
        
        # Try to parse
        try:
            grade_data = json.loads(json_text)
            
            # Validate and clean the grade data
            coverage = int(grade_data.get("coverage", 0))
            correctness = int(grade_data.get("correctness", 0))
            clarity = int(grade_data.get("clarity", 0))
            comment = str(grade_data.get("comment", "Good effort. Keep practicing!"))
            
            # Clamp values to 0-5 range
            coverage = max(0, min(5, coverage))
            correctness = max(0, min(5, correctness))
            clarity = max(0, min(5, clarity))
            
            grade: Dict[str, Any] = {
                "coverage": coverage,
                "correctness": correctness,
                "clarity": clarity,
                "comment": comment[:200]  # Limit comment length
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Fallback: parse failed, return safe defaults
            grade: Dict[str, Any] = {  # type: ignore[no-redef]
                "coverage": 2,
                "correctness": 2,
                "clarity": 2,
                "comment": "Submission received. Try to explain your reasoning more clearly."
            }
        
        # Compute input hash for deduplication
        input_hash = hashlib.sha1(
            (code_snippet + (explanation_text or "")).encode("utf-8")
        ).hexdigest()
        
        return {
            "grade": grade,
            "input_hash": input_hash
        }
        
    except Exception as e:
        # Graceful fallback if model call fails
        input_hash = hashlib.sha1(
            (code_snippet + (explanation_text or "")).encode("utf-8")
        ).hexdigest()
        
        return {
            "grade": {
                "coverage": 0,
                "correctness": 0,
                "clarity": 0,
                "comment": f"Grading error: {str(e)[:100]}"
            },
            "input_hash": input_hash
        }
