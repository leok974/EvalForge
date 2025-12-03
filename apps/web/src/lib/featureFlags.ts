/// <reference types="vite/client" />

export const fxEnabled =
    import.meta.env.VITE_FX_ENABLED === "1" ||
    import.meta.env.VITE_FX_ENABLED === "true";

export const orionEnabled =
    import.meta.env.VITE_LAYOUT_ORION_ENABLED === "1" ||
    import.meta.env.VITE_LAYOUT_ORION_ENABLED === "true";
