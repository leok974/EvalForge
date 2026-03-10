import os
import json
from sqlmodel import create_engine, Session, select
from arcade_app.models import QuestDefinition

os.environ["DATABASE_URL"] = "postgresql://evalforge:evalforge@localhost:5435/evalforge"

def check():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        for slug in ["sql-select", "sql-where"]:
            q = session.exec(select(QuestDefinition).where(QuestDefinition.slug == slug)).first()
            if q:
                print(f"--- {slug} ---")
                wjson = q.workspace_json or {}
                files = wjson.get("files", [])
                print(f"Files in workspace_json:")
                for f in files:
                    print(f"  - {f.get('path')}")
            else:
                print(f"--- {slug} --- NOT FOUND")

if __name__ == "__main__":
    check()
