#!/usr/bin/env python3
"""
World Backfill Runner - Tier-1 Baseline Coverage

Generates tutorial stubs, terms.json, and codex pages for quests with zero coverage.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Set

# Full term definitions (one-paragraph)
TERM_DEFINITIONS = {
    # Core Python (non-systems)
    "data-pipeline": "A data pipeline is a repeatable series of steps that takes raw input (files, text, API responses), transforms it (clean/parse/validate), and produces structured output (lists/dicts/tables) that other code can use. In Python, pipelines often look like \"read → parse → transform → aggregate → write\".",
    "parse": "Parsing means converting unstructured text (like `\"42,Alex,true\"`) into structured values (like `{\"age\": 42, \"name\": \"Alex\", \"active\": True}`). Good parsers also handle bad input gracefully (missing fields, wrong types) and give clear errors.",
    "dictionary": "A dictionary is Python's key→value mapping type, used to label and retrieve values by name instead of position. It's ideal for structured records (`{\"id\": 7, \"status\": \"ok\"}`) and fast lookups.",
    "keyerror": "A `KeyError` happens when you try to access a dictionary key that doesn't exist (e.g., `d[\"missing\"]`). Prevent it by using `in`, `dict.get()`, or by ensuring keys are created before access.",
    "csv": "CSV (\"comma-separated values\") is a common plain-text tabular format where each line is a row and commas separate columns. In Python you typically use the `csv` module to avoid edge cases like quoted commas and newlines.",
    "for-loop": "A `for` loop runs a block of code once for each item in a sequence (list, string, file lines, etc.), and is Python's standard way to iterate safely and clearly. It's preferred over manual indexing when you just need each item.",
    "iteration": "Iteration is the process of stepping through items in an iterable one at a time. In Python, \"iterable\" means anything you can loop over (`for x in ...`), like lists, dict keys, ranges, and generators.",
    "range": "`range()` generates a sequence of integers, commonly used for counting loops or indexing. It's memory-efficient because it represents the sequence without creating a full list.",
    "infinite-loop": "An infinite loop is a loop that never stops because its exit condition is never reached (or doesn't exist). It's often caused by forgetting to update state, using the wrong condition, or accidentally reprocessing the same input.",
    "break-continue": "`break` exits the nearest loop immediately, while `continue` skips the rest of the current iteration and moves to the next one. They're useful for early exits and filtering, but can hide logic bugs if overused.",
    
    # Python Systems shared glossary
    "separation-of-concerns": "Separation of concerns means dividing a system so each part has one clear responsibility (e.g., parsing, validation, storage, UI). It makes code easier to test, reuse, and change because you can modify one part without breaking unrelated behavior.",
    "interface": "An interface is a contract that describes what operations a component provides (methods, inputs/outputs) without tying you to one implementation. In Python, interfaces are often expressed via protocols, abstract base classes, or simple \"duck typing\" patterns.",
    "dependency-injection": "Dependency injection means giving a function/class the helpers it needs (logger, database client, clock) as parameters instead of creating them inside. This improves testability and makes behavior configurable across environments.",
    "side-effect": "A side effect is any action that changes something outside a function's return value, like writing files, mutating global state, printing, or calling external services. Side effects make debugging harder, so good system design isolates them behind clear boundaries.",
    "configuration-env-vars": "Configuration is environment-specific settings (URLs, keys, modes) that should not be hardcoded into logic. Environment variables are a common way to inject config at runtime so the same code runs differently in dev/staging/prod.",
    "retry": "A retry is re-attempting a failed operation (network call, job step) to handle transient failures. Good retries use limits and backoff (wait longer after each failure) so you don't overload the system.",
    "idempotency": "Idempotency means repeating the same operation has the same effect as doing it once (no duplicate charges, no double writes). It's essential for job runners and APIs because retries and timeouts can cause the same request to run multiple times.",
    "timeout": "A timeout is a maximum time allowed for an operation before you treat it as failed. Timeouts prevent systems from hanging forever and help keep queues and workers healthy under slow or stuck conditions.",
    "exception-handling": "Exception handling lets you catch errors, log them, and either recover or fail cleanly. Good `try/except` blocks catch specific exceptions (not everything) and preserve the original error context.",
    "queue-worker": "A queue holds work items (jobs) to be processed later; a worker pulls jobs from the queue and runs them. This pattern increases reliability and throughput by decoupling job creation from job execution.",
    "observability": "Observability is the ability to understand what your system is doing based on outputs like logs, metrics, and traces. It's more than monitoring: it helps you explain *why* things are slow or failing.",
    "sli": "A Service Level Indicator is a measurable metric that reflects user experience (latency, error rate, freshness). SLIs are the numbers you track to know if the system is \"healthy\".",
    "slo": "A Service Level Objective is a target threshold for an SLI (e.g., \"99% of requests under 300ms\"). SLOs help you decide when to pause feature work to improve reliability.",
    "correlation-id": "A correlation ID is a unique identifier attached to logs/events so you can follow a single request or job across services. It's one of the fastest ways to debug multi-step flows.",
    "structured-logging": "Structured logging means logs are emitted as structured fields (JSON-like) instead of just plain text. That makes it easy to filter by `request_id`, `user_id`, `job_id`, and to build dashboards.",
    "profiling": "Profiling measures where time (and sometimes memory) is spent in your program so you can optimize the right thing. It prevents \"guess-driven optimization\" by showing what's actually slow.",
    "time-complexity": "Time complexity describes how runtime grows as input size increases (e.g., O(n), O(n²)). It's useful for predicting performance problems before they show up in production.",
    "hot-path": "A hot path is the part of code executed most frequently or consuming most runtime. Optimizing a hot path yields large gains; optimizing cold paths usually doesn't matter.",
    "bottleneck": "A bottleneck is the limiting step that caps overall throughput or latency (slowest database query, tight loop, serialized resource). Fixing bottlenecks often means reducing work, caching, or parallelizing.",
    "cprofile": "`cProfile` is Python's built-in deterministic profiler that records function call timings. It's a reliable starting point for finding slow functions and validating optimizations.",
    "venv": "A virtual environment isolates Python packages per project so dependencies don't conflict across projects. It's the simplest way to ensure consistent installs on your machine and in CI.",
    "dependency": "A dependency is an external package your project relies on to work (libraries you install). Managing dependencies carefully avoids version conflicts and \"works on my machine\" failures.",
    "package-manager": "A package manager installs, updates, and resolves dependencies. In Python, `pip` is the default tool; other ecosystems add lockfiles or environment management on top.",
    "module-not-found-error": "`ModuleNotFoundError` occurs when Python can't import a module because it's not installed, not in your environment, or your import path is wrong. It's commonly fixed by activating the correct venv and installing requirements.",
    "pip": "`pip` is Python's standard package installer used to add dependencies to your environment. Using `pip` inside an activated venv is the safest default to avoid polluting global Python.",
}

# Systems terms (go in python/systems/ subfolder)
SYSTEMS_TERMS = {
    "separation-of-concerns", "interface", "dependency-injection", "side-effect", "configuration-env-vars",
    "retry", "idempotency", "timeout", "exception-handling", "queue-worker",
    "observability", "sli", "slo", "correlation-id", "structured-logging",
    "profiling", "time-complexity", "hot-path", "bottleneck", "cprofile",
    "venv", "dependency", "package-manager", "module-not-found-error", "pip"
}

# Default term mappings for Python quests (Tier-1)
PYTHON_QUEST_TERMS = {
    "python-data-forge": [
        {"term": "data pipeline", "slug": "data-pipeline", "category": "concept", "one_liner": "A sequence of transformations that process raw data into a usable format"},
        {"term": "parse", "slug": "parse", "category": "concept", "one_liner": "Convert raw text or data into structured format"},
        {"term": "dictionary (dict)", "slug": "dictionary", "category": "concept", "one_liner": "Python's key-value data structure for mapping"},
        {"term": "KeyError", "slug": "keyerror", "category": "debugging", "one_liner": "Exception raised when accessing a non-existent dictionary key"},
        {"term": "CSV", "slug": "csv", "category": "runtime", "one_liner": "Comma-separated values file format for tabular data"},
    ],
    "python-loop": [
        {"term": "for loop", "slug": "for-loop", "category": "concept", "one_liner": "Iterate over a sequence of items"},
        {"term": "iteration", "slug": "iteration", "category": "concept", "one_liner": "The process of repeating steps over a collection"},
        {"term": "range()", "slug": "range", "category": "concept", "one_liner": "Generate a sequence of numbers for iteration"},
        {"term": "infinite loop", "slug": "infinite-loop", "category": "debugging", "one_liner": "A loop that never terminates, often a bug"},
        {"term": "break / continue", "slug": "break-continue", "category": "runtime", "one_liner": "Control flow statements to exit or skip loop iterations"},
    ],
    "python-systems-service-boundaries": [
        {"term": "separation of concerns", "slug": "separation-of-concerns", "category": "concept", "one_liner": "Design principle: different responsibilities should be separate modules"},
        {"term": "interface", "slug": "interface", "category": "concept", "one_liner": "A contract defining how components interact"},
        {"term": "dependency injection", "slug": "dependency-injection", "category": "concept", "one_liner": "Pass dependencies to a component rather than hardcoding them"},
        {"term": "side effect", "slug": "side-effect", "category": "debugging", "one_liner": "Unintended changes to state outside a function's scope"},
        {"term": "configuration (env vars)", "slug": "configuration-env-vars", "category": "runtime", "one_liner": "External settings passed via environment variables"},
    ],
    "python-systems-resilient-job-runner": [
        {"term": "retry", "slug": "retry", "category": "concept", "one_liner": "Automatically re-attempt a failed operation"},
        {"term": "idempotency", "slug": "idempotency", "category": "concept", "one_liner": "An operation that produces the same result when repeated"},
        {"term": "timeout", "slug": "timeout", "category": "concept", "one_liner": "Maximum time to wait before aborting an operation"},
        {"term": "exception handling (try/except)", "slug": "exception-handling", "category": "debugging", "one_liner": "Catch and handle errors gracefully"},
        {"term": "queue / worker", "slug": "queue-worker", "category": "runtime", "one_liner": "Background jobs processed by worker threads or processes"},
    ],
    "python-systems-observability-sli": [
        {"term": "observability", "slug": "observability", "category": "concept", "one_liner": "Measure system health through logs, metrics, and traces"},
        {"term": "SLI", "slug": "sli", "category": "concept", "one_liner": "Service Level Indicator: a quantifiable measure of service quality"},
        {"term": "SLO", "slug": "slo", "category": "concept", "one_liner": "Service Level Objective: target value for an SLI"},
        {"term": "correlation id", "slug": "correlation-id", "category": "debugging", "one_liner": "Unique identifier to trace a request across services"},
        {"term": "structured logging", "slug": "structured-logging", "category": "runtime", "one_liner": "Log messages as queryable key-value pairs, not plain text"},
    ],
    "python-systems-performance-profile": [
        {"term": "profiling", "slug": "profiling", "category": "concept", "one_liner": "Measure where your code spends time and memory"},
        {"term": "time complexity", "slug": "time-complexity", "category": "concept", "one_liner": "How execution time scales with input size (Big-O notation)"},
        {"term": "hot path", "slug": "hot-path", "category": "concept", "one_liner": "Code sections executed most frequently"},
        {"term": "bottleneck", "slug": "bottleneck", "category": "debugging", "one_liner": "The slowest part of your code that limits overall performance"},
        {"term": "cProfile", "slug": "cprofile", "category": "runtime", "one_liner": "Python's built-in profiling tool"},
    ],
    "python-systems-platform-tooling": [
        {"term": "virtual environment (venv)", "slug": "venv", "category": "concept", "one_liner": "Isolated Python environment with its own packages"},
        {"term": "dependency", "slug": "dependency", "category": "concept", "one_liner": "External package or library your code requires"},
        {"term": "package manager", "slug": "package-manager", "category": "concept", "one_liner": "Tool to install and manage dependencies (pip, poetry, etc.)"},
        {"term": "ImportError / ModuleNotFoundError", "slug": "module-not-found-error", "category": "debugging", "one_liner": "Exception when Python can't find a module to import"},
        {"term": "pip", "slug": "pip", "category": "runtime", "one_liner": "Python's default package installer"},
    ],
}


def generate_tutorial_stub(slug: str) -> str:
    """Generate Tier-1 tutorial stub (7-section format, no TODO)."""
    title = slug.replace("-", " ").title()
    
    return f"""# {title}

