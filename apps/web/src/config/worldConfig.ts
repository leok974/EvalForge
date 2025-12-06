
export interface World {
    slug: string;
    name: string;
    description: string;
    color: string;
}

export const worlds: World[] = [
    {
        slug: 'world-python',
        name: 'Python',
        description: 'Master the language of snakes and data.',
        color: 'cyan',
    },
    {
        slug: 'world-js',
        name: 'JavaScript',
        description: 'Apply functionality to the web substrate.',
        color: 'yellow',
    },
    {
        slug: 'world-sql',
        name: 'SQL',
        description: 'Query the multiverse databases.',
        color: 'purple',
    },
    {
        slug: 'world-infra',
        name: 'Infrastructure',
        description: 'Construct the underlying reality matrix.',
        color: 'orange',
    },
];
