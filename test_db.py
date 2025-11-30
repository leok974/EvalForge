import asyncio
import sys
sys.path.insert(0, "d:\\EvalForge")

async def test():
    from arcade_app.project_helper import list_projects
    try:
        result = await list_projects("leo")
        print(f"Success! Got {len(result)} projects")
        print(result)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
