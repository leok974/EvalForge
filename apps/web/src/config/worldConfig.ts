
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
        slug: 'world-typescript',
        name: 'The Prism',
        description: 'Refract your logic through the lens of strict types.',
        color: 'yellow',
    },
    {
        slug: 'world-java',
        name: 'The Reactor',
        description: 'Forge robust systems in the fusion core.',
        color: 'orange',
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
