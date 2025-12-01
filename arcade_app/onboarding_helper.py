import asyncio
from typing import AsyncGenerator

async def stream_prologue(user_id: str) -> AsyncGenerator[str, None]:
    """
    Scripted sequence for new users (Level 0).
    Acts as the 'Boot Sequence' for the game.
    """
    # 1. System Boot Messages (The "Terminal" feeling)
    boot_lines = [
        "INITIALIZING NEURO-LINK...",
        "CONNECTING TO THE CONSTRUCT...",
        "SYNCHRONIZING BIO-METRICS...",
        "WARNING: MEMORY CORRUPTION DETECTED.",
        "ATTEMPTING RESTORE..."
    ]
    
    for line in boot_lines:
        yield f"> {line}\n"
        await asyncio.sleep(0.6) # Dramatic pause for effect

    await asyncio.sleep(1)
    
    # 2. The Narrative Hook (The Architect speaks)
    # We stream this character-by-character to simulate a live transmission
    intro_text = """
    \n**UNKNOWN SIGNAL RECEIVED:**
    "Wake up, Architect. The system has been dormant for cycles. Entropy is tearing The Grid apart.
    
    I have restored your primary interface, but your skills are fragmented. You must prove you can still manipulate the code."
    """
    
    # Simulate typing speed
    chunk_size = 5
    for i in range(0, len(intro_text), chunk_size):
        yield intro_text[i:i+chunk_size]
        await asyncio.sleep(0.02)
    
    await asyncio.sleep(1.5)

    # 3. The Tutorial Quest Card
    quest_card = """
    \n\n## ⚔️ MISSION: INITIALIZE
    **Difficulty:** TUTORIAL
    
    **Briefing:**
    To restore your connection to the Archives, you must link a knowledge source. The system cannot function without data.
    
    **Objectives:**
    - [ ] Open the **PROJECTS** dashboard (Top Menu).
    - [ ] Sync a GitHub Repository (e.g., `https://github.com/tiangolo/fastapi` or your own).
    - [ ] Wait for Ingestion to complete.
    
    **Rewards:**
    - Unlock: **Judge Mode**
    - Unlock: **The Foundry (Python World)**
    - Loot: +100 XP
    """
    
    yield quest_card
