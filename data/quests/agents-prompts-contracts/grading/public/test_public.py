import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_valid_contract_ok():
    c = {"system":"s","user":"u","tools":["add"],"max_tokens":128}
    assert main.validate_prompt_contract(c) == []

def test_invalid_contract_errors():
    c = {"system":"", "user": 123, "tools":"x", "max_tokens":0}
    errs = main.validate_prompt_contract(c)
    assert "system_invalid" in errs
    assert "user_invalid" in errs
    assert "tools_invalid" in errs
    assert "max_tokens_invalid" in errs
