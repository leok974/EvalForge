import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { LayoutId } from "../features/layouts/layoutConfig";
import { useLayoutUnlocks, enforceLayoutUnlocked } from "../features/layouts/useLayoutUnlocks";
import { useGameStore } from "../store/gameStore";

const LAYOUT_STORAGE_KEY = "ef:layout";

interface LayoutContextValue {
    layout: LayoutId;
    setLayout: (id: LayoutId) => void;
}

const LayoutContext = createContext<LayoutContextValue | undefined>(undefined);

export const LayoutProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    // Initial state from URL > LocalStorage > Default (orion)
    const [layout, setInternalLayout] = useState<LayoutId>(() => {
        // 1. URL override
        const params = new URLSearchParams(window.location.search);
        const urlLayout = params.get('layout');
        if (urlLayout === 'orion' || urlLayout === 'cyberdeck') {
            return urlLayout;
        }

        // 2. LocalStorage
        try {
            const saved = localStorage.getItem(LAYOUT_STORAGE_KEY);
            if (saved === 'orion' || saved === 'cyberdeck') {
                return saved;
            }
        } catch (e) {
            console.warn("Layout storage read error", e);
        }

        // 3. Default
        return 'orion';
    });

    const setLayout = (id: LayoutId) => {
        if (id === 'workshop') return; // Deprecated
        setInternalLayout(id);
        localStorage.setItem(LAYOUT_STORAGE_KEY, id);

        // Sync to URL if present (optional, generally refrain from dirtying URL unless needed)
        // For deep linking support, we just respect it on load.
    };

    // removed legacy gameStore sync for now to avoid loops, 
    // unless gameStore is the source of truth for other things? 
    // The instructions say "Update useCurrentLayout to persist ef:layout".
    // We can sync TO gameStore if needed, but let's make this the authority for UI.
    const { setLayout: setStoreLayout } = useGameStore();
    useEffect(() => {
        setStoreLayout(layout);
    }, [layout, setStoreLayout]);


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
