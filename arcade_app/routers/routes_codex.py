"""
Phase 9.1: Codex API Router
Provides safe read-only access to Codex markdown documentation.
"""
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
import re
import frontmatter

router = APIRouter(prefix="/api/codex", tags=["codex"])

# Codex root directory
CODEX_ROOT = Path("docs/codex")

# Allowed root directories
ALLOWED_ROOTS = {"glossary", "concepts", "patterns", "react", "world-agents", "world-cli", "world-git", "world-infra", "world-java", "world-ml", "world-node", "world-python", "world-react", "world-sql", "world-typescript"}

# Safe path segment regex (alphanumeric, hyphens, underscores, slashes)
SAFE_PATH_REGEX = re.compile(r"^[a-zA-Z0-9/_-]+$")


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
    Follows 'redirect_to' in frontmatter if present.
    """
    # Max recursion depth for redirects
    MAX_REDIRECTS = 5
    current_ref = ref
    visited_refs = set()
    
    for _ in range(MAX_REDIRECTS):
        if current_ref in visited_refs:
            raise HTTPException(500, f"Circular redirect detected: {current_ref}")
        visited_refs.add(current_ref)

        # Validate and resolve ref
        file_path = validate_and_resolve_ref(current_ref)
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(404, f"Codex entry not found: {current_ref}")
        
        # Read and parse frontmatter
        try:
            post = frontmatter.load(file_path)
        except Exception as e:
            raise HTTPException(500, f"Failed to parse codex entry {current_ref}: {str(e)}")
            
        # Check for redirect
        redirect_target = post.metadata.get("redirect_to")
        if redirect_target:
            # Ensure target has prefix
            if not redirect_target.startswith("codex:"):
                 redirect_target = f"codex:{redirect_target}"
            current_ref = redirect_target
            continue
            
        # Found real content
        # Extract title if not in metadata
        title = post.metadata.get("title")
        if not title:
            title = extract_title_from_markdown(post.content)
        if not title:
            title = file_path.stem.replace("-", " ").title()
            
        return {
            "ref": ref, # Return original ref so client knows what it asked for? Or canonical?
                        # Usually better to return canonical ref in metadata, but client might expect original.
                        # Let's return the content of the canonical, but maybe hint it resolved?
            "canonical_ref": current_ref, 
            "title": title,
            "md": post.content,
            "path": str(file_path.relative_to(Path.cwd())),
            "metadata": post.metadata
        }
    
    raise HTTPException(500, "Too many redirects")

@router.get("/index/structure")
async def get_codex_index():
    """
    Get structure of Codex for navigation/filtering.
    Excludes pages that are redirects.
    """
    index = []
    
    if not CODEX_ROOT.exists():
        return {"sections": []}

    structure = {}
    
    # World name normalization (short name -> canonical world ID)
    def normalize_world_name(world: str) -> str:
        """Normalize world name to canonical form (e.g. 'python' -> 'world-python')"""
        if not world:
            return "unknown"
        # If already prefixed, return as-is
        if world.startswith("world-"):
            return world
        # Map short names to canonical IDs
        world_map = {
            "python": "world-python",
            "sql": "world-sql",
            "node": "world-node",
            "java": "world-java",
            "typescript": "world-typescript",
            "ts": "world-typescript",
            "js": "world-js",
            "react": "world-react",
            "infra": "world-infra",
            "git": "world-git",
            "agents": "world-agents",
            "ml": "world-ml",
            "web": "world-web",
            "cli": "world-cli"
        }
        return world_map.get(world, world)
    
    for world_dir in CODEX_ROOT.iterdir():
        if not world_dir.is_dir() or world_dir.name not in ALLOWED_ROOTS:
            continue
            
        world_name = world_dir.name
        
        # Index root-level files (e.g., boss files, README)
        for page_file in world_dir.glob("*.md"):
            page_id = f"{world_name}/{page_file.stem}"
            
            try:
                post = frontmatter.load(page_file)
                if post.metadata.get("redirect_to"):
                     continue
                     
                title = post.metadata.get("title")
                if not title:
                    title = post.metadata.get("id") or page_file.stem
                
                # Normalize world from metadata or use directory name
                # Check both 'world' and 'world_id' keys
                meta_world = post.metadata.get("world") or post.metadata.get("world_id")
                if not meta_world:
                    # If no world metadata and we're in glossary dir, infer from section
                    if world_name == "glossary":
                        meta_world = section_name  # e.g., "node", "python", "java"
                    else:
                        meta_world = world_name
                normalized_world = normalize_world_name(meta_world)
                    
                if normalized_world not in structure:
                    structure[normalized_world] = []
                    
                structure[normalized_world].append({
                    "id": page_id,
                    "title": title,
                    "world": normalized_world,
                    "section": "General"  # Root-level file
                })
            except Exception:
                pass
        
        # Index subdirectory files
        for section_dir in world_dir.iterdir():
            if not section_dir.is_dir():
                continue
                
            section_name = section_dir.name
            
            pages = []
            # Use rglob to recursively find all .md files in subdirectories
            for page_file in section_dir.rglob("*.md"):
                # Calculate relative path for ID
                rel_path = page_file.relative_to(world_dir)
                page_id = f"{world_name}/{rel_path.as_posix()[:-3]}"  # Remove .md extension
                
                # Check for redirect - skip if present
                try:
                    # We use frontmatter.load (lazy check would be better for perf but this is robust)
                    post = frontmatter.load(page_file)
                    if post.metadata.get("redirect_to"):
                         continue
                         
                    title = post.metadata.get("title")
                    if not title:
                         title = extract_title_from_markdown(post.content)
                    if not title:
                         title = page_file.stem.replace("-", " ").title()
                    
                    # Normalize world from metadata or use directory name
                    # Check both 'world' and 'world_id' keys
                    meta_world = post.metadata.get("world") or post.metadata.get("world_id")
                    if not meta_world:
                        # If no world metadata and we're in glossary dir, infer from section
                        if world_name == "glossary":
                            meta_world = section_name  # e.g., "node", "python", "java"
                        else:
                            meta_world = world_name
                    normalized_world = normalize_world_name(meta_world)
                         
                    pages.append({
                        "id": page_id,
                        "title": title,
                        "world": normalized_world,
                        "section": section_name
                    })
                except:
                    continue
            
            if pages:
                # Group pages by their normalized world (not directory structure)
                pages_by_world = {}
                for page in pages:
                    world = page["world"]
                    if world not in pages_by_world:
                        pages_by_world[world] = []
                    pages_by_world[world].append(page)
                
                # Add each world group as a separate section
                for world, world_pages in pages_by_world.items():
                    index.append({
                        "world": world,
                        "section": section_name,
                        "pages": sorted(world_pages, key=lambda x: x["title"])
                    })
    
    # Add root-level files to index
    for world_name, pages in structure.items():
        if pages:
            index.append({
                "world": world_name,
                "section": "General",
                "pages": sorted(pages, key=lambda x: x["title"])
            })
                
    return {"sections": index}
