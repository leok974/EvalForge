"""
Debugging mentor helper for analyzing code issues.
Uses Vertex AI to act as a senior code reviewer.
"""
import os
from typing import Dict, Any
import vertexai
from vertexai.generative_models import GenerativeModel

from .session_state import session_store

# Shared configuration - matches agent.py
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")


def analyze_code_issue(session_id: str, code_snippet: str) -> Dict[str, Any]:
    """
    Use the model to act like a senior code reviewer / debugger.
    
    Goals:
    - Identify the main bug / risk / logic flaw
    - Propose a concrete fix or corrected version
    - Summarize what concept the user is missing
    
    Args:
        session_id: Current session identifier
        code_snippet: User's code to analyze
    
    Returns:
        Dictionary with:
            - debug_problem: High-level description of the bug
            - debug_next_step: Suggested action / next thing to try
            - reply_text: Full assistant message to send back
    """
    # Get current session state for context
    state = session_store.get(session_id)
    
    # Build structured prompt for senior engineer behavior
    prompt = f"""You are a senior engineer helping a learner debug code.
Be direct, kind, and practical.

Session context:
- Known recurring problem so far (if any): {state.debug_problem or "none"}
- Preferred language hint: {state.language_hint or "unknown"}

User-submitted code:
```
{code_snippet}
```

Tasks:
1. Explain the most important bug or misunderstanding in plain language.
2. Show exactly how to fix it (either corrected code block or minimal diff).
3. Name the main concept they need to learn next (e.g. 'async/await basics' or 'Python indentation/scope').

Your response should be 3 short sections:

**What's wrong:**
[One or two sentences explaining the bug]

**How to fix it:**
[Show corrected code or describe the fix]

**What to learn next:**
[Name the concept they should study]

Be concise and actionable. 3-5 sentences total max.
"""

    try:
        # Initialize Vertex AI if not already done
        vertexai.init(project=VERTEX_PROJECT_NUMBER, location=VERTEX_REGION)
        
        # Create model instance
        model = GenerativeModel(VERTEX_MODEL_ID)
        
        # Generate response
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Parse the response to extract structured fields
        debug_problem = None
        debug_next_step = None
        
        # Try to extract from structured sections
        lines = result_text.split('\n')
        current_section = None
        problem_lines = []
        fix_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            if "what's wrong" in line_lower or "what is wrong" in line_lower:
                current_section = "problem"
                continue
            elif "how to fix" in line_lower:
                current_section = "fix"
                continue
            elif "what to learn" in line_lower:
                current_section = "learn"
                continue
            
            if current_section == "problem" and line.strip() and not line.startswith('**'):
                problem_lines.append(line.strip())
            elif current_section == "fix" and line.strip() and not line.startswith('**') and not line.startswith('```'):
                fix_lines.append(line.strip())
        
        # Build summaries from extracted sections
        if problem_lines:
            debug_problem = ' '.join(problem_lines[:2])  # First 2 sentences
        if fix_lines:
            debug_next_step = ' '.join(fix_lines[:2])  # First 2 sentences
        
        # Fallback: if parsing failed, do heuristic extraction
        if not debug_problem or not debug_next_step:
            # Split by sentences
            sentences = []
            current = ""
            for char in result_text:
                current += char
                if char in '.!?' and len(current.strip()) > 15:
                    sentences.append(current.strip())
                    current = ""
            if current.strip():
                sentences.append(current.strip())
            
            # Use first sentence as problem, second as fix
            if len(sentences) >= 1 and not debug_problem:
                debug_problem = sentences[0]
            if len(sentences) >= 2 and not debug_next_step:
                debug_next_step = sentences[1]
            elif len(sentences) == 1 and not debug_next_step:
                debug_next_step = sentences[0]
        
        # Ensure we have some content
        if not debug_problem:
            debug_problem = "Analyzing code..."
        if not debug_next_step:
            debug_next_step = "Review the code carefully"
        
        # Try to infer language from code snippet
        language_hint = None
        code_lower = code_snippet.lower()
        if 'def ' in code_snippet or 'import ' in code_snippet or 'print(' in code_snippet:
            language_hint = "python"
        elif 'function ' in code_snippet or 'const ' in code_snippet or 'let ' in code_snippet or '=>' in code_snippet:
            language_hint = "javascript"
        elif 'public class' in code_snippet or 'void main' in code_snippet:
            language_hint = "java"
        
        return {
            "debug_problem": debug_problem,
            "debug_next_step": debug_next_step,
            "reply_text": result_text,
            "language_hint": language_hint
        }
        
    except Exception as e:
        # Graceful fallback if model call fails
        error_msg = f"I'm having trouble analyzing that code right now. Error: {str(e)}"
        return {
            "debug_problem": f"Analysis error: {str(e)[:50]}",
            "debug_next_step": "Try simplifying the code and submit again",
            "reply_text": error_msg,
            "language_hint": None
        }
