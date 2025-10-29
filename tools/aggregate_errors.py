#!/usr/bin/env python3
"""
Aggregate error journal entries to find recurring failure patterns.
Helps identify the most common errors for creating new quest exercises.
"""
import json
import sys
import collections
import hashlib
from pathlib import Path
from typing import Dict, List, Any


def main() -> None:
    journal_path = Path("logs/error-journal.ndjson")
    
    if not journal_path.exists():
        print(f"Error journal not found at: {journal_path}")
        print("Run some tasks first to generate error data.")
        sys.exit(1)
    
    counts: collections.Counter[str] = collections.Counter()
    buckets: Dict[str, List[Dict[str, Any]]] = {}
    total_runs = 0
    failed_runs = 0
    
    for line in journal_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
            
        try:
            obj: Dict[str, Any] = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        total_runs += 1
        
        # Skip successful runs
        if obj.get("exit_code", 0) == 0:
            continue
            
        failed_runs += 1
        
        # Use fingerprint or create one from stderr
        key: str = obj.get("fingerprint", "")
        if not key:
            stderr: str = obj.get("stderr_tail", "")
            key = hashlib.sha1(stderr.encode()).hexdigest()
        
        counts[key] += 1
        buckets.setdefault(key, []).append(obj)
    
    print(f"\n{'='*80}")
    print(f"Error Journal Analysis")
    print(f"{'='*80}")
    print(f"Total runs: {total_runs}")
    print(f"Failed runs: {failed_runs}")
    print(f"Success rate: {((total_runs - failed_runs) / total_runs * 100):.1f}%")
    print(f"Unique error patterns: {len(counts)}")
    print(f"{'='*80}\n")
    
    if not counts:
        print("No failures found! 🎉")
        return
    
    print("Top 10 recurring failures:\n")
    
    for i, (key, n) in enumerate(counts.most_common(10), 1):
        first: Dict[str, Any] = buckets[key][0]
        tag: str = first.get('tag', 'unknown')
        stderr: str = first.get('stderr_tail', '')
        
        # Get last non-empty line from stderr
        last_line: str = ""
        for line in stderr.strip().splitlines():
            if line.strip():
                last_line = line.strip()
        
        # Truncate if too long
        if len(last_line) > 100:
            last_line = last_line[:97] + "..."
        
        print(f"{i}. [{tag}] × {n} occurrences")
        print(f"   Fingerprint: {key[:16]}...")
        print(f"   Error: {last_line}")
        print(f"   Command: {first.get('command', 'N/A')}")
        
        # Show quest_id if available
        quest_id: Any = first.get('quest_id')
        if quest_id:
            print(f"   Quest: {quest_id}")
        
        print()
    
    # Generate quest suggestions
    print(f"\n{'='*80}")
    print("💡 Quest Generation Suggestions")
    print(f"{'='*80}\n")
    
    for i, (key, n) in enumerate(counts.most_common(3), 1):
        first: Dict[str, Any] = buckets[key][0]
        tag: str = first.get('tag', 'unknown')
        stderr: str = first.get('stderr_tail', '').strip()
        
        print(f"Quest Candidate #{i} ({n} occurrences):")
        print(f"  Tag: {tag}")
        print(f"  Create: seed/quests/{tag}_{key[:8]}.json")
        print(f"  Symptom: {stderr.splitlines()[-1] if stderr.splitlines() else 'Unknown error'}")
        print(f"  Goal: Fix the {tag} issue and achieve 100% test pass")
        print()


if __name__ == "__main__":
    main()
