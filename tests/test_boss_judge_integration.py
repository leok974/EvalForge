import asyncio
from arcade_app.bosses.registry import evaluate_boss
from arcade_app.bosses.reactor_core_rubric import score_reactor_core
from arcade_app.bosses.types import BossOutcome

GOOD_SUBMISSION = """
import asyncio
from pydantic import BaseModel


class ReactorStatus(BaseModel):
    core_id: str
    temperature: float
    status: str


async def reactor_status(core_id: str) -> ReactorStatus:
    \"\"\"Return the current status of a reactor core.\"\"\"  # docstring required
    await asyncio.sleep(0.1)
    return ReactorStatus(
        core_id=core_id,
        temperature=900.0,
        status="stable",
    )


async def fetch_reactor_status() -> ReactorStatus:
    return await reactor_status("alpha-core")
"""


def test_evaluate_boss_reactor_core_good_submission():
    outcome: BossOutcome = evaluate_boss("boss-reactor-core", GOOD_SUBMISSION)

    assert outcome.boss_id == "boss-reactor-core"
    assert outcome.score >= 80
    assert outcome.passed is True
    assert outcome.xp_awarded > 0
    # Good runs shouldn't damage integrity
    assert outcome.integrity_delta >= 0
