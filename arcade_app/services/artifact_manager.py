import os
import shutil
import uuid
from pathlib import Path
from typing import List, Dict, Any

STORAGE_ROOT = Path("d:/EvalForge/storage/artifacts")

def ensure_storage():
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

def save_artifact(attempt_id: str, filename: str, source_path: Path) -> str:
    """
    Saves a file to the persistent artifact store and returns the relative URL/path.
    """
    ensure_storage()
    attempt_dir = STORAGE_ROOT / attempt_id
    attempt_dir.mkdir(exist_ok=True)
    
    dest_path = attempt_dir / filename
    shutil.copy2(source_path, dest_path)
    
    # Return a path relative to STORAGE_ROOT or a full API URL
    return f"/api/artifacts/{attempt_id}/{filename}"

def get_artifact_path(attempt_id: str, filename: str) -> Path:
    return STORAGE_ROOT / attempt_id / filename
