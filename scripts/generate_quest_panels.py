
import json
import os
import sys
import hashlib
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict, Any

# Add root to pythonpath
sys.path.append(os.getcwd())

ARTIFACTS_DIR = Path("artifacts")

# --- LORE TEMPLATES ---
LORE_TEMPLATES = {
    "world-node": {
        "voice": "System Log",
        "template": "## System Log: {title}\n\n> *Establishing secure uplink...*\n>\n> Target: {title}\n> Status: Priority Alpha\n> Protocol: **NODE_RUNTIME**\n\nThe runtime environment is destabilized. Re-initialize the core logic to restore functionality."
    },
    "world-python": {
        "voice": "Holocron",
        "template": "## Holocron Entry: {title}\n\n> *Accessing archival records...*\n>\n> Subject: {title}\n> Clearance: Acolyte\n\nThe ancient scripts have fragmented. Reconstruct the logic to preserve the knowledge."
    },
    "world-cli": {
        "voice": "Terminal",
        "template": "## Terminal Log: {title}\n\n> *Secure shell connection established...*\n>\n> Operation: {title}\n> Clearance: Root\n\nCommand execution required. Standard input parameters missing. Execute directive immediately."
    },
    "world-sql": {
        "voice": "Database",
        "template": "## Query Log: {title}\n\n> *Connected to primary data store...*\n>\n> Query Plan: {title}\n> Optimization Level: High\n\nThe schema is inconsistent. Construct precise queries to retrieve the required dataset."
    },
    "world-git": {
        "voice": "Repository",
        "template": "## Git Reflog: {title}\n\n> *Checking out revision...*\n>\n> HEAD -> {title}\n> State: Detached\n\nVersion control integrity compromised. Commit the correct changes to restore the timeline."
    },
    "world-infra": {
        "voice": "DevOps",
        "template": "## Infrastructure Alert: {title}\n\n> *Monitoring systems active...*\n>\n> Service: {title}\n> Health: Degraded\n\nConfiguration drift detected. Apply the necessary manifest to stabilize the environment."
    },
    "world-ml": {
        "voice": "AI Core",
        "template": "## Model Weights: {title}\n\n> *Loading neural parameters...*\n>\n> Architecture: {title}\n> Loss: Infinity\n\nThe model is failing to converge. Adjust the hyperparameters or data pipeline to achieve optimization."
    },
    "world-agents": {
        "voice": "Agent Swarm",
        "template": "## Agent Trace: {title}\n\n> *Swarm intelligence synchronizing...*\n>\n> Directive: {title}\n> Status: Hallucinating\n\nThe agent is deviating from the prompt. Refine the context window and tools to align behavior."
    },
    "world-web": {
        "voice": "Browser Console",
        "template": "## Console Output: {title}\n\n> *DOM Content Loaded...*\n>\n> Element: {title}\n> State: Rendering Error\n\nThe interface is unresponsive. Update the markup and styles to meet the visual specification."
    },
    "world-react": {
        "voice": "React DevTools",
        "template": "## Component Tree: {title}\n\n> *Mounting component...*\n>\n> Component: {title}\n> Props: Invalid\n\nThe render cycle is broken. Fix the hook dependencies and state management to prevent infinite loops."
    },
    "world-javascript": {
         "voice": "JS Engine",
         "template": "## Runtime Exception: {title}\n\n> *Execution context created...*\n>\n> Stack: {title}\n> Error: Logic Failure\n\nThe scripts are throwing unhandled exceptions. Debug the control flow to ensure smooth execution."
    },
    "world-typescript": {
        "voice": "Compiler",
        "template": "## Compilation Log: {title}\n\n> *Type checking in progress...*\n>\n> Module: {title}\n> Status: Type Mismatch\n\nStrict mode is active. Define interfaces and types to satisfy the compiler."
    }
}
DEFAULT_LORE = "## Mission Log: {title}\n\nMission objectives downloaded. Proceed with implementation."

def generate_briefing(signal: Dict) -> str:
    title = signal.get("title", "Unknown Mission")
    entry_files = signal.get("entry_files", [])
    file_list = ", ".join([f"`{f}`" for f in entry_files[:2]])
    
    # 2-4 sentences
    # Intro
    text = f"# Mission: {title}\n\n"
    text += f"**Objective:** {title}.\n\n"
    
    if file_list:
        text += f"You need to implement the solution in {file_list}. "
    else:
        text += "You need to implement the solution in the workspace. "
        
    text += "Focus on meeting the requirements defined by the test suite.\n\n"
    
    return text

