import subprocess
import sys
from pathlib import Path


def _run_main():
    """Execute main.py and return its stdout."""
    p = Path("main.py")
    if not p.exists():
        p = Path(__file__).parent.parent / "solutions" / "main.py"
    result = subprocess.run(
        [sys.executable, str(p)],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout


def test_prints_system_online():
    out = _run_main()
    assert "System Online" in out, (
        "Solution must print 'System Online' (assign message = 'System Online' and print it)"
    )


def test_solution_syntax():
    p = Path("main.py")
    if not p.exists():
        p = Path(__file__).parent.parent / "solutions" / "main.py"
    import ast
    ast.parse(p.read_text(encoding="utf-8"))
