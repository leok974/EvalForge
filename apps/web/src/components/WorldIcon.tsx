import React from 'react';
import {
    Aperture, Factory, Sun, Gem, Database, Server,
    Bot, GitBranch, Brain, Box, HelpCircle
} from 'lucide-react';

const ICON_MAP: Record<string, any> = {
    "aperture": Aperture,     // The Construct
    "factory": Factory,       // The Foundry
    "sun": Sun,               // The Prism
    "gem": Gem,               // Crystal Spire
    "database": Database,     // Archives
    "server": Server,         // The Grid
    "bot": Bot,               // The Oracle
    "git-branch": GitBranch,  // Timeline
    "brain": Brain,           // Synapse
    "box": Box                // Fallback
};

interface Props {
    iconName: string;
    className?: string;
}

export function WorldIcon({ iconName, className }: Props) {
    const Icon = ICON_MAP[iconName] || HelpCircle;
    return <Icon className={className} />;
}
