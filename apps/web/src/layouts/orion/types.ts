export type OrionWorldId =
    | "world-python"
    | "world-js"
    | "world-sql"
    | "world-infra"
    | "world-agents"
    | "world-git"
    | "world-ml";

export interface OrionWorldConfig {
    id: OrionWorldId;
    label: string;
    color: string;  // main glow color
    radius: number; // "size" on screen
    angleDeg: number; // initial angle on ring
}

export interface OrionTrackNode {
    id: string;
    title: string;
    difficulty: "novice" | "intermediate" | "advanced";
    progressPct: number;
    orbitIndex: number; // distance from center
    angleDeg: number;   // position on orbit
}

export const ORION_WORLDS: OrionWorldConfig[] = [
    { id: "world-python", label: "PYTHON", color: "#38bdf8", radius: 70, angleDeg: 210 },
    { id: "world-js", label: "JAVASCRIPT", color: "#facc15", radius: 55, angleDeg: 320 },
    { id: "world-sql", label: "SQL", color: "#22c55e", radius: 50, angleDeg: 30 },
    { id: "world-infra", label: "INFRA", color: "#e5e5e5", radius: 60, angleDeg: 110 },
    { id: "world-agents", label: "AGENTS", color: "#a855f7", radius: 58, angleDeg: 40 },
    { id: "world-git", label: "GIT", color: "#fb7185", radius: 45, angleDeg: 150 },
    { id: "world-ml", label: "ML", color: "#2dd4bf", radius: 52, angleDeg: 270 },
];