## 1. What You'll Build

In this quest, you'll work with {title.lower()} to practice core Python concepts.

## 2. The Concept in 30 Seconds

{title} demonstrates fundamental programming patterns used in real-world applications.

## 3. Key Terms

The key terms for this quest are defined below and linked to the Codex for reference.

## 4. Step-by-Step Walkthrough

### Setup
Review the starting code and understand the structure.

### Implementation
Follow the objectives to complete the implementation.

### Testing
Run your code to verify it works as expected.

## 5. Example Implementation

```python
# Example will be added based on quest objectives
pass
```

## 6. Common Mistakes

- Not reading the error messages carefully
- Forgetting to test edge cases
- Missing import statements

## 7. Check Yourself

- Does your code run without errors?
- Have you tested with different inputs?
- Does it match the expected output?
"""


def generate_terms_json(slug: str, terms_list: List[Dict]) -> List[Dict]:
    """Generate terms.json for a quest."""
    terms = []
    for term_data in terms_list:
        terms.append({
            "term": term_data["term"],
            "one_liner": term_data["one_liner"],
            "codex_ref": f"codex:glossary/python/{term_data['slug']}",
            "tags": [term_data["category"], "python"]
        })
    return terms


def generate_codex_stub(term_slug: str, term_name: str, one_liner: str, category: str) -> str:
    """Generate Codex glossary stub page with full definition."""
    
    # Get full definition if available, otherwise use one-liner
    full_definition = TERM_DEFINITIONS.get(term_slug, one_liner)
    
    # Check if this is a systems term (needs frontmatter ID)
    is_systems_term = term_slug in SYSTEMS_TERMS
    codex_id = f"codex:glossary/python/{term_slug}"
    
    # Build frontmatter for systems terms
    frontmatter = ""
    if is_systems_term:
        frontmatter = f"""---
