#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install EvalForge git hooks for this clone.

.DESCRIPTION
    Copies hook scripts from scripts/ into .git/hooks/ and marks them executable.
    Run once after cloning. Safe to re-run — idempotent.

.EXAMPLE
    .\scripts\install-hooks.ps1
#>

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$HooksDir = Join-Path $RepoRoot ".git\hooks"

if (-not (Test-Path $HooksDir)) {
    Write-Error ".git/hooks directory not found. Are you in the repo root?"
    exit 1
}

# ── pre-push ─────────────────────────────────────────────────────────────────
# Runs check_cherry_pick_diff.py on every commit being pushed.
# Blocks the push if any symbol deletion is detected without documentation.

$prePushSrc = Join-Path $PSScriptRoot "pre-push.hook.py"
$prePushDst = Join-Path $HooksDir "pre-push"

if (-not (Test-Path $prePushSrc)) {
    Write-Error "Hook source not found: $prePushSrc"
    exit 1
}

Copy-Item -Force $prePushSrc $prePushDst
Write-Host "[install-hooks] Installed pre-push hook -> $prePushDst"

# On Unix/macOS, mark executable. On Windows, git respects the shebang line.
if ($IsLinux -or $IsMacOS) {
    chmod +x $prePushDst
    Write-Host "[install-hooks] Marked pre-push executable (Unix mode)."
}

Write-Host ""
Write-Host "[install-hooks] Done. Hooks installed:"
Write-Host "  pre-push  — blocks pushes containing undocumented symbol deletions"
Write-Host ""
Write-Host "To bypass in an emergency (intentional deletion documented in commit):"
Write-Host "    git push --no-verify"
