import os
import vertexai
from vertexai.generative_models import GenerativeModel

# Configuration for Phase 10
PROJECT_ID = "291179078777"  
LOCATION = "us-central1"
# UPDATED: Fallback to 1.5
TARGET_MODEL = "gemini-1.5-flash-001" 

def test_connection():
    print(f"📡 Connecting to Vertex AI...")
    print(f"   Target: {TARGET_MODEL}")
    print(f"   Region: {LOCATION}")
    
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = GenerativeModel(TARGET_MODEL)
        
        print("⏳ Sending 'Hello' to Gemini 3.0...")
        # Use a generation config to force deterministic short output
        response = model.generate_content(
            "Reply with 'ONLINE'.",
            generation_config={"temperature": 0.0, "max_output_tokens": 5}
        )
        
        print(f"✅ Success! Response: {response.text.strip()}")
        
    except Exception as e:
        print(f"\n❌ FAILED. The model '{TARGET_MODEL}' might not be enabled yet.")
        print(f"   Error: {e}")
        print("\n💡 Tip: Check 'Model Garden' in GCP Console to see enabled versions.")

if __name__ == "__main__":
    test_connection()
