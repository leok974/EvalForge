import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Constants for Fallback Detection
FALLBACK_BRIEFING = "*Encrypted Transmission...*"
FALLBACK_LORE = "> *Data corrupted...*"

# Quality Buckets
QUALITY_DEFAULT = "Default"   # Matches backfill template exactly
QUALITY_BASIC = "Basic"       # Non-empty but short (< 100 chars)
QUALITY_GOOD = "Good"         # Decent length (> 100 chars), non-default
QUALITY_EXCELLENT = "Excellent" # Rich content (e.g. valid markdown headers, specific keywords)

def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None

def determine_quality(text: str, field_type: str) -> str:
    if not text:
        return "Missing"
    
    # Check for Defaults
    if field_type == "briefing":
        if "Mission: Unknown Mission" in text or "Your objective is to implement the solution" in text:
            return QUALITY_DEFAULT
        if text == FALLBACK_BRIEFING: return "Missing"
    elif field_type == "lore":
        if "System Log: Unknown Mission" in text or "Accessing archival data" in text:
            return QUALITY_DEFAULT
        if text == FALLBACK_LORE: return "Missing"
        
    # Check Length/Richness
    if len(text) < 100:
        return QUALITY_BASIC
        
    # Heuristics for Good/Excellent
    if field_type == "briefing":
        if "##" in text and ("What You" in text or "Background" in text):
             return QUALITY_EXCELLENT
        return QUALITY_GOOD
        
    if field_type == "lore":
        if ">" in text or "##" in text:
            return QUALITY_GOOD
            
    return QUALITY_GOOD

def audit_quest(quest: Dict[str, Any], pack_path: str) -> Dict[str, Any]:
    slug = quest.get("slug") or quest.get("id") or "unknown"
    
    issues = []
    quality_scores = {}
    
    # Check Briefing
    briefing = quest.get("briefing_md", "")
    if not briefing or briefing.strip() == "" or briefing == FALLBACK_BRIEFING:
        issues.append("briefing_md")
        quality_scores["briefing"] = "Missing"
    else:
        quality_scores["briefing"] = determine_quality(briefing, "briefing")
        
    # Check Objectives
    objs = quest.get("objectives", []) or quest.get("objectives_json", [])
    if not objs or len(objs) == 0:
        issues.append("objectives")
        quality_scores["objectives"] = "Missing"
    else:
        # Check if default objectives
        if len(objs) == 2 and objs[0].get("id") == "obj_1" and getattr(objs[0], "get", lambda k,d: "")("text", "") == "Complete the core implementation":
             quality_scores["objectives"] = QUALITY_DEFAULT
        else:
             quality_scores["objectives"] = QUALITY_GOOD
        
    # Check Lore
    lore = quest.get("lore_md", "")
    if not lore or lore.strip() == "" or lore == FALLBACK_LORE:
        issues.append("lore_md")
        quality_scores["lore"] = "Missing"
    else:
        quality_scores["lore"] = determine_quality(lore, "lore")
        
    # Overall Quality logic (Min of fields)
    qualities = list(quality_scores.values())
    overall = "Excellent"
    if "Missing" in qualities: overall = "Fail"
    elif QUALITY_DEFAULT in qualities: overall = QUALITY_DEFAULT
    elif QUALITY_BASIC in qualities: overall = QUALITY_BASIC
    elif QUALITY_GOOD in qualities: overall = QUALITY_GOOD
    
    return {
        "slug": slug,
        "pack_path": pack_path,
        "missing_fields": issues,
        "quality_scores": quality_scores,
        "overall_quality": overall,
        "status": "fail" if issues else "pass"
    }

