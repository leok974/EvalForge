# arcade_app/project_questline_apply.py
"""
Compiler that transforms a ProjectQuestlineSpec into database records.
"""
from sqlalchemy.orm import Session
from arcade_app.models import QuestDefinition, BossDefinition
from arcade_app.project_questline_spec import ProjectQuestlineSpec


def apply_project_questline_spec(db: Session, spec: ProjectQuestlineSpec):
    """
    Idempotently apply a project questline spec to the database.
    Creates or updates QuestDefinition and BossDefinition records.
    """
    # Bosses
    for boss in spec.bosses:
        existing = (
            db.query(BossDefinition)
            .filter(BossDefinition.id == boss.slug)
            .one_or_none()
        )
        if existing:
            existing.name = boss.name
            existing.world_id = boss.world_id
            existing.project_slug = boss.project_slug
            existing.tech_focus = boss.tech_focus
            existing.technical_objective = boss.technical_objective
            existing.starting_code = boss.starting_code_path or ""
            existing.rubric = boss.rubric_id
            existing.hint_codex_id = boss.hint_codex_id
            existing.phase = boss.phase
            existing.max_hp = boss.base_hp
        else:
            db.add(
                BossDefinition(
                    id=boss.slug,
                    name=boss.name,
                    world_id=boss.world_id,
                    project_slug=boss.project_slug,
                    tech_focus=boss.tech_focus,
                    technical_objective=boss.technical_objective,
                    starting_code=boss.starting_code_path or "",
                    rubric=boss.rubric_id,
                    hint_codex_id=boss.hint_codex_id,
                    phase=boss.phase,
                    max_hp=boss.base_hp,
                    description=f"Project boss for {spec.project_name}",
                )
            )

    # Quests
    for track in spec.tracks:
        for q in track.quests:
            existing = (
                db.query(QuestDefinition)
                .filter(QuestDefinition.slug == q.slug)
                .one_or_none()
            )
            if existing:
                existing.world_id = q.world_id
                existing.track_id = q.track_id
                existing.order_index = q.order_index
                existing.title = q.title
                existing.short_description = q.short_description
                existing.detailed_description = q.detailed_description
                existing.rubric_id = q.rubric_id
                existing.starting_code_path = q.starting_code_path
                existing.unlocks_boss_id = q.unlocks_boss_id
                existing.unlocks_layout_id = q.unlocks_layout_id
                existing.base_xp_reward = q.base_xp_reward
                existing.mastery_xp_bonus = q.mastery_xp_bonus
            else:
                db.add(
                    QuestDefinition(
                        slug=q.slug,
                        world_id=q.world_id,
                        track_id=q.track_id,
                        order_index=q.order_index,
                        title=q.title,
                        short_description=q.short_description,
                        detailed_description=q.detailed_description,
                        rubric_id=q.rubric_id,
                        starting_code_path=q.starting_code_path,
                        unlocks_boss_id=q.unlocks_boss_id,
                        unlocks_layout_id=q.unlocks_layout_id,
                        base_xp_reward=q.base_xp_reward,
                        mastery_xp_bonus=q.mastery_xp_bonus,
                        is_repeatable=False,
                    )
                )

    db.commit()
