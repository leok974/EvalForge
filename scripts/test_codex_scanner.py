"""
Test script for RepoScanner and CandidateSelector.

Usage:
    python test_codex_scanner.py /path/to/repo
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from arcade_app.codex_scanner import RepoScanner
from arcade_app.codex_candidate_selector import CandidateSelector

def test_scanner(repo_path: str):
    """Test the RepoScanner on a given repository."""
    print(f"🔍 Scanning repository: {repo_path}\n")
    
    scanner = RepoScanner()
    results = scanner.scan(repo_path)
    
    print("📄 Core Documentation Files:")
    for pattern, path in results["core_docs"].items():
        print(f"  ✓ {pattern}: {path.relative_to(repo_path)}")
    
    print(f"\n🔧 Stack Detected: {', '.join(results['stack'])}")
    
    print(f"\n💻 Languages:")
    for lang, lines in sorted(results["languages"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang}: {lines:,} lines")
    
    print(f"\n🌍 EvalForge Worlds: {', '.join(results['worlds'])}")
    
    if results["services"]:
        print(f"\n🐳 Services (from docker-compose):")
        for service in results["services"]:
            print(f"  {service['name']}: {service['type']}")
    
    if results["frameworks"]:
        print(f"\n📦 Frameworks:")
        for category, frameworks in results["frameworks"].items():
            if frameworks:
                print(f"  {category}: {', '.join(frameworks)}")
    
    return results

def test_candidate_selector(repo_path: str, scan_results: dict):
    """Test the CandidateSelector on a given repository."""
    print(f"\n\n📝 Testing Candidate Selection...\n")
    
    selector = CandidateSelector()
    
    doc_types = ["overview", "architecture", "data_model", "infra", "agents", "quest_hooks"]
    
    for doc_type in doc_types:
        candidates = selector.select_candidates(repo_path, doc_type, scan_results)
        
        if candidates:
            print(f"\n{doc_type.upper()} - Found {len(candidates)} candidates:")
            for i, candidate in enumerate(candidates, 1):
                print(f"  {i}. {candidate['path']} (score: {candidate['relevance_score']:.1f})")
                print(f"     Snippet: {len(candidate['snippet'])} chars")
        else:
            print(f"\n{doc_type.upper()} - No candidates found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_codex_scanner.py <repo_path>")
        print("\nExample:")
        print("  python test_codex_scanner.py /path/to/EvalForge")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    if not Path(repo_path).exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Run scanner
    scan_results = test_scanner(repo_path)
    
    # Run candidate selector
    test_candidate_selector(repo_path, scan_results)
    
    print("\n✅ Testing complete!")
