from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from arcade_app.database import get_session
from arcade_app.auth_helper import get_current_user
from typing import List, Dict, Any

router = APIRouter(prefix="/api/db", tags=["database"])

@router.get("/introspect")
async def introspect_db(
    quest_id: str = Query(...),
    include_all: bool = Query(False),
    db: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    """
    Returns a tree structure of schemas, tables, and columns for the current quest context.
    Supports quest-scoped filtering by default.
    """
    # 1. Fetch quest to verify engine and get scoping metadata
    from arcade_app.models import QuestDefinition
    from sqlalchemy import select
    q_result = await db.execute(select(QuestDefinition).where(QuestDefinition.slug == quest_id))
    quest = q_result.scalar_one_or_none()
    
    if not quest or quest.db_engine != "postgres":
        return {"engine": "sqlite", "schemas": []}

    # 2. Extract scoping metadata
    mode = getattr(quest, "db_explorer_mode", "full")
    featured = set(getattr(quest, "featured_tables", []) or [])
    related = set(getattr(quest, "related_tables", []) or [])
    hidden = set(getattr(quest, "hidden_tables", []) or [])

    # Global platform tables to hide by default
    INTERNAL_TABLES = {
        "trackdefinition", "avatardefinition", "worlddefinition", "questdefinition",
        "enrollment", "questattempt", "user", "alembic_version", "queststate"
    }
    
    # 3. Query Postgres information_schema
    query = """
    SELECT 
        table_schema, 
        table_name, 
        column_name, 
        data_type 
    FROM information_schema.columns 
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY table_schema, table_name, ordinal_position;
    """
    
    try:
        result = await db.execute(text(query))
        rows = result.fetchall()
        
        # Build tree: schema -> table -> column
        tree = {}
        for s_name, t_name, c_name, c_type in rows:
            # Filtering Logic
            is_featured = t_name in featured
            is_related = t_name in related
            is_hidden = t_name in hidden
            
            # If in quest_scoped mode and not include_all:
            # - Show ONLY featured and related
            # - Hide hidden explicitly
            if mode == "quest_scoped" and not include_all:
                if not is_featured and not is_related:
                    continue
            
            # Always hide hidden tables or internal tables unless include_all is true
            if (is_hidden or t_name in INTERNAL_TABLES) and not include_all:
                continue

            if s_name not in tree: tree[s_name] = {"name": s_name, "tables": {}}
            if t_name not in tree[s_name]["tables"]: 
                tree[s_name]["tables"][t_name] = {
                    "name": t_name, 
                    "columns": [],
                    "relevance": "featured" if is_featured else ("related" if is_related else "other")
                }
            
            tree[s_name]["tables"][t_name]["columns"].append({
                "name": c_name,
                "type": c_type
            })
            
        # Convert to list for frontend
        schemas = []
        for s in tree.values():
            s["tables"] = list(s["tables"].values())
            # Sort tables by relevance: featured -> related -> other
            relevance_order = {"featured": 0, "related": 1, "other": 2}
            s["tables"].sort(key=lambda t: relevance_order.get(t.get("relevance", "other"), 99))
            schemas.append(s)
            
        return {
            "engine": "postgres",
            "schemas": schemas,
            "mode": mode,
            "has_hidden": len(rows) > sum(len(s["tables"]) for s in schemas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database introspection failed: {str(e)}")

@router.get("/preview")
async def preview_table(
    quest_id: str,
    table: str,
    schema: str = "public",
    limit: int = 50,
    db: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    """
    Returns the first N rows of a specific table.
    """
    # Safety: Validate table/schema names to prevent injection
    if not table.isidentifier() or not schema.isidentifier():
        raise HTTPException(status_code=400, detail="Invalid table or schema name")
        
    query = f"SELECT * FROM {schema}.{table} LIMIT :limit"
    try:
        result = await db.execute(text(query), {"limit": limit})
        columns = list(result.keys())
        rows = [list(row) for row in result.fetchall()]
        
        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Table preview failed: {str(e)}")
