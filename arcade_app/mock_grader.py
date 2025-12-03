"""
Mock grader for testing Phase 5 features without Vertex AI dependency.
Provides deterministic grades based on Golden Dataset matches.
"""
import json
import os
import hashlib
from typing import Dict, Any, Optional

DATASET_PATH = "data/golden_dataset.jsonl"

class MockGrader:
    def __init__(self):
        self.lookup_table = self._load_dataset_lookup()

    def _load_dataset_lookup(self) -> Dict[str, Any]:
        """
        Loads the golden dataset and creates a lookup map.
        Key: SHA1 of normalized input
        Value: The entire case dict (including expected_score)
        """
        lookup = {}
        if not os.path.exists(DATASET_PATH):
            return lookup

        with open(DATASET_PATH, "r") as f:
            for line in f:
                if line.strip():
                    case = json.loads(line)
                    # Normalize input to ensure matches work despite whitespace
                    key = self._hash_input(case["input"])
                    lookup[key] = case
        return lookup

    def _hash_input(self, text: str) -> str:
        """Create a consistent hash for text inputs."""
        normalized = " ".join(text.split()).strip()
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest()

    async def grade(self, user_input: str, track: str) -> Dict[str, Any]:
        """
        Returns a deterministic grade.
        1. If input matches a Golden Dataset case -> Return expected_score.
        2. Else -> Return a generic fallback score.
        """
        key = self._hash_input(user_input)
        
        # Magic Pass for QA
        if "MAGIC_BOSS_PASS" in user_input:
             return {
                "coverage": 5,
                "correctness": 5,
                "clarity": 5,
                "comment": "[MOCK] Magic Pass detected! Perfect score.",
                "mock_lookup_hit": True
            }

        case = self.lookup_table.get(key)

        if case:
            # HIT: We found this exact case in our dataset.
            # We reverse-engineer the component scores to match the expected weighted score.
            # (Simplified for mock purposes: give uniform component scores close to expected)
            target = case.get("expected_score", 50)
            component_val = max(1, min(5, int(target / 20))) # Approx scale 0-100 to 0-5
            
            return {
                "coverage": component_val,
                "correctness": component_val,
                "clarity": component_val,
                "comment": f"[MOCK] Dataset Match! Returning deterministic score for Case ID: {case.get('id')}",
                "mock_lookup_hit": True
            }
        else:
            # MISS: Fallback generic response
            return {
                "coverage": 3,
                "correctness": 3,
                "clarity": 2,
                "comment": "[MOCK] Unknown input. Returning generic fallback grade.",
                "mock_lookup_hit": False
            }

# Singleton instance
mock_grader_instance = MockGrader()
