
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
# Single source of truth: only packs listed in questpacks_active.json are verified.
ACTIVE_PACKS_CONFIG = Path("configs/questpacks_active.json")
RUNNER_SCRIPT = "scripts/run_world_public_tests.mjs"
OUTPUT_JSON = Path("docs/audits/FINAL_SWEEP_VERIFICATION.json")
OUTPUT_MD = Path("docs/audits/FINAL_SWEEP_VERIFICATION.md")

def run_pack(pack_path, mode):
    """Runs a questpack in a specific mode and returns the parsed JSON result."""
    print(f">> Running {pack_path.name} [{mode}]...")
    
    cmd = ["node", RUNNER_SCRIPT, "--questpack", str(pack_path), "--mode", mode]
    
    # We capture stdout to parse EF_RUNNER_RESULT_JSON
    # FORCE UTF-8 to avoid Windows CP1252 issues with emojis
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    
    output = result.stdout
    json_result = None
    
    for line in output.splitlines():
        if line.startswith("EF_RUNNER_RESULT_JSON="):
            try:
                json_part = line.replace("EF_RUNNER_RESULT_JSON=", "", 1)
                json_result = json.loads(json_part)
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse JSON for {pack_path.name} [{mode}]")
    
    return {
        "pack": pack_path.name,
        "mode": mode,
        "exit_code": result.returncode,
        "result": json_result,
        "raw_output": output if result.returncode != 0 else None # Save output on fail
    }

def generate_markdown(results):
    md = f"# Final Sweep Verification Report\n\n"
    md += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"**Status:** FINAL_VERIFICATION\n\n"
    
    md += "## Summary\n\n"
    md += "| Questpack | Mode | Status | Pass/Total | Notes |\n"
    md += "|---|---|---|---|---|\n"
    
    for res in results:
        pack = res['pack']
        mode = res['mode']
        data = res.get('result')
        
        status_icon = "✅" if res['exit_code'] == 0 else "❌"
        if mode == "student" and res['exit_code'] != 0:
             status_icon = "✅ (Expected)" # Student fail is good usually
        
        counts = "N/A"
        if data:
            counts = f"{data.get('passed', 0)}/{data.get('total', 0)}"
            
        md += f"| `{pack}` | `{mode}` | {status_icon} | {counts} | |\n"
        
    md += "\n## Detailed Failures\n\n"
    
    has_failures = False
    for res in results:
        # We only care about Solution failures. Student failures are expected.
        if res['mode'] == "solution" and res['exit_code'] != 0:
            has_failures = True
            md += f"### ❌ {res['pack']} (Solution Mode)\n"
            md += "```\n"
            if res['raw_output']:
                # Tail of output
                lines = res['raw_output'].splitlines()
                md += "\n".join(lines[-20:]) 
            else:
                md += "No output captured."
            md += "\n```\n"
            
    if not has_failures:
        md += "No solution failures detected.\n"
        
    return md

def main():
    with open(ACTIVE_PACKS_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
    packs = sorted([Path(p) for p in config["active_questpacks"]], key=lambda p: p.name)

    missing = [p for p in packs if not p.exists()]
    packs = [p for p in packs if p.exists()]  # skip missing packs
    if missing:
        print(f"[WARN] {len(missing)} active pack(s) not found on disk (skipped):")
        for m in missing:
            print(f"   - {m}")

    all_results = []

    print(f"=== Starting Final Sweep on {len(packs)} Modern Packs ===")
    
    for pack in packs:
        # Solution Mode
        res_sol = run_pack(pack, "solution")
        all_results.append(res_sol)
        
        # Student Mode
        res_stu = run_pack(pack, "student")
        all_results.append(res_stu)
        
    # Write JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n[OK] JSON Report written to {OUTPUT_JSON}")
    
    # Write MD
    md_content = generate_markdown(all_results)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[OK] Markdown Report written to {OUTPUT_MD}")

    # Final check
    failures = [r for r in all_results if r['mode'] == 'solution' and r['exit_code'] != 0]
    if failures:
        print(f"\n[FAIL] FINAL SWEEP FAILED: {len(failures)} solution packs failed.")
        exit(1)
    else:
        print("\n[PASS] FINAL SWEEP PASSED: All solution packs passed.")
        exit(0)

if __name__ == "__main__":
    main()
