import libcst as cst
from libcst import matchers as m
import json
from pathlib import Path
import sys

def create_objective_dict(id, title, kind, rule):
    """Create a CST Dict for an objective."""
    elements = [
        cst.DictElement(cst.SimpleString(f"'{k}'"), cst.SimpleString(repr(v)))
        for k, v in [("id", id), ("title", title), ("kind", kind)]
    ]
    
    # Rule is a nested dict
    rule_elements = []
    for k, v in rule.items():
        # Handle list values
        if isinstance(v, list):
            # We assume list of strings for now
            list_elements = [cst.Element(cst.SimpleString(repr(x))) for x in v]
            val_node = cst.List(elements=list_elements)
        elif isinstance(v, int):
            val_node = cst.Integer(str(v))
        else:
            val_node = cst.SimpleString(repr(v))
            
        rule_elements.append(cst.DictElement(cst.SimpleString(f"'{k}'"), val_node))
        
    elements.append(cst.DictElement(cst.SimpleString("'rule'"), cst.Dict(elements=rule_elements)))
    
    return cst.Dict(elements=elements)

class StateObjectiveTransformer(cst.CSTTransformer):
    def __init__(self, golden_map):
        self.golden_map = golden_map
        self.current_slug = None
        self.quest_depth = 0
        self.in_list = False
        self.modified_count = 0

    def visit_Assign(self, node: cst.Assign):
        if len(node.targets) == 1 and m.matches(node.targets[0].target, m.Name("STANDARD_QUESTLINES")):
            self.in_list = True
        return True
        
    def visit_AnnAssign(self, node: cst.AnnAssign):
        if m.matches(node.target, m.Name("STANDARD_QUESTLINES")):
            self.in_list = True
        return True

    def leave_Dict(self, original_node, updated_node):
        if not self.in_list:
            return updated_node

        # Identify slug
        slug = None
        for element in original_node.elements:
            if isinstance(element, cst.DictElement) and m.matches(element.key, m.SimpleString()):
                key = element.key.value.strip("'\"")
                if key == "slug" and m.matches(element.value, m.SimpleString()):
                    slug = element.value.value.strip("'\"")
                    break
        
        if not slug or slug not in self.golden_map:
            return updated_node

        state = self.golden_map[slug]
        # Only process if state is captured
        if state.get("type") != "state":
            return updated_node

        # We found a quest with golden state!
        # Find 'objectives' key
        obj_element_index = -1
        obj_list_node = None
        
        new_elements = list(updated_node.elements)
        
        for i, el in enumerate(new_elements):
            if isinstance(el, cst.DictElement) and m.matches(el.key, m.SimpleString()):
                key = el.key.value.strip("'\"")
                if key == "objectives_json": # key in seed file
                    obj_element_index = i
                    obj_list_node = el.value
                    break
        
        if obj_element_index == -1:
            print(f"⚠️ [{slug}] No 'objectives_json' key found. Skipping.")
            return updated_node
            
        if not isinstance(obj_list_node, cst.List):
             print(f"⚠️ [{slug}] 'objectives_json' is not a List. Skipping.")
             return updated_node
             
        # Generate new objectives
        existing_ids = set()
        for el in obj_list_node.elements:
             if isinstance(el.value, cst.Dict):
                 for field in el.value.elements:
                     if m.matches(field.key, m.SimpleString("'id'")):
                         existing_ids.add(field.value.value.strip("'\""))

        new_objs = []
        
        # 1. FS Snapshot
        files = state.get("files", [])
        if files and "fs_snapshot" not in existing_ids:
            # Filter? Maybe just all files for now.
            # Avoid huge lists?
            new_objs.append(create_objective_dict(
                "fs_snapshot", 
                "Verify file structure", 
                "fs_snapshot", 
                {"must_exist": files}
            ))

        # 2. Git Status
        git_info = state.get("git", {})
        if git_info.get("has_dot_git"):
             if "git_status_clean" not in existing_ids:
                 status = git_info.get("status_porcelain", "").strip()
                 new_objs.append(create_objective_dict(
                     "git_status_clean",
                     "Verify git status",
                     "git_status_clean",
                     {"expected_porcelain": status}
                 ))
                 
             if "git_log_contains" not in existing_ids:
                 logs = git_info.get("log_oneline", [])
                 if logs:
                     # Just check first commit?
                     # Or check "Initial commit" if present
                     targets = []
                     for l in logs:
                         if "Initial" in l or "init" in l.lower():
                             targets.append(l)
                             
                     if not targets and logs:
                         targets.append(logs[-1]) # Oldest? or newest? logs[0] is newest usually.
                         
                     if targets:
                         new_objs.append(create_objective_dict(
                             "git_log_contains",
                             "Verify commit history",
                             "git_log_contains",
                             {"must_contain": targets, "min_commits": 1}
                         ))

        if not new_objs:
            return updated_node
            
        print(f" [UPDATED] [{slug}] Adding {len(new_objs)} state objectives.")
        self.modified_count += 1
        
        # Append to list
        new_list_elements = list(obj_list_node.elements)
        for obj in new_objs:
            new_list_elements.append(cst.Element(obj))
            
        new_obj_list = obj_list_node.with_changes(elements=new_list_elements)
        
        # Update dict element
        new_elements[obj_element_index] = new_elements[obj_element_index].with_changes(value=new_obj_list)
        
        return updated_node.with_changes(elements=new_elements)

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Run in drift detection mode (fail if changes needed)")
    args = parser.parse_args()
    
    print("LibCST State Objective Injector" + (" [DRIFT DETECTION]" if args.check else ""))
    
    has_drift = False
    
    # ... (loading logic same)
    
    # 1. Load Golden State
    golden_map = {}
    quests_dir = Path("data/quests")
    for q_dir in quests_dir.iterdir():
        state_path = q_dir / "grading" / "golden.state.json"
        
        if state_path.exists():
            try:
                with open(state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("type") == "state":
                        golden_map[q_dir.name] = data
            except Exception as e:
                print(f"Error loading {state_path}: {e}")

    print(f"loaded {len(golden_map)} golden states.")

    # 2. Parse Source
    source_path = Path("arcade_app/seed_quests_standard_worlds.py")
    with open(source_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = cst.parse_module(source_code)
    
    # 3. Transform
    transformer = StateObjectiveTransformer(golden_map)
    modified_tree = tree.visit(transformer)
    
    # 4. Save or Report (Seed File)
    if transformer.modified_count > 0:
        if args.check:
            print(f"[FAIL] DRIFT DETECTED (Seed): {transformer.modified_count} quests need objective updates.")
            has_drift = True
        else:
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(modified_tree.code)
            print(f"[OK] Updated {transformer.modified_count} quests in {source_path}")
            
    # 5. Process JSON files in docs/quests (for quests not in seed file, or generally)
    # We iterate ALL golden maps, if we find matching docs/quests JSON, we update it.
    
    json_drift_count = 0
    json_updated_count = 0
    
    for slug, golden_data in golden_map.items():
        # Check if json exists
        json_path = Path(f"docs/quests/{slug}/quest.json")
        if not json_path.exists():
            continue
            
        # We found a quest.json and we have golden state.
        # Let's see if we need to inject objectives.
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                quest_data = json.load(f)
                
            # Generate expected objectives
            new_objectives = []
            
            # fs_snapshot
            if golden_data.get("files"):
                 # Filter out hidden/system files if needed
                 files = [f for f in golden_data["files"] if not f.startswith(".")]
                 if files:
                     new_objectives.append({
                         "id": "fs_snapshot",
                         "kind": "fs_snapshot",
                         "title": "Verify file structure",
                         "rule": {
                             "kind": "fs_snapshot",
                             "must_exist": files
                         }
                     })
                     
            # git_status_clean
            if "git" in golden_data and "status_porcelain" in golden_data["git"]:
                # If clean, enforce clean. If dirty, enforce specific dirty?
                # For now, if clean, enforce clean.
                status = golden_data["git"]["status_porcelain"]
                if not status: # Clean
                     new_objectives.append({
                         "id": "git_status_clean",
                         "kind": "git_status_clean",
                         "title": "Clean git status",
                         "rule": {
                             "kind": "git_status_clean",
                             "expected_porcelain": ""
                         }
                     })
            
            # git_log_contains
            if "git" in golden_data and "log_oneline" in golden_data["git"]:
                logs = golden_data["git"]["log_oneline"]
                if logs:
                    # Simple heuristic: require first commit message
                    first_msg = logs[-1].split(" ", 1)[-1] # oldest commit
                    new_objectives.append({
                         "id": "git_log_contains",
                         "kind": "git_log_contains",
                         "title": "Verify commit history",
                         "rule": {
                             "kind": "git_log_contains",
                             "must_contain": [first_msg],
                             "min_commits": 1
                         }
                    })

            if not new_objectives:
                continue

            # Compare with existing
            # We look for objectives with same ID and content
            # Or just check if they exist.
            # Simplified: If we have new objectives, and they aren't in current, add them.
            # THIS IS A NAIVE IMPLEMENTATION. It appends if missing.
            
            current_objs = quest_data.get("objectives", [])
            # Map by ID
            current_map = {o["id"]: o for o in current_objs}
            
            modified = False
            for new_obj in new_objectives:
                if new_obj["id"] not in current_map:
                    current_objs.append(new_obj)
                    modified = True
                else:
                    # Update existing?
                    # For now, let's just check existence to avoid overwriting custom tweaks
                    pass
            
            if modified:
                if args.check:
                     print(f"[FAIL] DRIFT DETECTED (JSON): {slug} needs objective updates.")
                     json_drift_count += 1
                     has_drift = True
                else:
                     quest_data["objectives"] = current_objs
                     with open(json_path, "w", encoding="utf-8") as f:
                         json.dump(quest_data, f, indent=4)
                     json_updated_count += 1
                     print(f"[OK] Updated {slug} in {json_path}")

        except Exception as e:
            print(f"[WARN] Error processing {json_path}: {e}")

    if has_drift:
        print("Run 'python scripts/upgrade_objectives_state.py' to fix.")
        sys.exit(1)

    if transformer.modified_count == 0 and json_updated_count == 0:
        print("[OK] No changes needed. Objectives match golden state.")
        sys.exit(0)

if __name__ == "__main__":
    main()
