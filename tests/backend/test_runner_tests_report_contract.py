
import unittest
import os
import json
from arcade_app.services.code_runner import run_code

class TestRunnerTestsReportContract(unittest.TestCase):
    def setUp(self):
        os.environ["EXECUTION_BACKEND"] = "docker"

    def test_python_tests_mode_returns_report(self):
        # 1. Setup workspace with passing tests
        code = """
import unittest
class TestDemo(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(True)
"""
        workspace = {
            "entrypoint": "main.py",
            "files": [
                {"path": "main.py", "content": code},
                {"path": "test_demo.py", "content": code} # run_unittest_json scans *_test.py ?? pattern='*_test.py'
            ]
        }
        # Note: pattern is *_test.py in run_unittest_json.py. Let's match it.
        # Wait, run_unittest_json.py uses pattern='*_test.py'.
        # My file "test_demo.py" matches? No. "demo_test.py" matches.
        
        workspace["files"][1]["path"] = "demo_test.py"

        # 2. Run
        print("\n--- Starting Contract Test Run ---")
        res = run_code(
            language="python",
            code="",
            mode="tests",
            timeout_ms=5000,
            workspace=workspace
        )
        print(f"--- Finished. ExecResult: ok={res.ok}, exit={res.exit_code} ---")
        print(f"Stdout: {res.stdout}")
        print(f"Stderr: {res.stderr}")

        # 3. Assertions
        # Expect successful execution (exit code 0)
        self.assertEqual(res.exit_code, 0, f"Runner exited with {res.exit_code}. Stderr: {res.stderr}")
        
        # Expect JSON report in stdout
        self.assertTrue(res.stdout.strip(), "Stdout should not be empty")
        
        try:
            report = json.loads(res.stdout)
            self.assertIn("passed", report)
            self.assertIn("total", report)
            self.assertGreaterEqual(report["total"], 1)
        except json.JSONDecodeError:
            self.fail(f"Stdout is not valid JSON: {res.stdout}")

if __name__ == "__main__":
    unittest.main()
