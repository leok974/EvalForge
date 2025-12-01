import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsState {
    // Audio
    masterVolume: number; // 0.0 to 1.0
    sfxVolume: number;
    uiVolume: number;
    muted: boolean;

    // Visuals
    crtMode: boolean;
    screenShake: boolean;
    particles: boolean;

    // Actions
    setVolume: (type: 'master' | 'sfx' | 'ui', val: number) => void;
    toggleMute: () => void;
    toggleVisual: (key: 'crtMode' | 'screenShake' | 'particles') => void;
}

export const useSettingsStore = create<SettingsState>()(
    persist(
        (set) => ({
            masterVolume: 0.5,
            sfxVolume: 0.8,
            uiVolume: 0.3,
            muted: false,

            crtMode: false,
            screenShake: true,
            particles: true,

            setVolume: (type, val) => set((state) => {
                const key = type === 'master' ? 'masterVolume' : type === 'sfx' ? 'sfxVolume' : 'uiVolume';
                return { [key]: Math.max(0, Math.min(1, val)) };
            }),

            toggleMute: () => set((state) => ({ muted: !state.muted })),

            toggleVisual: (key) => set((state) => ({ [key]: !state[key] }))
        }),
        { name: 'evalforge-settings' }
    )
);
