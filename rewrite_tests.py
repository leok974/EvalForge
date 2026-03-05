import os
import re
from pathlib import Path

quests_dir = Path("data/quests")
sql_t2_dirs = [d for d in quests_dir.iterdir() if d.is_dir() and d.name.startswith("sql-t2-")]

for qdir in sql_t2_dirs:
    public_dir = qdir / "grading" / "public"
    if not public_dir.exists():
        continue
    
    for test_file in public_dir.glob("test*.py"):
        old_content = test_file.read_text(encoding="utf-8")
        
        replacement = """BASE_DIR = Path(__file__).resolve().parent
if (BASE_DIR / "fixtures").exists():
    SCHEMA_SQL = BASE_DIR / "fixtures" / "schema.sql"
    SEED_SQL = BASE_DIR / "fixtures" / "seed.sql"
    TASK_SQL = BASE_DIR / "task.sql"
else:
    QUEST_DIR = BASE_DIR.parents[2]
    TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
    SCHEMA_SQL = QUEST_DIR / "fixtures" / "schema.sql"
    SEED_SQL = QUEST_DIR / "fixtures" / "seed.sql" """
        
        new_content = re.sub(
            r'QUEST_DIR = Path\(__file__\)\.resolve\(\)\.parents\[2\]\nTASK_SQL = QUEST_DIR / "workspace" / "task\.sql"\nSCHEMA_SQL = QUEST_DIR / "fixtures" / "schema\.sql"\nSEED_SQL = QUEST_DIR / "fixtures" / "seed\.sql"\n*',
            replacement + "\n",
            old_content
        )
        
        if new_content != old_content:
            test_file.write_text(new_content, encoding="utf-8")
            print(f"Fixed paths in {test_file}")

