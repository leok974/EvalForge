import os
import frontmatter

CODEX_DIR = r"d:\EvalForge\docs\codex\glossary\sql"

# Core SQL terms that I definitely messed up and need to restore/ensure quality
CORE_TERMS = {
    "select": {
        "title": "SELECT",
        "content": """The `SELECT` statement is the most fundamental command in SQL. It is used to retrieve data from one or more tables.

## Basic Syntax

```sql
SELECT column1, column2 FROM table_name;
```

## Selecting All Columns

To select every column in a table, use the asterisk (`*`) wildcard:

```sql
SELECT * FROM users;
```

## Unique Values

Use the `DISTINCT` keyword to return only unique values, suppressing duplicates:

```sql
SELECT DISTINCT country FROM users;
```""",
        "level": "beginner",
        "tags": ["fundamentals", "query"]
    },
    "from": {
        "title": "FROM",
        "content": """The `FROM` clause specifies the database table from which you want to retrieve data. It is used in combination with the [SELECT](codex:glossary/sql/select) statement.

## Usage

```sql
SELECT name FROM employees;
```

In this example, `employees` is the source table.

## Joining Tables

`FROM` is also where you define [JOIN](codex:glossary/sql/join) operations to combine data from multiple tables.

```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
```""",
        "level": "beginner",
        "tags": ["fundamentals", "query"]
    },
    "where": {
        "title": "WHERE",
        "content": """The `WHERE` clause is used to filter records. It ensures that only those rows that fulfill a specific condition are returned.

## Basic Comparison

```sql
SELECT * FROM users WHERE age >= 18;
```

## Logical Operators

You can combine multiple conditions using [AND](codex:glossary/sql/and) and **OR**.

```sql
SELECT * FROM users WHERE country = 'USA' AND is_active = 1;
```

## Special Operators

- **IN**: To match against a list of values.
- **LIKE**: To perform simple pattern matching (e.g., `%` for any characters).
- **BETWEEN**: To match within a range of values.
- **IS NULL**: To find [NULL](codex:glossary/sql/null) values.""",
        "level": "beginner",
        "tags": ["fundamentals", "filtering"]
    },
    "order-by": {
        "title": "ORDER BY",
        "content": """The `ORDER BY` clause is used to sort the result set in either [ascending](codex:glossary/sql/asc) or [descending](codex:glossary/sql/desc) order.

## Usage

By default, `ORDER BY` sorts in ascending order.

```sql
-- Sort by name A-Z
SELECT * FROM users ORDER BY name;

-- Sort by age oldest to youngest
SELECT * FROM users ORDER BY age DESC;
```

## Multiple Columns

You can sort by multiple columns. If the first column has duplicate values, the second column will be used to break the tie.

```sql
SELECT * FROM users ORDER BY last_name ASC, first_name ASC;
```""",
        "level": "beginner",
        "tags": ["fundamentals", "sorting"]
    },
    "limit": {
        "title": "LIMIT",
        "content": """The `LIMIT` clause is used to specify the maximum number of records to return. It is extremely useful for performance on large tables or for creating pagination.

## Usage

```sql
-- Get the 5 most recent users
SELECT * FROM users ORDER BY created_at DESC LIMIT 5;
```

## Offset

You can use `OFFSET` to skip a specified number of rows before beginning to return results.

```sql
-- Skip the first 10, then get 10
SELECT * FROM users LIMIT 10 OFFSET 10;
```""",
        "level": "beginner",
        "tags": ["fundamentals", "pagination"]
    },
    "group-by": {
        "title": "GROUP BY",
        "content": """The `GROUP BY` clause groups rows that have the same values into summary rows, like "find the number of customers in each country".

## Usage with Aggregates

`GROUP BY` is almost always used with aggregate functions like `COUNT()`, `MAX()`, `MIN()`, `SUM()`, or `AVG()`.

```sql
-- Count users per country
SELECT country, COUNT(*) 
FROM users 
GROUP BY country;
```

## Rules

Any column in your `SELECT` list that is not part of an aggregate function **must** be included in the `GROUP BY` clause.""",
        "level": "intermediate",
        "tags": ["fundamentals", "aggregates"]
    },
    "having": {
        "title": "HAVING",
        "content": """The `HAVING` clause was added to SQL because the [WHERE](codex:glossary/sql/where) keyword could not be used with aggregate functions.

## Difference between WHERE and HAVING

- `WHERE`: Filters rows **before** they are grouped.
- `HAVING`: Filters the groups themselves **after** grouping is performed.

## Usage

```sql
-- Find countries with more than 100 users
SELECT country, COUNT(*)
FROM users
GROUP BY country
HAVING COUNT(*) > 100;
```""",
        "level": "intermediate",
        "tags": ["fundamentals", "aggregates"]
    },
    "count": {
        "title": "COUNT",
        "content": """The `COUNT()` function returns the number of rows that matches a specified criterion.

## Variations

- **COUNT(*)**: Returns the total number of rows in the table.
- **COUNT(col)**: Returns the number of non-null values in a specific column.
- **COUNT(DISTINCT col)**: Returns the number of unique non-null values.

## Usage

```sql
-- Count active users
SELECT COUNT(*) FROM users WHERE is_active = 1;

-- Count unique zip codes
SELECT COUNT(DISTINCT zip_code) FROM users;
```""",
        "level": "beginner",
        "tags": ["fundamentals", "aggregates"]
    }
}

def fix_codex():
    for filename in os.listdir(CODEX_DIR):
        if not filename.endswith(".md"):
            continue
        
        path = os.path.join(CODEX_DIR, filename)
        stem = filename[:-3]
        
        try:
            post = frontmatter.load(path)
            
            # 1. Check if we should restore quality for a core term
            if stem in CORE_TERMS:
                spec = CORE_TERMS[stem]
                post.metadata["title"] = spec["title"]
                post.metadata["id"] = f"glossary/sql/{stem}"
                post.metadata["world"] = "sql"
                if "level" in spec: post.metadata["level"] = spec["level"]
                if "tags" in spec: post.metadata["tags"] = spec["tags"]
                post.content = spec["content"]
                print(f"✨ Restored high-quality core term: {stem}")
            else:
                # 2. Add boilerplate frontmatter to others if missing
                if not post.metadata.get("id"):
                    post.metadata["id"] = f"glossary/sql/{stem}"
                if not post.metadata.get("title"):
                    # Extract H1 title if possible
                    lines = post.content.split("\n")
                    for line in lines:
                        if line.startswith("# "):
                            post.metadata["title"] = line[2:].strip()
                            break
                    else:
                        post.metadata["title"] = stem.replace("-", " ").title()
                
                if not post.metadata.get("world"):
                    post.metadata["world"] = "sql"
                
                print(f"✅ Adjusted frontmatter for: {stem}")

            # Ensure related links in frontmatter have codex: prefix if they are missing it
            related = post.metadata.get("related", [])
            if related:
                new_related = []
                for r in related:
                    if r.startswith("glossary/") and not r.startswith("codex:"):
                        new_related.append(f"codex:{r}")
                    else:
                        new_related.append(r)
                post.metadata["related"] = new_related

            with open(path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    fix_codex()
