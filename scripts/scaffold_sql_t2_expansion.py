import os
import shutil
import json
from pathlib import Path
import textwrap

# --- Configuration ---
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = REPO_ROOT / "data" / "quests"

# Shared Schemas and Seeds for Tier 2 Expansions
SCHEMA_SQL = """DROP TABLE IF EXISTS user_logins;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  manager_id INTEGER,
  salary INTEGER,
  bonus INTEGER,
  hire_date TEXT,
  FOREIGN KEY (manager_id) REFERENCES employees(id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  event_type TEXT NOT NULL,
  event_date TEXT NOT NULL
);

CREATE TABLE user_logins (
  user_id INTEGER PRIMARY KEY,
  login_count INTEGER NOT NULL,
  last_login TEXT NOT NULL
);
"""

SEED_SQL = """INSERT INTO employees (id, name, manager_id, salary, bonus, hire_date) VALUES
(1, 'Alice (CEO)', NULL, 200000, 50000, '2020-01-01'),
(2, 'Bob (VP)', 1, 150000, NULL, '2020-06-15'),
(3, 'Charlie (Manager)', 2, 100000, 10000, '2021-03-20'),
(4, 'Diana (IC)', 3, 80000, NULL, '2022-08-10'),
(5, 'Evan (IC)', 3, 75000, 5000, '2023-01-05');

INSERT INTO events (id, event_type, event_date) VALUES
(1, 'click', '2023-10-01 10:00:00'),
(2, 'view', '2023-10-01 12:30:00'),
(3, 'click', '2023-10-02 09:15:00'),
(4, 'purchase', '2023-10-02 14:00:00'),
(5, 'view', '2023-10-03 16:45:00'),
(6, 'click', '2023-10-03 16:50:00');

INSERT INTO user_logins (user_id, login_count, last_login) VALUES
(1, 10, '2023-09-01'),
(2, 5, '2023-09-15');
"""

