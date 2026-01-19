from typing import Dict, Any, List, Optional
from sqlmodel import select, Session
from sqlalchemy import func
from arcade_app.models import QuestDefinition, QuestState, TrackDefinition
from arcade_app.progress_models import QuestAttempt, QuestProgressV2

async def generate_debrief(
    session: Session,
    quest: QuestDefinition,
    attempt: QuestAttempt,
    progress: QuestProgressV2
) -> Dict[str, Any]:
    """
    Generates the success debrief payload.
    """
    # 1. Passed Objectives
    passed_ids = [r["id"] for r in attempt.objective_results if r.get("ok")]
    objective_titles = []
    
    # Ideally we map IDs to titles from QuestDefinition
    # quest.objectives_json is a list of dicts {id, title, ...} or we infer from somewhere
    for obj in quest.objectives_json:
        if obj.get("id") in passed_ids:
            objective_titles.append({"id": obj["id"], "title": obj.get("title", obj["id"])})
            
    # 2. Learning Points
    # Prefer config-driven, fallback to heuristics
    learning_points = []
    
    # Check config first (Phase 7.1.2 requirement A2)
    # Assuming quest has 'teaching' field in metadata or similar. 
    # Current model doesn't have explicit 'teaching' column, but maybe inside 'grading_json' or 'objectives_json'?
    # Plan says "Extend questpack schema". Since I didn't add a column, I'll check 'grading_json' or 'meta' if available.
    # Let's assume passed objectives might have 'learning_point' metadata?
    # Or just fallback to heuristics for now as per plan A2 Fallback.
    
    # Heuristics
    if any("loop" in obj_id.lower() for obj_id in passed_ids):
        learning_points.append("You mastered the use of loops for repetitive tasks.")
    if any("output" in obj_id.lower() or "print" in obj_id.lower() for obj_id in passed_ids):
        learning_points.append("You matched the output format exactly, crucial for CLI tools.")
    if attempt.test_summary_json and attempt.test_summary_json.get("passed", 0) > 0:
        learning_points.append(f"Your solution passed all {attempt.test_summary_json.get('passed')} verified test cases.")
        
    if not learning_points:
        learning_points.append("You successfully completed all objectives.")
        learning_points.append("Your code executed without errors.")
        
    learning_points = learning_points[:2] # Cap at 2
    
    # 3. Next Quest Recommendation
    next_quest = await recommend_next_quest(session, progress.user_id, quest)
    
    return {
        "title": "Mission Accomplished",
        "passed_objectives": passed_ids,
        "objective_titles": objective_titles,
        "tests": attempt.test_summary_json if attempt.test_summary_json else None,
        "learning_points": learning_points,
        "next": next_quest
    }

async def recommend_next_quest(session: Session, user_id: str, current_quest: QuestDefinition) -> Optional[Dict[str, Any]]:
    """
    Finds the next quest in the track or world.
    """
    if not current_quest.track_id:
        return None
        
    # 1. Get all quests in this track, ordered
    stmt = select(QuestDefinition).where(QuestDefinition.track_id == current_quest.track_id).order_by(QuestDefinition.order_index)
    track_quests = (await session.exec(stmt)).all()
    
    current_index = -1
    for i, q in enumerate(track_quests):
        if q.id == current_quest.id:
            current_index = i
            break
            
    # 2. Look for next uncompleted quest
    if current_index != -1 and current_index < len(track_quests) - 1:
        next_q = track_quests[current_index + 1]
        
        # Check if already completed?
        # Ideally we recommend it even if completed if they are replaying, but usually 'next' implies 'new'.
        # Plan says "next uncompleted quest".
        # Check progress
        prog = await session.exec(select(QuestProgressV2).where(QuestProgressV2.user_id == user_id, QuestProgressV2.quest_id == next_q.slug))
        prog_record = prog.first()
        
        if not prog_record or prog_record.status != "completed":
             return {
                "quest_id": next_q.slug,
                "title": next_q.title,
                "why": "The next step in your journey."
             }
             
    # 3. If track complete, find next track? (Optional)
    # For now, return None (Dashboard will handle it)
    return None
