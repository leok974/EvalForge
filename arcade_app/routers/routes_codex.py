"""
Phase 9.1: Codex API Router
Provides safe read-only access to Codex markdown documentation.
"""
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
import re

router = APIRouter(prefix="/api/codex", tags=["codex"])

# Codex root directory
CODEX_ROOT = Path("docs/codex")

# Allowed root directories
ALLOWED_ROOTS = {"glossary", "concepts", "patterns", "react", "world-agents", "world-cli", "world-git", "world-infra", "world-java", "world-ml", "world-node", "world-python", "world-react", "world-sql", "world-typescript"}

# Safe path segment regex (alphanumeric, hyphens, underscores, slashes)
SAFE_PATH_REGEX = re.compile(r"^[a-z0-9/_-]+$")


def validate_and_resolve_ref(ref: str) -> Path:
    """
    Validate codex reference and resolve to safe file path.
    
    Args:
        ref: Codex reference (e.g., "codex:glossary/python/print")
        
    Returns:
        Resolved Path object
        
    Raises:
        HTTPException: If ref is invalid or unsafe
        
    Security:
        - Only allows refs with prefix "codex:"
        - Only allows roots: glossary, concepts, patterns
        - Rejects path traversal (.., //, leading /, backslashes)
        - Ensures resolved path stays within CODEX_ROOT
    """
    # Must start with "codex:"
    if not ref.startswith("codex:"):
        raise HTTPException(400, f"Invalid ref format: must start with 'codex:'")
    
    # Remove prefix
    path_part = ref[6:]  # Remove "codex:"
    
    # Check for dangerous patterns
    if ".." in path_part or "\\" in path_part or path_part.startswith("/"):
        raise HTTPException(400, f"Invalid ref: path traversal not allowed")
    
    if "//" in path_part:
        raise HTTPException(400, f"Invalid ref: double slashes not allowed")
    
    # Validate path format
    if not SAFE_PATH_REGEX.match(path_part):
        raise HTTPException(400, f"Invalid ref: contains unsafe characters")
    
    # Split and validate root
    parts = path_part.split("/", 1)
    if not parts:
        raise HTTPException(400, f"Invalid ref: empty path")
    
    root = parts[0]
    if root not in ALLOWED_ROOTS:
        raise HTTPException(400, f"Invalid ref: root must be one of {ALLOWED_ROOTS}")
    
    # Build path
    full_path = CODEX_ROOT / f"{path_part}.md"
    
    # Resolve to absolute path and ensure it's within CODEX_ROOT
    try:
        resolved = full_path.resolve()
        codex_root_resolved = CODEX_ROOT.resolve()
        
        # Check if resolved path is within codex root
        if not str(resolved).startswith(str(codex_root_resolved)):
            raise HTTPException(400, f"Invalid ref: path escape attempt")
    except Exception as e:
        raise HTTPException(400, f"Invalid ref: {str(e)}")
    
    return resolved


def extract_title_from_markdown(md_content: str) -> Optional[str]:
    """
    Extract title from markdown (first H1).
    
    Args:
        md_content: Markdown content
        
    Returns:
        Title string or None
    """
    lines = md_content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


@router.get("")
async def get_codex_entry(ref: str = Query(..., description="Codex reference (e.g., codex:glossary/python/print)")):
    """
    Fetch Codex markdown entry by reference.
    
    Args:
        ref: Codex reference string
        
    Returns:
        JSON with title, markdown content, and path
        
    Example:
        GET /api/codex?ref=codex:glossary/python/print
        
        Response:
        {
            "ref": "codex:glossary/python/print",
            "title": "print()",
            "md": "# print()\\n\\n**Definition**: ...",
            "path": "data/codex/glossary/python/print.md"
        }
    """
    # Validate and resolve ref
    file_path = validate_and_resolve_ref(ref)
    
    # Check if file exists
    if not file_path.exists():
        raise HTTPException(404, f"Codex entry not found: {ref}")
    
    # Read markdown content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except Exception as e:
        raise HTTPException(500, f"Failed to read codex entry: {str(e)}")
    
    # Extract title
    title = extract_title_from_markdown(md_content)
    if not title:
        # Fallback to last path segment
        title = file_path.stem.replace("-", " ").title()
    
    return {
        "ref": ref,
        "title": title,
        "md": md_content,
        "path": str(file_path.relative_to(Path.cwd()))
    }
