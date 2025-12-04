import { useEffect, useState, useCallback } from "react";

const STORAGE_KEY = "evalforge:workshop:tutorial-dismissed";

// 🔹 Shared event name + helper
export const WORKSHOP_GUIDE_OPEN_EVENT =
    "evalforge:workshop:guide:open";

export function openWorkshopGuide() {
    if (typeof window === "undefined") return;
    window.dispatchEvent(new CustomEvent(WORKSHOP_GUIDE_OPEN_EVENT));
}

export interface WorkshopTipsState {
    showTips: boolean;
    dismiss: () => void;
    open: () => void;
}

export function useWorkshopTips(): WorkshopTipsState {
    const [showTips, setShowTips] = useState<boolean>(false);

    // Read localStorage (SSR-safe)
    useEffect(() => {
        try {
            if (typeof window === "undefined") return;
            const raw = window.localStorage.getItem(STORAGE_KEY);
            if (raw === "1") {
                setShowTips(false);
            } else {
                setShowTips(true);
            }
        } catch {
            // If localStorage explodes for some reason, just show tips once.
            setShowTips(true);
        }
    }, []);

    const dismiss = useCallback(() => {
        setShowTips(false);
        try {
            if (typeof window !== "undefined") {
                window.localStorage.setItem(STORAGE_KEY, "1");
            }
        } catch {
            // ignore
        }
    }, []);

    const open = useCallback(() => {
        // Don’t touch localStorage here; just show the guide again.
        setShowTips(true);
    }, []);

    return { showTips, dismiss, open };
}
