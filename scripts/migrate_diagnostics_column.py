from sqlalchemy import create_engine, text
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://evalforge:evalforge@127.0.0.1:5435/evalforge")
engine = create_engine(DATABASE_URL)

def run_migration():
    """
    Adds diagnostics_json to quest_attempts
    """
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='quest_attempts' AND column_name='diagnostics_json'"))
            if result.fetchone():
                print("Column 'diagnostics_json' already exists. Skipping.")
                return

            print("Adding 'diagnostics_json' to quest_attempts...")
            conn.execute(text("ALTER TABLE quest_attempts ADD COLUMN diagnostics_json JSONB DEFAULT '[]'"))
            conn.commit()
            print("Migration successful.")
        except Exception as e:
            print(f"Migration failed: {e}")
            conn.rollback()

if __name__ == "__main__":
    run_migration()
