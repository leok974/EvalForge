import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type LayoutId = 'cyberdeck' | 'orion' | 'workshop';

export type ActiveTrack = {
    worldSlug: string;
    trackSlug: string;
    label: string;
};

interface GameState {
    // --- Progression ---
    xp: number;
    level: number;
    activeQuestId: string | null;
    integrity: number;
    bossesUnlocked: string[];

    // --- Interface ---
    layout: LayoutId;
    setLayout: (layout: LayoutId) => void;

    // --- Active State ---
    activeTrack: ActiveTrack | null;
    setActiveTrack: (track: ActiveTrack | null) => void;

    // --- Actions ---
    addXp: (amount: number) => void;
    damageIntegrity: (amount: number) => void;
    restoreIntegrity: () => void;
    setBossesUnlocked: (bosses: string[]) => void;
}

export const useGameStore = create<GameState>()(
    persist(
        (set) => ({
            // Initial State
            xp: 0,
            level: 1,
            activeQuestId: null,
            layout: 'cyberdeck',
            integrity: 100,
            bossesUnlocked: [],
            activeTrack: null,

            // Actions
            setLayout: (layout) => set({ layout }),
            setActiveTrack: (track) => set({ activeTrack: track }),

            addXp: (amount) => set((state) => {
                const newXp = state.xp + amount;
                // Simple formula: Level up every 1000 XP
                const newLevel = Math.floor(newXp / 1000) + 1;
                return { xp: newXp, level: newLevel };
            }),

            damageIntegrity: (amount) => set((state) => ({
                integrity: Math.max(0, state.integrity - amount)
            })),

            restoreIntegrity: () => set({ integrity: 100 }),

            setBossesUnlocked: (bosses) => set({ bossesUnlocked: bosses }),
        }),
        { name: 'evalforge-save-data' } // LocalStorage key
    )
);
