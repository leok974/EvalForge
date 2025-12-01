from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BossOutcome:
    boss_id: str
    score: int
    passed: bool
    breakdown: Dict[str, int]
    comments: List[str]
    xp_awarded: int
    integrity_delta: int  # negative = damage, 0 = none, positive = heal
