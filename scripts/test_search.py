import asyncio
import os
import sys

# Add root to path so we can import arcade_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.rag_helper import search_knowledge

async def test_rag():
    # 1. Define a query that should match your Codex data
    query = "How do I handle request bodies in FastAPI?"
    print(f"🔎 Searching Vector DB for: '{query}'...\n")
    
    # 2. Perform Vector Search
    try:
        results = await search_knowledge(query, limit=2)
        
        if not results:
            print("❌ No results found.") 
            print("   (Did you run 'python scripts/ingest_codex.py' first?)")
        else:
            print(f"✅ Success! Found {len(results)} relevant chunks:")
            for i, text in enumerate(results):
                print(f"\n--- [Result {i+1}] ---")
                # Print first 300 chars to verify content
                print(text[:300].replace("\n", " ") + "...") 
                
    except Exception as e:
        print(f"❌ Error during search: {e}")

if __name__ == "__main__":
    # Windows-specific event loop fix
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_rag())
