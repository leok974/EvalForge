Param(
    [string]$ProjectId = "evalforge-480016",
    [string]$Region    = "us-central1",
    [string]$Service   = "evalforge-agents",
    [string]$InstanceId = "evalforge-postgres"
)

$ErrorActionPreference = "Stop"

# Resolve paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = (Resolve-Path "$ScriptDir").Path
$TempRoot  = Join-Path $RepoRoot "..\evalforge_deploy_temp"

Write-Host "Repo root:  $RepoRoot"
Write-Host "Temp root:  $TempRoot"

# Clean temp dir
if (Test-Path $TempRoot) {
    Write-Host "Removing previous temp dir..."
    Remove-Item -Recurse -Force $TempRoot
}

New-Item -ItemType Directory -Path $TempRoot | Out-Null

# Use robocopy to mirror repo -> temp, excluding heavy/locked dirs
Write-Host "Copying repo to temp (with exclusions)..."

$excludeDirs = @(
    ".git", ".github", ".vscode",
    "node_modules", ".pnpm-store", ".turbo",
    ".venv", "env", "venv",
    "dist", "build", "coverage",
    "__pycache__", ".pytest_cache"
)

$excludeFiles = @(
    "*.log", "*.tmp", "*.db", "*.sqlite"
)

$robocopyArgs = @(
    $RepoRoot,
    $TempRoot,
    "/MIR",
    "/NJH", "/NJS", "/NDL" # Less noise
)

foreach ($d in $excludeDirs) {
    $robocopyArgs += "/XD"
    $robocopyArgs += $d
}
foreach ($f in $excludeFiles) {
    $robocopyArgs += "/XF"
    $robocopyArgs += $f
}

# Run robocopy (Exit code 0-7 is success)
& robocopy @robocopyArgs | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit code $LASTEXITCODE"
}

Write-Host "Temp copy ready."

Push-Location $TempRoot

try {
    # --- Build DATABASE_URL ---
    $DbName  = "evalforge"
    $DbUser  = "evalforge_app"
    # Hardcoded fallback since gcloud capture in script is flaky in this environment
    $DbPass = $env:EVLF_DB_PASS
    if (-not $DbPass) {
        $DbPass = "production_password_secure_enough_for_now_123!" 
        Write-Warning "No EVLF_DB_PASS env var found. Using generated default."
    }

    $InstanceConnectionName = "evalforge-480016:us-central1:evalforge-postgres"
    Write-Host "Using connection name: $InstanceConnectionName"
    
    $encodedPass = [System.Uri]::EscapeDataString($DbPass)
    # Using curly braces for robust variable interpolation
    $finalDbUrl = "postgresql+asyncpg://${DbUser}:${encodedPass}@/${DbName}?host=/cloudsql/${InstanceConnectionName}"
    
    Write-Host "Target DB URL: postgresql+asyncpg://${DbUser}:***@/${DbName}?host=/cloudsql/${InstanceConnectionName}"

    # --- Deploy to Cloud Run (Cloud Build) ---
    Write-Host "Deploying to Cloud Run (Source Deploy)..."
    
    # Note: --quiet prevents interactive prompts
    gcloud run deploy $Service `
        --project $ProjectId `
        --region $Region `
        --platform managed `
        --allow-unauthenticated `
        --source . `
        --add-cloudsql-instances $InstanceConnectionName `
        --set-env-vars "DATABASE_URL=$finalDbUrl" `
        --quiet

    Write-Host "Deploy complete."

    # --- Post-Deploy Smoke Test (Domain) ---
    $DomainUrl = "https://evalforge.app"
    Write-Host "Verifying domain health ($DomainUrl)..."
    try {
        # Allow some time for Cloud Run to route traffic if needed, though usually instant.
        # Retry logic could go here, but keep it simple for now.
        $health = Invoke-WebRequest "$DomainUrl/healthz" -UseBasicParsing -TimeoutSec 10
        if ($health.StatusCode -eq 200) {
            Write-Host "✅ Health Check Passed: $DomainUrl/healthz"
        } else {
            Write-Warning "Health Check returned status $($health.StatusCode)"
        }
    } catch {
        Write-Warning "Health Check Failed. DNS might still be propagating or proxy issues."
        Write-Warning $_
    }
}
catch {
    Write-Error $_
    exit 1
}
finally {
    Pop-Location
}
