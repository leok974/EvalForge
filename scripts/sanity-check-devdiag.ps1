#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick sanity checks for DevDiag proxy integration
    
.DESCRIPTION
    Runs health check and diagnostic tests against local or remote EvalForge instance.
    Tests graceful degradation, rate limiting, and artifact URL handling.
    
.PARAMETER BaseUrl
    Base URL of EvalForge instance (default: http://127.0.0.1:19010)
    
.PARAMETER IncludeDiagnostic
    Also run a full diagnostic (may be slow)
    
.EXAMPLE
    # Quick health check only
    .\sanity-check-devdiag.ps1
    
.EXAMPLE
    # Health check + full diagnostic
    .\sanity-check-devdiag.ps1 -IncludeDiagnostic
    
.EXAMPLE
    # Test production deployment
    .\sanity-check-devdiag.ps1 -BaseUrl https://evalforge.app -IncludeDiagnostic
#>

param(
    [string]$BaseUrl = "http://127.0.0.1:19010",
    [switch]$IncludeDiagnostic
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          DevDiag Proxy Sanity Checks                          ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: $BaseUrl" -ForegroundColor Yellow
Write-Host ""

# Test 1: Health Check
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "✓ Test 1: Health Check" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$healthUrl = "$BaseUrl/api/ops/diag/health"
Write-Host "GET $healthUrl" -ForegroundColor DarkGray

try {
    $healthResponse = Invoke-RestMethod -Uri $healthUrl -Method Get -ErrorAction Stop
    
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    $healthResponse | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    if ($healthResponse.ok -eq $true) {
        Write-Host "✅ PASS: DevDiag is configured and healthy" -ForegroundColor Green
    } elseif ($healthResponse.ok -eq $false -and $healthResponse.message -match "not configured") {
        Write-Host "✅ PASS: Graceful degradation working (DevDiag not configured)" -ForegroundColor Green
        Write-Host "   Note: Set DEVDIAG_BASE to enable DevDiag functionality" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️  WARN: Unexpected health response" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ FAIL: Health check request failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 2: Full Diagnostic (optional)
if ($IncludeDiagnostic) {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "✓ Test 2: Full Diagnostic Run" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    $diagUrl = "$BaseUrl/api/ops/diag"
    $diagBody = @{
        url = $BaseUrl
        preset = "app"
    } | ConvertTo-Json
    
    Write-Host "POST $diagUrl" -ForegroundColor DarkGray
    Write-Host "Body: $diagBody" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Running diagnostic (this may take 30-90 seconds)..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        $diagResponse = Invoke-RestMethod -Uri $diagUrl -Method Post -ContentType "application/json" -Body $diagBody -ErrorAction Stop
        
        Write-Host "Response:" -ForegroundColor Cyan
        $diagResponse | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor White
        Write-Host ""
        
        if ($diagResponse.ok -eq $true) {
            Write-Host "✅ PASS: Diagnostic completed successfully" -ForegroundColor Green
            
            # Check for artifact URLs
            if ($diagResponse.playwright_report_url) {
                Write-Host "   📊 Playwright Report: $($diagResponse.playwright_report_url)" -ForegroundColor Cyan
            }
            if ($diagResponse.export_tar_url) {
                Write-Host "   📦 Export Archive: $($diagResponse.export_tar_url)" -ForegroundColor Cyan
            }
            if (-not $diagResponse.playwright_report_url -and -not $diagResponse.export_tar_url) {
                Write-Host "   Note: No artifact URLs in response" -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  WARN: Diagnostic returned ok=false" -ForegroundColor Yellow
            if ($diagResponse.error) {
                Write-Host "   Error: $($diagResponse.error)" -ForegroundColor Red
            }
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        
        if ($statusCode -eq 503) {
            Write-Host "✅ PASS: Graceful degradation (503 Service Unavailable)" -ForegroundColor Green
            Write-Host "   DevDiag server not configured - expected when DEVDIAG_BASE is unset" -ForegroundColor Yellow
        } elseif ($statusCode -eq 429) {
            Write-Host "✅ PASS: Rate limiting active (429 Too Many Requests)" -ForegroundColor Green
            Write-Host "   Wait 15 seconds before retrying" -ForegroundColor Yellow
        } else {
            Write-Host "❌ FAIL: Diagnostic request failed with HTTP $statusCode" -ForegroundColor Red
            Write-Host "   Error: $_" -ForegroundColor Red
        }
    }
    
    Write-Host ""
}

# Test 3: Rate Limiting (if diagnostic was run)
if ($IncludeDiagnostic -and $healthResponse.ok -eq $true) {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "✓ Test 3: Rate Limiting" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    Write-Host "Testing rate limit (immediate retry should fail with 429)..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        $diagUrl = "$BaseUrl/api/ops/diag"
        $diagBody = @{
            url = $BaseUrl
            preset = "app"
        } | ConvertTo-Json
        
        $null = Invoke-RestMethod -Uri $diagUrl -Method Post -ContentType "application/json" -Body $diagBody -ErrorAction Stop
        Write-Host "⚠️  WARN: Rate limiting may not be working (expected 429, got success)" -ForegroundColor Yellow
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        
        if ($statusCode -eq 429) {
            Write-Host "✅ PASS: Rate limiting working correctly (429 Too Many Requests)" -ForegroundColor Green
            Write-Host "   Rate limit: 6 requests/min, min 15s between requests" -ForegroundColor Cyan
        } else {
            Write-Host "⚠️  WARN: Unexpected status code $statusCode (expected 429)" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
}

# Summary
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

if ($healthResponse.ok -eq $true) {
    Write-Host "✅ DevDiag proxy is configured and operational" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Open Dev UI: $BaseUrl/dev-ui/" -ForegroundColor White
    Write-Host "  2. Click 'Run DevDiag' button" -ForegroundColor White
    Write-Host "  3. Check for artifact URLs in results" -ForegroundColor White
} else {
    Write-Host "⚠️  DevDiag proxy is not configured (graceful degradation active)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To enable DevDiag:" -ForegroundColor Cyan
    Write-Host "  1. Set DEVDIAG_BASE environment variable" -ForegroundColor White
    Write-Host "     Example: export DEVDIAG_BASE=https://devdiag.example.com" -ForegroundColor DarkGray
    Write-Host "  2. Set DEVDIAG_JWT if authentication required" -ForegroundColor White
    Write-Host "  3. Restart EvalForge backend" -ForegroundColor White
}

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   docs/DEVDIAG_SANITY_CHECKS.md     - Quick reference & rollout steps" -ForegroundColor White
Write-Host "   docs/devdiag.md                   - Integration guide" -ForegroundColor White
Write-Host "   docs/DEVDIAG_TROUBLESHOOTING.md   - Detailed troubleshooting" -ForegroundColor White
Write-Host ""
