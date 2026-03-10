import os
from sqlmodel import create_engine, Session, select
from arcade_app.models import QuestDefinition

os.environ["DATABASE_URL"] = "postgresql://evalforge:evalforge@localhost:5435/evalforge"

def check():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        q_where = session.exec(select(QuestDefinition).where(QuestDefinition.slug == "sql-where")).first()
        if q_where:
            print(f"--- sql-where ---")
            print(f"Language: {q_where.language}")

if __name__ == "__main__":
    check()
