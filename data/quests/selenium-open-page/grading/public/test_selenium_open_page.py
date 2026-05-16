"""
Structural tests for selenium-open-page.
These run without a browser — they verify the solution is syntactically valid
and contains the required sentinel output. Functional verification is done via
the live Docker API which runs the full Selenium/Chrome stack.
"""
import ast
from pathlib import Path


def _code():
    """Read main.py from wherever the runner placed it."""
    p = Path("main.py")
    if not p.exists():
        p = Path(__file__).parent.parent / "solutions" / "main.py"
    return p.read_text(encoding="utf-8")


def test_solution_syntax():
    """Solution must be syntactically valid Python."""
    ast.parse(_code())


def test_solution_uses_webdriver():
    code = _code()
    assert "webdriver" in code, "Solution must import and use selenium.webdriver"


def test_solution_prints_title_match_sentinel():
    code = _code()
    assert "TITLE_MATCH" in code, (
        "Solution must print 'TITLE_MATCH: ...' sentinel "
        "so the objective rule can match it"
    )


def test_solution_navigates_to_app_url():
    code = _code()
    assert "driver.get" in code, "Solution must call driver.get() to navigate"
    assert "EVALFORGE_APP_URL" in code or "APP_URL" in code, (
        "Solution must read APP_URL from environment"
    )
