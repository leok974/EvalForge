# EvalForge Backend Dev Server
# Starts uvicorn with proper environment variables and auto-healing guards

# Set environment variables
$env:DATABASE_URL = "postgresql+asyncpg://evalforge:evalforge@127.0.0.1:5435/evalforge"
$env:REDIS_URL = "redis://127.0.0.1:6380/0"
$env:PYTHONPATH = "D:\EvalForge"
$env:ENV = "development"
$env:AUTO_INIT_DB = "1"
$env:EXECUTION_ENABLED = "1"

function Test-Port {
    param([string]$hostName, [int]$port)
    try {
        $tcp = New-Object Net.Sockets.TcpClient
        $connect = $tcp.BeginConnect($hostName, $port, $null, $null)
        $wait = $connect.AsyncWaitHandle.WaitOne(1000, $false)
        if ($wait) {
             $tcp.EndConnect($connect)
             $tcp.Close()
             return $true
        } else {
             return $false
        }
    } catch {
        return $false
    }
}

function Wait-For-Services {
    Write-Host "🔍 Checking services..." -ForegroundColor Cyan
    
    $maxRetries = 30
    $retry = 0
    
    while ($retry -lt $maxRetries) {
        $db = Test-Port "127.0.0.1" 5435
        $redis = Test-Port "127.0.0.1" 6380
        
        if ($db -and $redis) {
            Write-Host "✅ Services are UP (DB:5435, Redis:6380)" -ForegroundColor Green
            return $true
        }
        
        Write-Host "⏳ Waiting for services... (DB:$db, Redis:$redis)" -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        $retry++
    }
    
    Write-Host "❌ Services verification failed." -ForegroundColor Red
    return $false
}

Write-Host "🚀 Starting EvalForge Backend with Auto-Healing..." -ForegroundColor Cyan
Write-Host "📍 DATABASE_URL: $env:DATABASE_URL" -ForegroundColor Gray

while ($true) {
    if (Wait-For-Services) {
        Write-Host "⚡ Starting Uvicorn..." -ForegroundColor Green
        try {
            python -m uvicorn arcade_app.agent:app --reload --host 127.0.0.1 --port 8092
        } catch {
            Write-Host "⚠️ Uvicorn crashed: $_" -ForegroundColor Red
        }
    }
    
    Write-Host "🔄 Restarting in 5 seconds..." -ForegroundColor Magenta
    Start-Sleep -Seconds 5
}
