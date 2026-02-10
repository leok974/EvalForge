#!/usr/bin/env python3
"""Add Usage sections to TS terms that are missing them."""
import frontmatter
from pathlib import Path

# Mapping of term ID to Usage bullets
USAGE_SECTIONS = {
    "generic": [
        "Write reusable functions that work with multiple types while preserving type safety.",
        "Avoid `any` by using generic type parameters (`<T>`) that preserve type information.",
        "Let TypeScript infer the type parameter from arguments when possible."
    ],
    "discriminated-union": [
        "Model states or variants with a shared discriminant field (like `kind` or `type`).",
        "Use `switch` or `if` statements on the discriminant to narrow types safely.",
        "Ensure exhaustiveness checks with `never` to catch missing cases."
    ],
    "type-guard": [
        "Create custom runtime checks that TypeScript recognizes for narrowing.",
        "Use `value is Type` predicates to tell TypeScript about the refined type.",
        "Combine with `typeof`, `instanceof`, or property checks for validation."
    ],
    "type-alias": [
        "Name complex types for reusability and readability.",
        "Define union types, object shapes, or function signatures concisely.",
        "Use with generics to create flexible, composable types."
    ],
    "interface": [
        "Define object shapes for domain models and public APIs.",
        "Use `extends` to compose interfaces and build type hierarchies.",
        "Prefer interfaces for object types; use type aliases for unions and primitives."
    ],
    "in-operator": [
        "Check for property existence in objects at runtime.",
        "Narrow union types based on distinct properties.",
        "Combine with nullish checks to safely access object properties."
    ],
    "never": [
        "Use in `switch` exhaustiveness checks to catch unhandled cases.",
        "Appears naturally when all possibilities are eliminated in control flow.",
        "Signals to TypeScript (and future readers) that a code path is unreachable."
    ],
    "type-annotation": [
        "Explicitly declare types at API boundaries (parameters, return values).",
        "Use when inference is unclear or when you want to enforce a specific type.",
        "Add to variables when the initial value doesn't reveal the intended type."
    ],
    "result-type": [
        "Replace exceptions with explicit success/failure values for error handling.",
        "Use discriminated unions (`ok: true | false`) to model outcomes.",
        "Force callers to handle errors explicitly instead of relying on try/catch."
    ],
    "union-type": [
        "Model values that can be one of several types (e.g., `string | number`).",
        "Narrow unions with type guards before accessing type-specific properties.",
        "Keep unions focused; overly broad unions reduce type safety."
    ],
    "type-narrowing": [
        "Refine types within conditional blocks using runtime checks.",
        "Use `typeof`, `instanceof`, or custom guards to tell TypeScript about narrowed types.",
        "Understand that type narrowing is scoped to the block where the check occurs."
    ],
    "type-parameter": [
        "Define generic functions, classes, or types with type parameters like `<T>`.",
        "Let TypeScript infer type parameters from arguments to reduce verbosity.",
        "Add constraints (`<T extends SomeType>`) to limit allowed types."
    ],
    "typeof": [
        "Check primitive types at runtime (`string`, `number`, `boolean`, etc.).",
        "Use as a type guard to narrow unions in conditionals.",
        "Remember `typeof null === 'object'` — guard against null explicitly."
    ],
    "type-inference": [
        "Let TypeScript figure out types from context (values, return statements, etc.).",
        "Rely on inference for local variables to reduce annotation noise.",
        "Add explicit annotations at API boundaries even if inference works."
    ]
}

def add_usage_section(file_path: Path, usage_bullets: list):
    """Add Usage section after Definition."""
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    content = post.content
    
    # Check if Usage already exists
    if "## Usage" in content:
        print(f"  ✓ {file_path.name} already has Usage section")
        return
    
    # Find Definition section and insert Usage after it
    if "## Definition" in content and "## Example" in content:
        # Build usage section
        usage_lines = ["## Usage"]
        for bullet in usage_bullets:
            usage_lines.append(f"- {bullet}")
        usage_lines.append("")  # Empty line before Example
        
        usage_section = "\n".join(usage_lines)
        
        # Insert between Definition and Example
        content = content.replace("\n## Example", f"\n\n{usage_section}\n## Example")
        
        post.content = content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        print(f"  ✓ Added Usage section to {file_path.name}")
    else:
        print(f"  ✗ Could not find Definition/Example sections in {file_path.name}")

def main():
    glossary_ts = Path("docs/codex/glossary/ts")
    
    for term_name, usage_bullets in USAGE_SECTIONS.items():
        file_path = glossary_ts / f"{term_name}.md"
        if file_path.exists():
            add_usage_section(file_path, usage_bullets)
        else:
            print(f"  ✗ File not found: {file_path}")

if __name__ == "__main__":
    main()
