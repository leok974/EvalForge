"""
Wrapper script to deploy to Cloud Run with gcloud in PATH.
This ensures subprocess calls can find gcloud.cmd on Windows.
"""
import os
import sys
import subprocess

# Add gcloud to PATH
gcloud_bin = r"C:\Users\pierr\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if gcloud_bin not in os.environ["PATH"]:
    os.environ["PATH"] = f"{gcloud_bin};{os.environ['PATH']}"
    print(f"✓ Added gcloud to PATH: {gcloud_bin}")

# Verify gcloud is accessible
try:
    result = subprocess.run(["gcloud.cmd", "version"], 
                          capture_output=True, text=True, shell=True, timeout=10)
    if result.returncode == 0:
        print("✓ gcloud.cmd is accessible from Python subprocess")
    else:
        print(f"⚠ Warning: gcloud.cmd returned code {result.returncode}")
except Exception as e:
    print(f"❌ Error testing gcloud: {e}")
    sys.exit(1)

# Import ADK
try:
    from google.adk.cli import main as adk_main
except ImportError as e:
    print(f"❌ google-adk import failed: {e}")
    sys.exit(1)

# Run ADK deploy command
print("\n" + "=" * 60)
print("Starting ADK Cloud Run deployment...")
print("=" * 60 + "\n")

sys.argv = [
    "adk",
    "deploy",
    "cloud_run",
    "--project=evalforge-1063529378",
    "--region=us-central1",
    "--service_name=evalforge-agents",
    "--app_name=evalforge",
    "--with_ui",
    "."
]

try:
    adk_main()
except SystemExit as e:
    if e.code == 0:
        print("\n✓ Deployment completed successfully!")
    else:
        print(f"\n❌ Deployment failed with exit code: {e.code}")
    sys.exit(e.code)
except Exception as e:
    print(f"\n❌ Deployment failed with error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
