from __future__ import annotations

from typing import Callable, Dict

from arcade_app.bosses.reactor_core_rubric import score_reactor_core
from arcade_app.bosses.types import BossOutcome

# Map track IDs (or boss IDs) to scoring functions and thresholds
BOSS_CONFIG: Dict[str, Dict] = {
    "boss-reactor-core": {
        "id": "boss-reactor-core",
        "name": "Reactor Core Meltdown",
        "score_fn": score_reactor_core,
        "pass_threshold": 80,
        "xp_reward": 500,
        "integrity_on_fail": -20,
        "integrity_on_pass": 0,
    },
    # Also mapping the ID used in the database seed for consistency
    "boss_py_fastapi_refactor_01": {
        "id": "boss_py_fastapi_refactor_01",
        "name": "Reactor Core Meltdown",
        "score_fn": score_reactor_core,
        "pass_threshold": 80,
        "xp_reward": 500,
        "integrity_on_fail": -20,
        "integrity_on_pass": 0,
    }
}


def is_boss_track(track_id: str) -> bool:
    return track_id in BOSS_CONFIG


def evaluate_boss(track_id: str, submission: str) -> BossOutcome:
    cfg = BOSS_CONFIG.get(track_id)
    if not cfg:
        raise ValueError(f"Unknown boss track_id: {track_id}")

    score_obj = cfg["score_fn"](submission)
    passed = score_obj.total >= cfg["pass_threshold"]

    xp = cfg["xp_reward"] if passed else 0
    integrity_delta = cfg["integrity_on_pass"] if passed else cfg["integrity_on_fail"]

    return BossOutcome(
        boss_id=cfg["id"],
        score=score_obj.total,
        passed=passed,
        breakdown=score_obj.breakdown,
        comments=score_obj.comments,
        xp_awarded=xp,
        integrity_delta=integrity_delta,
    )
