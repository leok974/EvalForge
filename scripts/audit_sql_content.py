import os
import sys
import json

def get_tier1_slugs():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sql_core_path = os.path.join(root, "data", "questpacks", "sql_core.json")
    try:
        with open(sql_core_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [q["slug"] for q in data.get("quests", []) if q.get("tier") == 1]
    except Exception as e:
        print(f"Failed to read sql_core.json: {e}", file=sys.stderr)
        return []

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_dir = os.path.join(root_dir, "docs", "quests")
    
    if not os.path.exists(docs_dir):
        print("Error: docs/quests directory not found.")
        sys.exit(1)
        
    # Get all SQL quests
    sql_quests = [d for d in os.listdir(docs_dir) if d.startswith("sql-") and os.path.isdir(os.path.join(docs_dir, d))]
    tier1_slugs = get_tier1_slugs()
    
    missing_content = {}
    
    required_files = ["tutorial.md", "briefing.md", "hints.md", "lore.md"]
    placeholder_keywords = ["todo", "placeholder", "tbd", "[insert", "test data"]
    
    for slug in sql_quests:
        quest_dir = os.path.join(docs_dir, slug)
            
        missing = []
        has_placeholder = []
        
        for rf in required_files:
            file_path = os.path.join(quest_dir, rf)
            if not os.path.exists(file_path):
                missing.append(rf)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    
                    # Strip out basic markdown headers and whitespace to check true length
                    import re
                    content_clean = re.sub(r'#.*?\n', '', content)
                    content_clean = re.sub(r'<!--.*?-->', '', content_clean, flags=re.DOTALL)
                    content_clean = content_clean.strip()
                    
                    if any(kw in content for kw in placeholder_keywords) or len(content_clean) < 20:
                        has_placeholder.append(rf)
                        
        if missing or has_placeholder:
            missing_content[slug] = {"missing": missing, "placeholders": has_placeholder}
            
    print(f"--- SQL Content Audit (Total SQL Quests: {len(sql_quests)}) ---")
    
    tier1_fails = 0
    
    for slug, issues in missing_content.items():
        is_tier1 = slug in tier1_slugs
        prefix = "🚨 TIER 1 FAILURE: " if is_tier1 else "⚠️ "
        print(f"{prefix}{slug}:")
        if issues["missing"]:
            print(f"   Missing: {', '.join(issues['missing'])}")
        if issues["placeholders"]:
            print(f"   Placeholder content: {', '.join(issues['placeholders'])}")
            
        if is_tier1:
            tier1_fails += 1
            
    # Ratchet Target: No placeholder content in SQL Tier-1
    if tier1_fails > 0:
        print(f"\n❌ Audit Failed: Ratchet target exceeded. {tier1_fails} Tier-1 SQL quests have missing or placeholder content.")
        sys.exit(1)
    else:
        print("\n✅ Ratchet Check Passed: All Tier-1 SQL quests are fully materialized.")
        sys.exit(0)

if __name__ == "__main__":
    main()
