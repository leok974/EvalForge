
from fastapi import APIRouter, HTTPException, Depends
import logging

from arcade_app.schemas.coach_schemas import CoachRequest, CoachResponse
from arcade_app.services.coach_service import coach_service

router = APIRouter(prefix="/api", tags=["coach"])

logger = logging.getLogger(__name__)

@router.post("/coach", response_model=CoachResponse)
async def invoke_coach(req: CoachRequest):
    """
    EvalForge Coach: Explain + Debug (Gemini Powered)
    
    Modes:
    - explain: Conceptual teaching (no diffs)
    - debug: Root cause analysis + fix plan (diffs allowed only if student_mode=False)
    - auto: Routes based on failure signals
    """
    logger.info(f"Coach API invoked: mode={req.mode}, quest={req.quest_slug}")
    
    try:
        response = await coach_service.process_request(req)
        return response
    except Exception as e:
        logger.error(f"Coach API Error: {e}")
        # Return a fallback response instead of 500ing to keep UI resilient
        return coach_service._mock_fallback(req, f"Internal Error: {str(e)}")
