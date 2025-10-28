# EvalForge - Hard Guards Summary

This document lists all protection mechanisms preventing TasteOS from being scaffolded in EvalForge.

## 🛡️ Active Guards

### 1. `.gitignore` Protection
**File:** `.gitignore`  
**Status:** ✅ Active  
**What it does:** Prevents `tasteos/` directory from being tracked by Git

```gitignore
# Guard: Prevent TasteOS scaffolding in EvalForge repo
tasteos/
```

### 2. VS Code Settings Lock
**File:** `.vscode/settings.json`  
**Status:** ✅ Active  
**What it does:** 
- Blocks TasteOS MCP server registration
- Prevents workspace bleed-over

```json
{
  "mcp.servers": {},
  "files.simpleDialog.enable": true
}
```

### 3. Repo Contract Document
**File:** `.vscode/README_EVALFORGE_CONTRACT.md`  
**Status:** ✅ Active  
**What it does:** Instructions for AI agents (Copilot) to refuse TasteOS scaffolding

### 4. Pre-commit Hook
**File:** `scripts/pre-commit.ps1`  
**Status:** 🟡 Ready (install after `git init`)  
**What it does:** Blocks commits containing `tasteos/` paths

**Installation:**
```powershell
git init
Copy-Item scripts\pre-commit.ps1 .git\hooks\pre-commit -Force
```

See: `scripts/INSTALL_PRECOMMIT_HOOK.md`

### 5. Pre-push Hook
**Files:** `scripts/pre-push.sh` (bash) & `scripts/pre-push.ps1` (PowerShell)  
**Status:** 🟡 Ready (install after `git init`)  
**What it does:** 
- Blocks pushes containing `tasteos/` paths BEFORE reaching remote
- Scans full commit range being pushed
- Cross-platform compatibility (bash + PowerShell)
- Last local defense layer

**Installation:**
```powershell
# Windows
git init
Copy-Item scripts\pre-push.ps1 .git\hooks\pre-push -Force

# Linux/Mac
git init
cp scripts/pre-push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

See: `scripts/INSTALL_PREPUSH_HOOK.md`

### 6. CI/CD Workflow
**File:** `.github/workflows/no-tasteos.yml`  
**Status:** 🟡 Ready (activates on first push)  
**What it does:** 
- **Fast lint job:** Scans working tree with `find` (2min timeout)
- **Full check job:** Scans tracked files + validates guard integrity
- Blocks PRs/merges containing TasteOS paths
- Two-stage defense: working tree → git history

**Fast lint command:**
```bash
find . -path ./\.git -prune -o -iregex '.*[/\\]tasteos[/\\]?.*' -print -quit | grep .
```

### 7. README Banner
**File:** `README.md`  
**Status:** ✅ Active  
**What it does:** Visible warning at top of README

```markdown
> 🔒 This repo is EvalForge only.  
> If you are about to scaffold TasteOS, use a separate folder: D:\TasteOS
```

## 🤖 AI Agent Instructions

When Copilot/AI sees a TasteOS request, it should respond:

```
⚠️ This workspace is EvalForge only.

To work on TasteOS:
1. Open separate workspace: code D:\TasteOS
2. Or extract backup: Expand-Archive D:\tasteos_backup.zip -DestinationPath D:\TasteOS

I will not scaffold TasteOS inside EvalForge.
```

## 📦 Backup & Recovery

**Backup Location:** `D:\tasteos_backup.zip`

**To restore TasteOS separately:**
```powershell
# Extract to new directory
Expand-Archive -Path "D:\tasteos_backup.zip" -DestinationPath "D:\TasteOS"

# Open in VS Code
code D:\TasteOS
```

## ✅ Verification Checklist

Run these commands to verify all guards are in place:

```powershell
# 1. Check gitignore
Select-String -Path .gitignore -Pattern "tasteos" -SimpleMatch

# 2. Check VS Code settings
Test-Path .vscode\settings.json

# 3. Check repo contract
Test-Path .vscode\README_EVALFORGE_CONTRACT.md

# 4. Check pre-commit script
Test-Path scripts\pre-commit.ps1

# 5. Check pre-push scripts
(Test-Path scripts\pre-push.sh) -or (Test-Path scripts\pre-push.ps1)

# 6. Check CI workflow
Test-Path .github\workflows\no-tasteos.yml

# 7. Check README banner
Select-String -Path README.md -Pattern "EvalForge only" -SimpleMatch

# 8. Verify no tasteos directory
Test-Path tasteos  # Should be False
```

## 🚨 What If Guards Fail?

If TasteOS somehow gets scaffolded again:

1. **Stop immediately**
2. **Don't commit**
3. **Run cleanup:**
   ```powershell
   Remove-Item tasteos -Recurse -Force
   git reset HEAD tasteos/ 2>$null
   ```
4. **Check guards:**
   ```powershell
   pwsh scripts/pre-commit.ps1
   ```

## 📊 Guard Effectiveness

| Guard Type | Prevents | Status |
|------------|----------|--------|
| `.gitignore` | Git tracking | ✅ Active |
| VS Code Settings | MCP registration | ✅ Active |
| Repo Contract | AI scaffolding | ✅ Active |
| Pre-commit Hook | Git commits | 🟡 Ready |
| Pre-push Hook | Git pushes | 🟡 Ready |
| CI Workflow | PR merges | 🟡 Ready |
| README Banner | Human awareness | ✅ Active |

**Legend:**
- ✅ Active = Currently protecting
- 🟡 Ready = Will activate when git/CI is set up

## 🔗 Related Documents

- [.vscode/README_EVALFORGE_CONTRACT.md](.vscode/README_EVALFORGE_CONTRACT.md) - Full repo contract
- [scripts/INSTALL_PRECOMMIT_HOOK.md](../scripts/INSTALL_PRECOMMIT_HOOK.md) - Pre-commit hook installation
- [scripts/INSTALL_PREPUSH_HOOK.md](../scripts/INSTALL_PREPUSH_HOOK.md) - Pre-push hook installation
- [.github/workflows/no-tasteos.yml](../.github/workflows/no-tasteos.yml) - CI workflow
- [README.md](../README.md) - Main project README with banner

---

**Last Updated:** October 28, 2025  
**Guard Count:** 7 active/ready mechanisms  
**Effectiveness:** 🔒 Maximum protection
