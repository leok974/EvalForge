# scripts/dev-up.ps1
# SINGLE ENTRYPOINT for starting EvalForge Local Dev Environment

$ErrorActionPreference = "Stop"

function Check-Port {
    param([int]$port, [string]$name)
    $tcp = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | Where-Object { $_.Port -eq $port }
    if ($tcp) {
        Write-Host "⚠️  Port $port ($name) is already in use. This might block startup." -ForegroundColor Yellow
        return $false
    }
    return $true
}

function Wait-For-Health {
    param([string]$containerName)
    Write-Host "⏳ Waiting for $containerName to be healthy..." -NoNewline
    $maxRetries = 60 # 60 * 1s = 60s timeout
    $retry = 0
    while ($retry -lt $maxRetries) {
        $status = docker inspect --format='{{json .State.Health.Status}}' $containerName 2>$null
        if ($status -eq '"healthy"') {
            Write-Host " ✅ Ready!" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline
        $retry++
    }
    Write-Host " ❌ Timed out!" -ForegroundColor Red
    return $false
}

Write-Host "🚀 Starting EvalForge Dev Environment..." -ForegroundColor Cyan

# 1. Docker Check
if (!(docker info 2>$null)) {
    Write-Host "❌ Docker is NOT running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# 2. Port Checks (Backend & Frontend to warn user)
Check-Port 8092 "Backend" > $null
Check-Port 5174 "Frontend" > $null

# 3. Start Full Stack
Write-Host "📦 Starting Full Stack (Containers)..." -ForegroundColor Cyan
docker compose up -d --build

# 4. Wait for Healthchecks
if (!(Wait-For-Health "evalforge-db")) { exit 1 }
if (!(Wait-For-Health "evalforge-redis")) { exit 1 }
if (!(Wait-For-Health "evalforge-backend")) { exit 1 }
# Frontend might not have healthcheck in compose, check logic if needed
# But usually verified by port check later.

# 5. Connect to Logs
Write-Host "⚡ Environment Up! Tailing logs..." -ForegroundColor Green
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "   Backend:  http://localhost:8092" -ForegroundColor Gray
Write-Host "   (Ctrl+C to stop following logs, containers will keep running)" -ForegroundColor DarkGray

docker compose logs -f
