import { ORION_WORLDS, OrionWorldId, OrionWorldConfig, OrionTrackNode } from "./orion/types";
import { useEffect, useMemo, useState } from "react";
import { getTrackNodesForWorld, getWorldNodes } from "./orion/adapters";
import { cn } from "@/lib/utils";
import { useGameStore, ActiveTrack } from "@/store/gameStore";
import { fxEnabled } from "@/lib/featureFlags";
import { subscribeWorldProgress } from "@/lib/worldProgressEvents";
import { subscribeWorldProgress } from "@/lib/worldProgressEvents";
import { LadderPanel } from "../features/ladders/LadderPanel";
import { useSeniorProgress } from "@/hooks/useSeniorProgress";

type ParallaxState = { x: number; y: number }; // normalized -1..1

export function OrionMap() {
    const [localWorldId, setLocalWorldId] = useState<OrionWorldId>('world-python');
    const [hoverTrackId, setHoverTrackId] = useState<string | null>(null);
    const [parallax, setParallax] = useState<ParallaxState>({ x: 0, y: 0 });

    // REAL-TIME UPDATES STATE
    const [progressVersion, setProgressVersion] = useState(0);
    const [highlightTrackSlug, setHighlightTrackSlug] = useState<string | null>(null);

    const activeTrack = useGameStore((s) => s.activeTrack);
    const setActiveTrack = useGameStore((s) => s.setActiveTrack);

    // 🔔 Listen for world progress updates
    useEffect(() => {
        const unsubscribe = subscribeWorldProgress((event) => {
            setProgressVersion((v) => v + 1);

            if (event.trackSlug) {
                setHighlightTrackSlug(event.trackSlug);
                // Clear highlight after a short glow
                window.setTimeout(() => {
                    setHighlightTrackSlug((current) =>
                        current === event.trackSlug ? null : current
                    );
                }, 1200);
            }
        });
        return unsubscribe;
    }, []);

    // Default to the first world if no valid ID
    const activeWorld: OrionWorldConfig =
        ORION_WORLDS.find((w) => w.id === localWorldId) ?? ORION_WORLDS[0];

    // Get all worlds for the navigation ring
    const worldNodes = useMemo(() => getWorldNodes(), []);

    const tracks: OrionTrackNode[] = useMemo(
        () => getTrackNodesForWorld(activeWorld.id),
        [activeWorld.id, progressVersion] // 👈 progressVersion forces recompute
    );

    const selectedTrack =
        tracks.find((t) => t.id === hoverTrackId) ?? tracks[0] ?? null;

    function handleMouseMove(e: React.MouseEvent<HTMLDivElement>) {
        if (!fxEnabled) return;
        if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return;

        const rect = e.currentTarget.getBoundingClientRect();
        const nx = (e.clientX - rect.left) / rect.width;  // 0..1
        const ny = (e.clientY - rect.top) / rect.height;  // 0..1

        const strength = 40;
        const x = (nx - 0.5) * strength;
        const y = (ny - 0.5) * strength;

        setParallax({ x: Math.max(-1, Math.min(1, x / 20)), y: Math.max(-1, Math.min(1, y / 20)) }); // Keep normalized state roughly same range but use stronger effect in render or just bump state range?
        // User patch said:
        // const strength = 40;
        // setOffset({ x: -relX * strength, y: -relY * strength });
        // My implementation uses normalized -1..1 state.

        // Let's adjust the calculation to match the "stronger" desire while keeping my state shape simple.
        // I will just bump the multipliers in the render function instead of changing state range here to minimize regression.
        setParallax({ x: (nx - 0.5) * 2, y: (ny - 0.5) * 2 });
    }

    function handleMouseLeave() {
        if (!fxEnabled) return;
        setParallax({ x: 0, y: 0 });
    }

    function handleWorldClick(worldId: OrionWorldId) {
        setLocalWorldId(worldId);

        // Clear active track if switching to a different world
        const targetWorld = ORION_WORLDS.find(w => w.id === worldId);
        if (activeTrack && targetWorld && activeTrack.worldSlug !== targetWorld.slug) {
            setActiveTrack(null);
        }
    }

    return (
        <div
            className="relative flex h-full w-full"
            onMouseMove={fxEnabled ? handleMouseMove : undefined}
            onMouseLeave={fxEnabled ? handleMouseLeave : undefined}
            data-testid="orion-map"
        >
            {/* starfield + grid */}
            <Starfield parallax={parallax} />

            {/* main map area */}
            <div className="relative z-10 flex flex-1">
                <div className="relative flex-1">
                    <GalaxyView
                        activeWorld={activeWorld}
                        worldNodes={worldNodes}
                        tracks={tracks}
                        onWorldChange={handleWorldClick}
                        onTrackHover={setHoverTrackId}
                        onTrackClick={(id) => {
                            // find the track node to pass full details
                            const trackNode = tracks.find(t => t.id === id);
                            if (trackNode) {
                                setActiveTrack({
                                    worldSlug: trackNode.worldSlug,
                                    trackSlug: trackNode.slug,
                                    label: trackNode.title
                                });
                            }
                        }}
                        parallax={parallax}
                        activeTrack={activeTrack}
                        highlightTrackSlug={highlightTrackSlug}
                    />
                </div>

                <div className="relative w-[320px] border-l border-cyan-400/25 bg-slate-950/80 backdrop-blur-sm hidden xl:block">
                    <InfoPanel world={activeWorld} track={selectedTrack} />
                </div>
            </div>
        </div>
    );
}

