import asyncio
import json
import os
import sys

# Add root to pythonpath
sys.path.append(os.getcwd())

from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import TrackDefinition

async def seed_tracks():
    tracks_file = os.path.join("data", "tracks.json")
    if not os.path.exists(tracks_file):
        print(f"❌ Error: {tracks_file} not found.")
        return

    with open(tracks_file, "r", encoding="utf-8") as f:
        tracks_data = json.load(f)

    print(f"🌱 Seeding {len(tracks_data)} tracks from {tracks_file}...")

    async for session in get_session():
        for t_data in tracks_data:
            track_id = t_data.get("id")
            if not track_id:
                continue

            # Upsert Track
            stmt = select(TrackDefinition).where(TrackDefinition.id == track_id)
            existing = (await session.exec(stmt)).first()

            if not existing:
                print(f"  + Creating {track_id}...")
                track = TrackDefinition(
                    id=track_id,
                    world_id=t_data.get("world_id", "world-unknown"),
                    name=t_data.get("name", track_id),
                    description=t_data.get("description", ""),
                    # tags can be added if the model supports it, but TrackDefinition 
                    # usually has id, world_id, name, description.
                    # order_index is also common.
                )
                session.add(track)
            else:
                print(f"  ~ Updating {track_id}...")
                existing.world_id = t_data.get("world_id", existing.world_id)
                existing.name = t_data.get("name", existing.name)
                existing.description = t_data.get("description", existing.description)
                session.add(existing)

        await session.commit()
    print("✅ Track seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_tracks())
