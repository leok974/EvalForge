#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

DOCS_DIR = Path("docs/quests")

BRIEFING_TMPL = """# Briefing — {slug}

## Objective
Implement the required behavior for **{slug}** so all public tests pass.

## Context
This quest is about **<core concept>**: learning to implement distinct functionality with clear boundaries and minimal side effects.

## Where You’ll Work
- Primary file(s): (see **README.md** for exact paths)
- Tests: (see **README.md** / questpack)
- Do not edit: (see **README.md**)

## Requirements
- ✅ Complete the assignment as described in **README.md**
- ✅ Match the expected behavior and output shapes
- ✅ Keep changes minimal and test-driven

## Constraints
- Follow the quest constraints described in the prompt and starter code.
- Prefer small, test-driven changes; avoid extra dependencies unless explicitly allowed.

## Success Criteria
- [ ] All public tests pass for this quest
- [ ] Implementation matches expected function signatures and output shapes
- [ ] No unnecessary complexity or hidden side effects

## How To Verify
```bash
# (See README.md for exact command)
node scripts/run_world_public_tests.mjs --questpack <questpack_path> --only-slug {slug}
```

## Spec and Codex References

* README: `README.md` (this quest’s source-of-truth spec)
* Codex: [[codex:systems/service-boundary]] (example)
"""

TUTORIAL_TMPL = """# Tutorial — {slug}

## What You’ll Learn
- How to implement the core logic for **{slug}**
- How to isolate responsibilities into clear boundary surfaces
- How to shape inputs/outputs so tests can validate behavior cleanly

## Approach
Treat this quest like building a small service with a clean contract:
**inputs in → deterministic behavior → outputs out**, with side effects isolated (or eliminated).

## Implementation Plan
1. **Read the README spec**
   - Identify the required behavior and the “contract” (inputs/outputs).
2. **Locate the entrypoint**
   - Find the function/module the tests exercise (the first failing test usually reveals it).
3. **Implement the baseline path**
   - Start with the simplest valid case the tests expect.
4. **Enforce the boundary**
   - If logic is mixed (parsing + formatting), split responsibilities.
5. **Handle edge cases**
   - Follow what tests imply: empty inputs, invalid cases, ordering, defaults.

## Testing
```bash
# (See README.md for exact command)
node scripts/run_world_public_tests.mjs --questpack <questpack_path> --only-slug {slug}
```

* Run once to see the first assertion failure.
* Fix *only what that failure requires*, then re-run.
* Repeat until green.

## Pitfalls

* Hardcoding values that only satisfy one test case
* Mixing concerns inside the boundary function (making it hard to reason about)
* Returning the right data but in the wrong shape/order

## If You’re Stuck

Use `hints.md` in order—Hint 3 should be enough to unblock you without reading a full solution.
"""

HINTS_TMPL = """# Hints — {slug}

## Hint 1 (nudge)
The tests are checking a **contract**. Focus on shaping the output exactly as expected (types/keys/order), and keep side effects out of the core logic.

## Hint 2 (more specific)
Look for the first failing assertion and trace backwards:
- What input did the test pass in?
- What output shape is expected?
The entrypoint is usually the function named in the failure message or the module imported by the test.

## Hint 3 (close)
If the logic feels tangled, split it into:
- a “pure” function that does transformation/validation
- a wrapper that handles any I/O (if any exists)
Then test expectations should align naturally.

## Hint 4 (optional spoiler)
> Spoiler: The cleanest fix is usually to make the boundary function return a single normalized structure and keep parsing/formatting outside.
"""

LORE_TMPL = """# Lore

In the Systems world, every module is a city—and boundaries are the walls that keep it from collapsing.
Build the contract cleanly here, and the rest of the system can evolve without breaking.
"""


def _write_if_missing(path: Path, content: str, dry_run: bool, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    if dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="Quest slug (e.g., react-effects).")
    ap.add_argument("--tier", type=int, default=1, help="Tutorial tier used to decide which files to scaffold.")
    ap.add_argument("--with-lore", action="store_true", help="Also scaffold lore.md.")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be created without writing files.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files even if they have content.")
    args = ap.parse_args()

    slug = args.slug.strip()
    qdir = DOCS_DIR / slug

    created = []

    if args.tier >= 1:
        if _write_if_missing(qdir / "briefing.md", BRIEFING_TMPL.format(slug=slug), args.dry_run, args.force):
            created.append(str(qdir / "briefing.md"))
        if _write_if_missing(qdir / "tutorial.md", TUTORIAL_TMPL.format(slug=slug), args.dry_run, args.force):
            created.append(str(qdir / "tutorial.md"))
        if _write_if_missing(qdir / "hints.md", HINTS_TMPL.format(slug=slug), args.dry_run, args.force):
            created.append(str(qdir / "hints.md"))
        if args.with_lore:
            if _write_if_missing(qdir / "lore.md", LORE_TMPL.format(slug=slug), args.dry_run, args.force):
                created.append(str(qdir / "lore.md"))
    else:
        # Tier-0 drafts: only briefing by default
        if _write_if_missing(qdir / "briefing.md", BRIEFING_TMPL.format(slug=slug), args.dry_run, args.force):
            created.append(str(qdir / "briefing.md"))
        if args.with_lore:
            if _write_if_missing(qdir / "lore.md", LORE_TMPL.format(slug=slug), args.dry_run, args.force):
                created.append(str(qdir / "lore.md"))

    if args.dry_run:
        print("[scaffold_quest_docs] dry-run")
    if created:
        print("[scaffold_quest_docs] created:")
        for p in created:
            print(f"  - {p}")
    else:
        print("[scaffold_quest_docs] nothing to do (all files already exist).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
