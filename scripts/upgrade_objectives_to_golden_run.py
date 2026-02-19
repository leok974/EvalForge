import yaml
import json
import sys
from pathlib import Path

# Try to use LibYAML for speed, but fallback to Python implementation
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def upgrade_objectives(target_slug=None):
    print("🚀 Starting Objective Upgrade to Golden Run...")
    quests_dir = Path("data/quests")
    
    upgraded_count = 0
    skipped_count = 0
    
    for q_dir in quests_dir.iterdir():
        if not q_dir.is_dir():
            continue
            
        if target_slug and q_dir.name != target_slug:
            continue
            
        golden_path = q_dir / "grading" / "golden.run.json"
        quest_yaml_path = q_dir / "quest.yaml"
        
        # Only process if we have a golden run capture AND a quest definition
        if not golden_path.exists():
            continue
            
        if not quest_yaml_path.exists():
            print(f"⚠️  {q_dir.name}: Has golden.run.json but missing quest.yaml")
            continue
            
        # Load Golden Data
        try:
            with open(golden_path, "r", encoding="utf-8") as f:
                golden = json.load(f)
            golden_stdout = golden.get("stdout", "")
        except Exception as e:
            print(f"❌ {q_dir.name}: Failed to load golden run: {e}")
            continue
            
        # Load Quest YAML
        try:
            with open(quest_yaml_path, "r", encoding="utf-8") as f:
                quest_data = yaml.load(f, Loader=Loader)
        except Exception as e:
            print(f"❌ {q_dir.name}: Failed to load quest.yaml: {e}")
            continue
            
        if not quest_data or "objectives" not in quest_data:
            print(f"ℹ️  {q_dir.name}: No objectives found.")
            continue
            
        updated = False
        objectives = quest_data["objectives"]
        
        for obj in objectives:
            kind = obj.get("kind")
            
            # Target stdout-related rules
            if kind in ["stdout_exact", "stdout_regex", "stdout_match"]:
                current_expected = obj.get("expected")
                current_pattern = obj.get("pattern")
                
                # Check if update is needed
                # If we convert regex to exact, we effectively "freeze" the output
                if kind != "stdout_exact" or current_expected != golden_stdout:
                    
                    print(f"   [{q_dir.name}] Converting '{kind}' -> 'stdout_exact'")
                    if len(golden_stdout) < 50:
                        print(f"   Value: {repr(golden_stdout)}")
                    else:
                        print(f"   Value: {len(golden_stdout)} bytes")
                        
                    obj["kind"] = "stdout_exact"
                    obj["expected"] = golden_stdout
                    
                    # Clean up regex fields if present
                    if "pattern" in obj:
                        del obj["pattern"]
                        
                    updated = True
        
        if updated:
            try:
                with open(quest_yaml_path, "w", encoding="utf-8") as f:
                    yaml.dump(quest_data, f, Dumper=Dumper, sort_keys=False, default_flow_style=False)
                print(f"✅ Saved updates to {q_dir.name}/quest.yaml")
                upgraded_count += 1
            except Exception as e:
                print(f"❌ Failed to save {q_dir.name}: {e}")
        else:
            # print(f"⏹️  {q_dir.name}: Already up to date.")
            skipped_count += 1
            
    print(f"\nSummary: {upgraded_count} quests upgraded, {skipped_count} skipped/unchanged.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Limit to specific quest slug")
    args = parser.parse_args()
    
    upgrade_objectives(args.slug)
