import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.audit_objectives_schema import audit_all_quests

def backfill_objectives_legacy():
    print("🛠️ Backfilling Legacy Objectives...")
    
    report = audit_all_quests()
    invalid_quests = report['invalid_quests']
    
    print(f"Found {len(invalid_quests)} invalid quests to fix.")
    
    fixed_count = 0
    errors = []
    
    for q_record in invalid_quests:
        slug = q_record['slug']
        json_path = Path(f"docs/quests/{slug}/quest.json")
        
        if not json_path.exists():
            print(f"[WARN] Quest config not found for {slug} at {json_path}")
            errors.append(slug)
            continue
            
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            objs = data.get("objectives", [])
            new_objs = []
            modified = False
            
            # Determine strategy
            grading_mode = data.get("grading", {}).get("mode", "unknown")
            
            for obj in objs:
                # Check if invalid
                # Logic: missing kind, or kind not in VALIDATORS (we assume VALIDATORS logic from audit)
                # But here we just check if it LOOKS legacy.
                
                is_legacy = False
                if "kind" not in obj:
                    is_legacy = True
                elif obj["kind"] == "obj_default": # explicitly named legacy kind? no, usually id is obj_default
                     is_legacy = True
                
                if not is_legacy and obj.get("id") == "obj_default":
                    is_legacy = True

                if is_legacy:
                    modified = True
                    # Strategy
                    if grading_mode == "tests":
                        new_objs.append({
                            "id": "tests_pass",
                            "kind": "tests_pass",
                            "title": "Pass all tests",
                            "rule": {
                                "kind": "tests_pass"
                            }
                        })
                    else:
                        # Fallback: exit_code_zero
                        # We can try to be smarter, but safer is better.
                        # Maybe stdout? "Complete the assignment..." usually implies running something.
                        # But exit_code_zero is the minimal "it runs" check.
                        new_objs.append({
                            "id": "run_success",
                            "kind": "exit_code_zero",
                            "title": "Execute successfully",
                            "rule": {
                                "kind": "exit_code_zero"
                            }
                        })
                else:
                    # Keep valid object
                    new_objs.append(obj)
            
            if modified:
                data["objectives"] = new_objs
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print(f"✅ Fixed {slug} (Strategy: {grading_mode})")
                fixed_count += 1
            else:
                print(f"⚠️ {slug} marked invalid but no legacy objectives found/modified?")
                
        except Exception as e:
            print(f"❌ Error fixing {slug}: {e}")
            errors.append(slug)

    print(f"\nSummary: Fixed {fixed_count}/{len(invalid_quests)}")
    
    # Write report
    with open("docs/audits/LEGACY_OBJECTIVES_BACKFILL_REPORT.md", "w", encoding="utf-8") as f:
        f.write(f"# Legacy Objectives Backfill Report\n\nFixed: {fixed_count}\nErrors: {len(errors)}\n")

if __name__ == "__main__":
    backfill_objectives_legacy()
