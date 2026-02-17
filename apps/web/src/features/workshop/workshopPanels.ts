import { WorkshopMode } from "../../layouts/WorkshopLayout";

export type PanelId = 'judge' | 'explain' | 'debug' | 'codex';

export interface PanelDefinition {
    id: PanelId;
    label: string;
    icon?: string; // Optional icon name if we use dynamic icons
    description: string;
    isEnabled: (context: PanelContext) => boolean;
    disabledReason?: (context: PanelContext) => string;
}

export interface PanelContext {
    hasSkill: (skill: string) => boolean;
    lastRun?: {
        stdout?: string;
        stderr?: string;
        exitCode?: number;
    };
    lastSubmission?: {
        grade?: number;
        passed?: boolean;
    };
    questSlug?: string;
}

export const WORKSHOP_PANELS: Record<PanelId, PanelDefinition> = {
    judge: {
        id: 'judge',
        label: 'Results',
        description: 'Submission verdict and test results.',
        isEnabled: () => true, // Always enabled, but might show empty state
    },
    explain: {
        id: 'explain',
        label: 'Explain',
        description: 'Analysis of current situation.',
        isEnabled: (ctx) => import.meta.env.DEV || ctx.hasSkill('agent_explain'),
        disabledReason: () => "Skill locked: Requires 'Agent Explain' module.",
    },
    debug: {
        id: 'debug',
        label: 'Debug',
        description: 'Fix proposal for failures.',
        isEnabled: (ctx) => import.meta.env.DEV || ctx.hasSkill('agent_debug'),
        disabledReason: () => "Skill locked: Requires 'Agent Debug' module.",
    },
    codex: {
        id: 'codex',
        label: 'Codex',
        description: 'Knowledge base and glossary.',
        isEnabled: () => true, // Always enabled
    }
};

export function getEnabledPanels(ctx: PanelContext): PanelDefinition[] {
    return Object.values(WORKSHOP_PANELS).filter(p => p.isEnabled(ctx));
}
