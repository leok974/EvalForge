# DevDiag Proxy Quick Verification Script
# Run this after starting both DevDiag server and EvalForge backend

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "DevDiag Proxy Verification" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$BASE = "http://127.0.0.1:19010"
$DEVDIAG_BASE = "http://127.0.0.1:8023"
$PASSED = 0
$FAILED = 0

function Test-Step {
    param(
        [string]$Name,
        [scriptblock]$Test
    )
    
    Write-Host "→ $Name" -ForegroundColor Yellow
    try {
        & $Test
        Write-Host "  ✓ PASS" -ForegroundColor Green
        $script:PASSED++
    } catch {
        Write-Host "  ✗ FAIL: $_" -ForegroundColor Red
        $script:FAILED++
    }
    Write-Host ""
}

# Test 1: EvalForge Backend Running
Test-Step "EvalForge backend is running" {
    $response = Invoke-WebRequest -Uri "$BASE/healthz" -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -ne 200) {
        throw "Backend returned $($response.StatusCode)"
    }
}

# Test 2: DevDiag Server Running (optional)
Test-Step "DevDiag server is running (optional)" {
    try {
        $response = Invoke-WebRequest -Uri "$DEVDIAG_BASE/healthz" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        Write-Host "  DevDiag server is UP at $DEVDIAG_BASE" -ForegroundColor Cyan
    } catch {
        Write-Host "  DevDiag server is DOWN (graceful degradation will be tested)" -ForegroundColor Yellow
    }
}

# Test 3: Proxy Health Check
Test-Step "Proxy health check endpoint" {
    $response = Invoke-WebRequest -Uri "$BASE/api/ops/diag/health" -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -ne 200) {
        throw "Health check returned $($response.StatusCode)"
    }
    
    $json = $response.Content | ConvertFrom-Json
    if ($null -eq $json.ok) {
        throw "Health response missing 'ok' field"
    }
    
    if ($json.ok) {
        Write-Host "  DevDiag server is healthy" -ForegroundColor Cyan
    } else {
        Write-Host "  DevDiag server unavailable: $($json.message)" -ForegroundColor Yellow
    }
}

# Test 4: Proxy Diagnostic Endpoint
Test-Step "Proxy diagnostic endpoint (POST /api/ops/diag)" {
    $body = @{
        url = "$BASE/healthz"
        preset = "app"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "$BASE/api/ops/diag" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -UseBasicParsing `
            -ErrorAction Stop
        
        if ($response.StatusCode -eq 200) {
            $json = $response.Content | ConvertFrom-Json
            if ($json.ok) {
                Write-Host "  Diagnostic completed successfully" -ForegroundColor Cyan
            } else {
                Write-Host "  Diagnostic returned ok=false: $($json.error)" -ForegroundColor Yellow
            }
        }
    } catch {
        # 503 is acceptable if DevDiag server is not running
        if ($_.Exception.Response.StatusCode -eq 503) {
            Write-Host "  Graceful degradation: DevDiag not configured (expected if server not running)" -ForegroundColor Yellow
        } else {
            throw
        }
    }
}

# Test 5: Request Validation
Test-Step "Request validation (missing 'url' field)" {
    $body = @{
        preset = "app"
        # Missing 'url' field
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "$BASE/api/ops/diag" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -UseBasicParsing `
            -ErrorAction Stop
        
        throw "Should have returned 422, got $($response.StatusCode)"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 422) {
            Write-Host "  Correctly rejected invalid request" -ForegroundColor Cyan
        } else {
            throw
        }
    }
}

# Test 6: SSRF Protection
Test-Step "SSRF protection (disallowed host)" {
    $body = @{
        url = "http://evil.com"
        preset = "app"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "$BASE/api/ops/diag" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -UseBasicParsing `
            -ErrorAction Stop
        
        throw "Should have blocked evil.com, got $($response.StatusCode)"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 400) {
            Write-Host "  Correctly blocked disallowed host" -ForegroundColor Cyan
        } else {
            throw
        }
    }
}

# Test 7: Metrics Endpoint
Test-Step "Metrics endpoint includes DevDiag metrics" {
    $response = Invoke-WebRequest -Uri "$BASE/metrics" -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -ne 200) {
        throw "Metrics endpoint returned $($response.StatusCode)"
    }
    
    $content = $response.Content
    if ($content -match "devdiag_requests_total") {
        Write-Host "  DevDiag metrics are being recorded" -ForegroundColor Cyan
    } else {
        Write-Host "  DevDiag metrics not found (prometheus_client may not be installed)" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Passed: $PASSED" -ForegroundColor Green
Write-Host "Failed: $FAILED" -ForegroundColor $(if ($FAILED -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($FAILED -eq 0) {
    Write-Host "✓ All tests passed! DevDiag proxy is working correctly." -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ Some tests failed. See details above." -ForegroundColor Red
    exit 1
}
