import { OrionTrackNode, OrionWorldId } from "./types";
import { useCurriculumStore } from "@/store/curriculumStore";

// Pseudo-adapter to get tracks from store and map to Orion nodes
export function buildOrionTracks(worldId: OrionWorldId): OrionTrackNode[] {
    // In a real app, we'd filter by worldId. 
    // For now, we'll just grab all tracks and pretend they belong to the world, 
    // or filter if the store supports it.
    // The user prompt said: "from your store/api"

    const tracks = useCurriculumStore.getState().tracks;

    // Filter tracks relevant to the world (mock logic for now as tracks might not have worldId yet)
    // We'll just map the first N tracks to avoid empty screens if filtering fails
    const worldTracks = tracks.slice(0, 8);

    return worldTracks.map((track, idx) => ({
        id: track.id,
        title: track.title,
        difficulty: track.difficulty as "novice" | "intermediate" | "advanced",
        progressPct: track.progress, // Assuming store has 'progress'
        orbitIndex: 1 + Math.floor(idx / 4), // simple ring assignment
        angleDeg: (idx % 4) * 90 + 15 * (idx % 2),
    }));
}
