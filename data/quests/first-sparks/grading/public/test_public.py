import importlib.util
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


def test_prints_launch_sequence():
    out = _run_main()
    assert "T-minus 3" in out, "Must print 'T-minus 3'"
    assert "T-minus 2" in out, "Must print 'T-minus 2'"
    assert "T-minus 1" in out, "Must print 'T-minus 1'"
    assert "IGNITION" in out, "Must print 'IGNITION'"


def test_launch_sequence_order():
    out = _run_main()
    lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
    assert lines == ["T-minus 3", "T-minus 2", "T-minus 1", "IGNITION"], (
        f"Lines must appear in order T-minus 3, 2, 1, IGNITION. Got: {lines}"
    )
