import os
from sqlmodel import create_engine, Session, select
from arcade_app.models import QuestProgress, QuestDefinition
from arcade_app.progress_models import QuestAttempt

os.environ["DATABASE_URL"] = "postgresql://evalforge:evalforge@localhost:5435/evalforge"

def reset():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        # Get quest ID
        q = session.exec(select(QuestDefinition).where(QuestDefinition.slug == "sql-where")).first()
        if not q:
            print("Quest sql-where not found in DB.")
            return
            
        quest_id = q.id
        print(f"Found sql-where ID: {quest_id}")

        # Check attempts
        stmt = select(QuestAttempt).where(QuestAttempt.quest_id == str(quest_id))
        attempts = session.exec(stmt).all()
        for a in attempts:
            print(f"Deleting Attempt ID: {a.id}")
            session.delete(a)
            
        # Check progress
        stmt = select(QuestProgress).where(QuestProgress.quest_id == quest_id)
        progresses = session.exec(stmt).all()
        for p in progresses:
            print(f"Deleting Progress ID: {p.id}")
            session.delete(p)
            
        session.commit()
        print("Reset sql-where for all users.")

if __name__ == "__main__":
    reset()
