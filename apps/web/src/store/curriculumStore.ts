import { create } from 'zustand';
import { OrionWorldId } from '@/layouts/orion/types';

export interface Track {
    id: string;
    title: string;
    worldId: OrionWorldId;
    difficulty: 'novice' | 'intermediate' | 'advanced';
    progress: number;
}

interface CurriculumState {
    activeWorldId: OrionWorldId;
    activeTrackId: string | null;
    tracks: Track[];

    setActiveWorldId: (id: OrionWorldId) => void;
    setActiveTrackById: (id: string) => void;
}

// Mock Data
const MOCK_TRACKS: Track[] = [
    { id: 'py-1', title: 'Python Basics', worldId: 'world-python', difficulty: 'novice', progress: 100 },
    { id: 'py-2', title: 'Data Structures', worldId: 'world-python', difficulty: 'intermediate', progress: 45 },
    { id: 'py-3', title: 'Asyncio Deep Dive', worldId: 'world-python', difficulty: 'advanced', progress: 0 },
    { id: 'js-1', title: 'ES6+ Features', worldId: 'world-js', difficulty: 'novice', progress: 80 },
    { id: 'js-2', title: 'React Hooks', worldId: 'world-js', difficulty: 'intermediate', progress: 20 },
    { id: 'sql-1', title: 'Select & Joins', worldId: 'world-sql', difficulty: 'novice', progress: 10 },
    { id: 'infra-1', title: 'Docker Basics', worldId: 'world-infra', difficulty: 'novice', progress: 0 },
];

export const useCurriculumStore = create<CurriculumState>((set) => ({
    activeWorldId: 'world-python',
    activeTrackId: null,
    tracks: MOCK_TRACKS,

    setActiveWorldId: (id) => set({ activeWorldId: id }),
    setActiveTrackById: (id) => set({ activeTrackId: id }),
}));
