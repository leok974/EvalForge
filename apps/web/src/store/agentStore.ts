import { create } from 'zustand';

interface AgentContext {
    codex_id?: string;
    track_id?: string;
    // Add other context fields as needed
}

interface AgentState {
    isOpen: boolean;
    mode: 'judge' | 'quest' | 'explain' | 'debug';
    context: AgentContext;
    initialPrompt?: string;

    // Actions
    openAgent: (mode: AgentState['mode'], context?: AgentContext, initialPrompt?: string) => void;
    closeAgent: () => void;
    setContext: (context: AgentContext) => void;
}

export const useAgentStore = create<AgentState>((set) => ({
    isOpen: false,
    mode: 'judge',
    context: {},

    openAgent: (mode, context = {}, initialPrompt) => set({
        isOpen: true,
        mode,
        context,
        initialPrompt
    }),

    closeAgent: () => set({ isOpen: false }),

    setContext: (context) => set((state) => ({
        context: { ...state.context, ...context }
    })),
}));
