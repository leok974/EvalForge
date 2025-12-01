import { useCallback, useEffect, useRef } from 'react';
import { Howl } from 'howler';
import { useSettingsStore } from '../store/settingsStore';
import { useGameStore, LayoutId } from '../store/gameStore';

export type SoundKey = 'click' | 'hover' | 'type' | 'success' | 'boss' | 'lock';

const THEME_ASSETS: Record<LayoutId, Partial<Record<SoundKey, string>>> = {
    cyberdeck: {
        click: '/sounds/click.mp3',
        hover: '/sounds/hover.mp3',
        type: '/sounds/typewriter.mp3',
        success: '/sounds/success.mp3',
        boss: '/sounds/boss_alarm.mp3',
        lock: '/sounds/access_denied.mp3'
    },
    navigator: {
        click: '/sounds/nav_beep.mp3',
        hover: '/sounds/nav_hum.mp3',
        success: '/sounds/nav_chime.mp3',
        boss: '/sounds/nav_alert.mp3',
    },
    workshop: {
        click: '/sounds/work_tock.mp3',
        hover: '/sounds/work_hover.mp3',
        success: '/sounds/work_bell.mp3',
        boss: '/sounds/work_whistle.mp3',
    }
};

const DEFAULTS = THEME_ASSETS.cyberdeck;

export function useSound() {
    const { masterVolume, sfxVolume, uiVolume, muted } = useSettingsStore();
    const layout = useGameStore((s) => s.layout);
    const howls = useRef<Record<string, Record<string, Howl>>>({});

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            Object.values(howls.current).forEach(themeMap =>
                Object.values(themeMap).forEach(h => h.unload())
            );
        };
    }, []);

    const getHowl = (theme: string, key: string): Howl | null => {
        if (!howls.current[theme]) howls.current[theme] = {};

        if (!howls.current[theme][key]) {
            // Resolve asset with fallback
            // @ts-ignore
            const src = THEME_ASSETS[theme]?.[key] || DEFAULTS[key];
            if (!src) return null;

            howls.current[theme][key] = new Howl({
                src: [src],
                preload: true,
                volume: 1.0
            });
        }
        return howls.current[theme][key];
    };

    const play = useCallback((key: SoundKey) => {
        if (muted) return;

        const howl = getHowl(layout, key);
        if (!howl) return;

        let vol = masterVolume;
        if (['click', 'hover', 'type'].includes(key)) vol *= uiVolume;
        else vol *= sfxVolume;

        howl.volume(vol);
        howl.play();
    }, [layout, masterVolume, sfxVolume, uiVolume, muted]);

    return { play };
}
