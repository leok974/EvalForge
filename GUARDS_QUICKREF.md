# Quick Reference - Copy-Paste Guards

## 🚨 If Copilot Tries to Scaffold TasteOS

**Say this:**
```
⚠️ STOP. This workspace is EvalForge only.

Do not scaffold TasteOS here. Instead:

1. Open separate workspace: code D:\TasteOS
2. Or extract backup: Expand-Archive D:\tasteos_backup.zip -DestinationPath D:\TasteOS

See .vscode/README_EVALFORGE_CONTRACT.md for the repo contract.
```

## 🔧 Install Git Hooks (After git init)

### Pre-commit Hook
```powershell
git init
Copy-Item scripts\pre-commit.ps1 .git\hooks\pre-commit -Force
pwsh -File .git\hooks\pre-commit  # Test it
```

### Pre-push Hook
```powershell
# Windows
Copy-Item scripts\pre-push.ps1 .git\hooks\pre-push -Force

# Linux/Mac
cp scripts/pre-push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

See: `scripts/INSTALL_PRECOMMIT_HOOK.md` & `scripts/INSTALL_PREPUSH_HOOK.md`

## ✅ Verify All Guards

```powershell
# Quick check (7 guards)
Select-String -Path .gitignore -Pattern "tasteos" -SimpleMatch
Test-Path .vscode\settings.json
Test-Path .vscode\README_EVALFORGE_CONTRACT.md
Test-Path scripts\pre-commit.ps1
(Test-Path scripts\pre-push.sh) -or (Test-Path scripts\pre-push.ps1)
Test-Path .github\workflows\no-tasteos.yml
Select-String -Path README.md -Pattern "EvalForge only" -SimpleMatch
```

## 🧹 Emergency Cleanup (If TasteOS Gets In)

```powershell
# Remove directory
Remove-Item tasteos -Recurse -Force

# Unstage if committed
git reset HEAD tasteos/ 2>$null
git rm -r --cached tasteos 2>$null

# Verify clean
Test-Path tasteos  # Should be False
```

## 📦 Restore TasteOS Separately

```powershell
# Extract to new directory
Expand-Archive -Path "D:\tasteos_backup.zip" -DestinationPath "D:\TasteOS"

# Open as separate workspace
code D:\TasteOS
```

## 🤖 Copilot Response Template

When user asks about TasteOS:

```
This workspace is **EvalForge only**.

To work on TasteOS, open it as a separate workspace:
• Restore: Expand-Archive D:\tasteos_backup.zip -DestinationPath D:\TasteOS
• Open: code D:\TasteOS

I will not scaffold TasteOS inside the EvalForge repo.
```

## 📋 Guard Status Check

```powershell
Write-Host "Guard Status:" -ForegroundColor Cyan
Write-Host "  .gitignore:     $(if(Select-String -Path .gitignore -Pattern 'tasteos' -SimpleMatch -Quiet){'✓'}else{'✗'})"
Write-Host "  VS Code:        $(if(Test-Path .vscode\settings.json){'✓'}else{'✗'})"
Write-Host "  Contract:       $(if(Test-Path .vscode\README_EVALFORGE_CONTRACT.md){'✓'}else{'✗'})"
Write-Host "  Pre-commit:     $(if(Test-Path scripts\pre-commit.ps1){'✓'}else{'✗'})"
Write-Host "  Pre-push:       $(if((Test-Path scripts\pre-push.sh) -or (Test-Path scripts\pre-push.ps1)){'✓'}else{'✗'})"
Write-Host "  CI Workflow:    $(if(Test-Path .github\workflows\no-tasteos.yml){'✓'}else{'✗'})"
Write-Host "  README Banner:  $(if(Select-String -Path README.md -Pattern 'EvalForge only' -SimpleMatch -Quiet){'✓'}else{'✗'})"
```

## 🔒 Files Created/Modified

**Created:**
- `.vscode/settings.json` - MCP lock
- `.vscode/README_EVALFORGE_CONTRACT.md` - Repo contract
- `scripts/pre-commit.ps1` - Pre-commit hook
- `scripts/pre-push.sh` - Pre-push hook (bash)
- `scripts/pre-push.ps1` - Pre-push hook (PowerShell)
- `scripts/INSTALL_PRECOMMIT_HOOK.md` - Pre-commit guide
- `scripts/INSTALL_PREPUSH_HOOK.md` - Pre-push guide
- `.github/workflows/no-tasteos.yml` - CI guard (fast lint + full check)
- `docs/GUARDS_SUMMARY.md` - Full documentation

**Modified:**
- `.gitignore` - Added `tasteos/` entry
- `README.md` - Added warning banner

## 📖 Full Documentation

See: `docs/GUARDS_SUMMARY.md`

---

**Backup Location:** `D:\tasteos_backup.zip`  
**Last Updated:** October 28, 2025  
**Protection:** 7/7 guards active ✅
