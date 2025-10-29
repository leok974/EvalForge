# arcade_app/vertex_diag.py
import os, sys

def vertex_diag():
    project = os.getenv("VERTEX_PROJECT_NUMBER") or os.getenv("GOOGLE_CLOUD_PROJECT")
    region  = os.getenv("VERTEX_REGION") or os.getenv("GOOGLE_CLOUD_LOCATION")
    model   = os.getenv("VERTEX_MODEL_ID")
    print(f"[vertex-diag] PROJECT={project} REGION={region} MODEL={model}", file=sys.stderr)
    try:
        import google.auth
        creds, proj = google.auth.default()
        print(f"[vertex-diag] ADC resolved (project={proj})", file=sys.stderr)
    except Exception as e:
        print(f"[vertex-diag] ADC not resolved → {e}", file=sys.stderr)