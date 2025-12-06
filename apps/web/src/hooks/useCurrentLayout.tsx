import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { LayoutId } from "../features/layouts/layoutConfig";
import { useLayoutUnlocks, enforceLayoutUnlocked } from "../features/layouts/useLayoutUnlocks";
import { useGameStore } from "../store/gameStore";

const LAYOUT_STORAGE_KEY = "evalforge:layout";

interface LayoutContextValue {
    layout: LayoutId;
    setLayout: (id: LayoutId) => void;
}

const LayoutContext = createContext<LayoutContextValue | undefined>(undefined);

export const LayoutProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const unlockStates = useLayoutUnlocks();

    // We sync with gameStore for now, but enforce rules
    const { layout: storeLayout, setLayout: setStoreLayout } = useGameStore();

    // We use local state to handle the "requested" layout before enforcement
    // But actually, gameStore persists state, so we should probably just wrap that.

    const layout = useMemo(
        () => enforceLayoutUnlocked(storeLayout, unlockStates),
        [storeLayout, unlockStates],
    );

    const setLayout = (id: LayoutId) => {
        const enforced = enforceLayoutUnlocked(id, unlockStates);
        setStoreLayout(enforced);
    };

    // If the current store layout is invalid (e.g. locked), we should update it
    useEffect(() => {
        if (storeLayout !== layout) {
            setStoreLayout(layout);
        }
    }, [layout, storeLayout, setStoreLayout]);

    const value = useMemo(
        () => ({
            layout,
            setLayout,
        }),
        [layout, setLayout],
    );

    return <LayoutContext.Provider value={value}>{children}</LayoutContext.Provider>;
};

export function useCurrentLayout(): LayoutContextValue {
    const ctx = useContext(LayoutContext);
    if (!ctx) {
        throw new Error("useCurrentLayout must be used within LayoutProvider");
    }
    return ctx;
}
