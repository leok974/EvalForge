"""Diagnose blank quest content: checks DB field lengths and API response model."""
import asyncio, json, sys
sys.path.insert(0, '.')
from arcade_app.database import engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

SQL = """
SELECT slug,
       length(coalesce(briefing_md,''))      AS briefing_len,
       length(coalesce(starter_code,''))     AS starter_len,
       length(coalesce(lore_md,''))          AS lore_len,
       length(coalesce(tutorial_md,''))      AS tutorial_len,
       coalesce(jsonb_array_length(objectives_json::jsonb), 0)   AS obj_count,
       coalesce(jsonb_array_length((workspace_json::jsonb)->'files'), 0) AS ws_files
FROM questdefinition
WHERE slug LIKE '%sql-t2%' OR slug IN ('first-sparks','hello-variable','sql-ignition','sql-select')
ORDER BY slug
"""

async def main():
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as s:
        result = await s.execute(text(SQL))
        rows = result.mappings().all()
        for row in rows:
            print(json.dumps(dict(row)))

asyncio.run(main())
