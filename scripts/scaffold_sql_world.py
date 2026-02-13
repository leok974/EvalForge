
import os
import shutil
from pathlib import Path
import textwrap

# --- Configuration ---
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = REPO_ROOT / "data" / "quests"

# Shared Schemas and Seeds
SCHEMA_SQL = """DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS order_items;

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  age INTEGER NOT NULL,
  city TEXT NOT NULL,
  is_active INTEGER NOT NULL CHECK (is_active IN (0,1))
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  total_cents INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price_cents INTEGER NOT NULL,
  is_discontinued INTEGER NOT NULL CHECK (is_discontinued IN (0,1))
);

CREATE TABLE order_items (
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty INTEGER NOT NULL,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
"""

SEED_SQL = """INSERT INTO users (id, name, email, age, city, is_active) VALUES
  (1, 'Alice',   'alice@example.com',   28, 'Detroit', 1),
  (2, 'Bob',     'bob@example.com',     35, 'Austin',  1),
  (3, 'Charlie', 'charlie@example.com', 22, 'Detroit', 0),
  (4, 'Diana',   'diana@example.com',   41, 'Seattle', 1),
  (5, 'Evan',    'evan@example.com',    29, 'Austin',  0),
  (6, 'Fay',     'fay@example.com',     33, 'Miami',   1);

INSERT INTO products (id, name, category, price_cents, is_discontinued) VALUES
  (1, 'Laptop',      'electronics', 99900, 0),
  (2, 'Mouse',       'electronics',  2500, 0),
  (3, 'Coffee',      'grocery',       1200, 0),
  (4, 'Headphones',  'electronics',  7500, 1),
  (5, 'Notebook',    'office',         500, 0);

INSERT INTO orders (id, user_id, status, created_at, total_cents) VALUES
  (1, 1, 'paid',      '2025-01-02', 102400),
  (2, 1, 'shipped',   '2025-01-05',   3700),
  (3, 2, 'paid',      '2025-02-10',   9900),
  (4, 3, 'cancelled', '2025-02-11',      0),
  (5, 4, 'paid',      '2025-03-15',   1700),
  (6, 5, 'pending',   '2025-03-20',   7500);

INSERT INTO order_items (order_id, product_id, qty) VALUES
  (1, 1, 1),
  (1, 2, 1),
  (2, 2, 1),
  (2, 3, 1),
  (3, 4, 1),
  (3, 2, 1),
  (5, 5, 2),
  (5, 3, 1),
  (6, 4, 1);
"""

# --- Quest Definitions ---

