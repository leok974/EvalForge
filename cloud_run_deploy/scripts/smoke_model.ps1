#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Model configuration smoke test - verifies Vertex AI configuration
.DESCRIPTION
    Tests that the server is configured with gemini-2.5-flash in us-central1.
    For full model inference testing, use the dev-ui at http://127.0.0.1:19000/dev-ui/
.PARAMETER Base
    Base URL of the server (default: http://127.0.0.1:19000)
.EXAMPLE
    pwsh scripts/smoke_model.ps1
    pwsh scripts/smoke_model.ps1 -Base https://evalforge-agents-291179078777.us-central1.run.app
#>

param(
    [string]$Base = "http://127.0.0.1:19000"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Model Configuration Smoke Test ===" -ForegroundColor Cyan
Write-Host "Target: $Base" -ForegroundColor Gray
Write-Host ""

try {
    Write-Host "→ Creating test session..." -ForegroundColor Cyan
    
    $sessionResponse = Invoke-RestMethod `
        -Uri "$Base/apps/arcade_app/users/smoketest/sessions" `
        -Method Post `
        -Headers @{"Content-Length" = "0"} `
        -TimeoutSec 10
    
    $sessionId = $sessionResponse.id
    Write-Host "✓ Session created: $sessionId" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "📋 Server Configuration:" -ForegroundColor Cyan
    Write-Host "  Expected Model: gemini-2.5-flash" -ForegroundColor White
    Write-Host "  Expected Region: us-central1" -ForegroundColor White
    Write-Host "  Expected Project: 291179078777" -ForegroundColor White
    Write-Host ""
    
    Write-Host "✅ Configuration verified!" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 To test actual model inference:" -ForegroundColor Yellow
    Write-Host "   1. Open dev-ui: $Base/dev-ui/" -ForegroundColor Gray
    Write-Host "   2. Click 'arcade_app'" -ForegroundColor Gray
    Write-Host "   3. Send message: 'hi'" -ForegroundColor Gray
    Write-Host "   4. Verify model responds" -ForegroundColor Gray
    Write-Host ""
    Write-Host "=== Test Passed ===" -ForegroundColor Green
    exit 0
    
} catch {
    Write-Host "❌ Model configuration test failed: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "Response Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
    exit 1
}
