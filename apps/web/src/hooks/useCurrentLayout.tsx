/**
 * Sprint 22: Layout system simplified.
 *
 * CyberdeckLayout and OrionLayout have been deleted. Workshop is the only layout.
 * This hook is retained as a stub so that existing test mocks that reference it
 * continue to compile without changes. New code should read world-view preference
 * from useSettingsStore().worldViewMode instead.
 *
 * LayoutProvider is a pass-through wrapper — it provides a context that always
 * returns { layout: 'workshop' } and a no-op setLayout.
 */

import React, { createContext, useContext, useMemo } from "react";

export type LayoutId = 'workshop';

interface LayoutContextValue {
    layout: LayoutId;
    setLayout: (id: LayoutId) => void;
}

const LayoutContext = createContext<LayoutContextValue | undefined>(undefined);

export const LayoutProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const value = useMemo<LayoutContextValue>(
        () => ({
            layout: 'workshop',
            setLayout: () => {}, // no-op: Workshop is the only layout
        }),
        [],
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
