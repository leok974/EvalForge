import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsState {
    // Audio
    masterVolume: number; // 0.0 to 1.0
    sfxVolume: number;
    uiVolume: number;
    muted: boolean;

    // Visuals
    // Sprint 22: crtMode removed — Cyberdeck layout (the only user of CRT effects) was deleted.
    screenShake: boolean;
    particles: boolean;

    // World view mode: 'grid' (default QuestBoard) or 'map' (OrionMap star-chart)
    worldViewMode: 'grid' | 'map';

    // Actions
    setVolume: (type: 'master' | 'sfx' | 'ui', val: number) => void;
    toggleMute: () => void;
    toggleVisual: (key: 'screenShake' | 'particles') => void;
    setWorldViewMode: (mode: 'grid' | 'map') => void;
}

export const useSettingsStore = create<SettingsState>()(
    persist(
        (set) => ({
            masterVolume: 0.5,
            sfxVolume: 0.8,
            uiVolume: 0.3,
            muted: false,

            screenShake: true,
            particles: true,
            worldViewMode: 'grid',

            setVolume: (type, val) => set((state) => {
                const key = type === 'master' ? 'masterVolume' : type === 'sfx' ? 'sfxVolume' : 'uiVolume';
                return { [key]: Math.max(0, Math.min(1, val)) };
            }),

            toggleMute: () => set((state) => ({ muted: !state.muted })),

            toggleVisual: (key) => set((state) => ({ [key]: !state[key] })),

            setWorldViewMode: (mode) => set({ worldViewMode: mode }),
        }),
        { name: 'evalforge-settings' }
    )
);
