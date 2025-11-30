"""
Operations and diagnostics router for EvalForge.
Provides admin endpoints for running DevDiag and other operational tasks.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import logging

from arcade_app.devdiag_client import devdiag_quickcheck

log = logging.getLogger(__name__)

router = APIRouter(prefix="/ops", tags=["ops"])


def admin_required():
    """
    Admin authentication check.
    
    TODO: Replace with your real admin guard when ready.
    For now, this is a passthrough for development.
    
    In production, you might check:
    - JWT token with admin role
    - API key from headers
    - IP allowlist
    """
    return True


class DiagRequest(BaseModel):
    """Request payload for diagnostic check."""
    target_url: HttpUrl
    preset: str = "app"  # app, embed, chat, or full
    tenant: Optional[str] = "evalforge"


class DiagResponse(BaseModel):
    """Response from diagnostic check."""
    ok: bool
    devdiag: dict


@router.post("/diag", response_model=DiagResponse)
async def diag_now(
    req: DiagRequest,
    _=Depends(admin_required)
):
    """
    Run DevDiag diagnostic check on a target URL.
    
    This endpoint calls the MCP DevDiag server to perform automated
    diagnostics including:
    - CSP policy validation
    - Embed compatibility checks
    - Chat/streaming validation
    - Portal detection
    - Performance metrics
    
    Args:
        req: Diagnostic request with target URL and preset
    
    Returns:
        DiagResponse with diagnostic results
    
    Raises:
        HTTPException: If DevDiag server fails or returns error
    """
    try:
        log.info(f"Running DevDiag: url={req.target_url} preset={req.preset}")
        
        result = await devdiag_quickcheck(
            url=str(req.target_url),
            preset=req.preset,
            tenant=req.tenant or "evalforge"
        )
        
        log.info(f"DevDiag completed successfully for {req.target_url}")
        
        return DiagResponse(
            ok=True,
            devdiag=result
        )
    
    except Exception as e:
        log.error(f"DevDiag failed for {req.target_url}: {e}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"DevDiag failed: {str(e)}"
        )


@router.get("/health")
async def ops_health():
    """
    Health check for operations endpoints.
    
    Returns basic status information about the ops router.
    """
    return {
        "status": "healthy",
        "router": "ops",
        "endpoints": ["/ops/diag", "/ops/health"]
    }
