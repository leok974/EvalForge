# arcade_app/project_questline_spec.py
"""
Pydantic models for project-specific quest and boss specifications.
These are used by QuestMaster to generate structured questlines for synced projects.
"""
from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel


Difficulty = Literal["easy", "medium", "hard"]
QuestKind = Literal["reading", "small-code", "integration"]


class ProjectQuestSpec(BaseModel):
    slug: str
    title: str
    short_description: str
    detailed_description: str
    world_id: str = "world-projects"
    difficulty: Difficulty
    quest_kind: QuestKind
    track_id: str
    order_index: int
    rubric_id: str
    starting_code_path: Optional[str] = None
    base_xp_reward: int
    mastery_xp_bonus: int
    unlocks_boss_id: Optional[str] = None
    unlocks_layout_id: Optional[str] = None


class ProjectTrackSpec(BaseModel):
    track_id: str
    label: str
    order_index: int
    quests: List[ProjectQuestSpec]


class ProjectBossSpec(BaseModel):
    slug: str
    name: str
    world_id: str = "world-projects"
    project_slug: str
    tech_focus: List[str]
    technical_objective: str
    starting_code_path: Optional[str] = None
    rubric_id: str
    hint_codex_id: Optional[str] = None
    phase: str  # e.g. "runtime", "shipping", "intelligence"
    base_hp: int = 100


class ProjectQuestlineSpec(BaseModel):
    project_slug: str
    project_name: str
    template: str
    tracks: List[ProjectTrackSpec]
    bosses: List[ProjectBossSpec]
