import sqlite3
from pathlib import Path

def main():
    conn = sqlite3.connect(":memory:")
    
    # In runner, fixtures are at ./fixtures (relative to CWD/script)
    # as we moved them to workspace/fixtures
    fixtures_dir = Path("fixtures") 
    
    if (fixtures_dir / "schema.sql").exists():
        with open(fixtures_dir / "schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            
    if (fixtures_dir / "seed.sql").exists():
        with open(fixtures_dir / "seed.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            
    # Solution Query
    # Goal: Return only `name` and `city` from `users`. Order By `name` ascending.
    query = "SELECT name, city FROM users ORDER BY name ASC;"
    
    try:
        cursor = conn.execute(query)
        for row in cursor:
            print(row)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
