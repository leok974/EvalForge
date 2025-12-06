import { useEffect, useRef } from 'react';
import { useGameStore, ActiveTrack } from '@/store/gameStore';

/**
 * Listens for activeTrack changes and calls onWarp(track)
 * exactly once per trackSlug. Use in Workshop / Cyberdeck to
 * auto-select the track when user warps from Orion.
 */
export function useTrackWarp(onWarp: (track: ActiveTrack) => void) {
    const activeTrack = useGameStore((s) => s.activeTrack);
    const lastTrackSlugRef = useRef<string | null>(null);

    useEffect(() => {
        if (!activeTrack) return;

        // avoid re-applying the same warp
        if (lastTrackSlugRef.current === activeTrack.trackSlug) return;

        onWarp(activeTrack);
        lastTrackSlugRef.current = activeTrack.trackSlug;
    }, [activeTrack, onWarp]);
}
