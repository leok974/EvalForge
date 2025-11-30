#!/usr/bin/env bash
# DevDiag Smoke Test
# 
# Quick validation script for local DevDiag HTTP proxy integration.
# Tests health check and diagnostic endpoints without requiring
# a running DevDiag server (validates graceful degradation).
#
# Usage:
#   ./scripts/devdiag-smoke.sh [BASE_URL]
#
# Examples:
#   ./scripts/devdiag-smoke.sh
#   ./scripts/devdiag-smoke.sh http://127.0.0.1:19010

set -euo pipefail

# Configuration
BASE_URL="${1:-http://127.0.0.1:19010}"
HEALTH_ENDPOINT="$BASE_URL/api/ops/diag/health"
DIAG_ENDPOINT="$BASE_URL/api/ops/diag"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

test_passed() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

test_failed() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

# Test 1: Health Check Endpoint
test_health_check() {
    log_info "Testing health check endpoint..."
    
    HTTP_CODE=$(curl -s -o /tmp/devdiag-health.json -w "%{http_code}" "$HEALTH_ENDPOINT")
    
    if [[ "$HTTP_CODE" == "200" ]]; then
        test_passed "Health endpoint returns 200"
        
        # Validate response structure
        if jq -e '.ok' /tmp/devdiag-health.json > /dev/null 2>&1; then
            test_passed "Health response has 'ok' field"
            
            OK=$(jq -r '.ok' /tmp/devdiag-health.json)
            if [[ "$OK" == "false" ]]; then
                MESSAGE=$(jq -r '.message' /tmp/devdiag-health.json)
                log_warn "DevDiag server not available: $MESSAGE"
                test_passed "Health check gracefully reports unavailable server"
            else
                log_info "DevDiag server is healthy"
                test_passed "Health check reports healthy server"
            fi
        else
            test_failed "Health response missing 'ok' field"
        fi
    else
        test_failed "Health endpoint returned $HTTP_CODE (expected 200)"
    fi
    
    echo ""
}

# Test 2: Diagnostic Endpoint (without DevDiag server)
test_diagnostic_endpoint_no_server() {
    log_info "Testing diagnostic endpoint (no DEVDIAG_BASE)..."
    
    # Only test if health check showed no server configured
    OK=$(jq -r '.ok' /tmp/devdiag-health.json 2>/dev/null || echo "unknown")
    
    if [[ "$OK" == "false" ]]; then
        HTTP_CODE=$(curl -s -o /tmp/devdiag-result.json -w "%{http_code}" \
            -X POST "$DIAG_ENDPOINT" \
            -H "Content-Type: application/json" \
            -d '{"url":"https://example.com","preset":"app"}')
        
        if [[ "$HTTP_CODE" == "503" ]]; then
            test_passed "Diagnostic endpoint returns 503 when server not configured"
            
            # Validate error message
            if jq -e '.detail' /tmp/devdiag-result.json > /dev/null 2>&1; then
                DETAIL=$(jq -r '.detail' /tmp/devdiag-result.json)
                if [[ "$DETAIL" == *"not configured"* ]]; then
                    test_passed "Error message mentions configuration issue"
                else
                    test_failed "Error message unclear: $DETAIL"
                fi
            else
                test_failed "503 response missing 'detail' field"
            fi
        else
            test_failed "Diagnostic endpoint returned $HTTP_CODE (expected 503)"
        fi
    else
        log_info "Skipping no-server test (DevDiag server is configured)"
    fi
    
    echo ""
}

# Test 3: Diagnostic Endpoint Schema Validation
test_diagnostic_request_validation() {
    log_info "Testing diagnostic request validation..."
    
    # Test 1: Missing 'url' field
    HTTP_CODE=$(curl -s -o /tmp/devdiag-validation.json -w "%{http_code}" \
        -X POST "$DIAG_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d '{"preset":"app"}')
    
    if [[ "$HTTP_CODE" == "422" ]]; then
        test_passed "Returns 422 for missing 'url' field"
    else
        test_failed "Expected 422 for missing 'url', got $HTTP_CODE"
    fi
    
    # Test 2: Invalid JSON
    HTTP_CODE=$(curl -s -o /tmp/devdiag-validation.json -w "%{http_code}" \
        -X POST "$DIAG_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d 'not valid json')
    
    if [[ "$HTTP_CODE" == "422" ]]; then
        test_passed "Returns 422 for invalid JSON"
    else
        test_failed "Expected 422 for invalid JSON, got $HTTP_CODE"
    fi
    
    echo ""
}

# Test 4: Check Router Mounting
test_router_mounting() {
    log_info "Testing router mounting in FastAPI app..."
    
    # Check if /api/ops/diag is accessible (should return 405 for GET, not 404)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$DIAG_ENDPOINT")
    
    if [[ "$HTTP_CODE" == "405" ]]; then
        test_passed "Router mounted (GET not allowed, POST expected)"
    elif [[ "$HTTP_CODE" == "404" ]]; then
        test_failed "Router not mounted (404 Not Found)"
    else
        log_warn "Unexpected response: $HTTP_CODE"
    fi
    
    echo ""
}

# Main execution
main() {
    echo ""
    log_info "======================================"
    log_info "DevDiag HTTP Proxy Smoke Test"
    log_info "======================================"
    log_info "Target: $BASE_URL"
    echo ""
    
    # Verify backend is running
    if ! curl -s "$BASE_URL/healthz" > /dev/null 2>&1; then
        log_error "Backend not reachable at $BASE_URL"
        log_error "Start EvalForge backend first: cd apps/api && uvicorn main:app"
        exit 1
    fi
    
    log_info "Backend is running"
    echo ""
    
    # Run tests
    test_health_check
    test_diagnostic_endpoint_no_server
    test_diagnostic_request_validation
    test_router_mounting
    
    # Summary
    log_info "======================================"
    log_info "Test Summary"
    log_info "======================================"
    echo -e "${GREEN}Passed:${NC} $PASSED"
    echo -e "${RED}Failed:${NC} $FAILED"
    echo ""
    
    if [[ $FAILED -eq 0 ]]; then
        log_info "All tests passed! ✓"
        exit 0
    else
        log_error "Some tests failed. See details above."
        exit 1
    fi
}

# Run main
main "$@"
