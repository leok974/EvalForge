import { useEffect, useState } from 'react';
import { fetchWorldProgress } from '@/api/worldProgress';
import { setTrackProgress } from '@/features/progress/trackProgress';

export function useWorldProgressBootstrap() {
    const [loaded, setLoaded] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        let cancelled = false;

        async function load() {
            try {
                const data = await fetchWorldProgress();
                if (cancelled) return;

                for (const track of data.tracks) {
                    setTrackProgress(track.track_slug, track.progress);
                }

                setLoaded(true);
            } catch (err) {
                if (!cancelled) {
                    setError(err as Error);
                    console.error("Failed to load world progress:", err);
                }
            }
        }

        load();

        return () => {
            cancelled = true;
        };
    }, []);

    return { loaded, error };
}
