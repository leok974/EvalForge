
import json
import os
import sys
import re
import ast
import glob
from pathlib import Path
from typing import List, Dict, Any

# Add root to pythonpath
sys.path.append(os.getcwd())

from arcade_app.models import QuestDefinition # Determine if we use models or raw JSON. Raw JSON is safer for "disk-first" philosophy.

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

class SignalExtractor:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.quest_data = {}
        
    def load_active_questpacks(self):
        """Load list of active questpacks."""
        config_path = self.root_dir / "configs" / "questpacks_active.json"
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("active_questpacks", [])

    def load_questpack(self, pack_rel_path: str) -> List[Dict]:
        """Load quests from a pack file."""
        path = self.root_dir / pack_rel_path
        if not path.exists():
            print(f"⚠️ Questpack not found: {path}")
            return []
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        quests = []
        if isinstance(data, list):
            quests = data
        elif isinstance(data, dict):
             if "packs" in data: quests = data["packs"]
             if "packs" in data: quests = data["packs"]
             elif "quests" in data: 
                 quests = data["quests"]
                 # Propagate world/track from pack to quests
                 pack_world = data.get("world_id")
                 if pack_world:
                     for q in quests:
                         if "world_id" not in q: q["world_id"] = pack_world
                         
             elif "slug" in data: quests = [data]
        
        # Normalize result
        normalized = []
        for q in quests:
            # Handle redirection
            if "quest_path" in q:
                q_dir = self.root_dir / q["quest_path"]
                q_json = q_dir / "quest.json"
                if q_json.exists():
                    with open(q_json, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        loaded["_source_dir"] = str(q_dir) # Track source
                        normalized.append(loaded)
            else:
                 # Standard definition, try to find hidden workspace path from pack location
                 # (Not always reliable, better to rely on what's in the object)
                 pack_dir = path.parent
                 q["_source_dir"] = str(pack_dir) # Approximate, might be specific workspace subfolder
                 normalized.append(q)
                 
        return normalized

    def extract_from_python_ast(self, code: str) -> List[str]:
        """Extract function names from Python code."""
        symbols = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):
                         symbols.append(node.name)
        except:
            pass
        return symbols

    def extract_from_js_regex(self, code: str) -> List[str]:
        """Extract exports from JS/TS code."""
        symbols = []
        # exports.foo = ...
        symbols.extend(re.findall(r'exports\.(\w+)\s*=', code))
        # export function foo
        symbols.extend(re.findall(r'export\s+function\s+(\w+)', code))
        # module.exports = { foo }
        # This is harder, skipping for now or adding simple heuristic
        return list(set(symbols))

    def extract_test_cases(self, test_path: Path) -> List[Dict]:
        """Extract test cases from a test file."""
        if not test_path.exists():
            return []
            
        content = test_path.read_text(encoding="utf-8")
        ext = test_path.suffix.lower()
        
        tests = []
        
        # JS/TS Grading (node:test or jest)
        if ext in ['.js', '.ts', '.mjs', '.cjs', '.jsx', '.tsx']:
            # test("name", ...) or it("name", ...)
            matches = re.finditer(r'(?:test|it)\s*\(\s*["\']([^"\']+)["\']', content)
            for m in matches:
                test_name = m.group(1)
                
                # Try to find assertions within this test block (heuristic: next lines until end of block)
                # This is hard with regex. For now just grab the name.
                tests.append({
                    "name": test_name,
                    "file": test_path.name,
                    "type": "unit"
                })
                
        # Python Grading (unittest/pytest)
        elif ext == '.py':
             matches = re.finditer(r'def\s+(test_\w+)', content)
             for m in matches:
                 tests.append({
                     "name": m.group(1),
                     "file": test_path.name,
                     "type": "unit"
                 })
                 
        return tests

    def extract_terms(self, slug: str) -> Dict:
        """Extract terms and codex refs from overlay."""
        # Check docs/quests/<slug>/terms.json
        overlay_path = self.root_dir / "docs" / "quests" / slug / "terms.json"
        
        terms = []
        refs = []
        
        if overlay_path.exists():
            try:
                data = json.loads(overlay_path.read_text(encoding="utf-8"))
                terms = [t.get("term") for t in data if "term" in t]
                refs = [t.get("codex_ref") for t in data if "codex_ref" in t]
            except:
                pass
                
        return {"terms": terms, "codex_refs": refs}

    def process_quest(self, quest: Dict) -> Dict:
        slug = quest.get("slug")
        if not slug: return None
        
        # 1. Base Metadata
        signal = {
            "slug": slug,
            "title": quest.get("title"),
            "world_id": quest.get("world_id"),
            "track_id": quest.get("track_id"),
            "language": quest.get("language", "unknown"),
            "workspace_files": [],
            "entry_files": [],
            "starter_symbols": [],
            "public_test_cases": [],
            "terms": [],
            "codex_refs": [],
            "_quality": "Unknown" # To implement
        }
        
        # 2. Workspace Exploration
        # Determine exact workspace path
        ws_config = quest.get("workspace", {})
        files_from = ws_config.get("files_from")
        
        workspace_path = None
        if files_from:
            # Need to handle relative paths from the quest definition source file
            # This is tricky without knowing exactly where `quest` came from.
            # Use `_source_dir` if we populated it.
            source_dir = quest.get("_source_dir")
            if source_dir:
                 workspace_path = Path(source_dir) / files_from
            else:
                 # Fallback: assume typical data/quests/<slug>/workspace
                 workspace_path = self.root_dir / "data" / "quests" / slug / "workspace"
        else:
             workspace_path = self.root_dir / "data" / "quests" / slug / "workspace"

        # 3. Extract Starter Code Signals
        if workspace_path and workspace_path.exists():
             for f in workspace_path.rglob("*"):
                 if f.is_file():
                     rel = f.relative_to(workspace_path)
                     signal["workspace_files"].append(str(rel))
                     
                     # Check entry files
                     if f.name in ["index.js", "main.py", "index.html", "style.css", "App.tsx"]:
                         signal["entry_files"].append(str(rel))
                         
                         content = f.read_text(encoding="utf-8", errors="ignore")
                         
                         if f.suffix == ".py":
                             signal["starter_symbols"].extend(self.extract_from_python_ast(content))
                         elif f.suffix in [".js", ".ts", ".tsx"]:
                             signal["starter_symbols"].extend(self.extract_from_js_regex(content))

        # 4. Extract Tests
        # Assume data/quests/<slug>/grading/public/*
        grading_path = self.root_dir / "data" / "quests" / slug / "grading" / "public"
        if grading_path.exists():
            for f in grading_path.rglob("*"):
                if f.is_file() and ("test" in f.name or "spec" in f.name):
                    signal["public_test_cases"].extend(self.extract_test_cases(f))

        # 5. Extract Terms
        term_data = self.extract_terms(slug)
        signal["terms"] = term_data["terms"]
        signal["codex_refs"] = term_data["codex_refs"]
        
        # Dedup lists
        signal["starter_symbols"] = sorted(list(set(signal["starter_symbols"])))
        
        return signal

    def run(self, world=None):
        print("🔍 Scanning questpacks...")
        packs = self.load_active_questpacks()
        
        all_signals = {}
        
        for pack_path in packs:
            print(f"  Parsing {pack_path}...")
            quests = self.load_questpack(pack_path)
            
            for q in quests:
                if world and q.get("world_id") != world:
                    continue
                    
                print(f"    Extracting {q.get('slug')}...")
                sig = self.process_quest(q)
                if sig:
                    all_signals[sig["slug"]] = sig
                    
        # Write Output
        out_path = ARTIFACTS_DIR / "quest_signals.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_signals, f, indent=2)
            
        print(f"✅ Extracted signals for {len(all_signals)} quests -> {out_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", help="Filter by world_id")
    args = parser.parse_args()
    
    extractor = SignalExtractor(os.getcwd())
    extractor.run(world=args.world)