QUESTS = [
    {
        "slug": "sql-t2-subqueries-exists",
        "title": "Correlated Subqueries & EXISTS",
        "description": "Use EXISTS to find employees who manage other employees.",
        "readme": "# Mission: Correlated Subqueries & EXISTS\n**Goal**: Find all employees who manage at least one other employee.\nReturn `id, name`. Use `EXISTS`.\n**Order**: By `id` ASC.",
        "solution": "SELECT id, name FROM employees e1 WHERE EXISTS (SELECT 1 FROM employees e2 WHERE e2.manager_id = e1.id) ORDER BY id ASC;",
        "test_code": """def test_sql_subqueries_exists(run_sql):
    rows = run_sql()
    # 1 (Alice) manages 2
    # 2 (Bob) manages 3
    # 3 (Charlie) manages 4, 5
    assert len(rows) == 3
    assert rows[0] == (1, 'Alice (CEO)')
    assert rows[1] == (2, 'Bob (VP)')
    assert rows[2] == (3, 'Charlie (Manager)')
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses EXISTS", "kind": "source_regex", "rule_json": {"pattern": "(?i)EXISTS"}}
        ],
        "key_terms": ["glossary/sql/subquery", "glossary/sql/exists", "glossary/sql/correlated-subquery"],
        "tier": 2
    },
    {
        "slug": "sql-t2-cte-basics",
        "title": "CTE Basics",
        "description": "Use a Common Table Expression to simplify a query.",
        "readme": "# Mission: CTE Basics\n**Goal**: Use a `WITH` clause to create an `EventCounts` CTE that counts events per `event_type`.\nThen query the CTE to return `event_type, num_events` where `num_events > 1`.\n**Order**: By `event_type` ASC.",
        "solution": "WITH EventCounts AS (SELECT event_type, COUNT(*) as num_events FROM events GROUP BY event_type) SELECT event_type, num_events FROM EventCounts WHERE num_events > 1 ORDER BY event_type ASC;",
        "test_code": """def test_sql_cte_basics(run_sql):
    rows = run_sql()
    # click: 3, view: 2, purchase: 1
    # > 1: click (3), view (2)
    assert len(rows) == 2
    assert rows[0] == ('click', 3)
    assert rows[1] == ('view', 2)
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses WITH", "kind": "source_regex", "rule_json": {"pattern": "(?i)WITH "}}
        ],
        "key_terms": ["glossary/sql/cte-with", "glossary/sql/alias", "glossary/sql/query-planning"],
        "tier": 2
    },
    {
        "slug": "sql-t2-recursive-cte-hierarchy",
        "title": "Recursive CTEs (Hierarchy)",
        "description": "Use WITH RECURSIVE to traverse an organizational hierarchy.",
        "readme": "# Mission: Recursive CTEs (Hierarchy)\n**Goal**: Use `WITH RECURSIVE` to find all employees and their distance from the CEO (Alice, id 1).\nReturn `id, name, distance`.\n- Alice has distance 0.\n- Her direct reports have distance 1, and so on.\n**Order**: By `distance` ASC, then `id` ASC.",
        "solution": "WITH RECURSIVE OrgChart AS ( SELECT id, name, manager_id, 0 as distance FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, o.distance + 1 FROM employees e JOIN OrgChart o ON e.manager_id = o.id ) SELECT id, name, distance FROM OrgChart ORDER BY distance ASC, id ASC;",
        "test_code": """def test_sql_recursive_cte(run_sql):
    rows = run_sql()
    assert len(rows) == 5
    assert rows[0] == (1, 'Alice (CEO)', 0) # Alice
    assert rows[1] == (2, 'Bob (VP)', 1)    # Bob
    assert rows[2] == (3, 'Charlie (Manager)', 2) # Charlie
    assert rows[3] == (4, 'Diana (IC)', 3)  # Diana
    assert rows[4] == (5, 'Evan (IC)', 3)   # Evan
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses RECURSIVE", "kind": "source_regex", "rule_json": {"pattern": "(?i)RECURSIVE"}}
        ],
        "key_terms": ["glossary/sql/cte-recursive", "glossary/sql/hierarchy", "glossary/sql/termination-condition"],
        "tier": 2
    },
    {
        "slug": "sql-t2-nulls-coalesce",
        "title": "NULL Semantics & COALESCE",
        "description": "Use COALESCE to handle NULL values cleanly.",
        "readme": "# Mission: NULLs & COALESCE\n**Goal**: Return `id, name, total_comp`, where `total_comp = salary + COALESCE(bonus, 0)`.\n**Order**: By `total_comp` DESC, then `id` ASC.",
        "solution": "SELECT id, name, salary + COALESCE(bonus, 0) AS total_comp FROM employees ORDER BY total_comp DESC, id ASC;",
        "test_code": """def test_sql_nulls_coalesce(run_sql):
    rows = run_sql()
    assert len(rows) == 5
    assert rows[0] == (1, 'Alice (CEO)', 250000)
    assert rows[1] == (2, 'Bob (VP)', 150000)
    assert rows[2] == (3, 'Charlie (Manager)', 110000)
    assert rows[3] == (4, 'Diana (IC)', 80000)
    assert rows[4] == (5, 'Evan (IC)', 80000)
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses COALESCE", "kind": "source_regex", "rule_json": {"pattern": "(?i)COALESCE"}}
        ],
        "key_terms": ["glossary/sql/null", "glossary/sql/coalesce", "glossary/sql/case-when"],
        "tier": 2
    },
    {
        "slug": "sql-t2-dates-grouping",
        "title": "Date Bucketing & Grouping",
        "description": "Use date functions to bucket rows.",
        "readme": "# Mission: Date Bucketing\n**Goal**: Use `strftime('%Y-%m-%d', event_date)` to extract the date portion of the event.\nCount the number of events per date.\nReturn `event_date_only, num_events`.\n**Order**: By `event_date_only` ASC.",
        "solution": "SELECT strftime('%Y-%m-%d', event_date) AS event_date_only, COUNT(*) AS num_events FROM events GROUP BY event_date_only ORDER BY event_date_only ASC;",
        "test_code": """def test_sql_dates_grouping(run_sql):
    rows = run_sql()
    assert len(rows) == 3
    assert rows[0] == ('2023-10-01', 2)
    assert rows[1] == ('2023-10-02', 2)
    assert rows[2] == ('2023-10-03', 2)
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses strftime", "kind": "source_regex", "rule_json": {"pattern": "(?i)strftime"}}
        ],
        "key_terms": ["glossary/sql/date-functions", "glossary/sql/group-by", "glossary/sql/order-by"],
        "tier": 2
    },
    {
        "slug": "sql-t2-upsert-on-conflict",
        "title": "UPSERT & ON CONFLICT",
        "description": "Use ON CONFLICT DO UPDATE to perform UPSERTs in SQLite.",
        "readme": "# Mission: UPSERT (ON CONFLICT)\n**Goal**: \nInsert into `user_logins (user_id, login_count, last_login)` values `(1, 1, '2023-10-10')`.\nIf there is a conflict on `user_id` (PRIMARY KEY), update the existing row:\n- Add 1 to `login_count` (`login_count = login_count + 1`)\n- Update `last_login` to `excluded.last_login`\nReturn all rows from `user_logins` ordered by `user_id` ASC.",
        "solution": "INSERT INTO user_logins (user_id, login_count, last_login) VALUES (1, 1, '2023-10-10') ON CONFLICT(user_id) DO UPDATE SET login_count = user_logins.login_count + 1, last_login = excluded.last_login; SELECT * FROM user_logins ORDER BY user_id ASC;",
        "test_code": """def test_sql_upsert_on_conflict(run_sql):
    rows = run_sql()
    assert len(rows) == 2
    # User 1 originally had 10 logins, now should have 11 and new date.
    assert rows[0] == (1, 11, '2023-10-10')
    assert rows[1] == (2, 5, '2023-09-15')
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses ON CONFLICT DO UPDATE", "kind": "source_regex", "rule_json": {"pattern": "(?i)ON CONFLICT.*DO UPDATE"}}
        ],
        "key_terms": ["glossary/sql/upsert", "glossary/sql/unique-constraint", "glossary/sql/on-conflict"],
        "tier": 2
    },
    {
        "slug": "sql-t2-indexes-explain",
        "title": "Indexes & EXPLAIN",
        "description": "Create an index and use EXPLAIN QUERY PLAN.",
        "readme": "# Mission: Indexes & EXPLAIN\n**Goal**:\n1. Open `task.sql`.\n2. Add a `CREATE INDEX idx_emp_mgr ON employees(manager_id);` statement.\n3. Add an `EXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;` statement at the very end.\nThe test runner executes the final SQL statement and returns the `id, parent, notused, detail` output in SQLite.",
        "solution": "CREATE INDEX idx_emp_mgr ON employees(manager_id);\nEXPLAIN QUERY PLAN SELECT * FROM employees WHERE manager_id = 1;",
        "test_code": """def test_sql_indexes_explain(run_sql):
    rows = run_sql()
    # In SQLite 3.x, EXPLAIN QUERY PLAN returns rows with columns (id, parent, notused, detail).
    # We want to check that the 'detail' column mentions the index 'idx_emp_mgr'.
    found_index = False
    for r in rows:
        detail = str(r[-1]).upper()
        if "IDX_EMP_MGR" in detail and ("SEARCH" in detail or "INDEX" in detail):
            found_index = True
            break
    assert found_index, f"Query plan did not use idx_emp_mgr! Rows: {rows}"
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query Plan shows Index usage", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses CREATE INDEX and EXPLAIN", "kind": "source_regex", "rule_json": {"patterns": ["(?i)CREATE INDEX", "(?i)EXPLAIN QUERY PLAN"]}}
        ],
        "key_terms": ["glossary/sql/index", "glossary/sql/explain-query-plan", "glossary/sql/performance"],
        "tier": 2
    },
    {
        "slug": "sql-t2-transactions-rollback",
        "title": "Transactions & Rollback",
        "description": "Demonstrate atomicity using BEGIN and ROLLBACK.",
        "readme": "# Mission: Transactions & Rollback\n**Goal**:\n1. Issue a `BEGIN;` or `BEGIN TRANSACTION;`.\n2. Write an `INSERT` statement adding a new department or employee (e.g., `INSERT INTO employees (id, name) VALUES (99, 'Test');`).\n3. Issue a `ROLLBACK;` statement to cancel the transaction.\n4. Write a final query: `SELECT COUNT(*) FROM employees WHERE id = 99;` to verify the rollback worked.",
        "solution": "BEGIN; INSERT INTO employees (id, name) VALUES (99, 'Test'); ROLLBACK; SELECT COUNT(*) FROM employees WHERE id = 99;",
        "test_code": """def test_sql_transactions_rollback(run_sql):
    rows = run_sql()
    assert len(rows) == 1
    # Count should be 0 since it was rolled back.
    assert rows[0] == (0,)
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex", "title": "Query uses ROLLBACK", "kind": "source_regex", "rule_json": {"patterns": ["(?i)BEGIN", "(?i)ROLLBACK"]}}
        ],
        "key_terms": ["glossary/sql/transaction", "glossary/sql/rollback", "glossary/sql/atomicity"],
        "tier": 2
    },
    {
        "slug": "sql-t2-boss-data-quality-audit",
        "title": "BOSS: Data Quality Audit",
        "description": "Combine subqueries, CTEs, and JOINs to audit data.",
        "readme": "# Mission: BOSS Data Quality Audit\n**Goal**:\nFind all `manager_id`s in `employees` that do NOT have a corresponding valid `id` in the `employees` table (Orphaned Managers).\nReturn `id, name, manager_id` of the employees with the invalid manager_id.\n\n*Wait, our DB is small and clean. Let's insert a dirty row first inside your query!* \n**Task**:\n1. `INSERT INTO employees (id, name, manager_id) VALUES (99, 'Ghost Employee', 999);`\n2. Write a single query (using a CTE or Anti-Join `NOT EXISTS` / `LEFT JOIN ... IS NULL`) to find the employee(s) who reference a missing manager.\n3. Return `id, name, manager_id`. \n**Order**: By `id` ASC.",
        "solution": "INSERT INTO employees (id, name, manager_id) VALUES (99, 'Ghost Employee', 999);\nSELECT e.id, e.name, e.manager_id FROM employees e LEFT JOIN employees m ON e.manager_id = m.id WHERE e.manager_id IS NOT NULL AND m.id IS NULL ORDER BY e.id ASC;",
        "test_code": """def test_sql_boss_data_quality(run_sql):
    rows = run_sql()
    assert len(rows) == 1
    assert rows[0] == (99, 'Ghost Employee', 999)
""",
        "objectives": [
            {"id": "tests_pass", "title": "Query returns correct result", "kind": "quest_pass_fail"},
            {"id": "source_regex_join", "title": "Uses JOIN or EXISTS/IN", "kind": "source_regex", "rule_json": {"pattern": "(?i)JOIN|EXISTS|IN"}},
            {"id": "not_timed_out", "title": "Completed within time limit", "kind": "process_not_timed_out"}
        ],
        "key_terms": ["glossary/sql/constraint", "glossary/sql/anti-join", "glossary/sql/data-quality"],
        "tier": 2
    }
]

