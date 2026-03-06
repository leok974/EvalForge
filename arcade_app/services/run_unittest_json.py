import unittest
import json
import sys
import os

class JsonTestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super(JsonTestResult, self).__init__(stream, descriptions, verbosity)
        self.successes = []
        self.failures_list = []
        self.errors_list = []

    def addSuccess(self, test):
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append({"name": str(test)})

    def addFailure(self, test, err):
        super(JsonTestResult, self).addFailure(test, err)
        self.failures_list.append({"name": str(test), "message": str(err[1])})

    def addError(self, test, err):
        super(JsonTestResult, self).addError(test, err)
        self.errors_list.append({"name": str(test), "message": str(err[1])})

if __name__ == "__main__":
    # Disable buffering
    sys.stdout.reconfigure(line_buffering=True)
    
    # Discover and run
    loader = unittest.TestLoader()
    start_dir = '/workspace'
    suite = loader.discover(start_dir, pattern='test*.py')

    result = JsonTestResult()
    suite.run(result)

    summary = {
        "passed": len(result.successes),
        "failed": len(result.failures_list) + len(result.errors_list),
        "total": result.testsRun,
        "failures": result.failures_list + result.errors_list
    }

    # Write to file for robust extraction (Docker CP friendly)
    artifacts_dir = os.getenv("EVALFORGE_ARTIFACTS_DIR", os.path.join(start_dir, ".evalforge"))
    report_path = os.path.join(artifacts_dir, "test_results.json")
    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(summary, f)
    except Exception as e:
        print(f"WARN: Failed to write test report: {e}", file=sys.stderr)

    # Print JSON result to stdout
    print(json.dumps(summary))
