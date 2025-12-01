import os
from langchain_google_vertexai import ChatVertexAI

def get_chat_model(agent_name: str = "default"):
    """
    Factory for getting a chat model instance.
    """
    model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
    llm = ChatVertexAI(
        model_name=model_name,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        temperature=0.3
    )
    return llm
