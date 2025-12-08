export type OrionWorldId =
    | "world-python"
    | "world-typescript"
    | "world-java"
    | "world-sql"
    | "world-infra"
    | "world-agents"
    | "world-git"
    | "world-ml";

export interface OrionWorldConfig {
    id: OrionWorldId;
    slug: string; // Added for URL structure
    label: string;
    color: string;  // main glow color
    radius: number; // "size" on screen
    angleDeg: number; // initial angle on ring
}

export interface OrionTrackNode {
    id: string;
    title: string;
    difficulty: "NOVICE" | "INTERMEDIATE" | "ADVANCED" | "novice" | "intermediate" | "advanced";
    progressPct: number;
    orbitIndex: number; // distance from center
    angleDeg: number;   // position on orbit
    radius: number;     // calculated polar radius (px)
    angle: number;      // calculated polar angle (radians)
    slug: string;       // unique slug for URL/Selection
    worldSlug: string;  // parent world slug
}

export const ORION_WORLDS: OrionWorldConfig[] = [
    { id: "world-python", slug: "python", label: "PYTHON", color: "#38bdf8", radius: 70, angleDeg: 210 },
    { id: "world-typescript", slug: "typescript", label: "THE PRISM", color: "#facc15", radius: 55, angleDeg: 320 },
    { id: "world-java", slug: "java", label: "THE REACTOR", color: "#ea580c", radius: 65, angleDeg: 140 },
    { id: "world-sql", slug: "sql", label: "SQL", color: "#22c55e", radius: 50, angleDeg: 30 },
    { id: "world-infra", slug: "infra", label: "INFRA", color: "#e5e5e5", radius: 60, angleDeg: 110 },
    { id: "world-agents", slug: "agents", label: "AGENTS", color: "#a855f7", radius: 58, angleDeg: 40 },
    { id: "world-git", slug: "git", label: "GIT", color: "#fb7185", radius: 45, angleDeg: 150 },
    { id: "world-ml", slug: "ml", label: "ML", color: "#2dd4bf", radius: 52, angleDeg: 270 },
];
