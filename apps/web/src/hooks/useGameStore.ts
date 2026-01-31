import { create } from 'zustand';

interface GameStore {
    activeWorldSlug: string | null;
    activeTrackId: string | null;
    activeBossSlug: string | null;
    layout: {
        rightPanelMode: 'closed' | 'open';
        rightPanelExpanded: boolean;
    };

    setActiveWorldSlug: (slug: string | null) => void;
    setActiveTrackId: (id: string | null) => void;
    setActiveBossSlug: (slug: string | null) => void;
    setLayout: (layout: Partial<GameStore['layout']>) => void;
}

export const useGameStore = create<GameStore>((set) => ({
    activeWorldSlug: null,
    activeTrackId: null,
    activeBossSlug: null,
    layout: {
        rightPanelMode: 'open',
        rightPanelExpanded: false,
    },

    setActiveWorldSlug: (slug) => set({ activeWorldSlug: slug }),
    setActiveTrackId: (id) => set({ activeTrackId: id }),
    setActiveBossSlug: (slug) => set({ activeBossSlug: slug }),
    setLayout: (newLayout) => set((state) => ({
        layout: { ...state.layout, ...newLayout }
    })),
}));
