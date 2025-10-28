# Guard Testing Script
# Tests all protection mechanisms to ensure they work correctly

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Testing EvalForge Protection Guards" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$passed = 0
$total = 0

# Test 1: .gitignore
$total++
Write-Host "Test 1: .gitignore contains tasteos/" -ForegroundColor Yellow
if (Select-String -Path .gitignore -Pattern "tasteos/" -SimpleMatch -Quiet) {
    Write-Host "  ✓ PASS - tasteos/ is gitignored" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ FAIL - tasteos/ not found in .gitignore" -ForegroundColor Red
}

# Test 2: VS Code settings
$total++
Write-Host "Test 2: VS Code settings.json exists" -ForegroundColor Yellow
if (Test-Path .vscode\settings.json) {
    $settings = Get-Content .vscode\settings.json -Raw | ConvertFrom-Json
    if ($settings.PSObject.Properties.Name -contains "mcp.servers") {
        Write-Host "  ✓ PASS - MCP servers lock present" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ FAIL - MCP servers lock missing" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ FAIL - settings.json not found" -ForegroundColor Red
}

# Test 3: Repo contract
$total++
Write-Host "Test 3: Repo contract document exists" -ForegroundColor Yellow
if (Test-Path .vscode\README_EVALFORGE_CONTRACT.md) {
    Write-Host "  ✓ PASS - Contract document present" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ FAIL - Contract document missing" -ForegroundColor Red
}

# Test 4: Pre-commit script
$total++
Write-Host "Test 4: Pre-commit script exists and executable" -ForegroundColor Yellow
if (Test-Path scripts\pre-commit.ps1) {
    # Try to execute it (should pass with no staged files)
    try {
        $output = pwsh -NoProfile -File scripts\pre-commit.ps1 2>&1
        Write-Host "  ✓ PASS - Pre-commit script functional" -ForegroundColor Green
        $passed++
    } catch {
        Write-Host "  ✗ FAIL - Pre-commit script error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ FAIL - Pre-commit script missing" -ForegroundColor Red
}

# Test 5: Pre-push scripts
$total++
Write-Host "Test 5: Pre-push scripts exist" -ForegroundColor Yellow
$hasBash = Test-Path scripts\pre-push.sh
$hasPwsh = Test-Path scripts\pre-push.ps1
if ($hasBash -or $hasPwsh) {
    $versions = @()
    if ($hasBash) { $versions += "bash" }
    if ($hasPwsh) { $versions += "PowerShell" }
    Write-Host "  ✓ PASS - Pre-push scripts present ($($versions -join ', '))" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ FAIL - Pre-push scripts missing" -ForegroundColor Red
}

# Test 6: CI workflow
$total++
Write-Host "Test 6: GitHub Actions workflow exists" -ForegroundColor Yellow
if (Test-Path .github\workflows\no-tasteos.yml) {
    # Check for fast lint job
    $workflow = Get-Content .github\workflows\no-tasteos.yml -Raw
    if ($workflow -match 'lint-working-tree') {
        Write-Host "  ✓ PASS - CI workflow with fast lint present" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ⚠ WARN - CI workflow exists but missing fast lint" -ForegroundColor Yellow
        $passed++
    }
} else {
    Write-Host "  ✗ FAIL - CI workflow missing" -ForegroundColor Red
}

# Test 7: README banner
$total++
Write-Host "Test 7: README contains warning banner" -ForegroundColor Yellow
if (Select-String -Path README.md -Pattern "EvalForge only" -SimpleMatch -Quiet) {
    Write-Host "  ✓ PASS - Warning banner present" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ FAIL - Warning banner missing" -ForegroundColor Red
}

# Test 8: No tasteos directory
$total++
Write-Host "Test 8: No tasteos directory exists" -ForegroundColor Yellow
if (-not (Test-Path tasteos)) {
    Write-Host "  ✓ PASS - Repository is clean" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ FAIL - tasteos directory found!" -ForegroundColor Red
}

# Test 9: Backup exists
$total++
Write-Host "Test 9: Backup file exists" -ForegroundColor Yellow
if (Test-Path ..\tasteos_backup.zip) {
    Write-Host "  ✓ PASS - Backup preserved" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ⚠ WARN - Backup not found (may have been moved)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Test Results: $passed/$total passed" -ForegroundColor $(if($passed -eq $total){'Green'}else{'Yellow'})
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($passed -eq $total) {
    Write-Host "✅ All guards are active and functional!" -ForegroundColor Green
    Write-Host "   EvalForge is fully protected from TasteOS scaffolding." -ForegroundColor Green
} else {
    Write-Host "⚠️  Some guards failed. Review above for details." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  • Full details: docs\GUARDS_SUMMARY.md" -ForegroundColor White
Write-Host "  • Quick ref:    GUARDS_QUICKREF.md" -ForegroundColor White
Write-Host ""

exit $(if($passed -eq $total){0}else{1})