def scaffold_quest(quest):
    slug = quest["slug"]
    print(f"Scaffolding {slug}...")
    
    quest_dir = DATA_QUESTS / slug
    
    # 1. Clean existing grading to remove legacy files
    grading_dir = quest_dir / "grading"
    if grading_dir.exists():
        shutil.rmtree(grading_dir)
        
    # 2. Directories
    (quest_dir / "workspace").mkdir(parents=True, exist_ok=True)
    (quest_dir / "fixtures").mkdir(parents=True, exist_ok=True)
    (quest_dir / "grading" / "public").mkdir(parents=True, exist_ok=True)
    (quest_dir / "grading" / "solutions").mkdir(parents=True, exist_ok=True)
    
    # 3. Fixtures (shared)
    (quest_dir / "fixtures" / "schema.sql").write_text(SCHEMA_SQL, encoding="utf-8")
    (quest_dir / "fixtures" / "seed.sql").write_text(SEED_SQL, encoding="utf-8")
    
    # 4. Workspace
    (quest_dir / "workspace" / "README.md").write_text(quest["readme"], encoding="utf-8")
    (quest_dir / "workspace" / "task.sql").write_text("-- TODO: Write your query here\n", encoding="utf-8")
    
    # 5. Solutions
    (quest_dir / "grading" / "solutions" / "task.sql").write_text(quest["solution"], encoding="utf-8")
    
    # 6. Public Tests
    test_content = f"""
import pytest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql, assert_rows_match

QUEST_DIR = Path(__file__).resolve().parents[2]
# Using task.sql in workspace (swapped in solution mode)
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
SCHEMA_SQL = QUEST_DIR / "fixtures" / "schema.sql"
SEED_SQL = QUEST_DIR / "fixtures" / "seed.sql"

@pytest.fixture
def run_sql():
    return lambda: base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)

{quest["test_code"]}
"""
    safe_slug = slug.replace("-", "_")
    (quest_dir / "grading" / "public" / f"test_{safe_slug}.py").write_text(test_content, encoding="utf-8")
    
def update_questpack():
    pack_path = REPO_ROOT / "data" / "questpacks" / "_tier2" / "sql_tier2.json"
    
    if pack_path.exists():
        with open(pack_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"quests": []}
        
    existing_slugs = {q["slug"] for q in data.get("quests", [])}
    
    for q in QUESTS:
        if q["slug"] in existing_slugs:
            continue
            
        quest_def = {
            "slug": q["slug"],
            "title": q["title"],
            "tier": q.get("tier", 2),
            "world_id": "world-sql",
            "track_id": "core-sql",
            "language": "sql",
            "description": q["description"],
            "objectives": q["objectives"],
            "key_terms": q["key_terms"],
            "workspace": {"files": {}},
            "grading_json": {}
        }
        data["quests"].append(quest_def)
        
    with open(pack_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print(f"Updated {pack_path.relative_to(REPO_ROOT)} with new quests.")

def main():
    for q in QUESTS:
        scaffold_quest(q)
    print("Scaffolded 9 SQL Tier 2 Expansion Quests on disk.")
    update_questpack()

if __name__ == "__main__":
    main()
