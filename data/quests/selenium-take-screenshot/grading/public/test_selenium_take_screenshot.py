"""
Structural tests for selenium-take-screenshot.
These run without a browser — they verify the solution is syntactically valid
and contains the required sentinel output. Functional verification is done via
the live Docker API which runs the full Selenium/Chrome stack.
"""
import ast
from pathlib import Path


def _code():
    p = Path("main.py")
    if not p.exists():
        p = Path(__file__).parent.parent / "solutions" / "main.py"
    return p.read_text(encoding="utf-8")


def test_solution_syntax():
    ast.parse(_code())


def test_solution_uses_webdriver():
    code = _code()
    assert "webdriver" in code, "Solution must import and use selenium.webdriver"


def test_solution_prints_screenshot_saved_sentinel():
    code = _code()
    assert "SCREENSHOT_SAVED" in code, (
        "Solution must print 'SCREENSHOT_SAVED: <path>' sentinel "
        "so the objective rule can match it"
    )


def test_solution_saves_screenshot():
    code = _code()
    assert "save_screenshot" in code, "Solution must call driver.save_screenshot()"


def test_solution_performs_login():
    code = _code()
    assert "login-username" in code, "Solution must locate the username field"
    assert "login-password" in code, "Solution must locate the password field"
    assert "login-submit" in code, "Solution must click the submit button"