def generate_objectives(signal: Dict) -> List[Dict]:
    objs = []
    
    # 1. Test-based objectives
    tests = signal.get("public_test_cases", [])
    
    for i, t in enumerate(tests):
        # Clean up test name
        name = t.get("name", "").replace("EF_CLI_IGNITION_BASENAME:", "").strip()
        name = name[0].upper() + name[1:] if name else "Pass test case"
        
        objs.append({
            "id": f"obj_test_{i+1}",
            "text": name,
            "why": "Specification requirement"
        })
        
    # 2. Starter symbol objectives (if no tests or as supplement)
    if not objs:
        symbols = signal.get("starter_symbols", [])
        for i, s in enumerate(symbols[:3]):
             objs.append({
                "id": f"obj_sym_{i+1}",
                "text": f"Implement function `{s}`",
                "why": "Core logic"
            })
            
    # Fallback
    if not objs:
        objs.append({
            "id": "obj_default",
            "text": "Complete the assignment as described in README.md",
            "why": "Specification"
        })
        
    return objs

def generate_hints(signal: Dict) -> Dict:
    # 3 Progressive hints
    hints = {}
    
    lang = signal.get("language", "code")
    entry_files = signal.get("entry_files", [])
    terms = signal.get("terms", [])
    
    # Tier 1: Location/Start
    if entry_files:
        hints["concept"] = f"Start by analyzing the structure of `{entry_files[0]}`."
    else:
        hints["concept"] = "Review the workspace file structure."
        
    # Tier 2: Concept/Term
    if terms:
        t = terms[0]
        hints["guided"] = f"Review the concept of **{t}** in the Codex."
    else:
        hints["guided"] = f"Remember to check standard library documentation for {lang}."
        
    # Tier 3: Debugging (Hard to gen without specific error strings, so generic debug)
    hints["full_solution"] = "No full solution provided. Check your syntax and ensure all tests pass."
    
    return hints

def generate_lore(signal: Dict) -> str:
    wid = signal.get("world_id")
    title = signal.get("title", "Mission")
    
    tmpl = LORE_TEMPLATES.get(wid, {}).get("template", DEFAULT_LORE)
    return tmpl.format(title=title)

