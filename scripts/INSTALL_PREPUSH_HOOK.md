# 🚀 Installing Pre-Push Hook

## Overview
The pre-push hook runs **before** `git push` and blocks any push that contains `tasteos/` paths in the commit range. This catches mistakes before they reach the remote repository.

## Quick Install (Copy-Paste)

### Windows (PowerShell)
```powershell
# Initialize git repository (if not already done)
if (!(Test-Path .git)) { git init }

# Copy pre-push hook
Copy-Item scripts\pre-push.ps1 .git\hooks\pre-push -Force

Write-Host "✅ Pre-push hook installed (PowerShell version)" -ForegroundColor Green
```

### Linux/Mac (Bash)
```bash
# Initialize git repository (if not already done)
[ ! -d .git ] && git init

# Copy and make executable
cp scripts/pre-push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push

echo "✅ Pre-push hook installed (bash version)"
```

---

## Testing the Hook

### Test 1: Verify installation
```powershell
# Windows
Test-Path .git\hooks\pre-push

# Linux/Mac
[ -f .git/hooks/pre-push ] && echo "✅ Installed"
```

### Test 2: Trigger a block (safe test)
```bash
# Create a test tasteos file (NOT committed)
New-Item -ItemType File -Path "tasteos-test.txt" -Force -ErrorAction SilentlyContinue

# Stage and commit it
git add tasteos-test.txt
git commit -m "Test: TasteOS violation"

# Try to push (should be BLOCKED by hook)
git push origin main

# Clean up
git reset --soft HEAD~1
Remove-Item tasteos-test.txt
```

**Expected output:**
```
════════════════════════════════════════════════════════
❌ PUSH BLOCKED: TasteOS path detected
════════════════════════════════════════════════════════

Violations found in commit range:
  • tasteos-test.txt

EvalForge is for EvalForge only. TasteOS belongs in a separate repo.
```

---

## How It Works

1. **Triggered on `git push`**: Intercepts push BEFORE sending to remote
2. **Scans commit range**: Checks all files in commits being pushed
3. **Pattern match**: Looks for `(^|/)tasteos(/|$)` (case-insensitive)
4. **Blocks with error**: Returns exit code 1 if violations found
5. **Shows fixes**: Provides guidance on how to remediate

### Bypass (Not Recommended)
```bash
# Skip pre-push hook (emergency only)
git push --no-verify
```
⚠️ **Warning**: This bypasses protection. CI will still catch violations.

---

## Difference: Pre-Commit vs Pre-Push

| Hook | When | What It Checks | Bypass Risk |
|------|------|----------------|-------------|
| Pre-commit | `git commit` | Staged files in current commit | Low (runs frequently) |
| Pre-push | `git push` | All commits in push range | Medium (can use `--no-verify`) |
| CI Workflow | PR/merge | Full git history + working tree | None (enforced remotely) |

**Defense-in-depth**: Pre-push is the **last local guard** before code reaches remote.

---

## Troubleshooting

### Hook not running on push
```powershell
# Check if file exists
Get-Content .git\hooks\pre-push | Select-Object -First 5

# Verify it's not marked as bypassed
git config --get push.verify  # Should be empty or "true"
```

### Hook fails with permission error (Linux/Mac)
```bash
chmod +x .git/hooks/pre-push
```

### Want to see full commit range being checked
```bash
# Add debug logging to hook (line 12):
echo "DEBUG: Checking $local_ref -> $remote_ref ($range)"
```

---

## Related Files
- `scripts/pre-commit.ps1` - Runs on commit (staged files)
- `.github/workflows/no-tasteos.yml` - CI enforcement (remote)
- `.vscode/README_EVALFORGE_CONTRACT.md` - Full repo contract
- `GUARDS_QUICKREF.md` - Copy-paste command reference

## Guard Layers
This is **Layer 5** of 7:
1. `.gitignore` (prevents tracking)
2. VS Code settings (locks MCP)
3. Repo contract (AI instructions)
4. Pre-commit hook (blocks commits) ← Previous layer
5. **Pre-push hook (blocks pushes)** ← YOU ARE HERE
6. CI workflow (blocks PRs)
7. README banner (human warning)
