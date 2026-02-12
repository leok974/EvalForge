import React, { useEffect } from "react";

export function LifecycleLogger({ onMount, onUnmount } = {}) {
    useEffect(() => {
        if (typeof onMount === "function") onMount();
        return () => {
            if (typeof onUnmount === "function") onUnmount();
        };
    }, []);

    return React.createElement("div", { "data-testid": "logger" }, "logger");
}
