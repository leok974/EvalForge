import { ComponentType } from "react";
import { CyberdeckLayout } from "@/components/layouts/CyberdeckLayout";

export type LayoutId = "cyberdeck" | "orion" | "workshop";

export interface LayoutDefinition {
    id: LayoutId;
    label: string;
    component: ComponentType<{ children: React.ReactNode }>;
}

// We'll populate this fully once we have the other layouts.
// For now, we point "cyberdeck" to the new v2 layout (or v1 if we want to toggle).
// But the plan says "Wire up feature flags", so we might want a wrapper that chooses.

import { OrionLayout } from "@/layouts/OrionLayout";
import { orionEnabled } from "@/lib/featureFlags";

export const LAYOUTS: LayoutDefinition[] = [
    { id: "cyberdeck", label: "Cyberdeck", component: CyberdeckLayout },
];

if (orionEnabled) {
    LAYOUTS.push({ id: "orion", label: "Orion Map", component: OrionLayout });
}

export const DEFAULT_LAYOUT: LayoutId = "cyberdeck";
