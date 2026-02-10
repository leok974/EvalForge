#!/usr/bin/env python3
"""
Codex Placeholder Audit Script
Detects stub/placeholder content in Codex markdown files.
"""
import sys
import re
from pathlib import Path
import frontmatter
from typing import List, Set

# Banned placeholder phrases
PLACEHOLDER_PHRASES = [
    "Example pending",
    "currently being updated",
    "This definition is a scaffold",
    "fundamental concept in general",
    "TODO:",
    "TBD",
    "Example code",  # Generic placeholder
    "Common misunderstanding 1",  # Generic placeholder
    "concept/related-1",  # Generic placeholder link
]

# Required sections
REQUIRED_SECTIONS = [
    "## Definition",
    "## Usage",
    "## Example",
    "## Pitfalls",
    "## Related",
]

def check_file(file_path: Path) -> List[str]:
    """Check a single file for placeholder content."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        post = frontmatter.loads(content)
        body = post.content
        
        # Check for placeholder phrases
        for phrase in PLACEHOLDER_PHRASES:
            if phrase.lower() in body.lower():
                issues.append(f"Contains placeholder phrase: '{phrase}'")
        
        # Check for required sections
        for section in REQUIRED_SECTIONS:
            if section not in body:
                issues.append(f"Missing section: {section}")
        
        # Check for fenced code blocks
        if "```" not in body:
            issues.append("Missing fenced code block (no ```)")
        
        # Check for generic example comments
        if "// Example code" in body or "# Example code" in body:
            issues.append("Contains generic 'Example code' comment")
            
    except Exception as e:
        issues.append(f"Error reading file: {e}")
    
    return issues

def audit_directory(directory: Path, world_filter: str = None) -> dict:
    """Audit all markdown files in a directory."""
    results = {}
    
    for md_file in directory.rglob("*.md"):
        # Skip if world filter is set and doesn't match
        if world_filter:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    file_world = post.metadata.get("world", "")
                    if world_filter not in file_world:
                        continue
            except:
                continue
        
        issues = check_file(md_file)
        if issues:
            results[str(md_file.relative_to(directory.parent))] = issues
    
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit Codex for placeholder content")
    parser.add_argument("--world", help="Filter by world (e.g., 'python', 'typescript')")
    parser.add_argument("--fail-on-placeholders", action="store_true", help="Exit 1 if placeholders found")
    args = parser.parse_args()
    
    codex_root = Path("docs/codex/glossary")
    
    if not codex_root.exists():
        print(f"Error: {codex_root} not found")
        sys.exit(1)
    
    results = audit_directory(codex_root, args.world)
    
    if not results:
        print(f"✓ No placeholders found!")
        sys.exit(0)
    
    print(f"\n🚨 Found {len(results)} files with placeholder content:\n")
    
    for file_path, issues in sorted(results.items()):
        print(f"📄 {file_path}")
        for issue in issues:
            print(f"   - {issue}")
        print()
    
    if args.fail_on_placeholders:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
