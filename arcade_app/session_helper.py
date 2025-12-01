from datetime import datetime
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import ChatSession

async def get_or_create_session(user_id: str) -> dict:
    """
    Loads the most recent active session for the user, or creates a new one.
    """
    async for session in get_session():
        # 1. Try to find the latest session
        statement = select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc())
        result = await session.execute(statement)
        chat_session = result.scalars().first()
        
        # 2. Create if missing
        if not chat_session:
            chat_session = ChatSession(user_id=user_id)
            session.add(chat_session)
            await session.commit()
            await session.refresh(chat_session)
            
        return chat_session.model_dump()

async def update_session_state(session_id: str, context: dict):
    """
    Updates the 'Cursor Position' (World/Track/Mode) timestamp.
    """
    async for session in get_session():
        chat_session = await session.get(ChatSession, session_id)
        if chat_session:
            # Update fields if provided
            if "world_id" in context: chat_session.world_id = context["world_id"]
            if "track_id" in context: chat_session.track_id = context["track_id"]
            if "mode" in context: chat_session.mode = context["mode"]
            
            chat_session.updated_at = datetime.utcnow()
            session.add(chat_session)
            await session.commit()

async def append_message(session_id: str, role: str, content: str, meta: dict = None):
    """
    Appends a new message to the session history log.
    """
    async for session in get_session():
        chat_session = await session.get(ChatSession, session_id)
        if chat_session:
            new_msg = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
                **(meta or {})
            }
            
            # ⚠️ SQLModel requires re-assigning the JSON list to detect mutation
            # We clone the existing list, append, and re-assign
            current_history = list(chat_session.history) if chat_session.history else []
            current_history.append(new_msg)
            
            chat_session.history = current_history
            chat_session.updated_at = datetime.utcnow()
            
            session.add(chat_session)
            await session.commit()
