from __future__ import annotations
from pathlib import Path
import os
import json

def detect_codex_root(explicit: str | None = None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.exists():
            raise SystemExit(f"[codex] --codex-root not found: {p}")
        return p

    env = os.getenv("EF_CODEX_ROOT")
    if env:
        p = Path(env)
        if not p.exists():
            raise SystemExit(f"[codex] EF_CODEX_ROOT not found: {p}")
        return p

    # Check config file
    config_path = Path("configs/codex_config.json")
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                if "codex_root" in config:
                    p = Path(config["codex_root"])
                    if p.exists():
                        return p
        except Exception:
            pass

    candidates = [Path("docs/codex"), Path("data/codex")]
    for p in candidates:
        if p.exists():
            return p

    raise SystemExit(
        "[codex] No codex root found. Expected one of: docs/codex or data/codex. "
        "Set EF_CODEX_ROOT or pass --codex-root."
    )

def resolve_codex_ref(ref: str, codex_root: Path | None = None) -> str | None:
    """
    Resolve a Codex reference string (e.g. 'codex:glossary/python/foo') to a file path.
    Returns the absolute path as a string, or None if invalid ref format.
    Does NOT check if file exists (caller should do that).
    """
    if not ref or not ref.startswith("codex:"):
        return None
        
    if not codex_root:
        codex_root = detect_codex_root()
        
    clean_ref = ref.replace("codex:", "").strip()
    target_subpath = ""

    # Strategy 1: Legacy glossary/ -> world-X
    if clean_ref.startswith("glossary/"):
        parts = clean_ref.replace("glossary/", "").split("/")
        if len(parts) >= 1:
            world_part = parts[0]
            rest = parts[1:]
            
            # Fix double-prefix (e.g. glossary/world-agents -> world-world-agents)
            if world_part.startswith("world-"):
                final_world = world_part
            else:
                final_world = f"world-{world_part}"
                
            target_subpath = os.path.join(final_world, *rest) + ".md"
        else:
            return None
            
    # Strategy 2: Direct / Modern
    else:
        # e.g. "world-agents/agent-loop"
        if not clean_ref.endswith(".md"):
            target_subpath = clean_ref + ".md"
        else:
            target_subpath = clean_ref

    return str(codex_root / target_subpath)
