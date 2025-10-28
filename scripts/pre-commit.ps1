# Pre-commit guard: Block TasteOS paths from EvalForge
# Usage: Copy to .git/hooks/pre-commit after git init

$ErrorActionPreference = "Stop"

Write-Host "🔍 Checking for TasteOS paths..." -ForegroundColor Cyan

# Get staged files
$changed = git diff --cached --name-only 2>$null

if (-not $changed) {
    Write-Host "✓ No staged files to check" -ForegroundColor Gray
    exit 0
}

# Check for tasteos violations
$violations = $changed | Where-Object { $_ -match '(^|/)tasteos(/|$)' }

if ($violations) {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host "❌ COMMIT BLOCKED: TasteOS paths not allowed in EvalForge" -ForegroundColor Red
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    Write-Host "The following files/paths violate the repo contract:" -ForegroundColor Yellow
    $violations | ForEach-Object { 
        Write-Host "  • $_" -ForegroundColor Red 
    }
    Write-Host ""
    Write-Host "To fix:" -ForegroundColor Yellow
    Write-Host "  1. Remove TasteOS files from this commit" -ForegroundColor White
    Write-Host "  2. Work on TasteOS in a separate repo: D:\TasteOS" -ForegroundColor White
    Write-Host ""
    Write-Host "See .vscode/README_EVALFORGE_CONTRACT.md for details" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "✓ No TasteOS violations found" -ForegroundColor Green
exit 0
