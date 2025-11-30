"""
DevDiag HTTP Proxy Router

Proxies DevDiag diagnostic requests to external DevDiag HTTP server.
Keeps JWT tokens server-side, never exposes them to browser.

Environment variables:
- DEVDIAG_BASE: Required. Base URL of DevDiag HTTP server (e.g., http://127.0.0.1:8080)
- DEVDIAG_JWT: Optional. Bearer token for DevDiag authentication
"""

import logging
import os
import random
import time
from typing import Optional
from urllib.parse import urlparse
from collections import defaultdict
from dataclasses import dataclass, field

import httpx
from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ops", tags=["operations", "devdiag"])

# Import metrics
try:
    from arcade_app.metrics import (
        DEVDIAG_REQUESTS_TOTAL,
        DEVDIAG_DURATION_SECONDS,
        DEVDIAG_ERRORS_TOTAL
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    logger.warning("Prometheus metrics not available for DevDiag proxy")


# ============================================================================
# Rate Limiting: Token Bucket per IP/Session
# ============================================================================
@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""
    tokens: float = 6.0  # Max 6 requests
    last_refill: float = field(default_factory=time.time)
    last_request: float = 0.0  # Track last request for minimum interval
    
    def try_consume(self, rate: float = 6.0, interval: float = 60.0, min_interval: float = 15.0) -> bool:
        """
        Try to consume a token from the bucket.
        
        Args:
            rate: Tokens per interval (default: 6 tokens/min)
            interval: Refill interval in seconds (default: 60s)
            min_interval: Minimum seconds between requests (default: 15s)
            
        Returns:
            True if request is allowed, False if rate limited
        """
        now = time.time()
        
        # Check minimum interval (prevent double-click storms)
        if self.last_request > 0 and (now - self.last_request) < min_interval:
            return False
        
        # Refill tokens based on time elapsed
        elapsed = now - self.last_refill
        refill_amount = (elapsed / interval) * rate
        self.tokens = min(rate, self.tokens + refill_amount)
        self.last_refill = now
        
        # Try to consume a token
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            self.last_request = now
            return True
        
        return False


# Rate limiting state: key = IP:session_id
_rate_limit_buckets: dict[str, TokenBucket] = defaultdict(TokenBucket)


def _check_rate_limit(client_ip: str, session_id: str = "default") -> bool:
    """
    Check if request is within rate limits.
    
    Args:
        client_ip: Client IP address
        session_id: Session identifier
        
    Returns:
        True if allowed, False if rate limited
    """
    key = f"{client_ip}:{session_id}"
    bucket = _rate_limit_buckets[key]
    return bucket.try_consume(rate=6.0, interval=60.0, min_interval=15.0)

# Configuration from environment
DEVDIAG_BASE = os.getenv("DEVDIAG_BASE", "").rstrip("/")
DEVDIAG_JWT = os.getenv("DEVDIAG_JWT", "")

# Timeout configuration (production-ready)
CONNECT_TIMEOUT = 5.0    # 5s for connection
READ_TIMEOUT = 90.0      # 90s for reading response (diagnostics can be slow)
TIMEOUT = httpx.Timeout(connect=CONNECT_TIMEOUT, read=READ_TIMEOUT, write=5.0, pool=5.0)
MAX_RETRIES = 2  # Max retry attempts for 502/503/504

# SSRF protection: allowlist of permitted target hosts (production-locked)
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "evalforge.app",
    "evalforge.int",
}


def _is_allowed_target(url: str) -> bool:
    """
    Validate target URL against allowlist to prevent SSRF attacks.
    
    Args:
        url: Target URL to validate
        
    Returns:
        True if URL is allowed, False otherwise
    """
    try:
        parsed = urlparse(url)
        
        # Must have valid scheme
        if parsed.scheme not in {"http", "https"}:
            return False
        
        # Must have hostname in allowlist
        hostname = parsed.hostname
        if not hostname:
            return False
        
        return hostname in ALLOWED_HOSTS
        
    except Exception as e:
        logger.warning(f"Failed to parse target URL: {url} - {e}")
        return False


class DiagRequest(BaseModel):
    """Request to run DevDiag diagnostics."""
    
    url: str = Field(..., description="Target URL to diagnose")
    preset: str = Field(
        default="app",
        description="Diagnostic preset: chat, embed, app, or full"
    )
    tenant: str = Field(default="evalforge", description="Tenant identifier")


