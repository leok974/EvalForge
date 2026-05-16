"""
Structural tests for selenium-click-and-type.
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


def test_solution_prints_login_success_sentinel():
    code = _code()
    assert "LOGIN_SUCCESS" in code, (
        "Solution must print 'LOGIN_SUCCESS' sentinel "
        "so the objective rule can match it"
    )


def test_solution_sends_credentials():
    code = _code()
    assert "send_keys" in code, "Solution must use send_keys to type credentials"
    assert "admin" in code, "Solution must type username 'admin'"
    assert "secret123" in code, "Solution must type password 'secret123'"


def test_solution_clicks_submit():
    code = _code()
    assert ".click()" in code, "Solution must click the submit button"
