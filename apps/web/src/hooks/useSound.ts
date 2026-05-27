// Sprint 22: LayoutId and layout removed from gameStore. Workshop is the only layout.
// THEME_ASSETS simplified to a single workshop set.
import { useCallback, useEffect, useRef } from 'react';
import { Howl } from 'howler';
import { useSettingsStore } from '../store/settingsStore';

export type SoundKey = 'click' | 'hover' | 'type' | 'success' | 'boss' | 'lock';

const WORKSHOP_SOUNDS: Partial<Record<SoundKey, string>> = {
    click: '/sounds/work_tock.mp3',
    hover: '/sounds/work_hover.mp3',
    success: '/sounds/work_bell.mp3',
    boss: '/sounds/work_whistle.mp3',
};

export function useSound() {
    const { masterVolume, sfxVolume, uiVolume, muted } = useSettingsStore();
    const howls = useRef<Record<string, Howl>>({});

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            Object.values(howls.current).forEach(h => h.unload());
        };
    }, []);

    const getHowl = (key: string): Howl | null => {
        if (!howls.current[key]) {
            const src = WORKSHOP_SOUNDS[key as SoundKey];
            if (!src) return null;
            howls.current[key] = new Howl({ src: [src], preload: true, volume: 1.0 });
        }
        return howls.current[key];
    };

    const play = useCallback((key: SoundKey) => {
        if (muted) return;

        const howl = getHowl(key);
        if (!howl) return;

        let vol = masterVolume;
        if (['click', 'hover', 'type'].includes(key)) vol *= uiVolume;
        else vol *= sfxVolume;

        howl.volume(vol);
        howl.play();
    }, [masterVolume, sfxVolume, uiVolume, muted]);

    return { play };
}
