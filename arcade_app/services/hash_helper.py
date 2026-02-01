"""
Workspace and submission hashing utilities - canonical, stable hash computation.

Phase 8.x: Enables drift detection and replay debugging for boss submissions.
"""
import hashlib
import json
from typing import Dict, Any


def hash_submission(submission_data: Any) -> str:
    """
    Compute canonical hash of boss submission.
    
    Args:
        submission_data: Any JSON-serializable submission payload
    
    Returns:
        Hash string in format 'sha256:abcdef...'
    
    Example:
        >>> submission = {"code": "print('hello')", "metrics": {...}}
        >>> hash_submission(submission)
        'sha256:a1b2c3...'
    """
    # Canonical JSON (sorted keys)
    canonical_json = json.dumps(submission_data, sort_keys=True, separators=(',', ':'))
    hash_bytes = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    
    return f"sha256:{hash_bytes}"
