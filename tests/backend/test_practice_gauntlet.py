# tests/backend/test_practice_gauntlet.py
from datetime import date, datetime

from arcade_app.practice_gauntlet import (
    PracticeCandidate,
    build_practice_round_from_candidates,
    stable_seed_for_profile_date,
)


def _make_candidate(
    *,
    item_type: str,
    identifier: str,
    world_slug: str | None = None,
    project_slug: str | None = None,
    struggle_score: int = 0,
    attempts: int = 0,
    label: str = "",
) -> PracticeCandidate:
    return PracticeCandidate(
        item_type=item_type,  # type: ignore[arg-type]
        identifier=identifier,
        world_slug=world_slug,
        project_slug=project_slug,
        struggle_score=struggle_score,
        attempts=attempts,
        last_run_at=datetime(2025, 1, 1),
        label=label or identifier,
        description="",
    )


def test_practice_gauntlet_deterministic_for_profile_and_date():
    profile_id = "player-123"
    today = date(2025, 12, 4)

    candidates = [
        _make_candidate(
            item_type="boss_review",
            identifier="reactor-core",
            world_slug="world-python",
            struggle_score=85,
            attempts=3,
        ),
        _make_candidate(
            item_type="quest_review",
            identifier="loops-101",
            world_slug="world-python",
            struggle_score=65,
            attempts=2,
        ),
        _make_candidate(
            item_type="project_maintenance",
            identifier="applylens-runtime-boss",
            project_slug="applylens",
            struggle_score=55,
            attempts=1,
        ),
    ]

    plan1 = build_practice_round_from_candidates(
        profile_id=profile_id,
        for_date=today,
        candidates=candidates,
        max_items=5,
        include_worlds={"world-python"},
        include_projects={"applylens"},
    )
    plan2 = build_practice_round_from_candidates(
        profile_id=profile_id,
        for_date=today,
        candidates=candidates,
        max_items=5,
        include_worlds={"world-python"},
        include_projects={"applylens"},
    )

    assert [i.id for i in plan1.items] == [i.id for i in plan2.items]
    assert plan1.total_count == plan2.total_count


def test_practice_gauntlet_prefers_struggle_targets():
    profile_id = "player-123"
    today = date(2025, 12, 4)

    # Two high-struggle items, one low-struggle, one exploration
    candidates = [
        _make_candidate(
            item_type="boss_review",
            identifier="reactor-core",
            world_slug="world-python",
            struggle_score=90,
            attempts=4,
        ),
        _make_candidate(
            item_type="boss_review",
            identifier="signal-prism",
            world_slug="world-js",
            struggle_score=80,
            attempts=3,
        ),
        _make_candidate(
            item_type="quest_review",
            identifier="loops-101",
            world_slug="world-python",
            struggle_score=35,
            attempts=1,
        ),
        _make_candidate(
            item_type="project_maintenance",
            identifier="applylens-runtime-boss",
            project_slug="applylens",
            struggle_score=0,
            attempts=0,
        ),
    ]

    plan = build_practice_round_from_candidates(
        profile_id=profile_id,
        for_date=today,
        candidates=candidates,
        max_items=3,
        include_worlds={"world-python", "world-js"},
        include_projects={"applylens"},
        struggle_threshold=60,
        maintenance_threshold=20,
    )

    ids = {item.id for item in plan.items}

    # We expect the two high-struggle bosses to be present, plus one of the others
    assert "boss_review:reactor-core" in ids
    assert "boss_review:signal-prism" in ids
    assert len(plan.items) == 3


def test_practice_gauntlet_includes_exploration_when_space():
    profile_id = "player-xyz"
    today = date(2025, 12, 4)

    candidates = [
        # One strong struggle
        _make_candidate(
            item_type="boss_review",
            identifier="reactor-core",
            world_slug="world-python",
            struggle_score=85,
            attempts=3,
        ),
        # One maintenance
        _make_candidate(
            item_type="quest_review",
            identifier="loops-101",
            world_slug="world-python",
            struggle_score=45,
            attempts=2,
        ),
        # Two exploration targets (attempts = 0)
        _make_candidate(
            item_type="quest_review",
            identifier="functions-101",
            world_slug="world-python",
            struggle_score=10,
            attempts=0,
        ),
        _make_candidate(
            item_type="project_maintenance",
            identifier="applylens-agent-boss",
            project_slug="applylens",
            struggle_score=20,
            attempts=0,
        ),
    ]

    plan = build_practice_round_from_candidates(
        profile_id=profile_id,
        for_date=today,
        candidates=candidates,
        max_items=4,
        include_worlds={"world-python"},
        include_projects={"applylens"},
        struggle_threshold=60,
        maintenance_threshold=20,
    )

    ids = {item.id for item in plan.items}

    # Should contain the struggle + maintenance
    assert "boss_review:reactor-core" in ids
    assert "quest_review:loops-101" in ids

    # And at least one exploration item if space allows
    exploration_ids = {
        "quest_review:functions-101",
        "project_maintenance:applylens-agent-boss",
    }
    assert ids & exploration_ids  # non-empty intersection


def test_stable_seed_changes_with_date():
    profile_id = "player-123"
    d1 = date(2025, 12, 4)
    d2 = date(2025, 12, 5)

    s1 = stable_seed_for_profile_date(profile_id, d1)
    s2 = stable_seed_for_profile_date(profile_id, d2)

    assert s1 != s2