class DiagResponse(BaseModel):
    """Response from DevDiag diagnostics."""
    
    ok: bool = Field(..., description="Whether diagnostics completed successfully")
    result: Optional[dict] = Field(None, description="Diagnostic results")
    error: Optional[str] = Field(None, description="Error message if failed")


class HealthResponse(BaseModel):
    """Health check response."""
    
    ok: bool = Field(..., description="Whether DevDiag server is reachable")
    message: Optional[str] = Field(None, description="Status message")


@router.get("/diag/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check if DevDiag server is reachable.
    
    Returns:
        HealthResponse with ok=True if reachable, ok=False otherwise
    """
    if not DEVDIAG_BASE:
        return HealthResponse(
            ok=False,
            message="DEVDIAG_BASE not configured"
        )
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{DEVDIAG_BASE}/healthz")
            
            if response.status_code == 200:
                return HealthResponse(ok=True, message="DevDiag server is healthy")
            else:
                return HealthResponse(
                    ok=False,
                    message=f"DevDiag server returned {response.status_code}"
                )
                
    except httpx.TimeoutException:
        logger.warning("DevDiag health check timed out")
        return HealthResponse(ok=False, message="Health check timed out")
        
    except Exception as e:
        logger.error(f"DevDiag health check failed: {e}")
        return HealthResponse(ok=False, message=f"Health check failed: {str(e)}")


@router.post("/diag", response_model=DiagResponse)
async def run_diagnostic(
    request: DiagRequest,
    req: Request,
    x_request_id: Optional[str] = Header(None)
) -> DiagResponse:
    """
    Run DevDiag diagnostics on a target URL.
    
    Proxies the request to the DevDiag HTTP server, adding authentication
    and request tracking headers server-side.
    
    Rate limits: 6 requests per minute per IP/session, minimum 15s between requests.
    
    Args:
        request: Diagnostic request with URL and preset
        req: FastAPI request object for logging
        x_request_id: Optional request ID for tracing
        
    Returns:
        DiagResponse with diagnostic results or error
        
    Raises:
        HTTPException: 400 if target URL not allowed (SSRF protection),
                      429 if rate limited,
                      503 if DevDiag not configured, 504 on timeout,
                      or propagates 4xx/5xx from DevDiag server
    """
    # Rate limiting check
    client_ip = req.client.host if req.client else "unknown"
    session_id = x_request_id or "default"
    
    if not _check_rate_limit(client_ip, session_id):
        logger.warning(f"[DevDiag] Rate limited: ip={client_ip}, session={session_id}")
        if METRICS_AVAILABLE:
            DEVDIAG_REQUESTS_TOTAL.labels(status="rate_limited").inc()
            DEVDIAG_ERRORS_TOTAL.labels(reason="rate_limited").inc()
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait at least 15 seconds between requests (max 6/minute)."
        )
    
    if not DEVDIAG_BASE:
        raise HTTPException(
            status_code=503,
            detail="DevDiag server not configured. Set DEVDIAG_BASE environment variable."
        )
    
    # SSRF protection: validate target URL
    if not _is_allowed_target(request.url):
        logger.warning(f"[DevDiag] Rejected disallowed target URL: {request.url}")
        if METRICS_AVAILABLE:
            DEVDIAG_REQUESTS_TOTAL.labels(status="ssrf_blocked").inc()
            DEVDIAG_ERRORS_TOTAL.labels(reason="ssrf_blocked").inc()
        raise HTTPException(
            status_code=400,
            detail=f"Target URL not allowed. Permitted hosts: {', '.join(sorted(ALLOWED_HOSTS))}"
        )
    
    # Build headers (redact JWT in logs)
    headers = {"Content-Type": "application/json"}
    
    if DEVDIAG_JWT:
        headers["Authorization"] = f"Bearer {DEVDIAG_JWT}"
        jwt_log = f"Bearer {'*' * 8}..."  # Redacted for logging
    else:
        jwt_log = "none"
    
    if x_request_id:
        headers["X-Request-ID"] = x_request_id
    
    # Prepare request payload
    payload = {
        "url": request.url,
        "preset": request.preset,
        "tenant": request.tenant
    }
    
    logger.info(
        f"[DevDiag] Running diagnostic: target_url={request.url}, preset={request.preset}, "
        f"jwt={jwt_log}, request_id={x_request_id or 'none'}"
    )
    
    # Retry logic for upstream errors
    last_error = None
    start_time = time.time()
    
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                response = await client.post(
                    f"{DEVDIAG_BASE}/diag/run",
                    json=payload,
                    headers=headers
                )
                
                # Log upstream response
                duration = time.time() - start_time
                logger.info(
                    f"[DevDiag] Upstream response: status={response.status_code}, "
                    f"duration={duration:.2f}s, attempt={attempt + 1}/{MAX_RETRIES}"
                )
                
                # Handle successful response
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"[DevDiag] Diagnostic completed successfully for {request.url}")
                    
                    # Record metrics
                    if METRICS_AVAILABLE:
                        DEVDIAG_REQUESTS_TOTAL.labels(status="success").inc()
                        DEVDIAG_DURATION_SECONDS.observe(duration)
                    
                    return DiagResponse(
                        ok=True,
                        result=result
                    )
                
                # Retry on 502/503/504 (upstream errors)
                if response.status_code in {502, 503, 504} and attempt < MAX_RETRIES - 1:
                    # Exponential backoff with jitter
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"[DevDiag] Upstream error {response.status_code}, "
                        f"retrying in {backoff:.2f}s (attempt {attempt + 1}/{MAX_RETRIES})"
                    )
                    time.sleep(backoff)
                    continue
                
                # Handle rate limiting (429)
                if response.status_code == 429:
                    logger.warning(f"[DevDiag] Rate limited for {request.url}")
                    if METRICS_AVAILABLE:
                        DEVDIAG_REQUESTS_TOTAL.labels(status="bad_request").inc()
                        DEVDIAG_ERRORS_TOTAL.labels(reason="bad_request").inc()
                    raise HTTPException(
                        status_code=429,
                        detail="DevDiag rate limit exceeded. Please try again later."
                    )
                
                # Handle server busy (503) - final attempt
                if response.status_code == 503:
                    logger.warning(f"[DevDiag] Server busy for {request.url}")
                    if METRICS_AVAILABLE:
                        DEVDIAG_REQUESTS_TOTAL.labels(status="upstream_5xx").inc()
                        DEVDIAG_ERRORS_TOTAL.labels(reason="upstream_5xx").inc()
                    raise HTTPException(
                        status_code=503,
                        detail="DevDiag server is currently busy. Please try again later."
                    )
                
                # Propagate other errors
                error_detail = response.text[:500]  # Truncate long errors
                logger.error(
                    f"[DevDiag] Diagnostic failed: status={response.status_code}, "
                    f"detail={error_detail}"
                )
                if METRICS_AVAILABLE:
                    status_label = "upstream_5xx" if response.status_code >= 500 else "bad_request"
                    DEVDIAG_REQUESTS_TOTAL.labels(status=status_label).inc()
                    DEVDIAG_ERRORS_TOTAL.labels(reason=status_label).inc()
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"DevDiag server error: {error_detail}"
                )
                    
        except httpx.TimeoutException as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                backoff = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    f"[DevDiag] Timeout, retrying in {backoff:.2f}s "
                    f"(attempt {attempt + 1}/{MAX_RETRIES})"
                )
                time.sleep(backoff)
                continue
            
            logger.error(f"[DevDiag] Timeout after {TIMEOUT}s for {request.url}")
            if METRICS_AVAILABLE:
                DEVDIAG_REQUESTS_TOTAL.labels(status="timeout").inc()
                DEVDIAG_ERRORS_TOTAL.labels(reason="timeout").inc()
            raise HTTPException(
                status_code=504,
                detail=f"DevDiag diagnostic timed out after {TIMEOUT} seconds"
            )
            
        except httpx.HTTPError as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                backoff = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    f"[DevDiag] HTTP error, retrying in {backoff:.2f}s "
                    f"(attempt {attempt + 1}/{MAX_RETRIES}): {e}"
                )
                time.sleep(backoff)
                continue
            
            logger.error(f"[DevDiag] HTTP error: {e}")
            if METRICS_AVAILABLE:
                DEVDIAG_REQUESTS_TOTAL.labels(status="upstream_5xx").inc()
                DEVDIAG_ERRORS_TOTAL.labels(reason="connection_error").inc()
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to DevDiag server: {str(e)}"
            )
            
        except HTTPException:
            # Re-raise FastAPI exceptions immediately (don't retry)
            raise
            
        except Exception as e:
            logger.exception(f"[DevDiag] Unexpected error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal error during diagnostic: {str(e)}"
            )
    
    # Should not reach here, but handle it gracefully
    if last_error:
        raise HTTPException(
            status_code=503,
            detail=f"DevDiag request failed after {MAX_RETRIES} attempts: {str(last_error)}"
        )
    
    raise HTTPException(
        status_code=500,
        detail="Internal error: retry loop exhausted"
    )
