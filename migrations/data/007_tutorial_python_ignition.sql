-- Phase 9.1.2: Populate Golden Tutorial Example #1
-- Quest: python-ignition (Python starter quest)

BEGIN;

UPDATE questdefinition
SET
  tutorial_md = '## Outcome
You will learn how EvalForge executes your code and how to fix basic syntax issues so your program runs successfully.

## Concept in 30 seconds
Code is executed by a language interpreter (Python). If the interpreter can''t *parse* your program, it stops immediately with a **SyntaxError** (or related errors like IndentationError/TabError). Fixing these early errors is the fastest way to get back to meaningful debugging.

## Key terms
- **Interpreter** (runs your Python code)
- **SyntaxError** (Python can''t parse your code)
- **String** (text values like "hello")
- **print()** (writes output)
- **Indentation** (Python uses whitespace to define blocks)

## Walkthrough
1) Click **Run** to see what error you''re getting.
2) Read the error message top-to-bottom: it usually tells you the file and line.
3) Fix the first syntax issue (often unmatched quotes, missing parentheses, or bad indentation).
4) Run again until the program executes without syntax errors.
5) Only then focus on matching the required output / objectives.

## Example implementation
A minimal Python program that prints a line:

```python
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

## Common mistakes
- Unmatched quotes in a string (`print("hello)`).
- Mixing tabs and spaces (can trigger TabError).
- Mis-indentation after `def` / `if` (IndentationError).
- Forgetting parentheses in `print(...)` (Python 3 requires them).

## Check yourself
- What does a SyntaxError mean compared to a logical bug?
- Why does indentation matter in Python?
- What does `print()` do?',

  key_terms = '[
    {
      "id": "python/interpreter",
      "term": "Interpreter",
      "one_liner": "A program that reads and executes your code.",
      "codex_ref": "glossary/python/interpreter",
      "tags": ["python", "basics"]
    },
    {
      "id": "python/syntax-error",
      "term": "SyntaxError",
      "one_liner": "Python couldn''t parse your code, so it can''t run.",
      "codex_ref": "glossary/python/syntax-error",
      "tags": ["python", "errors"]
    },
    {
      "id": "python/string",
      "term": "String",
      "one_liner": "Text data like \"hello\".",
      "codex_ref": "glossary/python/string",
      "tags": ["python", "types"]
    },
    {
      "id": "python/print",
      "term": "print()",
      "one_liner": "Writes output so you can see results.",
      "codex_ref": "glossary/python/print",
      "tags": ["python", "io"]
    },
    {
      "id": "python/indentation",
      "term": "Indentation",
      "one_liner": "Whitespace that defines code blocks in Python.",
      "codex_ref": "glossary/python/indentation",
      "tags": ["python", "syntax"]
    }
  ]'::jsonb,

  concept_tags = '["python-basics", "debugging", "syntax-errors"]'::jsonb,

  codex_references = '[
    "glossary/python/interpreter",
    "glossary/python/syntax-error",
    "glossary/python/indentation",
    "glossary/python/print",
    "glossary/python/string"
  ]'::jsonb

WHERE slug = 'python-ignition';

COMMIT;

-- Verification query
-- SELECT slug, 
--        CASE WHEN tutorial_md IS NOT NULL THEN 'YES' ELSE 'NO' END as has_tutorial,
--        jsonb_array_length(key_terms) as term_count,
--        jsonb_array_length(concept_tags) as tag_count
-- FROM questdefinition
-- WHERE slug = 'python-ignition';
