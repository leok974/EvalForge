import { create } from 'zustand';

export interface QuestState {
    activeWorldSlug: string | null;
    activeTrackId: string | null;
    activeBossSlug: string | null;
    focusMode: boolean;

    lastRunResult: any | null; // Typed loosely to avoid circular deps if needed, but ideally RunResult
    setLastRunResult: (result: any | null) => void;

    // Editor State
    editorActivePath: string | null;
    editorFiles: Record<string, { content: string }>;
    setEditorState: (activePath: string | null, files: Record<string, { content: string }>) => void;

    setActiveWorldSlug: (slug: string | null) => void;
    setActiveTrackId: (id: string | null) => void;
    setActiveBossSlug: (slug: string | null) => void;
    toggleFocusMode: () => void;
}

export const useQuestStore = create<QuestState>((set) => ({
    activeWorldSlug: null,
    activeTrackId: null,
    activeBossSlug: null,
    focusMode: typeof window !== 'undefined' ? localStorage.getItem('evalforge:focus_mode') === 'true' : false,

    lastRunResult: null,
    setLastRunResult: (result) => set({ lastRunResult: result }),

    // Editor State (Synced from QuestIDE for Tools access)
    editorActivePath: null,
    editorFiles: {},
    setEditorState: (activePath, files) => set({ editorActivePath: activePath, editorFiles: files }),

    setActiveWorldSlug: (slug) => set({ activeWorldSlug: slug }),
    setActiveTrackId: (id) => set({ activeTrackId: id }),
    setActiveBossSlug: (slug) => set({ activeBossSlug: slug }),
    toggleFocusMode: () => set((state) => {
        const next = !state.focusMode;
        localStorage.setItem('evalforge:focus_mode', String(next));
        return { focusMode: next };
    }),
}));
