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
import { WorkshopLayout } from "@/layouts/WorkshopLayout";
import { orionEnabled } from "@/lib/featureFlags";

// We'll use a dummy wrapper for Workshop since it requires props, 
// but the registry expects ComponentType<{ children: React.ReactNode }>.
// Actually, GameShell handles the rendering logic, so this registry is mostly for the switcher labels.
// We can just pass the component and handle props in the consumer.

export const LAYOUTS: LayoutDefinition[] = [
    { id: "cyberdeck", label: "Cyberdeck", component: CyberdeckLayout },
];

if (orionEnabled) {
    LAYOUTS.push({ id: "orion", label: "Orion Map", component: OrionLayout });
}

// Workshop is always available if unlocked (logic handled in switcher)
// For now we add it here so it shows up.
LAYOUTS.push({
    id: "workshop",
    label: "Workshop",
    // @ts-ignore - WorkshopLayout props don't match children-only signature, but we handle it in DevUI
    component: WorkshopLayout
});

export const DEFAULT_LAYOUT: LayoutId = "cyberdeck";
