import re
import os

MAX_WORKSPACE_FILES = 40
MAX_FILE_BYTES = 60_000
MAX_TOTAL_BYTES = 300_000
MAX_PATH_BYTES = 200

# Strict allowlist: alphanum, dot, underscore, hyphen, forward slash.
# No backslashes, no spaces, no other symbols.
PATH_ALLOWLIST_REGEX = re.compile(r"^[a-zA-Z0-9._/-]+$")

def safe_relpath(path: str) -> str:
    """
    Normalizes and validates a relative path.
    Raises ValueError if path is unsafe or invalid.
    """
    if not path:
        raise ValueError("Path cannot be empty")
    
    # 1. Length check
    if len(path.encode('utf-8')) > MAX_PATH_BYTES:
        raise ValueError(f"Path too long (max {MAX_PATH_BYTES} bytes)")

    # 2. Basic character check (strict regex)
    if not PATH_ALLOWLIST_REGEX.match(path):
        raise ValueError(f"Path contains invalid characters: {path}")

    # 3. Traversal check
    # Split into segments and ensure no '..'
    segments = path.split('/')
    for seg in segments:
        if seg == '..' or seg == '.':
            raise ValueError(f"Path traversal detected: {path}")
        if not seg: 
            # Empty segment means double slash or leading/trailing slash (if split by /)
            # We reject absolute paths (leading /) or empty segments.
            # But wait, allowlist regex ^[...]+$ implies non-empty. 
            # If path is "/foo", split -> ['', 'foo']. First seg empty.
            pass

    if path.startswith('/'):
         raise ValueError(f"Path must be relative (cannot start with /): {path}")
    
    if '//' in path:
         raise ValueError(f"Path contains empty segments: {path}")

    return path

def validate_workspace_limits(files: list[dict]):
    """
    Validates workspace file limits (count, individual size, total size).
    files: list of dicts with 'path' and 'content'.
    Raises ValueError with structured details if limits exceeded.
    """
    if len(files) > MAX_WORKSPACE_FILES:
        raise ValueError(f"Too many files (max {MAX_WORKSPACE_FILES})")

    total_bytes = 0
    for f in files:
        content = f.get("content", "")
        # Content might be str or bytes? consistently handling str (utf-8 len)
        c_len = len(content.encode('utf-8')) if isinstance(content, str) else len(content)
        
        if c_len > MAX_FILE_BYTES:
            raise ValueError(f"File '{f.get('path')}' too large ({c_len} > {MAX_FILE_BYTES} bytes)")
        
        total_bytes += c_len

    if total_bytes > MAX_TOTAL_BYTES:
        raise ValueError(f"Total workspace size exceeded ({total_bytes} > {MAX_TOTAL_BYTES} bytes)")

def sanitize_logs(logs: str) -> str:
    """
    Sanitizes logs by removing absolute paths and other sensitive info.
    """
    if not logs:
        return ""
        
    # 1. Normalize line endings
    logs = logs.replace('\r\n', '\n')
    
    # 2. Strip standard absolute paths (e.g. /workspace/, /tmp/, D:\...)
    # We want to keep the relative part usually, or just hide the prefix.
    # Simple regex for /workspace/ substitute to nothing or <workspace>
    # Note: Docker runner uses /workspace.
    
    logs = re.sub(r'/(?:tmp|workspace)/+', '', logs)
    
    # Also strip common windows paths if visible (D:\EvalForge...)
    # This is harder to genericize, but capturing drive letters matches
    logs = re.sub(r'[a-zA-Z]:\\[^ \n"]*\\', '', logs)
    
    return logs

