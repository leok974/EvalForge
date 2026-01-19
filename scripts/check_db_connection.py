import asyncio
import asyncpg

async def check():
    try:
        conn = await asyncpg.connect("postgresql://evalforge:evalforge@127.0.0.1:5435/evalforge")
        print("Successfully connected to DB")
        await conn.close()
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(check())
