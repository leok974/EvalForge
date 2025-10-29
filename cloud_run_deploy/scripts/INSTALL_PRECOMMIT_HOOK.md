# Installing Git Pre-commit Hook

When you initialize this as a Git repository, install the pre-commit hook to block TasteOS paths.

## Setup (PowerShell)

```powershell
# 1. Initialize git (if not already done)
git init

# 2. Create hooks directory
New-Item -ItemType Directory -Force -Path .git\hooks | Out-Null

# 3. Install pre-commit hook
Copy-Item scripts\pre-commit.ps1 .git\hooks\pre-commit -Force

# 4. Make it executable (if on Linux/Mac)
# chmod +x .git/hooks/pre-commit

# 5. Test the hook
Write-Host "Testing pre-commit hook..." -ForegroundColor Cyan
pwsh -File .git\hooks\pre-commit

# If it runs without errors, you're good!
```

## What It Does

The pre-commit hook will:

✅ Scan all staged files before each commit  
❌ **Block commits** that include `tasteos/` paths  
✅ Allow all other EvalForge commits  

## Testing the Guard

Try to commit a TasteOS file (it should be blocked):

```powershell
# This should FAIL
mkdir tasteos -ea 0
"test" > tasteos\test.txt
git add tasteos\test.txt
git commit -m "test tasteos block"

# Expected output:
# ❌ COMMIT BLOCKED: TasteOS paths not allowed in EvalForge
```

Clean up the test:

```powershell
git reset HEAD tasteos\test.txt
Remove-Item tasteos -Recurse -Force
```

## Manual Hook Trigger

To manually run the hook without committing:

```powershell
pwsh -File scripts\pre-commit.ps1
```

## Bypass (Emergency Only)

If you absolutely must bypass the hook (not recommended):

```powershell
git commit --no-verify -m "emergency commit"
```

**⚠️ Warning:** This defeats the purpose of the guard. Only use in emergencies.

## Hook Installation Verification

```powershell
# Check hook exists
Test-Path .git\hooks\pre-commit

# View hook content
Get-Content .git\hooks\pre-commit

# Test hook execution
pwsh -File .git\hooks\pre-commit
```

If everything works, you'll see:
```
🔍 Checking for TasteOS paths...
✓ No TasteOS violations found
```

---

**See also:** `.vscode/README_EVALFORGE_CONTRACT.md` for the full repo contract.
