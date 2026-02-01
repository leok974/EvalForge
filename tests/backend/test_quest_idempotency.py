"""
Phase 8.x PR 3: Quest Idempotency Tests

Test suite for idempotent quest run/submit operations.
"""
import pytest
import uuid
from datetime import datetime
from sqlmodel import select
from arcade_app.progress_models import QuestAttempt, QuestProgressV2


@pytest.mark.asyncio
async def test_run_is_idempotent(async_client, db_session, dev_user):
    """Run with same idempotency_key returns same attempt without re-execution."""
    quest_id = "test-quest"
    code = "print('hello')"
    idempotency_key = str(uuid.uuid4())
    
    # First request
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": idempotency_key
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response1.status_code == 200
    data1 = response1.json()
    attempt_id_1 = data1["attempt_id"]
    
    # Second request with SAME idempotency_key
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": idempotency_key  # SAME KEY
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response2.status_code == 200
    data2 = response2.json()
    attempt_id_2 = data2["attempt_id"]
    
    # Should return the SAME attempt
    assert attempt_id_1 == attempt_id_2
    
    # Verify only ONE attempt exists in DB
    result = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == dev_user,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.is_submit == False,
            QuestAttempt.idempotency_key == idempotency_key
        )
    )
    attempts = result.scalars().all()
    assert len(attempts) == 1, "Should only create one attempt for same idempotency_key"


@pytest.mark.asyncio
async def test_submit_is_idempotent(async_client, db_session, dev_user):
    """Submit with same idempotency_key returns same result."""
    quest_id = "first-sparks"  # Assuming this quest exists in seed data
    code = "x = 5\nprint(x)"
    idempotency_key = str(uuid.uuid4())
    
    # First submit
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/submit",
        json={
            "code": code,
            "language": "python",
            "idempotency_key": idempotency_key
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["ok"] is True
    
    # Second submit with SAME key
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/submit",
        json={
            "code": code,
            "language": "python",
            "idempotency_key": idempotency_key
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["ok"] is True
    
    # Verify only ONE submit attempt exists
    result = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == dev_user,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.is_submit == True,
            QuestAttempt.idempotency_key == idempotency_key
        )
    )
    attempts = result.scalars().all()
    assert len(attempts) == 1, "Should only create one submit for same idempotency_key"


@pytest.mark.asyncio
async def test_run_vs_submit_separation(async_client, db_session, dev_user):
    """Same idempotency_key for run and submit creates TWO distinct attempts."""
    quest_id = "test-quest"
    code = "print('test')"
    shared_key = str(uuid.uuid4())
    
    # Run with key
    response_run = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": shared_key
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response_run.status_code == 200
    run_attempt_id = response_run.json()["attempt_id"]
    
    # Submit with SAME key (different is_submit flag)
    response_submit = await async_client.post(
        f"/api/quests/{quest_id}/submit",
        json={
            "code": code,
            "language": "python",
            "idempotency_key": shared_key
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response_submit.status_code == 200
    
    # Verify TWO distinct attempts exist (is_submit differs)
    result = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == dev_user,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.idempotency_key == shared_key
        )
    )
    attempts = result.scalars().all()
    assert len(attempts) == 2, "Should create separate attempts for run vs submit"
    
    # One should be run, one should be submit
    is_submit_flags = [a.is_submit for a in attempts]
    assert True in is_submit_flags
    assert False in is_submit_flags


@pytest.mark.asyncio
async def test_null_key_allows_duplicates(async_client, db_session, dev_user):
    """Null idempotency_key allows multiple attempts (backwards compatible)."""
    quest_id = "test-quest"
    code = "print('duplicate')"
    
    # First request without key
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate"
            # idempotency_key NOT provided
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response1.status_code == 200
    attempt_id_1 = response1.json()["attempt_id"]
    
    # Second request also without key
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate"
            # idempotency_key NOT provided
        },
        headers={"X-Dev-User": dev_user}
    )
    assert response2.status_code == 200
    attempt_id_2 = response2.json()["attempt_id"]
    
    # Should create TWO different attempts
    assert attempt_id_1 != attempt_id_2
    
    # Verify TWO attempts exist with NULL idempotency_key
    result = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == dev_user,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.is_submit == False,
            QuestAttempt.idempotency_key == None
        )
    )
    attempts = result.scalars().all()
    assert len(attempts) >= 2, "Should allow multiple attempts when key is NULL"


@pytest.mark.asyncio
async def test_different_users_same_key(async_client, db_session):
    """Different users can use the same idempotency_key (user_id is part of uniqueness)."""
    quest_id = "test-quest"
    code = "print('same key')"
    shared_key = str(uuid.uuid4())
    user1 = "user-1"
    user2 = "user-2"
    
    # User 1 run
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": shared_key
        },
        headers={"X-Dev-User": user1}
    )
    assert response1.status_code == 200
    attempt_id_1 = response1.json()["attempt_id"]
    
    # User 2 run with SAME key
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": shared_key  # SAME KEY
        },
        headers={"X-Dev-User": user2}
    )
    assert response2.status_code == 200
    attempt_id_2 = response2.json()["attempt_id"]
    
    # Should create TWO different attempts (different users)
    assert attempt_id_1 != attempt_id_2
    
    # Verify both exist
    result_user1 = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == user1,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.idempotency_key == shared_key
        )
    )
    result_user2 = await db_session.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == user2,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.idempotency_key == shared_key
        )
    )
    
    assert result_user1.scalar_one_or_none() is not None
    assert result_user2.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_idempotent_run_preserves_all_fields(async_client, dev_user):
    """Idempotent run returns all fields from original attempt."""
    quest_id = "test-quest"
    code = "print('preserve')"
    idempotency_key = str(uuid.uuid4())
    
    # First request
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": idempotency_key
        },
        headers={"X-Dev-User": dev_user}
    )
    data1 = response1.json()
    
    # Second request (idempotent)
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": code,
            "language": "python",
            "mode": "validate",
            "idempotency_key": idempotency_key
        },
        headers={"X-Dev-User": dev_user}
    )
    data2 = response2.json()
    
    # All fields should match
    assert data1["attempt_id"] == data2["attempt_id"]
    assert data1["passed"] == data2["passed"]
    assert data1["objective_results"] == data2["objective_results"]
    assert data1["stdout"] == data2["stdout"]
    assert data1["stderr"] == data2["stderr"]
    assert data1["duration_ms"] == data2["duration_ms"]
    assert data1["exit_code"] == data2["exit_code"]
    assert data1["timed_out"] == data2["timed_out"]
