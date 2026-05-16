"""
Structural tests for selenium-read-text-and-assert.
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


def test_solution_prints_dashboard_title_sentinel():
    code = _code()
    assert "Dashboard Title" in code, (
        "Solution must print 'Dashboard Title: ...' sentinel "
        "so the objective rule can match it"
    )


def test_solution_reads_dashboard_element():
    code = _code()
    assert "dashboard-title" in code, (
        "Solution must locate [data-testid='dashboard-title'] to read the text"
    )
    assert ".text" in code, "Solution must read the element's .text property"


def test_solution_performs_login():
    code = _code()
    assert "login-username" in code, "Solution must locate the username field"
    assert "login-password" in code, "Solution must locate the password field"
    assert "login-submit" in code, "Solution must click the submit button"
