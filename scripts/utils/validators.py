
import os
import json
import re

def validate_tutorial_structure(quest_path):
    """Checks if tutorial.md exists and has required sections."""
    tut_path = os.path.join(quest_path, "tutorial.md")
    if not os.path.exists(tut_path):
        return ["Missing tutorial.md"]
        
    try:
        with open(tut_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read tutorial.md: {e}"]
        
    errors = []
    if len(content.strip()) < 50:
        errors.append("tutorial.md is too short (<50 chars)")
        
    # Phase 9.3: Support both Scaffolder (V1) and Refined (V2) templates
    headers_v1 = ["# Mission Briefing", "## 1. The Concept", "## 2. Key Term:", "## 3. The Details"]
    headers_v2 = ["## Outcome", "## Concept in 30 seconds", "## Key terms", "## Walkthrough", "## Example implementation", "## Common mistakes", "## Check yourself"]
    
    has_v1 = all(h in content for h in headers_v1)
    has_v2 = all(h in content for h in headers_v2)
    
    if not has_v1 and not has_v2:
        # Report which one was closer or just default to V1 missing
        # If it has 'Outcome', report V2 missing
        if "## Outcome" in content:
             for h in headers_v2:
                 if h not in content: errors.append(f"Refined tutorial.md missing header: '{h}'")
        else:
             for h in headers_v1:
                 if h not in content: errors.append(f"tutorial.md missing header: '{h}'")
            
    return errors

def validate_terms_schema(quest_path):
    """Checks if terms.json exists and is valid."""
    terms_path = os.path.join(quest_path, "terms.json")
    if not os.path.exists(terms_path):
        return ["Missing terms.json"]
        
    try:
        with open(terms_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON in terms.json: {e}"]
        
    if not isinstance(data, list):
         return ["terms.json must be a list"]
         
    errors = []
    for idx, item in enumerate(data):
        if "term" not in item:
            errors.append(f"Item {idx} missing 'term' field")
        if "definition" not in item:
             errors.append(f"Item {idx} missing 'definition' field")
        if "codex_ref" not in item:
             errors.append(f"Item {idx} missing 'codex_ref' field")
        elif not item["codex_ref"].startswith("codex:glossary/"):
             errors.append(f"Item {idx} 'codex_ref' must start with 'codex:glossary/'")
             
    return errors

def validate_codex_links(quest_path, root_dir):
    """Checks if Codex references in terms.json point to real files."""
    terms_path = os.path.join(quest_path, "terms.json")
    if not os.path.exists(terms_path):
        return [] # validate_terms_schema catches this
        
    try:
        with open(terms_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return []

    errors = []
    for idx, item in enumerate(data):
        ref = item.get("codex_ref", "")
        if not ref.startswith("codex:glossary/"): 
            continue
            
        # Ref format: codex:glossary/{world}/{term}
        # File path: data/codex/glossary/{world}/{term}.md
        
        parts = ref.replace("codex:glossary/", "").split("/")
        if len(parts) < 2:
            errors.append(f"Invalid reference format: {ref}")
            continue
            
        rel_path = os.path.join("data", "codex", "glossary", *parts) + ".md"
        abs_path = os.path.join(root_dir, rel_path)
        
        if not os.path.exists(abs_path):
            errors.append(f"Broken Codex Link: {ref} -> {rel_path} not found")
            
    return errors

def validate_tutorial_strict(quest_path, min_terms=2, require_example=True, allow_placeholders=False):
    """Strict validation for Starter Quests."""
    errors = validate_tutorial_structure(quest_path)
    if "Missing tutorial.md" in errors:
        return ["CRITICAL: Starter Quest MUST have tutorial.md"]
        
    term_errors = validate_terms_schema(quest_path)
    if "Missing terms.json" in term_errors:
        errors.append("CRITICAL: Starter Quest MUST have terms.json")
    else:
        errors.extend(term_errors)
        # Check count
        try:
             with open(os.path.join(quest_path, "terms.json"), "r") as f:
                 data = json.load(f)
                 if len(data) < min_terms:
                     errors.append(f"Starter Quest needs at least {min_terms} terms (found {len(data)})")
        except: pass
        
    # Check Example Implementation
    if require_example:
        tut_path = os.path.join(quest_path, "tutorial.md")
        if os.path.exists(tut_path):
            with open(tut_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "```" not in content:
                    errors.append("Starter Quest tutorial missing code example (```)")
                
                # Refinement Rubric Check (Warn on TODOs)
                if "TODO" in content:
                    if not allow_placeholders:
                         errors.append("POLICY: Tutorial contains 'TODO' placeholder (Not allowed in Tier-1)")
                    else:
                         errors.append("WARNING: Tutorial contains 'TODO' placeholder")

    return errors

def find_codex_orphans(root_dir, active_refs):
    """Finds Codex pages not referenced by any quest."""
    codex_root = os.path.join(root_dir, "data", "codex", "glossary")
    all_pages = []
    
    if not os.path.exists(codex_root):
        return []

    for r, _, files in os.walk(codex_root):
        for f in files:
            if f.endswith(".md"):
                # Use os.sep to handle windows backslashes correctly
                rel = os.path.relpath(os.path.join(r, f), codex_root)
                slug = rel.replace(os.sep, "/").replace(".md", "")
                ref = f"codex:glossary/{slug}"
                all_pages.append(ref)
                
    orphans = set(all_pages) - set(active_refs)
    return list(orphans)
