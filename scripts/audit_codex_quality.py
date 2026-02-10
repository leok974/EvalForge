#!/usr/bin/env python3
"""
Codex Quality Audit Script

Enforces strict quality standards for Codex documentation across all active quests.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

import frontmatter

# ==================== CONFIGURATION ====================

DOCS_DIR = Path("docs")
DATA_DIR = Path("data")
CODEX_ROOT = DOCS_DIR / "codex"
ARTIFACTS_DIR = Path("artifacts")

STUB_MARKERS = [
    "TODO", "TBD", "coming soon", "stub", "placeholder", "accessing archival data"
]

MIN_CONTENT_LENGTH = 120

# ==================== HELPERS ====================

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {path}: {e}")
        return {}

def resolve_active_quests() -> List[str]:
    """Resolve all active quest slugs from questpacks."""
    config_path = Path("configs/questpacks_active.json")
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        return []
    
    config = load_json(config_path)
    questpacks = config.get("active_questpacks", [])
    
    slugs = set()
    for pack_path in questpacks:
        pack_full_path = Path(pack_path)
        if not pack_full_path.exists():
            print(f"⚠️ Questpack not found: {pack_path}")
            continue
            
        pack_data = load_json(pack_full_path)
        
        quests = []
        if isinstance(pack_data, list):
            quests = pack_data
        elif isinstance(pack_data, dict):
            quests = pack_data.get("quests", [])
            
        for q in quests:
            if isinstance(q, str):
                slugs.add(q)
            elif isinstance(q, dict) and "slug" in q:
                slugs.add(q["slug"])
                
    return sorted(list(slugs))

def extract_terms(slug: str) -> Dict[str, str]:
    """Extract required terms for a quest."""
    terms = {} # ref -> source
    
    # 1. terms.json (Preferred)
    terms_json = DOCS_DIR / "quests" / slug / "terms.json"
    if terms_json.exists():
        data = load_json(terms_json)
        # Handle list or dict format
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "codex_ref" in item:
                    terms[item["codex_ref"]] = "terms.json"
        elif isinstance(data, dict):
             for ref in data.get("codex_references", []):
                 terms[ref] = "terms.json"

    # 2. quest.json
    quest_json = DATA_DIR / "quests" / slug / "quest.json"
    if quest_json.exists():
        data = load_json(quest_json)
        for ref in data.get("codex_references", []):
            if ref not in terms:
                terms[ref] = "quest.json"
                
    # 3. tutorial.md (Regex)
    tutorial_md = DOCS_DIR / "quests" / slug / "tutorial.md"
    if tutorial_md.exists():
        try:
            content = tutorial_md.read_text(encoding="utf-8")
            matches = re.findall(r'codex:([a-zA-Z0-9/_\-]+)', content)
            for m in matches:
                ref = f"codex:{m}"
                if ref not in terms:
                    terms[ref] = "tutorial.md"
        except:
            pass
            
    return terms


def resolve_codex_path(ref: str) -> Optional[Path]:
    """Resolve a codex: reference to a file path."""
    if not ref.startswith("codex:"):
        return None
        
    clean_ref = ref.replace("codex:", "")
    # Check direct mapping first
    candidate = CODEX_ROOT / f"{clean_ref}.md"
    if candidate.exists():
        return candidate
    
    # Fallback: Search by ID in frontmatter (expensive, maybe cache if needed)
    # For now, simplistic approach: assume path matches ID mostly. 
    # Or strict enforcement: Path MUST match ID logic? 
    # The prompt says: "verify codex pages exist" -> implied path resolution.
    # Let's try to find it if direct path fails.
    
    for root, _, files in os.walk(CODEX_ROOT):
        for file in files:
            if file.endswith(".md"):
                p = Path(root) / file
                try:
                    post = frontmatter.load(p)
                    if post.metadata.get("id") == ref or post.metadata.get("id") == clean_ref:
                        return p
                except:
                    continue
                    
    return None

def is_stub(path: Path) -> Tuple[bool, str]:
    """Check if a file is a stub."""
    try:
        post = frontmatter.load(path)
        content = post.content.strip()
        
        # 1. Metadata check
        if post.metadata.get("stub") is True or post.metadata.get("status") == "stub":
            return True, "Frontmatter stub flag"
            
        # 2. Length check
        if len(content) < MIN_CONTENT_LENGTH:
            return True, f"Too short ({len(content)} chars)"
            
        # 3. Phrase check
        content_lower = content.lower()
        for marker in STUB_MARKERS:
            if marker.lower() in content_lower:
                return True, f"Contains stub marker: '{marker}'"
                
        # 4. Content signals
        # if "```" not in content and "# " not in content:
        #    return True, "No code samples or headers"
            
        return False, ""
    except Exception as e:
        return True, f"Error parsing: {e}"

# ==================== MAIN ====================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["disk"], default="disk", help="Only disk supported for now")
    parser.add_argument("--active", action="store_true", default=True, help="Scan active quests only")
    args = parser.parse_args()
    
    print("🚀 Starting Codex Quality Audit...")
    
    slugs = resolve_active_quests()
    print(f"📦 Found {len(slugs)} active quests")
    
    required_terms = {} # slug -> {ref: source}
    all_refs = set()
    
    # Step 1: Gather Terms
    print("🔍 Gathering terms...")
    for slug in slugs:
        terms = extract_terms(slug)
        if terms:
            required_terms[slug] = terms
            for ref in terms:
                all_refs.add(ref)
                
    # Save required terms artifact
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    with open(ARTIFACTS_DIR / "codex_required_terms.json", "w") as f:
        json.dump(required_terms, f, indent=2)
        
    # Step 2: Audit
    print(f"🕵️ Auditing {len(all_refs)} unique references...")
    
    missing_refs = []
    stub_refs = []
    quality_warnings = []
    valid_refs = 0
    
    # Cache resolution to avoid repeated walks
    path_cache = {}
    
    for ref in sorted(list(all_refs)):
        path = resolve_codex_path(ref)
        
        if not path:
            missing_refs.append(ref)
            continue
            
        stub, reason = is_stub(path)
        if stub:
            stub_refs.append({"ref": ref, "path": str(path), "reason": reason})
        else:
            valid_refs += 1
            # Quality Checks (Warnings Only)
            signals = check_quality_signals(path)
            if signals:
                quality_warnings.append({"ref": ref, "path": str(path), "signals": signals})
            
    # Generate Report
    report_path = ARTIFACTS_DIR / "codex_quality_report.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Codex Quality Report\n\n")
        f.write(f"- **Active Quests:** {len(slugs)}\n")
        f.write(f"- **Unique Terms:** {len(all_refs)}\n")
        f.write(f"- **Valid:** {valid_refs}\n")
        f.write(f"- **Missing:** {len(missing_refs)}\n")
        f.write(f"- **Stubs:** {len(stub_refs)}\n")
        f.write(f"- **Quality Warnings:** {len(quality_warnings)}\n\n")
        
        if missing_refs:
            f.write("## ❌ Missing References\n\n")
            for ref in missing_refs:
                f.write(f"- `{ref}`\n")
            f.write("\n")
            
        if stub_refs:
            f.write("## ⚠️ Stub / Low Quality Pages\n\n")
            for item in stub_refs:
                f.write(f"- **{item['ref']}**: {item['reason']} (`{item['path']}`)\n")
            f.write("\n")

        if quality_warnings:
            f.write("## 💡 Quality Improvements (Non-Blocking)\n\n")
            for item in quality_warnings:
                f.write(f"### {item['ref']}\n")
                for sig in item['signals']:
                    f.write(f"- {sig}\n")
                f.write("\n")
            
        if not missing_refs and not stub_refs:
            f.write("✅ **All systems nominal.** Codex is complete and high-quality.\n")

    print(f"📄 Report generated: {report_path}")
    
    # Exit Code
    if missing_refs or stub_refs:
        print(f"❌ Audit FAILED: {len(missing_refs)} missing, {len(stub_refs)} stubs.")
        sys.exit(1)
    else:
        print(f"✅ Audit PASSED (with {len(quality_warnings)} quality warnings).")
        sys.exit(0)

def check_quality_signals(path: Path) -> List[str]:
    """Check for optional quality signals."""
    signals = []
    try:
        post = frontmatter.load(path)
        content = post.content
        
        # 1. Level checking
        if "level" not in post.metadata:
            signals.append("Missing 'level' metadata (beginner|intermediate|advanced)")
            
        # 2. Tags checking
        if "tags" not in post.metadata or not isinstance(post.metadata["tags"], list):
            signals.append("Missing or invalid 'tags' metadata")
            
        # 3. Examples check (heuristic: code blocks)
        if "```" not in content and "Example" not in content:
            signals.append("No examples found (code blocks or 'Example' header)")
            
        # 4. Related links check
        if "codex:" not in content and "related" not in post.metadata:
             signals.append("No related terms found (links or 'related' metadata)")

    except Exception as e:
        signals.append(f"Error checking quality: {e}")
        
    return signals

if __name__ == "__main__":
    main()
