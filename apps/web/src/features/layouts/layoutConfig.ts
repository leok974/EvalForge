export type LayoutId = "cyberdeck" | "orion" | "workshop";

export interface LayoutOption {
    id: LayoutId;
    label: string;
    description: string;
    requiresUnlock: boolean;
}

export const LAYOUT_OPTIONS: LayoutOption[] = [
    {
        id: "cyberdeck",
        label: "Cyberdeck",
        description: "Neon HUD for heads-down hacking.",
        requiresUnlock: false,
    },
    {
        id: "orion",
        label: "Orion",
        description: "Star map view for multi-world planning.",
        requiresUnlock: true,
    },
    {
        id: "workshop",
        label: "Workshop",
        description: "Isometric lab for projects and bosses.",
        requiresUnlock: true,
    },
];
