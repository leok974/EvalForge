# Quest Objective Contract

**Source of truth** for how objectives are stored, serialized, and rendered.

---

## Objective Shapes

There are three valid shapes an objective can take in the database.
All three are supported via normalization at the API layer.

### A) Legacy frontend format (old quests)
```json
{ "id": "o1", "text": "Define a main() function", "why": "Entry point", "validator": {"kind": "source_regex", "value": "def main"} }
```

### B) New authoring format (post Phase Debt-2)
```json
{ "id": "obj_syntax", "title": "Uses OVER + PARTITION BY", "kind": "source_regex", "rule": {"pattern": "OVER\\s*\\("} }
```

### C) State/tests-pass text-only format (CSS, HTML, CLI, Node quests)
```json
{ "id": "obj_default", "text": "Complete the assignment as described in README.md", "why": "Specification requirement" }
```
> No `validator` key — grading is handled entirely by the backend runner (state check or test runner).

---

## API Contract (what the UI always receives)

Regardless of which DB shape is stored, `GET /api/quests/{slug}` always returns:

```json
{
  "id": "string (required)",
  "text": "string (required — never blank)",
  "why": "string (optional)",
  "validator": {
    "kind": "source_regex | stdout_regex | exit_code_zero | tests_pass | ast | contains | regex",
    "value": "string (pattern / function name / test file)"
  }
}
```

`validator` may be **absent** for C-format state objectives — the UI renders text only, grading is server-side.

---

## Normalization

The mapping from DB → API lives entirely in:

```
arcade_app/quest_helper.py :: _normalize_objectives(objectives: list) -> list
```

Mapping rules:
| DB field | API field | Notes |
|---|---|---|
| `title` | `text` | Falls back to `id` if both missing |
| `kind` (top-level) | `validator.kind` | |
| `rule.pattern` | `validator.value` | For `source_regex` / `stdout_regex` |
| `rule.must_define_function` | `validator.value` | For `ast` |
| `rule.test_file` | `validator.value` | For `tests_pass` |
| — | `validator.value = "0"` | For `exit_code_zero` |

---

## Valid `validator.kind` values

| Kind | Runner |
|---|---|
| `source_regex` | Regex against submitted source code |
| `stdout_regex` | Regex against process stdout |
| `exit_code_zero` | Process exit code == 0 |
| `tests_pass` | Test runner (pytest / node --test) |
| `ast` | Python AST structural check |
| `contains` | Substring check on source |
| `regex` | Legacy alias for `source_regex` |
| `state` | World-level state check (git, fs, etc.) |

---

## Guards

| Guard | File | What it catches |
|---|---|---|
| Unit tests | `tests/test_objectives_serializer_shape.py` | Old + new format normalization; edge cases |
| Live DB audit | `scripts/audit_objectives_shape.py` | Blank `text` or malformed `validator` in any quest |
| Frontend fallback | `QuestDrawer.tsx` line ~154 | `obj.text \|\| obj.title \|\| "(missing objective text)"` + dev badge |

CI runs both audit + tests on every check via `scripts/ci_check.py`.

---

## Incident Reference

`incident_objectives_ui_blank_rows` — 2026-02-25

Symptom: Objectives count showed correct total (e.g. "0/2") but each row rendered as an empty shell with no text.

Root cause: Phase Debt-2 backfill wrote objectives in format B, but `quest_to_dict()` returned the raw array without normalizing to the frontend contract. `QuestDrawer` reads `obj.text` (undefined in format B) giving blank rows.

Fix: `_normalize_objectives()` added to `quest_helper.py`.

Full postmortem: `docs/audits/TRAINING_GRADE_RELEASE_SNAPSHOT.json` → `incident_objectives_ui_blank_rows`.