class ContentGenerator:
    def __init__(self, mode: str = "dry-run", world_filter: str = None, quality_filter: str = None):
        self.mode = mode
        self.world_filter = world_filter
        self.quality_filter = quality_filter
        self.signals = {}
        self.generated = {}

    def load_signals(self):
        with open(ARTIFACTS_DIR / "quest_signals.json", "r", encoding="utf-8") as f:
            self.signals = json.load(f)

    def run(self):
        print(f"🎨 Generating content (Mode: {self.mode})...")
        self.load_signals()
        
        report_lines = ["# Content Generation Report\n"]
        
        for slug, sig in self.signals.items():
            # Filters
            if self.world_filter and sig.get("world_id") != self.world_filter:
                continue
            
            # Generate
            briefing = generate_briefing(sig)
            objectives = generate_objectives(sig)
            hints = generate_hints(sig)
            lore = generate_lore(sig)
            
            gen_data = {
                "briefing_md": briefing,
                "objectives": objectives, # This is the list of dicts
                "tiered_hints": hints,
                "lore_md": lore
            }
            self.generated[slug] = gen_data
            
            # Report
            report_lines.append(f"## {slug}")
            report_lines.append(f"**Briefing:**\n> {briefing.replace(chr(10), chr(10)+'> ')}\n")
            report_lines.append(f"**Objectives:**")
            for o in objectives:
                report_lines.append(f"- {o['text']}")
            report_lines.append(f"\n**Lore:**\n> {lore.replace(chr(10), chr(10)+'> ')}\n")
            report_lines.append("---\n")
            
        # Write Report
        with open(ARTIFACTS_DIR / "quest_panels_check.md", "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
            
        print(f"✅ Generated content for {len(self.generated)} quests -> artifacts/quest_panels_check.md")

        if self.mode == "apply":
            self.apply_changes()

    def apply_changes(self):
        print("💾 Applying changes to quest definitions...")
        
        # Load active packs to locate quests
        with open("configs/questpacks_active.json", "r", encoding="utf-8") as f:
            active_packs = json.load(f).get("active_questpacks", [])
            
        # Map slug -> (pack_path, quest_index, is_external, external_path)
        quest_map = {}
        
        for pack_rel in active_packs:
             pack_path = Path(pack_rel)
             if not pack_path.exists(): continue
             
             try:
                 with open(pack_path, "r", encoding="utf-8") as f:
                     data = json.load(f)
                     
                 # Normalize list
                 quests = []
                 if isinstance(data, list): quests = data
                 elif isinstance(data, dict):
                     if "packs" in data: quests = data["packs"]
                     elif "quests" in data: quests = data["quests"]
                     elif "slug" in data: quests = [data]
                 for idx, q in enumerate(quests):
                     slug = q.get("slug")
                     
                     if "quest_path" in q:
                         # External
                         q_dir = Path(q["quest_path"])
                         q_json = q_dir / "quest.json"
                         
                         # Resolve slug from target if missing
                         resolved_slug = slug
                         if not resolved_slug and q_json.exists():
                             try:
                                 with open(q_json, "r", encoding="utf-8") as f:
                                     ext_data = json.load(f)
                                     resolved_slug = ext_data.get("slug")
                             except:
                                 pass
                                 
                         if resolved_slug:
                             quest_map[resolved_slug] = (pack_path, idx, True, q_json)
                     elif slug:
                         # Inline
                         quest_map[slug] = (pack_path, idx, False, None)
             except Exception as e:
                 print(f"  ⚠️ Error parsing {pack_rel}: {e}")

        updates_by_pack = {} # pack_path -> {idx: content}
        updates_external = {} # path -> content

        matched = 0
        for slug, content in self.generated.items():
            if slug not in quest_map:
                print(f"  ⚠️ Could not locate source for {slug}, skipping.")
                continue
                
            pack_path, idx, is_ext, ext_path = quest_map[slug]
            
            if is_ext:
                updates_external[ext_path] = content
            else:
                if pack_path not in updates_by_pack:
                    updates_by_pack[pack_path] = {}
                updates_by_pack[pack_path][idx] = content
            matched += 1

        # Apply External Updates
        for path, content in updates_external.items():
            if path.exists():
                self._update_json_file(path, content)
            else:
                print(f"  ❌ External file not found: {path}")

        # Apply Pack Updates (Inline)
        for pack_path, updates in updates_by_pack.items():
            try:
                with open(pack_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Navigate to quests array
                target_list = None
                if isinstance(data, list): target_list = data
                elif isinstance(data, dict):
                    if "packs" in data: target_list = data["packs"]
                    elif "quests" in data: target_list = data["quests"]
                    elif "slug" in data: target_list = [data] # Should check if right one
                
                if target_list is not None:
                    for idx, content in updates.items():
                        if idx < len(target_list):
                            self._merge_content(target_list[idx], content)
                            
                    with open(pack_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print(f"  ✅ Updated pack: {pack_path}")
                else:
                    print(f"  ❌ Could not find quest list in {pack_path}")
                    
            except Exception as e:
                print(f"  ❌ Failed to update pack {pack_path}: {e}")

        print(f"💾 Applied changes to {matched} quests.")

    def _update_json_file(self, path: Path, content: Dict):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self._merge_content(data, content)
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"  ✅ Updated file: {path}")
                
        except Exception as e:
            print(f"  ❌ Failed to update {path}: {e}")

    def _merge_content(self, target: Dict, content: Dict):
        target["briefing_md"] = content["briefing_md"]
        target["lore_md"] = content["lore_md"]
        target["objectives"] = content["objectives"]
        target["tiered_hints"] = content["tiered_hints"]
        target["content_source"] = "generated_v1"
        target["content_version"] = "9.9.0"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dry-run", "apply"], default="dry-run")
    parser.add_argument("--world", help="Filter by world_id")
    parser.add_argument("--only-quality", help="Only overwrite quests with this quality (Not Implemented yet)")
    args = parser.parse_args()
    
    gen = ContentGenerator(mode=args.mode, world_filter=args.world)
    gen.run()
