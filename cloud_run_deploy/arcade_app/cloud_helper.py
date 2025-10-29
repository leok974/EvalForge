"""
Cloud/SRE mentor helper for analyzing deployment issues.
Uses Vertex AI to act as an SRE debugging assistant.
"""
import os
from typing import Dict, Any, List
import vertexai
from vertexai.generative_models import GenerativeModel

from .session_state import session_store

# Shared configuration - matches agent.py
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")


def analyze_cloud_issue(session_id: str, user_message: str) -> Dict[str, Any]:
    """
    Use the model to act like an SRE/debug mentor.
    
    Goal: Summarize the problem and propose a next actionable step.
    
    Args:
        session_id: Current session identifier
        user_message: User's message containing logs or error description
    
    Returns:
        Dictionary with:
            - issue_summary: Best guess of root cause
            - next_step: Recommended next action
            - reply_text: Full assistant message to send back
    """
    # Get current session state for context
    state = session_store.get(session_id)
    
    # Build structured prompt for SRE mentor behavior
    prompt = f"""You are an SRE mentor helping a junior engineer debug Cloud Run / Docker deployment issues.

Context (persisted this session):
- Known issue so far (if any): {state.issue_summary or "none yet"}
- Last recommended step (if any): {state.next_step or "none yet"}

New user message / logs:
{user_message}

Tasks:
1. Briefly identify the most likely root cause (one clear sentence).
2. Suggest the single next step they should take (one clear sentence).
3. Ask a focused follow-up question if more info is needed (optional, one sentence).

Respond in plain language, 2-4 sentences max. Be direct and actionable like a senior engineer would be.

Format your response as follows:
ROOT CAUSE: [one sentence identifying the issue]
NEXT STEP: [one sentence with the action to take]
[Optional: One follow-up question or additional context]
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
        issue_summary = None
        next_step = None
        
        lines = result_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('ROOT CAUSE:'):
                issue_summary = line.replace('ROOT CAUSE:', '').strip()
            elif line.startswith('NEXT STEP:'):
                next_step = line.replace('NEXT STEP:', '').strip()
        
        # Fallback: if parsing failed, do heuristic extraction
        if not issue_summary or not next_step:
            # Split by sentences
            sentences: List[str] = []
            current = ""
            for char in result_text:
                current += char
                if char in '.!?' and len(current.strip()) > 10:
                    sentences.append(current.strip())
                    current = ""
            if current.strip():
                sentences.append(current.strip())
            
            # Use first sentence as issue summary, second as next step
            if len(sentences) >= 1 and not issue_summary:
                issue_summary = sentences[0]
            if len(sentences) >= 2 and not next_step:
                next_step = sentences[1]
            elif len(sentences) == 1 and not next_step:
                # Only one sentence - use it for both
                next_step = sentences[0]
        
        # Ensure we have some content
        if not issue_summary:
            issue_summary = "Analyzing deployment issue..."
        if not next_step:
            next_step = "Review error logs for more details"
        
        return {
            "issue_summary": issue_summary,
            "next_step": next_step,
            "reply_text": result_text
        }
        
    except Exception as e:
        # Graceful fallback if model call fails
        error_msg = f"I'm having trouble analyzing that right now. Error: {str(e)}"
        return {
            "issue_summary": f"Analysis error: {str(e)[:50]}",
            "next_step": "Check logs and try again",
            "reply_text": error_msg
        }
