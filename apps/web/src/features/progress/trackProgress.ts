import { fetchWorldProgress } from '@/api/worldProgress';
import { emitWorldProgressUpdated } from '@/lib/worldProgressEvents';

const trackProgressCache = new Map<string, number>();

export function setTrackProgress(slug: string, progress: number) {
    trackProgressCache.set(slug, progress);
}

export function getTrackProgress(slug: string): number {
    return trackProgressCache.get(slug) ?? 0;
}

// 🔥 New: refresh from backend + notify listeners
export async function refreshWorldProgress(
    changedTrackSlug?: string
): Promise<void> {
    const data = await fetchWorldProgress();

    trackProgressCache.clear();
    for (const track of data.tracks) {
        trackProgressCache.set(track.track_slug, track.progress);
    }

    emitWorldProgressUpdated({
        type: 'world-progress-updated',
        trackSlug: changedTrackSlug,
    });
}
