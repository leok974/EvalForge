import React, { useEffect } from "react";

/**
 * TODO:
 * Export LifecycleLogger({ onMount, onUnmount }).
 * - Call onMount() once after mount
 * - Call onUnmount() once on unmount (cleanup)
 * Use useEffect with correct deps. No JSX.
 */
export function LifecycleLogger(_props) {
    // TODO: implement useEffect wiring
    useEffect(() => { }, []);

    return React.createElement("div", { "data-testid": "logger" }, "logger");
}
