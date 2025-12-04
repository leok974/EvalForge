import { describe, it, expect } from "vitest";
import { enforceLayoutUnlocked } from "../useLayoutUnlocks";
import type { LayoutUnlockState } from "../useLayoutUnlocks";

const baseStates: LayoutUnlockState[] = [
    {
        id: "cyberdeck",
        label: "Cyberdeck",
        description: "",
        unlocked: true,
        requiresUnlock: false,
    },
    {
        id: "orion",
        label: "Orion",
        description: "",
        unlocked: false,
        requiresUnlock: true,
        lockedReason: "locked",
    },
    {
        id: "workshop",
        label: "Workshop",
        description: "",
        unlocked: false,
        requiresUnlock: true,
        lockedReason: "locked",
    },
];

describe("enforceLayoutUnlocked", () => {
    it("falls back to cyberdeck when requested is null or unknown", () => {
        expect(enforceLayoutUnlocked(null, baseStates)).toBe("cyberdeck");
        // @ts-expect-error for test
        expect(enforceLayoutUnlocked("unknown-layout", baseStates)).toBe("cyberdeck");
    });

    it("returns requested layout when unlocked", () => {
        expect(enforceLayoutUnlocked("cyberdeck", baseStates)).toBe("cyberdeck");
    });

    it("falls back to cyberdeck when requested layout is locked", () => {
        expect(enforceLayoutUnlocked("orion", baseStates)).toBe("cyberdeck");
        expect(enforceLayoutUnlocked("workshop", baseStates)).toBe("cyberdeck");
    });

    it("honors unlocked states for orion/workshop", () => {
        const unlockedAll: LayoutUnlockState[] = baseStates.map((s) => ({
            ...s,
            unlocked: true,
            lockedReason: undefined,
        }));
        expect(enforceLayoutUnlocked("orion", unlockedAll)).toBe("orion");
        expect(enforceLayoutUnlocked("workshop", unlockedAll)).toBe("workshop");
    });
});
