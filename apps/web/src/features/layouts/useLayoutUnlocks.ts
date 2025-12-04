import { useMemo } from "react";
import { LAYOUT_OPTIONS, LayoutId } from "./layoutConfig";
import { useGameStore } from "../../store/gameStore";

const UNLOCK_ALL =
    import.meta.env.VITE_LAYOUT_UNLOCK_ALL === "1" ||
    import.meta.env.VITE_UNLOCK_ALL === "1";

export interface LayoutUnlockState {
    id: LayoutId;
    label: string;
    description: string;
    unlocked: boolean;
    lockedReason?: string;
}

export function useLayoutUnlocks(): LayoutUnlockState[] {
    const { level, integrity } = useGameStore();

    // Progression Rules (Placeholders based on available store data)
    const orionUnlockedFromProgress = level >= 3;
    const workshopUnlockedFromProgress = level >= 2; // Simplified for now

    return useMemo(() => {
        return LAYOUT_OPTIONS.map((opt) => {
            if (!opt.requiresUnlock || UNLOCK_ALL) {
                return {
                    ...opt,
                    unlocked: true,
                } satisfies LayoutUnlockState;
            }

            let unlocked = false;
            let lockedReason: string | undefined;

            if (opt.id === "orion") {
                unlocked = orionUnlockedFromProgress;
                if (!unlocked) {
                    lockedReason = "Unlock Orion by reaching Level 3.";
                }
            } else if (opt.id === "workshop") {
                unlocked = workshopUnlockedFromProgress;
                if (!unlocked) {
                    lockedReason = "Unlock Workshop by reaching Level 2.";
                }
            }

            return {
                ...opt,
                unlocked,
                lockedReason,
            } satisfies LayoutUnlockState;
        });
    }, [orionUnlockedFromProgress, workshopUnlockedFromProgress]);
}

/**
 * Utility for enforcing layout validity (used by layout context / DevUI).
 */
export function enforceLayoutUnlocked(
    requested: LayoutId | null | undefined,
    states: LayoutUnlockState[],
): LayoutId {
    const fallback: LayoutId = "cyberdeck";

    if (!requested) return fallback;

    const match = states.find((s) => s.id === requested);
    if (!match) return fallback; // unknown id

    if (!match.unlocked) {
        return fallback;
    }

    return match.id;
}