QUESTS = [
    {
        "slug": "sql-ignition",
        "title": "Your First SELECT",
        "readme": """# Mission: SQL Ignition
**Goal:** Return all users (all columns).
**Order:** By `id` ascending.
""",
        "solution": """SELECT id, name, email, age, city, is_active FROM users ORDER BY id ASC;""",
        "test_code": """
def test_sql_ignition(run_sql):
    rows = run_sql()
    assert len(rows) == 6
    # Check first row
    assert rows[0] == (1, 'Alice', 'alice@example.com', 28, 'Detroit', 1)
    # Check columns count
    assert len(rows[0]) == 6
"""
    },
    {
        "slug": "sql-select",
        "title": "Select Specific Columns",
        "readme": """# Mission: Select Specific Columns
**Goal:** Return only `name` and `city` from `users`.
**Order:** By `name` ascending.
""",
        "solution": """SELECT name, city FROM users ORDER BY name ASC;""",
        "test_code": """
def test_sql_select(run_sql):
    rows = run_sql()
    assert len(rows) == 6
    assert len(rows[0]) == 2
    # Check ordering by name
    assert rows[0] == ('Alice', 'Detroit')
    assert rows[1] == ('Bob', 'Austin')
"""
    },
    {
        "slug": "sql-where",
        "title": "Filter Rows",
        "readme": """# Mission: Filter Rows
**Goal:** Active users in Detroit, age >= 25.
Return `id, name, age`.
**Order:** By `id` ascending.
""",
        "solution": """SELECT id, name, age FROM users WHERE is_active = 1 AND city = 'Detroit' AND age >= 25 ORDER BY id ASC;""",
        "test_code": """
def test_sql_where(run_sql):
    rows = run_sql()
    # Alice is 28, Detroit, Active -> Match
    # Charlie is 22, Detroit, Inactive -> No
    # Others don't match city or active
    # Only Alice matches strict criteria? 
    # Let's check seed:
    # 1: Alice, 28, Detroit, 1 -> Yes
    # 3: Charlie, 22, Detroit, 0 -> No (inactive, age<25)
    
    # Wait, spec says age >= 25.
    assert len(rows) == 1
    assert rows[0] == (1, 'Alice', 28)
"""
    },
    {
        "slug": "sql-order-limit",
        "title": "Order + Limit",
        "readme": """# Mission: Order + Limit
**Goal:** Top 3 most expensive products (not discontinued).
Return `id, name, price_cents`.
**Order:** `price_cents DESC`, then `id ASC`.
""",
        "solution": """SELECT id, name, price_cents FROM products WHERE is_discontinued = 0 ORDER BY price_cents DESC, id ASC LIMIT 3;""",
        "test_code": """
def test_sql_order_limit(run_sql):
    rows = run_sql()
    assert len(rows) == 3
    # 1. Laptop (99900)
    # 2. Mouse (2500)
    # 3. Coffee (1200) -- Notebook is 500. Headphones discontinued.
    assert rows[0] == (1, 'Laptop', 99900)
    assert rows[1] == (2, 'Mouse', 2500)
    assert rows[2] == (3, 'Coffee', 1200)
"""
    },
    {
        "slug": "sql-aggregates",
        "title": "COUNT / SUM / AVG",
        "readme": """# Mission: Aggregates
**Goal:** Stats for orders where status is 'paid'.
Return ONE row with: `paid_order_count`, `paid_total_cents_sum`, `paid_total_cents_avg` (rounded).
""",
        "solution": """SELECT COUNT(*) AS paid_order_count, SUM(total_cents) AS paid_total_cents_sum, ROUND(AVG(total_cents)) AS paid_total_cents_avg FROM orders WHERE status = 'paid';""",
        "test_code": """
def test_sql_aggregates(run_sql):
    rows = run_sql()
    assert len(rows) == 1
    # Paid orders:
    # 1: 102400
    # 3: 9900
    # 5: 1700
    # Sum: 114000
    # Count: 3
    # Avg: 38000
    assert rows[0] == (3, 114000, 38000.0)
"""
    },
    {
        "slug": "sql-groupby-having",
        "title": "GROUP BY + HAVING",
        "readme": """# Mission: Group By + Having
**Goal:** Cities with at least 2 users.
Return `city, user_count`.
**Order:** `user_count DESC`, then `city ASC`.
""",
        "solution": """SELECT city, COUNT(*) AS user_count FROM users GROUP BY city HAVING COUNT(*) >= 2 ORDER BY user_count DESC, city ASC;""",
        "test_code": """
def test_sql_groupby_having(run_sql):
    rows = run_sql()
    # Detroit: 2 (Alice, Charlie)
    # Austin: 2 (Bob, Evan)
    # Others are 1
    # Order: count DESC -> both 2. Then city ASC -> Austin, Detroit.
    assert len(rows) == 2
    assert rows[0] == ('Austin', 2)
    assert rows[1] == ('Detroit', 2)
"""
    },
    {
        "slug": "sql-joins",
        "title": "INNER JOIN Basics",
        "readme": """# Mission: Inner Join
**Goal:** List paid orders with user name.
Return `order_id, user_name, total_cents`.
**Filter:** `status = 'paid'`.
**Order:** `order_id ASC`.
""",
        "solution": """SELECT o.id, u.name, o.total_cents FROM orders o JOIN users u ON u.id = o.user_id WHERE o.status = 'paid' ORDER BY o.id ASC;""",
        "test_code": """
def test_sql_joins(run_sql):
    rows = run_sql()
    assert len(rows) == 3
    # 1 (Alice), 3 (Bob), 5 (Diana)
    assert rows[0] == (1, 'Alice', 102400)
    assert rows[1] == (3, 'Bob', 9900)
    assert rows[2] == (5, 'Diana', 1700)
"""
    },
    {
        "slug": "sql-left-join-null",
        "title": "Find Missing Rows",
        "readme": """# Mission: Left Join (Missing)
**Goal:** Active users with NO orders.
Return `id, name`.
**Order:** `id ASC`.
""",
        "solution": """SELECT u.id, u.name FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE u.is_active = 1 AND o.id IS NULL ORDER BY u.id ASC;""",
        "test_code": """
def test_sql_left_join_null(run_sql):
    rows = run_sql()
    # Users:
    # 1 Alice (Has order)
    # 2 Bob (Has order)
    # 3 Charlie (No order, but inactive)
    # 4 Diana (Has order)
    # 5 Evan (Has order, inactive) ?? Order 6 is Evan.
    # 6 Fay (Active, no orders)
    
    # Wait, check seed:
    # Orders: 1->1, 2->1, 3->2, 4->3, 5->4, 6->5.
    # User 6 (Fay) has no orders.
    # User 3 (Charlie) has order 4 (cancelled), but user 3 is inactive.
    # We want ACTIVE users with no orders.
    # Fay is active (1).
    
    assert len(rows) == 1
    assert rows[0] == (6, 'Fay')
"""
    },
    {
        "slug": "sql-cte-subquery",
        "title": "CTE for Summaries",
        "readme": """# Mission: CTE Summaries
**Goal:** Users with >5000 cents in paid orders.
Use a CTE `paid_totals`.
Return `user_id, name, paid_total_cents`.
**Order:** `paid_total_cents DESC`, then `user_id ASC`.
""",
        "solution": """WITH paid_totals AS ( SELECT user_id, SUM(total_cents) AS paid_total_cents FROM orders WHERE status = 'paid' GROUP BY user_id ) SELECT u.id, u.name, p.paid_total_cents FROM paid_totals p JOIN users u ON u.id = p.user_id WHERE p.paid_total_cents >= 5000 ORDER BY p.paid_total_cents DESC, u.id ASC;""",
        "test_code": """
def test_sql_cte_subquery(run_sql):
    rows = run_sql()
    # Paid totals:
    # Alice (1): 102400
    # Bob (2): 9900
    # Diana (4): 1700 (<5000)
    
    assert len(rows) == 2
    assert rows[0] == (1, 'Alice', 102400)
    assert rows[1] == (2, 'Bob', 9900)
"""
    },
    {
        "slug": "sql-insert-update-delete",
        "title": "DML + Verify",
        "readme": """# Mission: DML
**Goal:**
1. INSERT product 6: Pen, office, 300, not discontinued.
2. UPDATE product 2 (Mouse): price 2600.
3. DELETE product 4 (Headphones).
Finally SELECT `id, name, price_cents` from `products` order by `id`.
""",
        "solution": """INSERT INTO products (id, name, category, price_cents, is_discontinued) VALUES (6, 'Pen', 'office', 300, 0); UPDATE products SET price_cents = 2600 WHERE id = 2; DELETE FROM products WHERE id = 4; SELECT id, name, price_cents FROM products ORDER BY id ASC;""",
        "test_code": """
def test_sql_insert_update_delete(run_sql):
    rows = run_sql()
    # 1. Laptop (99900)
    # 2. Mouse (2600) - Updated
    # 3. Coffee (1200)
    # 4. Deleted
    # 5. Notebook (500)
    # 6. Pen (300) - Inserted
    
    assert len(rows) == 5
    assert rows[0] == (1, 'Laptop', 99900)
    assert rows[1] == (2, 'Mouse', 2600)
    assert rows[2] == (3, 'Coffee', 1200)
    assert rows[3] == (5, 'Notebook', 500)
    assert rows[4] == (6, 'Pen', 300)
"""
    }
]

# --- Scaffolding Logic ---

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
    (quest_dir / "workspace" / "task.sql").write_text("-- TODO: Write your query here\nSELECT 'TODO';\n", encoding="utf-8")
    
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
    # Use underscore for python module name
    safe_slug = slug.replace("-", "_")
    (quest_dir / "grading" / "public" / f"test_{safe_slug}.py").write_text(test_content, encoding="utf-8")

def main():
    for q in QUESTS:
        scaffold_quest(q)
    print("Done scaffolding 10 SQL quests.")

if __name__ == "__main__":
    main()
