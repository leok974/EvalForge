from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector

# --- USER & GAMIFICATION ---

class User(SQLModel, table=True):
    id: str = Field(primary_key=True) # "leo"
    name: str
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    profile: Optional["Profile"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(back_populates="owner")

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", unique=True)
    total_xp: int = 0
    global_level: int = 1
    # Store world-specific progress as JSON for flexibility
    world_progress: Dict = Field(default={}, sa_type=JSON) 
    
    user: User = Relationship(back_populates="profile")

# --- PROJECTS & CONTENT ---

class Project(SQLModel, table=True):
    id: str = Field(default_factory=lambda: f"proj-{uuid.uuid4().hex[:8]}", primary_key=True)
    owner_user_id: str = Field(foreign_key="user.id")
    name: str
    repo_url: str
    provider: str = "github"
    source: str = "user" # "personal" | "user"
    
    default_world_id: str
    summary_data: Dict = Field(default={}, sa_type=JSON) # Stack, languages
    
    sync_status: str = "pending"
    last_sync_at: Optional[datetime] = None
    
    owner: User = Relationship(back_populates="projects")

# --- KNOWLEDGE & RAG ---

class KnowledgeChunk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Metadata
    source_type: str  # "codex" | "repo"
    source_id: str    # filename or project_id
    chunk_index: int
    
    # The Content
    content: str
    
    # The Vector (768 dimensions is standard for Vertex/Gecko)
    embedding: List[float] = Field(sa_column=Column(Vector(768)))
