
import asyncio
import httpx
import sys

async def check_codex():
    ref = "codex:glossary/python/systems/dependency-injection"
    url = f"http://localhost:8092/api/codex?ref={ref}"
    print(f"👉 Requesting: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            print(f"   Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                print("   ✅ Response JSON:")
                print(data)
                
                md = data.get("md") or data.get("content") or ""
                print(f"   Markdown length: {len(md)}")
                if not md:
                    print("   ❌ Markdown is EMPTY!")
            else:
                print(f"   ❌ Error: {res.text}")
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_codex())
