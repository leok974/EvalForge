
# ✍️ Quest Authoring Guide

Welcome to EvalForge content authoring. This guide is the “Golden Path” for creating quests that are executable, testable, and CI-safe.

## 🛠️ Toolkit (Golden Path)

| Tool | Purpose | Command |
|---|---|---|
| **Scaffolder** | Create a new quest folder + files | `python scripts/quest_new.py ...` |
| **CI Mirror** | Run the exact CI checks locally | `python scripts/dev_validate_all.py ...` |
| **Preview** | Render quest metadata/description quickly | `python scripts/quest_preview.py --slug ...` |
| **Audit** | Structural checks (missing fields, duplicates, etc.) | `python scripts/content_audit.py` |

> **Invariant:** Every tests-based quest must satisfy:
> - **Starter FAILS**
> - **Solution PASSES**
> This is enforced locally and in CI.

---

## 🚀 1) Create a New Quest (Scaffold)

Do **not** hand-write JSON from scratch. Use the scaffolder:

```bash
python scripts/quest_new.py \
  --world foundry \
  --track python_novice \
  --slug variables-101 \
  --title "Variables 101" \
  --language python \
  --kind tests
```

This generates:

```
docs/quests/variables-101/
  quest.json
  starter/
    main.py
    test_public.py
  solution/
    main.py
```

### What the scaffolder guarantees

* (world, track, slug) uniqueness (no silent overwrite)
* minimal required schema fields
* starter + solution structure appropriate for `--kind`
* a default `entrypoint` (e.g. `main.py`)

---

## ✍️ 2) Edit Content

Open `docs/quests/variables-101/` in VSCode.

### Files you will edit

* **`quest.json`**: title, description (Markdown), objectives, grading rules
* **`starter/main.py`**: what the player starts with
* **`starter/test_public.py`**: visible tests (must fail for starter)
* **`solution/main.py`**: reference solution (must pass)

---

## ✅ 3) Tests & Objectives

### Tests (recommended)

We use `unittest` for Python quests.

* **Public tests**: always required for tests-based quests.
* **Hidden tests** (optional): used for edge cases and anti-cheat checks.

#### Hidden tests: how to add

1. Create `starter/test_hidden.py` (or similar name).
2. Reference it in `quest.json` under `grading.hidden_tests`:

```json
"grading": {
    "mode": "tests",
    "public_tests": ["test_public.py"],
    "hidden_tests": ["test_hidden.py"]
}
```

> **Rule of thumb:** Public tests validate the core skill. Hidden tests validate edge cases.

### Objectives

Objectives should be specific and user-actionable.
Good: “Define `main()` and print exactly `Liftoff!`”
Bad: “Fix the code”

---

## ✅ 4) Verify Locally (CI Mirror)

Before committing, run the CI mirror locally:

```bash
python scripts/dev_validate_all.py --only-slug variables-101
```

Optional speed-ups:

```bash
python scripts/dev_validate_all.py --fast
python scripts/dev_validate_all.py --only-track python_novice
```

### What this runs (same as CI)

1. **Runner preflight** (docker socket + CLI + ability to spawn containers)
2. **Seed** your quest into DB (and detect conflicts)
3. **Audit** for structural issues
4. **Smoke**:
   * starter run → must FAIL
   * solution run → must PASS

---

## 🔎 5) Preview

To quickly preview the quest metadata (without launching the whole UI):

```bash
python scripts/quest_preview.py --slug variables-101
```

This prints:

* description rendering context
* objectives + grading rules
* starter/solution file list
* entrypoint

---

## 📦 6) Commit

If `dev_validate_all.py` is green 🟢:

1. commit your new quest folder
2. open a PR
3. CI will run `content-integrity.yml` to enforce invariants

---

## 🧯 Troubleshooting

### “Starter passes but should fail”

* Your public tests are too weak OR not discovered.
* Confirm your public tests are named `test*.py` and include assertions that starter fails.
* Run: `python scripts/dev_validate_all.py --only-slug <slug> --debug`

### “0 tests found”

* Your test file naming/discovery is wrong.
* Ensure files match `test*.py` (and live in the expected folder).
* Ensure `grading.public_tests` correctly lists the file (for frontend visibility), although currently the runner discovers all `test*.py` in the workspace.

### “No test output received”

* Runner infra issue (docker backend not used) OR JSON reporter not invoked.
* Check: `python scripts/runner_preflight.py`
* Ensure tests mode uses docker (enforced by the engine).

---

## 🎨 Design Guidelines

* **Starter code:** should run but fail logic (unless the quest is explicitly about syntax/indentation).
* **Small surface area:** 1 file unless multi-file is required.
* **Clear expected output:** specify exact formatting if output-based.
* **Avoid brittle regex:** prefer tests-based validation when possible.

## 7) Terms & Codex (Glossary)

Quests should define key terms to help learners connect concepts to the canonical Codex.

### File: `terms.json`

We support two formats. **New quests should use the Standard (Dict) format.**

#### Standard Format (Dict) — **Preferred**
Decouples the list of terms from the specific Codex references. This is "Tier-1 friendly" because it allows simple term lists without forcing a 1:1 mapping for every single term, while still enforcing that *some* references exist.

```json
{
  "key_terms": [
    "command",
    "terminal",
    "stdout"
  ],
  "codex_references": [
    "codex:glossary/cli/working-directory",
    "codex:glossary/cli/streams"
  ]
}
```

#### Legacy Format (List)
Maps specific terms directly to Codex references. Supported for backward compatibility but more verbose.

```json
[
  {
    "term": "command",
    "definition": "Instruction for the computer",
    "codex_ref": "codex:glossary/cli/command"
  }
]
```

### Policy
* **Tier 1 Quests**: Must have `terms.json` and valid Codex references.
* **Codex Audit**: Run `python scripts/codex_audit_missing.py` to verify your references resolved to actual files.
