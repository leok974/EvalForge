
export type MinimalTrack = { worldSlug: string; trackSlug: string };
export type MinimalUniverse = { worlds: { slug: string; tracks: { id: string }[] }[] };

/**
 * Validates if the currently selected project (track) exists in the universe.
 * If invalid (stale), returns null.
 * If valid, returns the track.
 */
export function resolveSelectedProject(
    currentTrack: MinimalTrack | null,
    universe: MinimalUniverse
): MinimalTrack | null {
    if (!currentTrack) return null;

    // 1. Check World
    const world = universe.worlds.find(w => w.slug === currentTrack.worldSlug);
    if (!world) {
        return null;
    }

    // 2. Check Track
    const track = world.tracks.find(t => t.id === currentTrack.trackSlug);
    if (!track) {
        return null;
    }

    return currentTrack;
}
