// Single source of truth for Orion + Workshop + Cyberdeck

export type WorldTrackConfig = {
    worldSlug: string; // 'python', 'javascript', 'sql', 'infra', 'agents', 'git', 'ml'
    trackSlug: string;
    label: string;
    difficulty: 'NOVICE' | 'INTERMEDIATE' | 'ADVANCED';
};

export const WORLD_TRACKS: WorldTrackConfig[] = [
    // Python (The Foundry)
    {
        worldSlug: 'python',
        trackSlug: 'python-basics',
        label: 'Python Basics',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'python',
        trackSlug: 'data-structures',
        label: 'Data Structures',
        difficulty: 'INTERMEDIATE',
    },

    // JavaScript (The Prism)
    {
        worldSlug: 'javascript',
        trackSlug: 'es6-features',
        label: 'ES6+ Features',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'javascript',
        trackSlug: 'react-hooks',
        label: 'React Hooks',
        difficulty: 'INTERMEDIATE',
    },

    // SQL (The Archives)
    {
        worldSlug: 'sql',
        trackSlug: 'select-joins',
        label: 'Select & Joins',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'sql',
        trackSlug: 'data-modeling',
        label: 'Data Modeling',
        difficulty: 'INTERMEDIATE',
    },

    // Infra (The Grid)
    {
        worldSlug: 'infra',
        trackSlug: 'docker-basics',
        label: 'Docker Basics',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'infra',
        trackSlug: 'service-link',
        label: 'Service Mesh & Deploy',
        difficulty: 'INTERMEDIATE',
    },

    // Agents (The Oracle)
    {
        worldSlug: 'agents',
        trackSlug: 'agent-invocation',
        label: 'Agent Invocation',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'agents',
        trackSlug: 'tooling-grounding',
        label: 'Tools & Grounding',
        difficulty: 'INTERMEDIATE',
    },

    // Git (The Timeline)
    {
        worldSlug: 'git',
        trackSlug: 'git-fundamentals',
        label: 'Git Fundamentals',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'git',
        trackSlug: 'branch-boss',
        label: 'Branch & Merge',
        difficulty: 'INTERMEDIATE',
    },

    // ML (The Synapse)
    {
        worldSlug: 'ml',
        trackSlug: 'tensors',
        label: 'Tensors & Gradients',
        difficulty: 'NOVICE',
    },
    {
        worldSlug: 'ml',
        trackSlug: 'training-loop',
        label: 'Training Loop',
        difficulty: 'INTERMEDIATE',
    },
];
