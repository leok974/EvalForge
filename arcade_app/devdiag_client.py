"""
MCP DevDiag client for EvalForge.
Provides async helpers to call the DevDiag MCP server for diagnostics.
"""
import os
import httpx
from typing import Optional

# DevDiag server configuration
DEVDIAG_BASE = os.getenv("DEVDIAG_BASE", "http://localhost:8023")
DEVDIAG_JWT = os.getenv("DEVDIAG_JWT", "")


async def devdiag_quickcheck(
    url: str,
    preset: str = "app",
    tenant: str = "evalforge"
) -> dict:
    """
    Run a quick diagnostic check on a URL.
    
    Args:
        url: Target URL to diagnose
        preset: Diagnostic preset (app, embed, chat, full)
        tenant: Tenant identifier for multi-tenant setups
    
    Returns:
        dict: DevDiag response with diagnostic results
    
    Raises:
        httpx.HTTPError: If the DevDiag server returns an error
    """
    headers = {"Content-Type": "application/json"}
    
    # Add JWT token if configured (for production RBAC)
    if DEVDIAG_JWT:
        headers["Authorization"] = f"Bearer {DEVDIAG_JWT}"
    
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f"{DEVDIAG_BASE}/mcp/diag/quickcheck",
            headers=headers,
            json={
                "url": url,
                "preset": preset,
                "tenant": tenant
            }
        )
        response.raise_for_status()
        return response.json()


async def devdiag_remediation(
    problem_code: str,
    fix_code: str,
    confidence: float = 0.9,
    tenant: str = "evalforge"
) -> dict:
    """
    Record a successful remediation for DevDiag learning.
    
    Args:
        problem_code: Problem code (e.g., CSP_INLINE_BLOCKED)
        fix_code: Fix code (e.g., FIX_CSP_NONCE)
        confidence: Confidence score (0.0-1.0)
        tenant: Tenant identifier
    
    Returns:
        dict: DevDiag response
    
    Raises:
        httpx.HTTPError: If the DevDiag server returns an error
    """
    headers = {"Content-Type": "application/json"}
    
    # Remediation requires operator JWT (write permission)
    operator_jwt = os.getenv("DEVDIAG_OPERATOR_JWT", DEVDIAG_JWT)
    if operator_jwt:
        headers["Authorization"] = f"Bearer {operator_jwt}"
    
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f"{DEVDIAG_BASE}/mcp/diag/remediation",
            headers=headers,
            json={
                "tenant": tenant,
                "problem_code": problem_code,
                "fix_code": fix_code,
                "confidence": confidence
            }
        )
        response.raise_for_status()
        return response.json()
