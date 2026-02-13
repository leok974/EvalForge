import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_format_prompt_normalizes():
    out = main.format_prompt("  You are helpful.  ", "  hello    there   ")
    assert out == "SYSTEM: You are helpful.\nUSER: hello there"
