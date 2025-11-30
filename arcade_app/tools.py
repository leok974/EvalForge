from langchain_core.tools import tool
from arcade_app.rag_helper import search_knowledge

@tool
async def retrieve_docs(query: str):
    """
    Searches the Knowledge Base, which includes:
    1. The User's Project Codebase (files, folder structure, logic).
    2. The Codex (technical documentation and patterns).
    
    Use this tool whenever the user asks about:
    - The project structure or file organization.
    - Specific code implementations (e.g., "how does auth work?").
    - Technical concepts or syntax.
    """
    # 1. Reuse existing RAG logic
    results = await search_knowledge(query, limit=5) # Increased limit to get more context
    
    if not results:
        return "No relevant info found in Codebase or Codex."
    
    # 2. Format
    formatted = "\n\n---\n\n".join(results)
    return f"Found relevant fragments:\n\n{formatted}"
