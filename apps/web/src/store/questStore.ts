import { create } from 'zustand';

interface QuestState {
    activeWorldSlug: string | null;
    activeTrackId: string | null;
    activeBossSlug: string | null;

    setActiveWorldSlug: (slug: string | null) => void;
    setActiveTrackId: (id: string | null) => void;
    setActiveBossSlug: (slug: string | null) => void;
}

export const useQuestStore = create<QuestState>((set) => ({
    activeWorldSlug: null,
    activeTrackId: null,
    activeBossSlug: null,

    setActiveWorldSlug: (slug) => set({ activeWorldSlug: slug }),
    setActiveTrackId: (id) => set({ activeTrackId: id }),
    setActiveBossSlug: (slug) => set({ activeBossSlug: slug }),
}));
