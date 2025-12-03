import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type LayoutId = 'cyberdeck' | 'navigator' | 'workshop' | 'orion';

interface GameState {
    // --- Progression ---
    xp: number;
    level: number;
    activeQuestId: string | null;
    integrity: number;

    // --- Interface ---
    layout: LayoutId;
    setLayout: (layout: LayoutId) => void;

    // --- Actions ---
    addXp: (amount: number) => void;
    damageIntegrity: (amount: number) => void;
    restoreIntegrity: () => void;
    // We can add triggerBoss() or completeQuest() here later
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

            // Actions
            setLayout: (layout) => set({ layout }),

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
        }),
        { name: 'evalforge-save-data' } // LocalStorage key
    )
);
