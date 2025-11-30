import os
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "291179078777"
LOCATION = "us-central1"

def check_model(model_name):
    print(f"📡 Checking {model_name}...", end=" ")
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = GenerativeModel(model_name)
        response = model.generate_content("Ping", stream=False)
        print(f"✅ ONLINE")
        return True
    except Exception as e:
        print(f"❌ OFFLINE")
        print(f"   Error: {e}") # Uncomment for debug
        return False

if __name__ == "__main__":
    print("--- Verifying Model Availability (Late 2025) ---")
    # Check the most likely candidates for Late 2025
    check_model("gemini-2.5-flash-001") # Best for Arcade
    check_model("gemini-3.0-pro-001")   # Best for Coach
    check_model("gemini-2.0-flash-001") # Legacy fallback
    check_model("gemini-1.5-flash-001") # Old faithful
