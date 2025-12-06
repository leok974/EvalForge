import { renderHook, act } from '@testing-library/react';
import { useTrackWarp } from '../useTrackWarp';
import { useGameStore } from '@/store/gameStore';
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('useTrackWarp', () => {
    beforeEach(() => {
        // Reset store
        useGameStore.setState({ activeTrack: null });
    });

    it('calls onWarp when activeTrack changes', () => {
        const onWarp = vi.fn();
        renderHook(() => useTrackWarp(onWarp));

        const track = {
            worldSlug: 'python',
            trackSlug: 'python-basics',
            label: 'Python Basics',
            difficulty: 'NOVICE' as const
        };

        act(() => {
            useGameStore.setState({ activeTrack: track });
        });

        expect(onWarp).toHaveBeenCalledTimes(1);
        expect(onWarp).toHaveBeenCalledWith(track);
    });

    it('does not call onWarp if activeTrack is null', () => {
        const onWarp = vi.fn();
        renderHook(() => useTrackWarp(onWarp));

        expect(onWarp).not.toHaveBeenCalled();
    });

    it('calls onWarp only once per track slug change (deduplication)', () => {
        const onWarp = vi.fn();
        renderHook(() => useTrackWarp(onWarp));

        const track1 = {
            worldSlug: 'python',
            trackSlug: 'python-basics',
            label: 'Python Basics',
            difficulty: 'NOVICE' as const
        };

        act(() => {
            useGameStore.setState({ activeTrack: track1 });
        });
        expect(onWarp).toHaveBeenCalledTimes(1);

        // Re-setting same track should not trigger again
        act(() => {
            // Create new object reference but same content to test deep check or slug check
            // Hook uses slug check: if (lastTrackSlugRef.current === activeTrack.trackSlug)
            useGameStore.setState({ activeTrack: { ...track1 } });
        });
        expect(onWarp).toHaveBeenCalledTimes(1);

        // Changing track should trigger
        const track2 = { ...track1, trackSlug: 'python-advanced' };
        act(() => {
            useGameStore.setState({ activeTrack: track2 });
        });
        expect(onWarp).toHaveBeenCalledTimes(2);
    });
});
