import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from arcade_app.llm import chat_completion_json
except ImportError:
    print("WARNING: Could not import chat_completion_json from arcade_app.llm")
    chat_completion_json = None

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_mock_submission():
    base_dir = Path("d:/EvalForge")
    
    # 1. Load System Prompt
    system_prompt_path = base_dir / "rubrics/zero_boss_judge.md"
    print(f"Loading System Prompt from {system_prompt_path}...")
    system_prompt = load_file(system_prompt_path)
    
    # 2. Load Rubric
    rubric_path = base_dir / "rubrics/boss-prism-spectrum-curator-generic-arsenal.json"
    print(f"Loading Rubric from {rubric_path}...")
    boss_rubric = load_json(rubric_path)
    
    # 3. Load Codex
    codex_path = base_dir / "codex/world-typescript/track-spectrum-boss-curator-generic-arsenal.md"
    print(f"Loading Codex from {codex_path}...")
    codex_content = load_file(codex_path)
    boss_codex = {
        "title": "Codex: Curator of the Generic Arsenal",
        "content": codex_content
    }
    
    # 4. Load Solution (Submission)
    sol_dir = base_dir / "solutions/bosses/prism_spectrum"
    
    files = []
    for fname in ["collection.ts", "collection.test.ts"]:
        fpath = sol_dir / fname
        if not fpath.exists():
            print(f"⚠️ Solution file not found: {fpath}")
            continue

        print(f"Loading submission file {fpath}...")
        files.append({
            "path": fname,
            "content": load_file(fpath)
        })
        
    submission = {
        "files": files,
        "notes": "Golden generic arsenal implementation for smoke test."
    }
    
    # 5. Load Boss Definition
    # We can read it from the docs file we created
    boss_defs_path = base_dir / "docs/boss_definitions.world-typescript.json"
    print(f"Loading Boss Defs from {boss_defs_path}...")
    all_bosses = load_json(boss_defs_path)
    # Find Curator
    boss_definition = next(
        (b for b in all_bosses["bosses"] if b["slug"] == "curator-generic-arsenal"), 
        None
    )
    
    if not boss_definition:
        print("❌ Could not find 'curator-generic-arsenal' boss in definition file.")
        return

    # 6. Assemble Payload
    user_payload = {
        "boss_definition": boss_definition,
        "boss_rubric": boss_rubric,
        "boss_codex": boss_codex,
        "submission": submission
    }
    
    print("\n--- Payload Constructed ---")
    print(f"Boss: {boss_definition['title']}")
    print(f"Rubric Criteria: {[c['label'] for c in boss_rubric['criteria']]}")
    
    # 7. Call LLM
    if chat_completion_json:
        print("\n--- Calling ZERO Boss Judge (Mock) ---")
        try:
            result = chat_completion_json(
                system_prompt=system_prompt,
                user_payload=user_payload,
                model_name="gemini-2.0-flash-exp"
            )
            print("\n--- Judge Verdict ---")
            print(json.dumps(result, indent=2))
            
            if "verdict" in result and "score_total" in result:
                 print(f"\n✅ Judge Result: {result['verdict'].upper()} ({result['score_total']}/{result['score_max']})")
                 print(f"Summary: {result.get('summary')}")
            else:
                 print("\n⚠️ Judge output missing keys.")
                 
        except Exception as e:
            print(f"\n❌ LLM Call Failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\nSkipping LLM call (client not available).")

if __name__ == "__main__":
    run_mock_submission()