function GalaxyView({
    activeWorld,
    worldNodes,
    tracks,
    onWorldChange,
    onTrackHover,
    onTrackClick,
    parallax,
    activeTrack,
    highlightTrackSlug,
}: {
    activeWorld: OrionWorldConfig;
    worldNodes: ReturnType<typeof getWorldNodes>;
    tracks: OrionTrackNode[];
    onWorldChange: (id: OrionWorldId) => void;
    onTrackHover: (id: string | null) => void;
    onTrackClick: (id: string) => void;
    parallax: { x: number; y: number };
    activeTrack: ActiveTrack | null;
    highlightTrackSlug: string | null;
}) {
    return (
        <div className="absolute inset-0 flex items-center justify-center">
            {/* Central Planet (Active World) */}
            <div
                className={cn(
                    "absolute flex items-center justify-center rounded-full border-2 border-cyan-300 shadow-[0_0_40px_rgba(56,189,248,0.8)]",
                    fxEnabled && "orion-planet-breathe"
                )}
                style={{
                    width: activeWorld.radius * 2,
                    height: activeWorld.radius * 2,
                    // Parallax effect on planet? Optional
                    transform: `translate(${parallax.x * 10}px, ${parallax.y * 10}px)`,
                    backgroundImage: `radial-gradient(circle at 35% 25%, ${activeWorld.color}, #020617 55%)`,
                }}
            >
                <div className="flex flex-col items-center">
                    <span className="text-xs font-semibold tracking-[0.22em] text-white">
                        {activeWorld.label}
                    </span>
                    <span className="text-[9px] text-cyan-200/60 tracking-wider">SECTOR</span>
                </div>
            </div>

            {/* Orbiting Worlds (Navigation) */}
            {worldNodes.map((world: any) => { // TODO: Type this properly
                const isActive = world.id === activeWorld.id;
                // Calculate position based on its static angle from adapter
                const x = Math.cos(world.angle) * world.radius;
                const y = Math.sin(world.angle) * world.radius;

                return (
                    <button
                        key={world.id}
                        data-testid={`orion-world-${world.slug}`}
                        onClick={() => onWorldChange(world.id)}
                        className={cn(
                            "absolute flex h-12 w-12 items-center justify-center rounded-full border transition-all duration-500",
                            isActive
                                ? "border-cyan-300 bg-cyan-500/20 scale-110 shadow-[0_0_15px_rgba(34,211,238,0.4)]"
                                : "border-slate-800 bg-slate-900/40 text-slate-500 hover:border-cyan-500/50 hover:text-cyan-100"
                        )}
                        style={{
                            transform: `translate(calc(-50% + ${x + parallax.x * 5}px), calc(-50% + ${y + parallax.y * 5}px))`,
                        }}
                    >
                        <span className="text-[9px] font-bold tracking-wider">{world.label.slice(0, 3).toUpperCase()}</span>
                    </button>
                )
            })}

            {/* Tracks Orbiting */}
            {tracks.map((track) => {
                const x = Math.cos(track.angle) * track.radius;
                const y = Math.sin(track.angle) * track.radius;
                const progress = Math.round(track.progressPct);

                // Check selection using slugs
                const isSelected = activeTrack?.trackSlug === track.slug;
                const isHighlighted = highlightTrackSlug === track.slug;

                return (
                    <button
                        key={track.id}
                        onMouseEnter={() => onTrackHover(track.id)}
                        onMouseLeave={() => onTrackHover(null)}
                        onClick={() => onTrackClick(track.id)}
                        className="absolute"
                        style={{
                            // Start from center, add offset
                            transform: `translate(calc(-50% + ${x + parallax.x * 40}px), calc(-50% + ${y + parallax.y * 40}px))`,
                        }}
                    >
                        <div
                            className={cn(
                                "rounded-full border px-3 py-1.5 text-center text-[10px] tracking-[0.16em] shadow-[0_0_16px_rgba(56,189,248,0.55)] transition-all duration-300",
                                isSelected
                                    ? "border-cyan-300 bg-cyan-950/90 text-cyan-50 ring-2 ring-cyan-400/50 scale-110"
                                    : "border-cyan-400/70 bg-slate-950/90 text-slate-50 hover:bg-cyan-500/10 hover:border-cyan-300",
                                isHighlighted && "ring-2 ring-emerald-400 shadow-[0_0_24px_rgba(16,185,129,0.8)] scale-110 border-emerald-300"
                            )}
                        >
                            <div className="truncate">{track.title}</div>
                            <div className={cn("mt-0.5 text-[9px]", isSelected ? "text-cyan-200" : "text-slate-400")}>
                                {progress}% • {track.difficulty.toUpperCase()}
                            </div>
                        </div>
                    </button>
                );
            })}

        </div>
    );
}

