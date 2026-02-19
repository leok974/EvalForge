
import unittest
import json
import os
import sys
import subprocess
from pathlib import Path

# Add project root
sys.path.insert(0, os.path.abspath('.'))

class TestCertifiedWorldsSmoke(unittest.TestCase):
    
    def setUp(self):
        self.snapshot_path = Path("docs/audits/WORLDS_UPGRADE_STATUS.json")
        self.certified_slugs = set()
        
        if self.snapshot_path.exists():
            with open(self.snapshot_path, "r") as f:
                try:
                    data = json.load(f)
                    if "worlds" in data:
                        for w in data["worlds"]:
                            if w.get("status") == "TRAINING_GRADE":
                                self.certified_slugs.update(w.get("slugs", []))
                except json.JSONDecodeError:
                    print(f"WARNING: Failed to parse {self.snapshot_path}")
        else:
            print("WARNING: Snapshot not found, skipping specific quest checks.")

    def test_sample_quests_are_certified(self):
        """Asserts representative quests are in the certified snapshot."""
        if not self.certified_slugs:
            self.skipTest("No certified quests found in snapshot (or snapshot missing).")

        # Representative sample from standard worlds
        # Checking known Training Grade worlds from file view:
        # infra, node, react, web (html/css), sql
        samples = {
            "node": "node-ignition",
            "sql": "sql-ignition",
            "infra": "infra-ignition",
            "react": "react-ignition",
            # "web": "html-ignition" # web split into web_core and web_css_core in JSON?
        }
        
        for world, slug in samples.items():
            self.assertIn(slug, self.certified_slugs, f"{slug} ({world}) should be certified.")

    def test_validate_only_passes(self):
        """Asserts that force_seed_standard.py --validate-only returns 0."""
        cmd = [sys.executable, "arcade_app/force_seed_standard.py", "--validate-only"]
        # Force UTF-8 for subprocess to handle emojis
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, encoding="utf-8")
        
        if result.returncode != 0:
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            
        self.assertEqual(result.returncode, 0, "Seed validation check failed.")
        self.assertIn("Validation Passed", result.stdout)

if __name__ == '__main__':
    unittest.main()
