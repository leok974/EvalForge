Param(
    [string]$ProjectId = "evalforge-480016",
    [string]$Region    = "us-central1",
    [string]$Service   = "evalforge-agents"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 EvalForge quick deploy"
Write-Host "  Project: $ProjectId"
Write-Host "  Region:  $Region"
Write-Host "  Service: $Service"
Write-Host ""

# Resolve paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$DeployDir = Join-Path $RepoRoot "cloud_run_deploy"

if (-not (Test-Path $DeployDir)) {
    throw "cloud_run_deploy directory not found at '$DeployDir'. Run your staging/copy script first."
}

Write-Host "📁 Using deploy directory: $DeployDir"
Set-Location $DeployDir

# --- SYNC SOURCES ---
Write-Host "🔄 Syncing source files (using Robocopy)..."
$filesToCopy = @("arcade_app", "apps", "exercises", "scripts", "seed", "requirements.txt")
foreach ($item in $filesToCopy) {
    if (Test-Path "$RepoRoot\$item") {
        $src = "$RepoRoot\$item"
        $dst = "$DeployDir\$item"
        if (Test-Path "$src" -PathType Leaf) {
            # File
            Copy-Item -Force "$src" "$DeployDir"
        } else {
            # Directory
            robocopy $src $dst /MIR /XD node_modules .git __pycache__ .mypy_cache /XF .DS_Store *.pyc /NJH /NJS /NDL /NC /NS /NP
            if ($lastexitcode -ge 8) { throw "Robocopy failed with exit code $lastexitcode" }
            $global:LASTEXITCODE = 0
        }
    }
}
# --------------------

# Optional: load .env.prod into the current process (if you use it)
$envFile = Join-Path $RepoRoot ".env.prod"
if (Test-Path $envFile) {
    Write-Host "🔧 Loading .env.prod into environment for this session..."
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*#" -or $_ -match "^\s*$") { return }
        $pair = $_ -split "=", 2
        if ($pair.Count -eq 2) {
            $name  = $pair[0].Trim()
            $value = $pair[1].Trim()
            if ($name -and $value) {
                Set-Item -Path "env:$name" -Value $value
            }
        }
    }
}

# Compose env vars for the deploy command.
# Add or remove keys to match what your app expects.
$envVars = @()

if ($env:DATABASE_URL) { $envVars += "DATABASE_URL=$($env:DATABASE_URL)" }
if ($env:ENVIRONMENT)  { $envVars += "ENVIRONMENT=$($env:ENVIRONMENT)" }
if ($env:VERTEX_PROJECT) { $envVars += "VERTEX_PROJECT=$($env:VERTEX_PROJECT)" }
if ($env:VERTEX_LOCATION) { $envVars += "VERTEX_LOCATION=$($env:VERTEX_LOCATION)" }
# Add known EvalForge vars
if ($env:VERTEX_PROJECT_NUMBER) { $envVars += "VERTEX_PROJECT_NUMBER=$($env:VERTEX_PROJECT_NUMBER)" }
if ($env:VERTEX_MODEL_ID) { $envVars += "VERTEX_MODEL_ID=$($env:VERTEX_MODEL_ID)" }
if ($env:GITHUB_CLIENT_ID) { $envVars += "GITHUB_CLIENT_ID=$($env:GITHUB_CLIENT_ID)" }
if ($env:GITHUB_CLIENT_SECRET) { $envVars += "GITHUB_CLIENT_SECRET=$($env:GITHUB_CLIENT_SECRET)" }
if ($env:SECRET_KEY) { $envVars += "SECRET_KEY=$($env:SECRET_KEY)" }
if ($env:EVALFORGE_AUTH_MODE) { $envVars += "EVALFORGE_AUTH_MODE=$($env:EVALFORGE_AUTH_MODE)" }

# Ensure critical vars are set if missing from env (fallback logic or explicit set)
# We assume .env.prod has them, but manual_deploy.ps1 builds them too.
# Let's ensure strictness:
if (-not $env:GITHUB_CLIENT_ID) { Write-Warning "GITHUB_CLIENT_ID missing!" }

# Add specific hardcoded ones if needed or rely on .env.prod
# We'll rely on the loaded .env.prod + what is already in environment from set_auth_secrets.ps1 if run before.

$envVarsString = $envVars -join ","

Write-Host ""
Write-Host "🌐 Environment vars for this deploy:"
Write-Host "  $envVarsString"
Write-Host ""

# IMPORTANT: this uses the Dockerfile in cloud_run_deploy, which you patched to install git.
Write-Host "🛠  Running gcloud run deploy (Dockerfile-based, non-interactive)..."
$deployArgs = @(
    "run", "deploy", $Service,
    "--project", $ProjectId,
    "--region", $Region,
    "--platform", "managed",
    "--allow-unauthenticated",
    "--port", "8080",
    "--memory", "512Mi",
    "--timeout", "600",
    "--source", ".",       # uses the Dockerfile in this dir
    "--add-cloudsql-instances", "evalforge-480016:us-central1:evalforge-postgres",
    "--quiet"
)

if ($envVarsString) {
    $deployArgs += @("--set-env-vars", $envVarsString)
}

gcloud @deployArgs

Write-Host ""
Write-Host "✅ Deploy command finished. Recent revisions:"
gcloud run revisions list `
  --service=$Service `
  --project=$ProjectId `
  --region=$Region `
  --format="table(name,creationTimestamp,status.conditions[0].status)" `
  --limit=5
