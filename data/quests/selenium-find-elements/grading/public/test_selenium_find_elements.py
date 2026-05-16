"""
Structural tests for selenium-find-elements.
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


def test_solution_prints_status_value_sentinel():
    code = _code()
    assert "STATUS_VALUE" in code, (
        "Solution must print 'STATUS_VALUE: ...' sentinel "
        "so the objective rule can match it"
    )


def test_solution_finds_login_elements():
    code = _code()
    assert "login-username" in code, "Solution must locate [data-testid='login-username']"
    assert "login-password" in code, "Solution must locate [data-testid='login-password']"
    assert "login-submit" in code, "Solution must locate [data-testid='login-submit']"
