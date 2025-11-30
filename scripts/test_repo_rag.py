import asyncio
import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.rag_helper import search_knowledge

async def verify_repo_memory():
    # 1. Define a query that targets CODE, not docs
    # Use a generic query likely to match most frameworks/repos you might sync
    query = "Show me the routing logic or API endpoints."
    
    print(f"🕵️‍♀️ Agent Memory Check")
    print(f"   Query: '{query}'")
    print("   Target: Vector Database (Codex + Repos)\n")

    try:
        # 2. Search
        # Since rag_helper searches all chunks, this will return Codex OR Repo matches
        results = await search_knowledge(query, limit=3)

        if not results:
            print("❌ No results found.")
            print("   Troubleshooting:")
            print("   1. Did you add a project in the UI?")
            print("   2. Did the 'Sync' finish (Status: OK)?")
            print("   3. Is the repo public?")
            return

        print(f"✅ Found {len(results)} memory fragments:\n")
        
        for i, content in enumerate(results):
            # content string format from ingestion_helper: 
            # "File: {path}\nProject: {id}\n\n{code}"
            
            print(f"--- [Fragment {i+1}] ---")
            # Print the header (File path) and snippet
            preview = content[:400].replace("\n", "\n   ") 
            print(f"   {preview}...")
            print("--------------------\n")

    except Exception as e:
        print(f"❌ Error querying Vector DB: {e}")

if __name__ == "__main__":
    # Windows compatibility
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_repo_memory())
