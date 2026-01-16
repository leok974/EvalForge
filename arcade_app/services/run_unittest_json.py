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
    suite = loader.discover(start_dir, pattern='*_test.py')

    result = JsonTestResult()
    suite.run(result)

    summary = {
        "passed": len(result.successes),
        "failed": len(result.failures_list) + len(result.errors_list),
        "total": result.testsRun,
        "failures": result.failures_list + result.errors_list
    }

    # Print JSON result to stdout
    print(json.dumps(summary))
