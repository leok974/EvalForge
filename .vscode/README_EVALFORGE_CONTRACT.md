# Repo Contract: EvalForge Only

## 🔒 Critical Rules

This workspace is **EvalForge** and **EvalForge only**.

### ❌ DO NOT:
- Scaffold `tasteos/` or any TasteOS code here
- Register TasteOS MCP servers in `.vscode/settings.json`
- Add TasteOS-related tasks to `.vscode/tasks.json`
- Create TasteOS documentation in this repo
- Mix TasteOS and EvalForge concerns

### ✅ DO:
- Keep all code EvalForge-scoped (ADK agents, arcade_app, etc.)
- Use existing EvalForge tasks and workflows
- Document EvalForge features only
- Follow production-ready patterns already established

## 🤖 Instructions for AI Agents (Copilot/etc.)

If a user requests **TasteOS** work:

**Response Template:**
```
⚠️ This workspace is EvalForge only.

To work on TasteOS, please:
1. Open the TasteOS workspace: code D:\TasteOS
2. Or create it: mkdir D:\TasteOS && cd D:\TasteOS
3. Extract backup if needed: Expand-Archive D:\tasteos_backup.zip -DestinationPath D:\TasteOS

I will not scaffold TasteOS inside EvalForge.
```

## 📁 What Belongs in EvalForge

- **ADK Agents**: `arcade_app/` (Greeter, Judge, Coach)
- **Deployment**: Cloud Run scripts, fast rollback
- **Testing**: Smoke tests, guardrail tests
- **Documentation**: Production hardening, troubleshooting
- **Infrastructure**: Analytics, alerts, monitoring

## 🚫 What Does NOT Belong Here

- TasteOS backend (FastAPI)
- TasteOS frontend (Next.js, Vite)
- TasteOS MCP configurations
- TasteOS smoke tests
- Any recipe management code

## 🛡️ Guards in Place

1. `.gitignore` - Ignores `tasteos/` directory
2. `.vscode/settings.json` - Blocks TasteOS MCP registration
3. `.vscode/README_EVALFORGE_CONTRACT.md` - This file (repo contract)
4. `scripts/pre-commit.ps1` - Pre-commit hook blocks TasteOS paths
5. `.github/workflows/no-tasteos.yml` - CI workflow blocks TasteOS PRs

## 🔄 Backup & Recovery

If you need the TasteOS scaffolding that was removed:

```powershell
# Extract to separate directory
Expand-Archive -Path "D:\tasteos_backup.zip" -DestinationPath "D:\TasteOS"

# Open in VS Code as separate workspace
code D:\TasteOS
```

## ✅ Checklist Before Contributing

- [ ] My changes are EvalForge-scoped only
- [ ] No `tasteos/` paths exist
- [ ] No TasteOS references in code/docs
- [ ] All tests pass (EvalForge smoke tests)
- [ ] Pre-commit hook passes

---

**Last Updated**: October 28, 2025  
**Backup Location**: `D:\tasteos_backup.zip`
