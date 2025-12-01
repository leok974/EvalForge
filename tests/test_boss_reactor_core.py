from arcade_app.bosses.reactor_core_rubric import score_reactor_core


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


BAD_BLOCKING_SUBMISSION = """
import time


def reactor_status(core_id: str):
    time.sleep(1)
    return {"core_id": core_id}


def fetch_reactor_status():
    return reactor_status("alpha-core")
"""


def test_good_submission_scores_high():
    score = score_reactor_core(GOOD_SUBMISSION)

    # Sanity: score is reasonably high
    assert score.total >= 80

    # Async & model should be strong
    assert score.breakdown["async"] >= 30
    assert score.breakdown["model"] >= 20
    assert not any("time.sleep" in c for c in score.comments)


def test_blocking_submission_penalized():
    score = score_reactor_core(BAD_BLOCKING_SUBMISSION)

    # Async score should be low because we block and aren't async
    assert score.breakdown["async"] < 20

    # Comments should mention time.sleep and async issues
    joined = " ".join(score.comments).lower()
    assert "time.sleep" in joined
    assert "async" in joined or "asynchronously" in joined
