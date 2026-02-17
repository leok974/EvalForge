from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class KeyTerm(BaseModel):
    id: str
    term: str
    codex_ref: Optional[str] = None
    one_liner: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class QuestResponse(BaseModel):
    id: str
    slug: str
    world_id: str
    track_id: str
    order_index: int
    title: str
    short_description: str
    state: str
    best_score: Optional[float] = 0.0
    attempts: int = 0
    
    # Content
    briefing_md: Optional[str] = None
    lore_md: Optional[str] = None
    tutorial_md: Optional[str] = None
    
    # Metadata
    key_terms: List[KeyTerm] = Field(default_factory=list)
    concept_tags: List[str] = Field(default_factory=list)
    codex_references: List[str] = Field(default_factory=list)
    
    # Dynamic
    starter_code: Optional[str] = None
    objectives: List[Dict[str, Any]] = Field(default_factory=list)
    hints: List[Dict[str, Any]] = Field(default_factory=list)
    tiered_hints: Dict[str, str] = Field(default_factory=dict)
    
    # Unlocks
    unlocks_boss_id: Optional[str] = None
    unlocks_layout_id: Optional[str] = None
    
    # Rewards
    base_xp_reward: int = 50
    mastery_xp_bonus: int = 0
    
    # UI Metadata
    questpack: Optional[str] = "unknown"
    is_active: bool = False
    
    # Versioning
    schema_version: str = "v2" # Bump this to invalidate cache if shape changes
    content_version: Optional[str] = None

class QuestSubmission(BaseModel):
    code: str
    language: Optional[str] = "python"
    workspace: Optional[List[Dict[str, Any]]] = None
