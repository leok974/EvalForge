# 🐛 Cloud Run Deployment Issue - Windows gcloud PATH Problem

## Problem

ADK's `deploy cloud_run` command fails on Windows with:
```
Deploy failed: [WinError 2] The system cannot find the file specified
```

**Root Cause:** Python's `subprocess.run()` on Windows cannot find `gcloud.cmd` even when it's in PATH, because:
1. Windows requires the `.cmd` extension for batch files
2. Python subprocess doesn't automatically add extensions without `shell=True`
3. ADK's deployment code uses `subprocess` without `shell=True`

## ✅ Solution: Manual Deployment with gcloud

Since ADK's automated deployment has this Windows-specific bug, we'll deploy manually using the files ADK generates.

### Step 1: Let ADK Generate the Dockerfile

Run this to generate deployment files (it will fail at the gcloud step, but that's OK):

```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1

# This will generate files in C:\Users\pierr\AppData\Local\Temp\cloud_run_deploy_src\
# but fail to deploy. We'll copy the files before cleanup.
adk deploy cloud_run --project="evalforge-1063529378" --region="us-central1" --service_name="evalforge-agents" --app_name="evalforge" --with_ui . 2>&1 | Tee-Object -Variable output

# Extract the temp folder path from output
$tempFolder = ($output | Select-String "Start generating Cloud Run source files in (.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
Write-Host "Temp folder: $tempFolder"
```

### Step 2: Copy Files Before Cleanup

```powershell
# Quick! Copy before ADK deletes it
$deployFolder = "D:\EvalForge\cloud_run_deploy"
if (Test-Path $tempFolder) {
    Copy-Item -Recurse $tempFolder $deployFolder
    Write-Host "✓ Copied to: $deployFolder"
}
```

### Step 3: Deploy with gcloud Directly

```powershell
cd $deployFolder

# Deploy using gcloud
gcloud run deploy evalforge-agents `
  --source . `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --platform=managed `
  --allow-unauthenticated `
  --port=8080

```

### Step 4: Get the Service URL

```powershell
gcloud run services describe evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --format='value(status.url)'
```

## 🔧 Alternative: Use WSL or Linux

If you have WSL (Windows Subsystem for Linux):

```bash
# In WSL
cd /mnt/d/EvalForge
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk

adk deploy cloud_run \
  --project="evalforge-1063529378" \
  --region="us-central1" \
  --service_name="evalforge-agents" \
  --app_name="evalforge" \
  --with_ui \
  .
```

## 🐛 Report to ADK Team

This is a Windows-specific bug in google-adk. Consider reporting it:
- Repository: https://github.com/google/adk (if public)
- Issue: Python subprocess on Windows needs `shell=True` or full path to `gcloud.cmd`

## 📝 Technical Details

**Why Python can't find gcloud:**

```python
# ❌ Fails on Windows - needs .cmd extension
subprocess.run(['gcloud', 'version'])  # FileNotFoundError

# ✅ Works - shell resolves .cmd extension  
subprocess.run(['gcloud', 'version'], shell=True)

# ✅ Works - full path with extension
subprocess.run(['C:\\...\\gcloud.cmd', 'version'])

# ✅ Works - use shutil.which to find it
import shutil
gcloud = shutil.which('gcloud')  # Returns path with .cmd
subprocess.run([gcloud, 'version'])
```

**ADK probably does:**
```python
subprocess.run(['gcloud', 'run', 'deploy', ...])  # ❌ Fails on Windows
```

**Should do:**
```python
import shutil
gcloud = shutil.which('gcloud') or 'gcloud'
subprocess.run([gcloud, 'run', 'deploy', ...])  # ✅ Works everywhere
```

## ⚡ Quick Deploy Script

I've created `manual_deploy.ps1` that automates the manual deployment process.

Run it with:
```powershell
.\manual_deploy.ps1
```

---

**Status:** Awaiting manual deployment or ADK fix for Windows subprocess issue.
