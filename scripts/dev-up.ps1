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

# 3. Start Infrastructure (DB + Redis)
Write-Host "📦 Starting Database and Redis..." -ForegroundColor Cyan
docker compose up -d db redis

# 4. Wait for Healthchecks
if (!(Wait-For-Health "evalforge-db")) { exit 1 }
if (!(Wait-For-Health "evalforge-redis")) { exit 1 }

# 5. Environment Setup for Uvicorn
$env:DATABASE_URL = "postgresql+asyncpg://evalforge:evalforge@127.0.0.1:5435/evalforge"
$env:REDIS_URL = "redis://127.0.0.1:6380/0"
$env:PYTHONPATH = "D:\EvalForge"
$env:ENV = "development"
$env:AUTO_INIT_DB = "1"
$env:EXECUTION_ENABLED = "1"

# 6. Start Backend (in new window if technically possible, but for agent use we run here? 
# actually user wants "dev up", usually implies running the server too. 
# But if I run uvicorn here, it blocks shell. 
# I will run it in background job or just run it directly and user stops it with Ctrl+C)
Write-Host "⚡ Starting Uvicorn Backend..." -ForegroundColor Green
Write-Host "   API: http://127.0.0.1:8092" -ForegroundColor Gray
Write-Host "   Docs: http://127.0.0.1:8092/docs" -ForegroundColor Gray

# We wrap uvicorn to catch exit codes if needed, but direct invocation is fine for 'dev up'
python -m uvicorn arcade_app.agent:app --reload --host 127.0.0.1 --port 8092
