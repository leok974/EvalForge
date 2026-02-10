import { useSearchParams } from 'react-router-dom';
import { useCallback } from 'react';

export function useOpenCodex() {
    const [searchParams, setSearchParams] = useSearchParams();

    const openCodex = useCallback((ref: string) => {
        setSearchParams(prev => {
            const next = new URLSearchParams(prev);
            next.set('panel', 'codex');
            // Strip optional protocol for cleaner URL, but internal logic should handle it
            const term = ref.replace(/^codex:/, '');
            next.set('term', term);
            return next;
        });
    }, [setSearchParams]);

    return openCodex;
}
