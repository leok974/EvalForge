# Pre-push guard: Block pushes containing tasteos paths (PowerShell version)
# This runs BEFORE code is pushed to remote repository
$ErrorActionPreference = "Stop"

Write-Host "🔍 Pre-push check: Scanning for TasteOS paths..." -ForegroundColor Cyan

# Read stdin (remote name, URL, refs)
$remote = $args[0]
$url = $args[1]

# Read ref updates from stdin
$input = [Console]::In.ReadToEnd()
$lines = $input -split "`n" | Where-Object { $_ -match '\S' }

$hasViolations = $false

foreach ($line in $lines) {
    $parts = $line -split '\s+'
    if ($parts.Length -lt 4) { continue }
    
    $local_ref = $parts[0]
    $local_sha = $parts[1]
    $remote_ref = $parts[2]
    $remote_sha = $parts[3]
    
    # Skip branch deletions
    if ($local_sha -eq "0000000000000000000000000000000000000000") {
        continue
    }
    
    # Determine range to check
    if ($remote_sha -eq "0000000000000000000000000000000000000000") {
        # New branch - check all commits
        $range = $local_sha
        $files = git show --name-only --pretty="" $local_sha 2>$null
    } else {
        # Existing branch - check new commits
        $range = "$remote_sha..$local_sha"
        $files = git diff --name-only $range 2>$null
    }
    
    # Check for tasteos violations
    $violations = $files | Where-Object { $_ -match '(^|/)tasteos(/|$)' }
    
    if ($violations) {
        $hasViolations = $true
        Write-Host ""
        Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Red
        Write-Host "❌ PUSH BLOCKED: TasteOS paths not allowed in EvalForge" -ForegroundColor Red
        Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Red
        Write-Host ""
        Write-Host "The following files contain 'tasteos' in their path:" -ForegroundColor Yellow
        $violations | ForEach-Object { Write-Host "  • $_" -ForegroundColor Red }
        Write-Host ""
        Write-Host "To fix:" -ForegroundColor Yellow
        Write-Host "  1. Remove TasteOS files from this branch" -ForegroundColor White
        Write-Host "  2. Work on TasteOS in separate repo: D:\TasteOS" -ForegroundColor White
        Write-Host ""
        Write-Host "See .vscode/README_EVALFORGE_CONTRACT.md for details" -ForegroundColor Gray
        Write-Host ""
        exit 1
    }
}

if (-not $hasViolations) {
    Write-Host "✅ No TasteOS violations - push allowed" -ForegroundColor Green
}

exit 0
