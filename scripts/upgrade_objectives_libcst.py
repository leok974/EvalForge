import libcst as cst
from libcst import matchers as m
import json
from pathlib import Path
import sys

class ObjectiveTransformer(cst.CSTTransformer):
    def __init__(self, golden_map):
        self.golden_map = golden_map
        self.current_slug = None
        self.in_list_of_quests = False
        self.upgraded_count = 0
        self.quest_depth = 0

    def visit_Assign(self, node: cst.Assign):
        if len(node.targets) == 1 and m.matches(node.targets[0].target, m.Name("STANDARD_QUESTLINES")):
            print("Found STANDARD_QUESTLINES assign!")
            self.in_list_of_quests = True
        return True

    def visit_AnnAssign(self, node: cst.AnnAssign):
        if m.matches(node.target, m.Name("STANDARD_QUESTLINES")):
            print("Found STANDARD_QUESTLINES AnnAssign!")
            self.in_list_of_quests = True
        return True

    def leave_AnnAssign(self, original_node, updated_node):
        if self.in_list_of_quests:
            self.in_list_of_quests = False
        return updated_node

    def leave_Assign(self, original_node, updated_node):
        if self.in_list_of_quests:
            self.in_list_of_quests = False
        return updated_node

    def visit_Dict(self, node: cst.Dict):
        if not self.in_list_of_quests:
            return True
            
        # Try to identify if this is a QUEST dict (has 'slug')
        slug = None
        for element in node.elements:
            if isinstance(element, cst.DictElement) and m.matches(element.key, m.SimpleString()):
                key = element.key.value.strip("'\"")
                if key == "slug":
                    if m.matches(element.value, m.SimpleString()):
                        slug = element.value.value.strip("'\"")
                        break
        
        if slug:
            print(f"Entering Quest: {slug}")
            self.current_slug = slug
            self.quest_depth = 0 # Reset depth tracking relative to quest dict
        
        if self.current_slug:
            self.quest_depth += 1
            
        return True

    def leave_Dict(self, original_node, updated_node):
        if self.current_slug:
            self.quest_depth -= 1
            if self.quest_depth == 0:
                self.current_slug = None
        return updated_node

    def leave_DictElement(self, original_node, updated_node):
        # We are looking for "rule": {...}
        if not self.current_slug:
            return updated_node
            
        golden_stdout = self.golden_map.get(self.current_slug)
        if golden_stdout is None:
            return updated_node

        # Check if key is 'rule'
        if m.matches(updated_node.key, m.SimpleString('"rule"')) or m.matches(updated_node.key, m.SimpleString("'rule'")):
            rule_dict = updated_node.value
            if not isinstance(rule_dict, cst.Dict):
                return updated_node
            
            # Check kind inside rule
            is_target = False
            for el in rule_dict.elements:
                if isinstance(el, cst.DictElement) and (m.matches(el.key, m.SimpleString('"kind"')) or m.matches(el.key, m.SimpleString("'kind'"))):
                    if m.matches(el.value, m.SimpleString()):
                        val = el.value.value.strip("'\"")
                        # print(f"  Found kind: {val}")
                        if val in ["stdout_exact", "stdout_regex", "stdout_match"]:
                            is_target = True
                            print(f"  Found target kind: {val}")
                            break
            
            if is_target:
                print(f"   [{self.current_slug}] Upgrading rule -> stdout_exact")
                
                # Construct new elements
                new_elements = []
                
                # kind: 'stdout_exact'
                new_elements.append(cst.DictElement(
                    key=cst.SimpleString("'kind'"),
                    value=cst.SimpleString("'stdout_exact'")
                ))
                
                # expected: <golden>
                # Use repr() to handle escaping and quotes, but libcst expects the raw code string
                code_str = repr(golden_stdout) 
                
                # If it's a multiline string (has \n), maybe use triple quotes for readability?
                # But repr() uses \n escapes.
                # For now rely on repr() safety.
                
                new_elements.append(cst.DictElement(
                    key=cst.SimpleString("'expected'"),
                    value=cst.SimpleString(code_str)
                ))
                
                self.upgraded_count += 1
                return updated_node.with_changes(value=cst.Dict(elements=new_elements))
                
        return updated_node

def main():
    print("🚀 LibCST Objective Upgrader")
    
    # 1. Load Golden Data
    golden_map = {}
    quests_dir = Path("data/quests")
    for q_dir in quests_dir.iterdir():
        # Check both golden.run.json and golden.json
        run_path = q_dir / "grading" / "golden.run.json"
        legacy_path = q_dir / "grading" / "golden.json"
        
        path = run_path if run_path.exists() else (legacy_path if legacy_path.exists() else None)
        
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    stdout = data.get("stdout", "")
                    golden_map[q_dir.name] = stdout
            except Exception as e:
                print(f"Error loading {path}: {e}")

    print(f"loaded {len(golden_map)} golden captures.")

    # 2. Parse Source
    source_path = Path("arcade_app/seed_quests_standard_worlds.py")
    with open(source_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = cst.parse_module(source_code)
    
    # 3. Transform
    transformer = ObjectiveTransformer(golden_map)
    modified_tree = tree.visit(transformer)
    
    # 4. Save
    if transformer.upgraded_count > 0:
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(modified_tree.code)
        print(f"✅ Updated {transformer.upgraded_count} rules in {source_path}")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
