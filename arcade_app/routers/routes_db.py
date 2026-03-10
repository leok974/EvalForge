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
    db: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    """
    Returns a tree structure of schemas, tables, and columns for the current quest context.
    For Tier 3 Postgres quests, this queries the information_schema.
    """
    # 1. Fetch quest to verify engine
    from arcade_app.models import QuestDefinition
    from sqlalchemy import select
    q_result = await db.execute(select(QuestDefinition).where(QuestDefinition.slug == quest_id))
    quest = q_result.scalar_one_or_none()
    
    if not quest or quest.db_engine != "postgres":
        # Fallback for SQLite or missing quest
        return {"engine": "sqlite", "schemas": []}

    # 2. Query Postgres information_schema
    # Note: In EvalForge, we use an isolated schema per run, but the 'explorer' 
    # might want to see the 'public' or 'shared' schema if the runner hasn't created a temp one yet.
    # For this slice, we'll introspect the public schema or a quest-specific fixed schema if defined.
    
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
            if s_name not in tree: tree[s_name] = {"name": s_name, "tables": {}}
            if t_name not in tree[s_name]["tables"]: 
                tree[s_name]["tables"][t_name] = {"name": t_name, "columns": []}
            
            tree[s_name]["tables"][t_name]["columns"].append({
                "name": c_name,
                "type": c_type
            })
            
        # Convert to list for frontend
        schemas = []
        for s in tree.values():
            s["tables"] = list(s["tables"].values())
            schemas.append(s)
            
        return {
            "engine": "postgres",
            "schemas": schemas
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