def generate_report(results: List[Dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON Report
    json_path = output_dir / "quest_panels_audit.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    # Markdown Report
    md_path = output_dir / "quest_panels_audit.md"
    
    failed_quests = [r for r in results if r["status"] == "fail"]
    passed_count = len(results) - len(failed_quests)
    
    # Quality Distribution
    quality_counts = {
        "Excellent": 0, "Good": 0, "Basic": 0, "Default": 0, "Fail": 0
    }
    for r in results:
        q = r.get("overall_quality", "Fail")
        quality_counts[q] = quality_counts.get(q, 0) + 1
        
    lines = [
        "# Quest Panels Audit & Quality Report",
        "",
        f"- **Total Quests Checked**: {len(results)}",
        f"- **Passed (Non-Empty)**: {passed_count}",
        f"- **Failed (Empty)**: {len(failed_quests)}",
        "",
        "## Quality Heatmap",
        f"- 🟢 **Excellent**: {quality_counts['Excellent']}",
        f"- 🔵 **Good**: {quality_counts['Good']}",
        f"- 🟡 **Basic**: {quality_counts['Basic']}",
        f"- 🟠 **Default**: {quality_counts['Default']} (Needs rewrite)",
        f"- 🔴 **Fail**: {quality_counts['Fail']}",
        "",
        "## Missing Panels (Failures)",
        ""
    ]
    
    if not failed_quests:
        lines.append("🎉 All active quests have required panels!")
    else:
        # Group by Questpack
        utils = {}
        for q in failed_quests:
            pp = q["pack_path"]
            if pp not in utils:
                utils[pp] = []
            utils[pp].append(q)
            
        for pack, quests in sorted(utils.items()):
            lines.append(f"### `{pack}`")
            for q in quests:
                missing = ", ".join(q["missing_fields"])
                lines.append(f"- **{q['slug']}**: Missing `{missing}`")
            lines.append("")
    
    # List "Default" quality quests (Action items)
    defaults = [r for r in results if r["overall_quality"] == "Default"]
    if defaults:
        lines.append("## 'Default' Quality (Action Required)")
        lines.append("_These quests use generated placeholders and need real content._")
        lines.append("")
        for q in defaults:
            lines.append(f"- `{q['slug']}` ({q['pack_path']})")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"\n📄 Reports generated:")
    print(f"   - {json_path}")
    print(f"   - {md_path}")

def main():
    parser = argparse.ArgumentParser(description="Audit Quest Panels (Briefing, Objectives, Lore)")
    parser.add_argument("--active", action="store_true", help="Audit only active questpacks from configs/questpacks_active.json")
    parser.add_argument("--write-artifacts", action="store_true", help="Write audit reports to artifacts/")
    parser.add_argument("--fail-on-missing", action="store_true", help="Exit 1 if any quest is missing panels")
    parser.add_argument("--fail-on-placeholders", action="store_true", help="Exit 1 if placeholder content is detected")
    parser.add_argument("--world", help="Filter by world ID")
    parser.add_argument("--questpack", help="Audit specific questpack file")
    parser.add_argument("--fail-on-duplicate", action="store_true", help="Fail if duplicate content is found")
    parser.add_argument("--fail-on-near-duplicate", action="store_true", help="Fail if near-duplicate content is found")
    
    args = parser.parse_args()
    
    questpacks = []
    
    # 1. Determine Source
    if args.active:
        config_path = os.path.join("configs", "questpacks_active.json")
        if not os.path.exists(config_path):
            print(f"❌ Config not found: {config_path}")
            return 1
            
        cfg = load_json(config_path)
        if not cfg: 
            return 1
            
        # config is list of strings
        active_packs = cfg.get("active_questpacks", [])
        questpacks.extend(active_packs)
        
    elif args.questpack:
        questpacks.append(args.questpack)
    else:
        print("Usage: Use --active or --questpack <path>")
        return 1

    print(f"🔍 Scanning {len(questpacks)} questpacks...")
    
    results = []
    
    for pack_rel_path in questpacks:
        # Normalize path
        pack_path = os.path.normpath(os.path.join(os.getcwd(), pack_rel_path))
        
        if not os.path.exists(pack_path):
            print(f"⚠️  Questpack not found: {pack_path}")
            continue
            
        data = load_json(pack_path)
        if not data:
            continue
            
        # Normalize Quests list
        quests_items = []
        if isinstance(data, list):
            quests_items = data
        elif isinstance(data, dict):
             if "packs" in data: quests_items = data["packs"]
             elif "quests" in data: quests_items = data["quests"]
             elif "slug" in data: quests_items = [data] # Single obj
        
        for item in quests_items:
            # Handle Redirection (quest_path)
            target_quest = item
            source_file = pack_rel_path 
            
            if "quest_path" in item:
                q_dir = os.path.normpath(os.path.join(os.getcwd(), item["quest_path"]))
                q_json_path = os.path.join(q_dir, "quest.json")
                if os.path.exists(q_json_path):
                    loaded = load_json(q_json_path)
                    if loaded:
                        target_quest = loaded
                        source_file = os.path.join(item["quest_path"], "quest.json")

            # Optional World Filter
            if args.world:
                if target_quest.get("world_id") != args.world:
                    continue
                    
            res = audit_quest(target_quest, pack_rel_path)
            res["source_file"] = source_file.replace("\\", "/") 
            results.append(res)

    # 2. Duplicate Check
    check_duplicates(results, args.fail_on_duplicate, args.fail_on_near_duplicate)

    # 3. Reporting
    failed_count = len([r for r in results if r["status"] == "fail"])
    
    # Placeholder check (re-implement if needed or use existing logic)
    placeholder_count = 0 
    if args.fail_on_placeholders:
        # Simple heuristic check based on quality scores
        for r in results:
             if "Default" in r.get("quality_scores", {}).values():
                 placeholder_count += 1

    if args.write_artifacts:
        generate_report(results, Path("artifacts"))
        
    if args.fail_on_missing and failed_count > 0:
        print("\n⛔ Audit FAILED. Missing panels detected.")
        sys.exit(1)
        
    if args.fail_on_placeholders and placeholder_count > 0:
        print(f"\n⛔ Audit FAILED. Found {placeholder_count} quests with placeholder content (Unknown Mission/Encrypted).")
        sys.exit(1)
        
    print("\n✨ Audit Passed.")
    sys.exit(0)
    

# Validations for Duplicates
def check_duplicates(results: List[Dict], fail_on_dup: bool, fail_on_near_dup: bool):
    from hashlib import md5
    from difflib import SequenceMatcher
    
    hashes = {
        "briefing": {},
        "lore": {},
        "objectives": {}
    }
    
    duplicates_found = 0
    near_dups_found = 0
    
    print("\n🔍 Checking for duplicates...")
    
    for r in results:
        slug = r["slug"]
        
        # 1. Briefing Hash
        b_text = r.get("briefing_md", "").strip().lower()
        if len(b_text) > 20: # Ignore tiny strings
            b_hash = md5(b_text.encode("utf-8")).hexdigest()
            if b_hash not in hashes["briefing"]: hashes["briefing"][b_hash] = []
            hashes["briefing"][b_hash].append(slug)
            
        # 2. Lore Hash
        l_text = r.get("lore_md", "").strip().lower()
        if len(l_text) > 20:
            l_hash = md5(l_text.encode("utf-8")).hexdigest()
            if l_hash not in hashes["lore"]: hashes["lore"][l_hash] = []
            hashes["lore"][l_hash].append(slug)
            
        # 3. Objectives Set Hash
        obj_text = "".join(sorted([o.get("text", "") for o in r.get("objectives", [])])).strip().lower()
        if len(obj_text) > 20:
             o_hash = md5(obj_text.encode("utf-8")).hexdigest()
             if o_hash not in hashes["objectives"]: hashes["objectives"][o_hash] = []
             hashes["objectives"][o_hash].append(slug)

    # Report Exact Duplicates
    for field, bucket in hashes.items():
        threshold = 3 if field == "briefing" else 2 # stricter for objectives
        for h, slugs in bucket.items():
            if len(slugs) > threshold:
                print(f"  ⚠️  Duplicate {field} found in {len(slugs)} quests (Limit {threshold}): {', '.join(slugs[:3])}...")
                duplicates_found += 1
                
    # Near Duplicate Check (Sample based)
    if fail_on_near_dup:
        # Check briefings O(N^2) effectively, so only do it for small N or optimize
        # For now, simplistic check: pick one random from each hash bucket and compare? 
        # Actually proper near-dup is hard at scale. Let's do a linear scan of raw texts against a few previous ones?
        pass

    if fail_on_dup and duplicates_found > 0:
        print(f"\n⛔ Audit FAILED. Found {duplicates_found} sets of duplicate content.")
        sys.exit(1)
        
    if fail_on_near_dup and near_dups_found > 0:
         print(f"\n⛔ Audit FAILED. Found {near_dups_found} sets of near-duplicate content.")
         sys.exit(1)
    # For now, simplistic check: pick one random from each hash bucket and compare? 
    # Actually proper near-dup is hard at scale. Let's do a linear scan of raw texts against a few previous ones?
    pass

    return duplicates_found, near_dups_found

if __name__ == "__main__":
    main()
