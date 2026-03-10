import os
from sqlmodel import create_engine, Session, select
from arcade_app.models import QuestDefinition

os.environ["DATABASE_URL"] = "postgresql://evalforge:evalforge@localhost:5435/evalforge"

def check():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        quests = session.exec(select(QuestDefinition).where(QuestDefinition.world_id == "world-sql")).all()
        # Sort by order_index to match UI expectations
        quests.sort(key=lambda x: (x.track_id, x.order_index))
        
        print(f"{'Slug':<40} | {'Track':<15} | {'Order':<5} | {'Description'}")
        print("-" * 100)
        for q in quests:
            desc = q.short_description or "MISSING"
            print(f"{q.slug:<40} | {q.track_id:<15} | {q.order_index:<5} | {desc}")

if __name__ == "__main__":
    check()
