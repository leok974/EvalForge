import os
from sqlmodel import create_engine, Session, select
from arcade_app.models import QuestDefinition

# Set DATABASE_URL to localhost mapped port for local execution
os.environ["DATABASE_URL"] = "postgresql://evalforge:evalforge@localhost:5435/evalforge"

def check():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        q_select = session.exec(select(QuestDefinition).where(QuestDefinition.slug == "sql-select")).first()
        if q_select:
            print(f"--- sql-select ---")
            print(f"Starter Code: {q_select.starter_code[:50] if q_select.starter_code else 'None'}")
            print(f"Workspace JSON: {q_select.workspace_json}")
        
        q_where = session.exec(select(QuestDefinition).where(QuestDefinition.slug == "sql-where")).first()
        if q_where:
            print(f"\n--- sql-where ---")
            print(f"Starter Code: {q_where.starter_code[:50] if q_where.starter_code else 'None'}")
            print(f"Workspace JSON: {q_where.workspace_json}")

if __name__ == "__main__":
    check()
