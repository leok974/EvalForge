"""
EvalForge test runner — runs pytest against /workspace test files and emits
pytest output followed by a JSON summary on the last line of stdout.

Output format (two sections on stdout):
  <raw pytest text, up to 3000 chars>
  {"passed": N, "failed": N, "total": N, "failures": [{"name": "...", "message": "..."}]}

The tests_pass validator parses the *last* line as JSON; everything before it
appears verbatim in the learner's terminal so they can see assertion failures,
tracebacks, and the pytest summary line.

Works with pytest-style tests (pytest.raises, fixtures, etc.) as long as pytest
is available in the image (evalforge-backend:latest has pytest 9+).
"""
import json
import os
import re
import subprocess
import sys

WORKSPACE = "/workspace"
ARTIFACTS_DIR = os.getenv("EVALFORGE_ARTIFACTS_DIR", os.path.join(WORKSPACE, ".evalforge"))

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)

    # Run pytest in the workspace, collecting short tracebacks.
    # Pass PYTHONPATH so test files can do `from task import ...` etc.
    import copy
    env = copy.copy(os.environ)
    env["PYTHONPATH"] = WORKSPACE + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    proc = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            WORKSPACE,
            "--tb=short",
            "-q",
            "--no-header",
            "--color=no",
        ],
        capture_output=True,
        text=True,
        cwd=WORKSPACE,
        env=env,
    )

    output = proc.stdout + proc.stderr
    exit_code = proc.returncode

    # Parse pytest summary line, e.g. "3 passed", "2 failed, 1 passed", "1 error"
    passed = 0
    failed = 0
    errors_list = []

    for line in output.splitlines():
        m = re.search(r"(\d+) passed", line)
        if m:
            passed = int(m.group(1))
        m = re.search(r"(\d+) failed", line)
        if m:
            failed = int(m.group(1))
        m = re.search(r"(\d+) error", line)
        if m:
            failed += int(m.group(1))

    # Print raw pytest output to stdout BEFORE the JSON summary.
    # The tests_pass validator falls back to parsing the *last* line as JSON,
    # so everything printed here is safe and will appear in the learner's
    # terminal (QuestIDE.tsx line 730: addLog(result.stdout, 'output')).
    # Truncate at 3000 chars so runaway output doesn't flood the terminal.
    if output.strip():
        print(output[:3000])

    # Collect individual failure names
    for line in output.splitlines():
        m = re.match(r"FAILED (.+?) -\s*(.*)", line)
        if m:
            errors_list.append({"name": m.group(1).strip(), "message": m.group(2).strip() or "Test failed"})
            continue
        m = re.match(r"FAILED (.+)", line)
        if m:
            errors_list.append({"name": m.group(1).strip(), "message": "Test failed"})
            continue
        m = re.match(r"ERROR (.+)", line)
        if m:
            errors_list.append({"name": m.group(1).strip(), "message": "Test error"})

    # Fallback: if exit_code != 0 but we couldn't parse counts, mark as 1 failure
    if exit_code != 0 and passed == 0 and failed == 0:
        failed = 1
        errors_list.append({"name": "unknown", "message": output[-500:] if output else "no output"})

    summary = {
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "failures": errors_list,
    }

    # Write to artifacts file
    try:
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        report_path = os.path.join(ARTIFACTS_DIR, "test_results.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(summary, f)
    except Exception as e:
        print(f"WARN: Failed to write test report: {e}", file=sys.stderr)

    # Emit JSON summary as last line of stdout (validator reads this)
    print(json.dumps(summary))
