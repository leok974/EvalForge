import { OrionTrackNode, OrionWorldId } from "./types";
import { worlds } from "@/config/worldConfig";
import { WORLD_TRACKS } from "@/config/worldTracks";

export type { OrionTrackNode };

// Map world config to Orion nodes
export function getWorldNodes() {
    const ringRadius = 220;
    const angleStep = (2 * Math.PI) / worlds.length;

    return worlds.map((world, index) => ({
        id: world.slug as OrionWorldId,
        slug: world.slug,
        label: world.name,
        color: world.color,
        radius: ringRadius,
        angle: index * angleStep,
    }));
}

import { getTrackProgress } from "@/features/progress/trackProgress";

// Get tracks for a specific world from config
export function getTrackNodesForWorld(worldSlug: string): OrionTrackNode[] {
    const worldTracks = WORLD_TRACKS.filter(t => t.worldSlug === worldSlug);

    // Default to at least one 'empty' track slot if none found?
    // User request: "no more blank bubbles... every world gets at least one track"
    // Since WORLD_TRACKS covers all worlds, we should use that.

    // Fallback if somehow config is missing (safety)
    const count = worldTracks.length || 1;
    const ringRadius = 320;
    const angleStep = (2 * Math.PI) / count;
    const startAngle = -Math.PI / 2;

    return worldTracks.map((track, index) => {
        // Real progress from cache
        const progress = getTrackProgress(track.trackSlug);

        return {
            id: track.trackSlug, // Use slug as ID for compatibility
            title: track.label,
            difficulty: track.difficulty,
            progressPct: progress,
            orbitIndex: 1,
            angleDeg: 0,
            radius: ringRadius,
            angle: startAngle + (index * angleStep),
            slug: track.trackSlug,
            worldSlug: track.worldSlug,
        };
    });
}
