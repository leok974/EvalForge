import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

def load_run(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)

def get_emoji(diff: float) -> str:
    if diff > 0: return "🟢" # Improvement
    if diff < 0: return "🔴" # Regression
    return "⚪" # Neutral

def compare_runs(baseline_path: str, candidate_path: str):
    base = load_run(baseline_path)
    cand = load_run(candidate_path)

    base_map = {r["id"]: r for r in base["results"]}
    cand_map = {r["id"]: r for r in cand["results"]}
    
    # Calculate Summary Diffs
    base_avg = base["summary"]["avg_score"]
    cand_avg = cand["summary"]["avg_score"]
    avg_diff = cand_avg - base_avg
    
    print(f"# ⚖️ EvalForge Regression Report")
    print(f"\n**Baseline:** `{Path(baseline_path).name}` | **Candidate:** `{Path(candidate_path).name}`")
    
    # 1. Summary Table
    print("\n### 📈 Top-Level Metrics")
    print("| Metric | Baseline | Candidate | Diff |")
    print("| :--- | :--- | :--- | :--- |")
    print(f"| **Avg Score** | {base_avg:.1f} | {cand_avg:.1f} | {get_emoji(avg_diff)} `{avg_diff:+.1f}` |")
    
    # 2. Detailed Breakdown
    print("\n### 🔍 Case-by-Case Analysis")
    print("| Case ID | Old Score | New Score | Delta | Status |")
    print("| :--- | :--- | :--- | :--- | :--- |")

    regressions = 0
    
    # Union of all keys to handle added/removed cases
    all_keys = sorted(set(base_map.keys()) | set(cand_map.keys()))
    
    for kid in all_keys:
        b_res = base_map.get(kid)
        c_res = cand_map.get(kid)
        
        if not b_res:
            print(f"| `{kid}` | *N/A* | {c_res['score']} | 🆕 | New Case |")
            continue
        if not c_res:
            print(f"| `{kid}` | {b_res['score']} | *N/A* | ❌ | Removed |")
            continue
            
        score_diff = c_res['score'] - b_res['score']
        status_emoji = get_emoji(score_diff)
        
        if score_diff < 0:
            regressions += 1
            
        print(f"| `{kid}` | {b_res['score']} | {c_res['score']} | `{score_diff:+.1f}` | {status_emoji} |")

    if regressions == 0:
        print("\n> 🎉 **Success:** No regressions detected.")
    else:
        print(f"\n> ⚠️ **Warning:** Detected {regressions} regression(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two EvalForge run files.")
    parser.add_argument("baseline", help="Path to baseline JSON file")
    parser.add_argument("candidate", help="Path to candidate JSON file")
    args = parser.parse_args()
    
    compare_runs(args.baseline, args.candidate)
