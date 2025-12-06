import { OrionWorldId } from '@/layouts/orion/types';

export interface TrackConfig {
    id: string;
    slug: string;
    title: string;
    worldSlug: string; // Use 'python' instead of 'world-python' if you prefer, or mapped
    worldId: OrionWorldId; // Map to store type
    difficulty: 'novice' | 'intermediate' | 'advanced';
    description: string;
    progressPercent?: number; // In a real app this comes from user state, but config can have defaults
}

export const tracks: TrackConfig[] = [
    {
        id: 'py-1',
        slug: 'python-basics',
        title: 'Python Basics',
        worldSlug: 'python',
        worldId: 'world-python',
        difficulty: 'novice',
        description: 'Variables, loops, and functions.',
        progressPercent: 100
    },
    {
        id: 'py-2',
        slug: 'data-structures',
        title: 'Data Structures',
        worldSlug: 'python',
        worldId: 'world-python',
        difficulty: 'intermediate',
        description: 'Lists, dicts, and sets mastery.',
        progressPercent: 45
    },
    {
        id: 'py-3',
        slug: 'asyncio',
        title: 'Asyncio Deep Dive',
        worldSlug: 'python',
        worldId: 'world-python',
        difficulty: 'advanced',
        description: 'Concurrency and event loops.',
        progressPercent: 0
    },
    {
        id: 'js-1',
        slug: 'es6-features',
        title: 'ES6+ Features',
        worldSlug: 'js',
        worldId: 'world-js',
        difficulty: 'novice',
        description: 'Arrow functions and destructuring.',
        progressPercent: 80
    },
    {
        id: 'js-2',
        slug: 'react-hooks',
        title: 'React Hooks',
        worldSlug: 'js',
        worldId: 'world-js',
        difficulty: 'intermediate',
        description: 'State and effects.',
        progressPercent: 20
    },
    {
        id: 'sql-1',
        slug: 'select-joins',
        title: 'Select & Joins',
        worldSlug: 'sql',
        worldId: 'world-sql',
        difficulty: 'novice',
        description: 'Basic querying.',
        progressPercent: 10
    },
    {
        id: 'infra-1',
        slug: 'docker-basics',
        title: 'Docker Basics',
        worldSlug: 'infra',
        worldId: 'world-infra',
        difficulty: 'novice',
        description: 'Containerization fundamentals.',
        progressPercent: 0
    },
];
