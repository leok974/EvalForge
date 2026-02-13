import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_working_memory():
    mem = main.WorkingMemory()
    mem.remember("user:name", "leo")
    mem.remember("user:role", "mle")
    assert mem.recall("user:name") == "leo"
    assert mem.keys("user:") == ["user:name", "user:role"]
    mem.forget("user:role")
    assert mem.recall("user:role", "none") == "none"