id: {codex_id}
tags: [python, python-systems, {category}]
---

"""
    
    return f"""{frontmatter}# {term_name}

## Definition

{full_definition}

## Tiny Example

```python
# Example code demonstrating {term_name.lower()}
# TODO: Add concrete example
pass
```

## Common Pitfall

Watch out for common mistakes when using {term_name.lower()}.

## Related

- Other Python terms (to be linked)

**Category:** {category}
"""


def create_systems_landing_page() -> str:
    """Generate Python Systems shared glossary landing page."""
    return """---
id: codex:glossary/python/systems
tags: [python, python-systems]
---

# Python Systems

These entries cover reliability, observability, performance, and tooling concepts you'll reuse across Python "systems" quests.

## Categories

### Reliability & Resilience
- retry
- idempotency
- timeout
- exception handling
- queue / worker

### Observability
- observability
- SLI / SLO
- correlation id
- structured logging

### Performance
- profiling
- time complexity
- hot path
- bottleneck
- cProfile

### Architecture & Design
- separation of concerns
- interface
- dependency injection
- side effect
- configuration (env vars)

### Tooling
- venv
- dependency
- package manager
- pip
- ModuleNotFoundError
"""


def backfill_quest(slug: str, terms_list: List[Dict], write: bool = False, create_codex: bool = False):
    """Backfill a single quest with tutorial and terms."""
    print(f"\n📝 Processing: {slug}")
    
    # Determine quest directory
    # Check multiple locations for quest files
    quest_dirs = [
        Path(f"data/questpacks/{slug}"),
        Path(f"docs/quests/{slug}"),
    ]
    
    # Find or create quest directory
    quest_dir = None
    for qd in quest_dirs:
        if qd.exists():
            quest_dir = qd
            break
    
    if not quest_dir:
        quest_dir = Path(f"docs/quests/{slug}")
        if write:
            quest_dir.mkdir(parents=True, exist_ok=True)
            print(f"   Created directory: {quest_dir}")
    
    # Generate tutorial if missing
    tutorial_path = quest_dir / "tutorial.md"
    if not tutorial_path.exists():
        tutorial_content = generate_tutorial_stub(slug)
        if write:
            tutorial_path.write_text(tutorial_content, encoding="utf-8")
            print(f"   ✅ Created tutorial: {tutorial_path}")
        else:
            print(f"   [DRY-RUN] Would create tutorial: {tutorial_path}")
    else:
        print(f"   ⏭️  Tutorial exists: {tutorial_path}")
    
    # Generate terms.json if missing
    terms_path = quest_dir / "terms.json"
    if not terms_path.exists() or True:  # Always regenerate for now
        terms_content = generate_terms_json(slug, terms_list)
        if write:
            terms_path.write_text(json.dumps(terms_content, indent=2), encoding="utf-8")
            print(f"   ✅ Created terms: {terms_path} ({len(terms_content)} terms)")
        else:
            print(f"   [DRY-RUN] Would create terms: {terms_path} ({len(terms_content)} terms)")
    else:
        print(f"   ⏭️  Terms exist: {terms_path}")
    
    # Create codex stub pages
    if create_codex:
        for term_data in terms_list:
            term_slug = term_data['slug']
            # Determine path: systems terms go in systems/ subfolder
            if term_slug in SYSTEMS_TERMS:
                codex_path = Path(f"data/codex/glossary/python/systems/{term_slug}.md")
            else:
                codex_path = Path(f"data/codex/glossary/python/{term_slug}.md")
            
            if not codex_path.exists():
                codex_content = generate_codex_stub(
                    term_slug, 
                    term_data['term'], 
                    term_data['one_liner'],
                    term_data['category']
                )
                if write:
                    codex_path.parent.mkdir(parents=True, exist_ok=True)
                    codex_path.write_text(codex_content, encoding="utf-8")
                    print(f"   ✅ Created codex stub: {codex_path}")
                else:
                    print(f"   [DRY-RUN] Would create codex: {codex_path}")


def main():
    parser = argparse.ArgumentParser(description="Tier-1 Baseline Backfill Runner")
    parser.add_argument("--world", default="python", help="World to backfill (default: python)")
    parser.add_argument("--bucket", choices=["none", "partial", "all"], default="none", help="Which bucket to backfill")
    parser.add_argument("--write", action="store_true", help="Actually write files (default: dry-run)")
    parser.add_argument("--create-codex-stubs", action="store_true", default=True, help="Create codex stub pages")
    parser.add_argument("--min-terms", type=int, default=3, help="Minimum terms per quest")
    args = parser.parse_args()
    
    # Load bucket data
    bucket_file = Path(f"artifacts/world-{args.world}-buckets.json")
    if not bucket_file.exists():
        print(f"❌ Bucket file not found: {bucket_file}")
        print("   Run categorize_coverage_buckets.py first")
        return 1
    
    with open(bucket_file, 'r', encoding='utf-8') as f:
        buckets = json.load(f)
    
    # Determine which quests to process
    if args.bucket == "none":
        quests_to_process = [q["slug"] for q in buckets["none"]]
    elif args.bucket == "partial":
        quests_to_process = [q["slug"] for q in buckets["partial"]]
    else:
        quests_to_process = [q["slug"] for q in buckets["none"] + buckets["partial"]]
    
    print(f"\n🚀 Python Tier-1 Backfill")
    print(f"   World: {args.world}")
    print(f"   Bucket: {args.bucket}")
    print(f"   Quests: {len(quests_to_process)}")
    print(f"   Mode: {'WRITE' if args.write else 'DRY-RUN'}")
    print(f"   Create codex: {args.create_codex_stubs}")
    
    # Create systems landing page first
    if args.create_codex_stubs:
        systems_landing_path = Path("data/codex/glossary/python/systems/systems.md")
        if not systems_landing_path.exists():
            systems_content = create_systems_landing_page()
            if args.write:
                systems_landing_path.parent.mkdir(parents=True, exist_ok=True)
                systems_landing_path.write_text(systems_content, encoding="utf-8")
                print(f"\n✅ Created Python Systems landing page: {systems_landing_path}")
            else:
                print(f"\n[DRY-RUN] Would create systems landing: {systems_landing_path}")
    
    # Process each quest
    for slug in quests_to_process:
        if slug in PYTHON_QUEST_TERMS:
            terms_list = PYTHON_QUEST_TERMS[slug]
            backfill_quest(slug, terms_list, write=args.write, create_codex=args.create_codex_stubs)
        else:
            print(f"\n⚠️  Warning: No term mapping for {slug}")
    
    print(f"\n✅ Backfill complete!")
    print(f"   Processed: {len(quests_to_process)} quests")
    if not args.write:
        print(f"\n   ℹ️  This was a DRY-RUN. Use --write to actually create files.")


if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)