function Starfield({ parallax }: { parallax: { x: number; y: number } }) {
    // tie parallax very lightly to star offset for extra depth
    const offsetX = parallax.x * 6;
    const offsetY = parallax.y * 4;

    return (
        <>
            {/* base gradient + grid (unchanged) */}
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,#38bdf8/18,transparent_55%),radial-gradient(circle_at_bottom,#0f172a,black)]" />
            <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(#0b1220_1px,transparent_1px),linear-gradient(90deg,#0b1220_1px,transparent_1px)] bg-[size:60px_60px] opacity-25" />

            {fxEnabled && (
                <>
                    {/* distant stars */}
                    <div
                        className="pointer-events-none absolute inset-0 orion-stars orion-stars-slow"
                        style={{
                            transform: `translate3d(${offsetX * 0.3}px, ${offsetY * 0.3}px, 0)`,
                        }}
                    />
                    {/* midlayer stars */}
                    <div
                        className="pointer-events-none absolute inset-0 orion-stars orion-stars-mid"
                        style={{
                            transform: `translate3d(${offsetX * 0.6}px, ${offsetY * 0.6}px, 0)`,
                        }}
                    />
                    {/* near stars */}
                    <div
                        className="pointer-events-none absolute inset-0 orion-stars orion-stars-fast"
                        style={{
                            transform: `translate3d(${offsetX}px, ${offsetY}px, 0)`,
                        }}
                    />
                </>
            )}
        </>
    );
}

function InfoPanel({
    world,
    track,
}: {
    world: OrionWorldConfig;
    track: OrionTrackNode | null;
}) {
    // const { setLayout } = useGameStore();
    const { data: senior } = useSeniorProgress();
    const currentWorldSenior = senior?.worlds.find(w => w.world_slug === world.id);

    return (
        <div className="flex h-full flex-col px-4 py-4">
            <div className="mb-3 text-[10px] font-hud tracking-[0.24em] text-slate-500">
                ORION CONSOLE
            </div>

            <div className="mb-4 rounded-xl border border-cyan-400/40 bg-slate-950/80 p-3 shadow-[0_0_18px_rgba(56,189,248,0.4)]">
                <div className="text-[11px] font-semibold tracking-[0.22em] text-slate-200">
                    SECTOR: {world.label} WORLD
                </div>
                {track && (
                    <>
                        <div className="mt-2 text-sm font-medium text-cyan-200">
                            {track.title}
                        </div>
                        <div className="mt-1 text-[10px] font-mono text-slate-400">
                            Difficulty: {track.difficulty.toUpperCase()} • Progress:{" "}
                            {Math.round(track.progressPct)}%
                        </div>
                    </>
                )}
            </div>

            {/* Senior Track Status */}
            {currentWorldSenior && currentWorldSenior.senior_track_id && (
                <div className="mb-4 rounded-xl border border-amber-500/30 bg-amber-950/20 p-3">
                    <div className="flex justify-between items-center mb-1">
                        <span className="text-[10px] font-bold text-amber-500 tracking-wider uppercase">Senior Track</span>
                        {currentWorldSenior.senior_boss_cleared && (
                            <span className="text-[9px] px-1.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">CLEARED</span>
                        )}
                    </div>
                    <div className="text-[10px] text-amber-200/80">
                        {currentWorldSenior.senior_quests_completed}/{currentWorldSenior.senior_quests_total} Quests Complete
                    </div>
                </div>
            )}

            {/* Ladder Panel (Only for Java currently) */}
            <LadderPanel worldSlug={world.slug} className="mb-4" />

            {/* Later: quest/boss details, small log, etc. */}
            <div className="mt-auto flex flex-col gap-2">
                {/* Buttons moved to OrionLayout footer */}
            </div>
        </div>
    );
}
