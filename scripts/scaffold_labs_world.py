import json
import os
import shutil
from pathlib import Path

# Labs Specs
LABS_SPECS = [
    {
        "slug": "quest-py-workspace",
        "title": "Workspace Logic",
        "student_task_summary": "Fix `helper.py` so `calculate()` returns 42.",
        "test_code": """
import unittest
from helper import calculate

class TestWorkspace(unittest.TestCase):
    def test_calculate_returns_42(self):
        self.assertEqual(calculate(), 42)

if __name__ == '__main__':
    unittest.main()
""",
        "solution_py": """
def calculate():
    return 42
""",
        "workspace_files": {
            "main.py": "import helper\nprint(f'Result: {helper.calculate()}')\n",
            "helper.py": "def calculate():\n    return 0\n"
        }
    },
    {
        "slug": "quest-py-hidden",
        "title": "Hidden Tests Verification",
        "student_task_summary": "Implement `secret_value()` to return 100. (Public tests check > 0, Hidden tests check == 100)",
        "test_code": """
import unittest
from main import secret_value

class TestPublic(unittest.TestCase):
    def test_positive(self):
        # Public: just needs to be positive
        val = secret_value()
        self.assertGreater(val, 0)

if __name__ == '__main__':
    unittest.main()
""",
        "hidden_test_code": """
import unittest
from main import secret_value

class TestHidden(unittest.TestCase):
    def test_exact_value(self):
        # Hidden: must be exactly 100
        val = secret_value()
        self.assertEqual(val, 100, "Hidden test failed: Value must be 100")

if __name__ == '__main__':
    unittest.main()
""",
        "solution_py": """
def secret_value():
    return 100
""",
        "workspace_files": {
            "main.py": "def secret_value():\n    return 10  # Passes public, fails hidden\n"
        }
    }
]

def main():
    root = Path.cwd()
    quests_dir = root / "data" / "quests"
    
    for q in LABS_SPECS:
        slug = q["slug"]
        print(f"Scaffolding {slug}...")
        q_dir = quests_dir / slug
        
        # Paths
        ws_dir = q_dir / "workspace"
        grading_dir = q_dir / "grading"
        
        # Clean
        if ws_dir.exists(): shutil.rmtree(ws_dir)
        if grading_dir.exists(): shutil.rmtree(grading_dir)
        
        ws_dir.mkdir(parents=True, exist_ok=True)
        pub_dir = grading_dir / "public"
        sol_dir = grading_dir / "solutions"
        hidden_dir = grading_dir / "hidden" # Only used if hidden tests exist
        
        pub_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)
        
        # README
        readme_txt = f"# {q['title']}\n\n{q['student_task_summary']}\n"
        (ws_dir / "README.md").write_bytes(readme_txt.encode("utf-8"))
        
        # Workspace Files
        for fname, content in q.get("workspace_files", {}).items():
            (ws_dir / fname).write_bytes(content.encode("utf-8"))
            
        # Tests
        test_txt = q["test_code"].replace("\r\n", "\n").strip()
        # For Python runner, we usually look for test_*.py or *_test.py
        # Current pattern: <slug>_test.py or similar. Let's use test_public.py
        (pub_dir / "test_public.py").write_bytes(test_txt.encode("utf-8"))
        
        # Hidden Tests
        if "hidden_test_code" in q:
            hidden_dir.mkdir(parents=True, exist_ok=True)
            hidden_txt = q["hidden_test_code"].replace("\r\n", "\n").strip()
            (hidden_dir / "test_hidden.py").write_bytes(hidden_txt.encode("utf-8"))
            
        # Solution
        # For Python runner swap, we usually swap the file itself.
        # But `run_python_questpack.py` might need updating to handle `grading/solutions` correctly if it doesn't already.
        # It currently does:
        # if mode == "solution":
        #    ... copies solutions/{slug}/* to workspace ...
        # Standardizing to grading/solutions is better.
        sol_txt = q["solution_py"].replace("\r\n", "\n").strip()
        
        # We need to know WHICH file to replace.
        # In scaffolding, we assume 'helper.py' or 'main.py' is the target.
        # Let's write `helper.py` or `main.py` to solutions dir.
        if "helper.py" in q.get("workspace_files", {}):
            (sol_dir / "helper.py").write_bytes(sol_txt.encode("utf-8"))
        elif "main.py" in q.get("workspace_files", {}):
            (sol_dir / "main.py").write_bytes(sol_txt.encode("utf-8"))
            
    print("Done.")

if __name__ == "__main__":
    main()
