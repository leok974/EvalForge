import asyncio, json, sys
sys.path.insert(0, '.')
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def f():
    s = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()
    r = await s.execute(select(QuestDefinition).where(QuestDefinition.slug == 'first-sparks'))
    q = r.scalar_one_or_none()
    if q:
        print(json.dumps(q.objectives_json, indent=2))
    else:
        print('not found')

asyncio.run(f())
