import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_apply_diff_requires_approval():
    try:
        main.apply_diff("hello", [{"start":0,"end":5,"text":"hi"}], approved=False)
        assert False
    except PermissionError as e:
        assert str(e) == "NOT_APPROVED"

def test_apply_diff_replaces_range():
    out = main.apply_diff("hello world", [{"start":6,"end":11,"text":"agent"}], approved=True)
    assert out == "hello agent"
