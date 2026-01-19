import os
from sqlmodel import create_engine, text

# Use the same database URL as the app (dev default)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://evalforge:evalforge@127.0.0.1:5435/evalforge")

def migrate_debrief_column():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Checking for debrief_json column in quest_attempts...")
        
        # Check if column exists
        check_sql = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='quest_attempts' AND column_name='debrief_json';
        """)
        result = conn.execute(check_sql).fetchone()
        
        if result:
            print("[OK] Column debrief_json already exists.")
        else:
            print("[INFO] Column missing. Adding debrief_json...")
            try:
                # Add the column
                # JSONB is best for postgres, but SQLModel defaults to JSON type usually mapped to JSONB in PG
                alter_sql = text("ALTER TABLE quest_attempts ADD COLUMN debrief_json JSONB DEFAULT '{}'::jsonb;")
                conn.execute(alter_sql)
                conn.commit()
                print("[SUCCESS] Added debrief_json column.")
            except Exception as e:
                print(f"[ERROR] Failed to add column: {e}")
                conn.rollback()

if __name__ == "__main__":
    migrate_debrief_column()
