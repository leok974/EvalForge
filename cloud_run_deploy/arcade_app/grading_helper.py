"""
Grading helper for evaluating user debugging submissions.
Uses Vertex AI to act as a structured evaluator.
"""
from __future__ import annotations
import os
import json
from time import perf_counter
from typing import Dict, Any, Tuple
import vertexai
from vertexai.generative_models import GenerativeModel

from .session_state import SessionState, Grade, normalize_for_hash, sha1_of_text
from .metrics import JUDGE_GRADE_TOTAL, JUDGE_GRADE_SEC, JUDGE_INPUT_BYTES

# Shared configuration - matches agent.py
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")


def grade_once_with_dedupe(state: SessionState, submission: str) -> Tuple[Grade, str, bool]:
    """
    Grade submission with deduplication.
    
    Returns:
        Tuple of (grade, sha1, is_new)
        - grade: Grade object with rubric scores
        - sha1: Hash of normalized submission
        - is_new: True if this is a new submission, False if deduplicated
    """
    # Normalize and hash submission for deduplication
    norm = normalize_for_hash(submission)
    sha1 = sha1_of_text(norm)
    
    # Check for duplicate
    if state.last_graded_input_hash == sha1 and state.last_grade:
        JUDGE_GRADE_TOTAL.labels(result="dedupe").inc()  # type: ignore[attr-defined]
        return state.last_grade, sha1, False
    
    # New submission - grade it
    JUDGE_INPUT_BYTES.observe(len(submission.encode("utf-8")))  # type: ignore[attr-defined]
    t0 = perf_counter()
    
    # Call the actual grading logic
    grade_dict = _grade_submission_internal(submission, state)
    
    # Convert dict to Grade model
    grade = Grade(
        coverage=grade_dict["coverage"],
        correctness=grade_dict["correctness"],
        clarity=grade_dict["clarity"],
        comment=grade_dict["comment"]
    )
    
    # Update state
    state.last_grade = grade
    state.last_graded_input_hash = sha1
    
    JUDGE_GRADE_TOTAL.labels(result="new").inc()  # type: ignore[attr-defined]
    JUDGE_GRADE_SEC.observe(perf_counter() - t0)  # type: ignore[attr-defined]
    
    return grade, sha1, True


def _grade_submission_internal(submission: str, state: SessionState) -> Dict[str, Any]:
    """
    Grade a user's debugging submission using a structured rubric.
    
    Uses Vertex AI to evaluate the submission against the rubric.
    
    Args:
        submission: User's code/text submission
        state: Current session state for context
    
    Returns:
        Dictionary with coverage, correctness, clarity, comment
    """
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

**User's submission:**
```
{submission}
```

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
        
        return grade
        
    except Exception as e:
        # Graceful fallback if model call fails
        return {
            "coverage": 0,
            "correctness": 0,
            "clarity": 0,
            "comment": f"Grading error: {str(e)[:100]}"
        }
