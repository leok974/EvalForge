# Model Smoke Test - Tests actual LLM generation (not just endpoint health)
param(
    [ValidateSet("local", "prod")]
    [string]$Env = "local",
    [string]$ProdBase = "https://evalforge-agents-291179078777.us-central1.run.app"
)

$ErrorActionPreference = "Stop"

$base = if ($Env -eq "local") { "http://127.0.0.1:19000" } else { $ProdBase }

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🤖 MODEL SMOKE TEST - $Env" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Base URL: $base`n" -ForegroundColor Gray

# Test 1: Create session
Write-Host "→ Creating session..." -ForegroundColor Cyan
try {
    $sessionResponse = Invoke-RestMethod -Uri "$base/apps/arcade_app/users/user/sessions" -Method POST -UseBasicParsing
    $sessionId = $sessionResponse.id
    Write-Host "✓ Session created: $sessionId" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create session: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Send message that requires model generation
Write-Host "→ Sending message to model..." -ForegroundColor Cyan
try {
    $body = @{
        text = "Say 'pong' and nothing else"
    } | ConvertTo-Json
    
    $messageResponse = Invoke-RestMethod `
        -Uri "$base/apps/arcade_app/users/user/sessions/$sessionId/messages" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -UseBasicParsing
    
    Write-Host "✓ Model responded:" -ForegroundColor Green
    Write-Host "  Response: $($messageResponse.text)" -ForegroundColor White
    
    # Verify we got a non-empty response
    if ([string]::IsNullOrWhiteSpace($messageResponse.text)) {
        Write-Host "✗ Model returned empty response" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "✗ Model generation failed: $_" -ForegroundColor Red
    Write-Host "`nError details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host $responseBody -ForegroundColor Red
    }
    exit 1
}

Write-Host "`n✅ Model smoke test PASSED!" -ForegroundColor Green
Write-Host "   The LLM is working correctly in $Env environment.`n" -ForegroundColor Green
