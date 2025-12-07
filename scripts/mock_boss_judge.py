import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from arcade_app.llm import chat_completion_json
except ImportError:
    # If imports fail (environment issues), we might mock the LLM call or print instructions
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
    rubric_path = base_dir / "rubrics/boss-foundry-furnace-controller.json"
    print(f"Loading Rubric from {rubric_path}...")
    boss_rubric = load_json(rubric_path)
    
    # 3. Load Codex
    codex_path = base_dir / "codex/world-python/track-ignition.md"
    print(f"Loading Codex from {codex_path}...")
    # Codex is markdown, but input contract says 'object'. 
    # The System Prompt says: "boss_codex: optional object with lore and guidance"
    # Usually we pass the markdown content wrapped in an object or just the string if flexible.
    # Let's wrap it in a simple object for now.
    codex_content = load_file(codex_path)
    boss_codex = {
        "title": "Codex: Ignition",
        "content": codex_content
    }
    
    # 4. Load Solution (Submission)
    sol_dir = base_dir / "solutions/bosses/foundry_ignition"
    
    files = []
    for fname in ["furnace_controller.py", "test_furnace_controller.py"]:
        fpath = sol_dir / fname
        print(f"Loading submission file {fpath}...")
        files.append({
            "path": fname,
            "content": load_file(fpath)
        })
        
    submission = {
        "files": files,
        "notes": "Here is my submission for the Furnace Controller boss. I implemented the CLI and tests as requested."
    }
    
    # 5. Construct Boss Definition (Mock)
    # Since we haven't seeded specific BossDefinitions into JSON files we can read easily (they are in DB or python seed scripts),
    # I'll create a minimal one based on the rubric's boss_id
    boss_definition = {
        "boss_id": "boss-foundry-ignition-furnace-controller",
        "title": "Boss: The Furnace Controller",
        "short_description": "Build a robust sensor processing module.",
        "long_description": "Build `furnace_controller.py`: CLI entrypoint, JSON file IO, validation, logging, and exit codes.",
        "metadata": {
            "requirements": [
                "CLI with --target-temp and --tolerance flags.",
                "Reads a JSON file of sensor readings passed via --input.",
                "Computes average temp and decides 'HEAT', 'COOL', or 'STABLE'.",
                "Logs key decisions and errors; never crashes with an ugly traceback.",
                "Has at least 3 basic tests for decision logic."
            ]
        }
    }

    # 6. Assemble Payload
    user_payload = {
        "boss_definition": boss_definition,
        "boss_rubric": boss_rubric,
        "boss_codex": boss_codex,
        "submission": submission
    }
    
    print("\n--- Payload Constructed ---")
    print(json.dumps(user_payload, indent=2)[:500] + "\n... (truncated) ...")
    
    # 7. Call LLM (if available)
    if chat_completion_json:
        print("\n--- Calling ZERO Boss Judge (Mock) ---")
        try:
            result = chat_completion_json(
                system_prompt=system_prompt,
                user_payload=user_payload,
                model_name="gemini-2.0-flash-exp" # Force a model known to exist or use env default
            )
            print("\n--- Judge Verdict ---")
            print(json.dumps(result, indent=2))
            
            # Verify result schema
            if "verdict" in result and "integrity" in result:
                 print("\n✅ Judge returned valid schema.")
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
