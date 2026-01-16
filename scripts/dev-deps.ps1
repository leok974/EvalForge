# EvalForge Local Dev Stack Checker
# Ensures all required services (DB, Redis) are running

Write-Host "🔍 Checking EvalForge Dependencies..." -ForegroundColor Cyan

# Check if Docker is running
try {
    $dockerRunning = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker is not running" -ForegroundColor Red
        Write-Host "   Please start Docker Desktop and try again" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check Postgres container
Write-Host "" -ForegroundColor Gray
Write-Host "Checking Postgres..." -ForegroundColor Gray
$pgContainer = docker ps --filter "name=evalforge-db" --filter "status=running" --format "{{.Names}}"
if ($pgContainer -eq "evalforge-db") {
    Write-Host "✅ Postgres (evalforge-db) is running on port 5435" -ForegroundColor Green
} else {
    Write-Host "⚠️  Postgres container not found. Starting it now..." -ForegroundColor Yellow
    docker run -d `
        --name evalforge-db `
        -e POSTGRES_USER=evalforge_app `
        -e POSTGRES_PASSWORD=evalforge_dev `
        -e POSTGRES_DB=evalforge `
        -p 5435:5432 `
        pgvector/pgvector:pg16
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Postgres started successfully" -ForegroundColor Green
        Start-Sleep -Seconds 3  # Give it time to initialize
    } else {
        Write-Host "❌ Failed to start Postgres" -ForegroundColor Red
        exit 1
    }
}

# Check Redis container
Write-Host "" -ForegroundColor Gray
Write-Host "Checking Redis..." -ForegroundColor Gray
$redisContainer = docker ps --filter "name=evalforge-redis" --filter "status=running" --format "{{.Names}}"
if ($redisContainer -eq "evalforge-redis") {
    Write-Host "✅ Redis (evalforge-redis) is running on port 6379" -ForegroundColor Green
} else {
    Write-Host "⚠️  Redis container not found. Starting it now..." -ForegroundColor Yellow
    docker run -d `
        --name evalforge-redis `
        -p 6379:6379 `
        redis:7-alpine
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Redis started successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to start Redis" -ForegroundColor Red
        exit 1
    }
}

Write-Host "" -ForegroundColor Gray
Write-Host "✨ All dependencies are ready!" -ForegroundColor Green
Write-Host "" -ForegroundColor Gray
Write-Host "Database: postgresql://evalforge_app:evalforge_dev@127.0.0.1:5435/evalforge" -ForegroundColor Gray
Write-Host "Redis:    redis://127.0.0.1:6379/0" -ForegroundColor Gray
