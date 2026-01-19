# scripts/verify_stack.ps1
# Agent-Proof Verification Script
# Returns PASS or FAIL based on stack health

$ErrorActionPreference = "Stop"
$verified = $true

function Verify-Step {
    param([string]$name, [scriptblock]$check)
    Write-Host "Checking $name... " -NoNewline
    try {
        if (& $check) {
            Write-Host "PASS" -ForegroundColor Green
            return $true
        } else {
            Write-Host "FAIL" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "FAIL (Error: $_)" -ForegroundColor Red
        return $false
    }
}

Write-Host "🔍 Verifying EvalForge Stack..." -ForegroundColor Cyan

# 1. Docker
$verified = $verified -and (Verify-Step "Docker Engine" { docker info 2>$null })

# 2. Database Connectivity
$verified = $verified -and (Verify-Step "Database Port (5435)" { Test-NetConnection -ComputerName 127.0.0.1 -Port 5435 -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded })

# 3. Redis Connectivity
$verified = $verified -and (Verify-Step "Redis Port (6380)" { Test-NetConnection -ComputerName 127.0.0.1 -Port 6380 -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded })

# 4. Backend Health (JSON Check)
$verified = $verified -and (Verify-Step "Backend Health (/health)" {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:8092/health" -Method Get -ErrorAction SilentlyContinue
    return ($res.status -eq "ok")
})

# 5. Backend Readiness (Components Check)
$verified = $verified -and (Verify-Step "Backend Readiness (/api/ready)" {
    try {
        $res = Invoke-RestMethod -Uri "http://127.0.0.1:8092/api/ready" -Method Get -ErrorAction Stop
        return ($res.status -eq "ready" -and $res.components.database -eq "ok")
    } catch { return $false }
})

# 6. Quest Availability (Logic Verification)
$verified = $verified -and (Verify-Step "Quest API (/api/quests)" {
    $quests = Invoke-RestMethod -Uri "http://127.0.0.1:8092/api/quests" -Method Get -ErrorAction Stop
    # Check if we got a list and at least one is available (starter quest)
    if ($quests.Count -gt 0) {
        $starter = $quests | Where-Object { $_.state -eq "available" -or $_.state -eq "completed" }
        return ($starter -ne $null)
    }
    return $false
})


if ($verified) {
    Write-Host "`n✅ STACK VERIFIED: READY FOR AGENT ACTION" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n❌ STACK VERIFICATION FAILED" -ForegroundColor Red
    exit 1
}
