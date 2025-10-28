# scripts/smoke.ps1 - Cloud Run smoke tests (Windows/PowerShell)
$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path logs | Out-Null

Write-Host "Fetching Cloud Run service URL..." -ForegroundColor Cyan
$BASE = (gcloud run services describe evalforge-agents --region us-central1 --format='value(status.url)')

function Log-And-Tee {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
    Add-Content -Path logs/smoke.cloud.log -Value $Message
}

# Clear log
"" | Set-Content -Path logs/smoke.cloud.log

Log-And-Tee "BASE=$BASE" "Cyan"
Log-And-Tee ""

# Test 1: Discovery
Log-And-Tee "→ discovery" "Cyan"
try {
    $null = curl.exe -sf "$BASE/list-apps?relative_path=arcade_app"
    if ($LASTEXITCODE -eq 0) {
        Log-And-Tee "✓ discovery passed" "Green"
    } else {
        throw "Discovery endpoint failed with exit code $LASTEXITCODE"
    }
} catch {
    Log-And-Tee "✗ discovery failed: $_" "Red"
    exit 1
}

# Test 2: Session creation
Log-And-Tee "→ session" "Cyan"
try {
    $null = curl.exe -sf -X POST -H "Content-Length: 0" "$BASE/apps/arcade_app/users/user/sessions"
    if ($LASTEXITCODE -eq 0) {
        Log-And-Tee "✓ session passed" "Green"
    } else {
        throw "Session endpoint failed with exit code $LASTEXITCODE"
    }
} catch {
    Log-And-Tee "✗ session failed: $_" "Red"
    exit 1
}

# Test 3: Model env verification
Log-And-Tee "→ grep model env in service spec" "Cyan"
try {
    $envVars = gcloud run services describe evalforge-agents --region us-central1 --format='value(spec.template.spec.containers[0].env)'
    if ($envVars -match 'gemini-1\.5-flash-002') {
        Log-And-Tee "✓ model env verified" "Green"
    } else {
        throw "Model environment variable not found or incorrect"
    }
} catch {
    Log-And-Tee "✗ model env check failed: $_" "Red"
    exit 1
}

Log-And-Tee ""
Log-And-Tee "✓ cloud smoke passed" "Green"

Write-Host ""
Write-Host "Full log saved to: logs/smoke.cloud.log" -ForegroundColor Cyan
