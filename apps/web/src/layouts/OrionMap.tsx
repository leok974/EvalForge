import { ORION_WORLDS, OrionWorldId, OrionWorldConfig, OrionTrackNode } from "./orion/types";
import { useMemo, useState } from "react";
import { buildOrionTracks } from "./orion/adapters";
import { cn } from "@/lib/utils";
import { useGameStore } from "@/store/gameStore";
import { fxEnabled } from "@/lib/featureFlags";

type Props = {
    activeWorldId: OrionWorldId;
    onWorldChange: (worldId: OrionWorldId) => void;
    onTrackSelected: (trackId: string) => void;
};

type ParallaxState = { x: number; y: number }; // normalized -1..1

export function OrionMap({ activeWorldId, onWorldChange, onTrackSelected }: Props) {
    const [hoverTrackId, setHoverTrackId] = useState<string | null>(null);
    const [parallax, setParallax] = useState<ParallaxState>({ x: 0, y: 0 });

    const activeWorld: OrionWorldConfig =
        ORION_WORLDS.find((w) => w.id === activeWorldId) ?? ORION_WORLDS[0];

    const tracks: OrionTrackNode[] = useMemo(
        () => buildOrionTracks(activeWorld.id),
        [activeWorld.id]
    );

    const selectedTrack =
        tracks.find((t) => t.id === hoverTrackId) ?? tracks[0] ?? null;

    function handleMouseMove(e: React.MouseEvent<HTMLDivElement>) {
        if (!fxEnabled) return;
        if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return;

        const rect = e.currentTarget.getBoundingClientRect();
        const nx = (e.clientX - rect.left) / rect.width;  // 0..1
        const ny = (e.clientY - rect.top) / rect.height;  // 0..1

        const x = (nx - 0.5) * 2; // -1..1
        const y = (ny - 0.5) * 2; // -1..1

        setParallax({ x: Math.max(-1, Math.min(1, x)), y: Math.max(-1, Math.min(1, y)) });
    }

    function handleMouseLeave() {
        if (!fxEnabled) return;
        setParallax({ x: 0, y: 0 });
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
                        tracks={tracks}
                        onWorldChange={onWorldChange}
                        onTrackHover={setHoverTrackId}
                        onTrackClick={(id) => {
                            onTrackSelected(id);
                            setHoverTrackId(id);
                        }}
                        parallax={parallax}
                    />
                </div>

                <div className="relative w-[320px] border-l border-cyan-400/25 bg-slate-950/80 backdrop-blur-sm">
                    <InfoPanel world={activeWorld} track={selectedTrack} />
                </div>
            </div>
        </div>
    );
}

function GalaxyView({
    activeWorld,
    tracks,
    onWorldChange,
    onTrackHover,
    onTrackClick,
    parallax,
}: {
    activeWorld: OrionWorldConfig;
    tracks: OrionTrackNode[];
    onWorldChange: (id: OrionWorldId) => void;
    onTrackHover: (id: string | null) => void;
    onTrackClick: (id: string) => void;
    parallax: { x: number; y: number };
}) {
    const orbitIndices = Array.from(new Set(tracks.map((t) => t.orbitIndex)));

    const worldParallaxStyle = fxEnabled
        ? {
            transform: `translate3d(${parallax.x * 18}px, ${parallax.y * 12}px, 0)`,
        }
        : undefined;

    const orbitParallaxStyle = fxEnabled
        ? {
            transform: `translate3d(${parallax.x * -10}px, ${parallax.y * -8}px, 0)`,
        }
        : undefined;

    return (
        <div className="relative flex h-full w-full items-center justify-center">
            {/* World selector planets (outer ring) */}
            <div
                className="absolute inset-0 flex items-center justify-center pointer-events-none"
                style={worldParallaxStyle}
            >
                <div
                    className={cn(
                        "relative h-[520px] w-[520px] pointer-events-auto",
                        fxEnabled && "orion-spin-worlds"
                    )}
                >
                    {ORION_WORLDS.map((world) => {
                        const radius = 230;
                        const angle = (world.angleDeg * Math.PI) / 180;
                        const x = Math.cos(angle) * radius;
                        const y = Math.sin(angle) * radius;
                        const isActive = world.id === activeWorld.id;

                        return (
                            <button
                                key={world.id}
                                onClick={() => onWorldChange(world.id)}
                                className={cn(
                                    "absolute -translate-x-1/2 -translate-y-1/2 rounded-full border-2 transition-transform duration-200 ease-out",
                                    isActive ? "scale-110" : "scale-95 hover:scale-105"
                                )}
                                style={{
                                    left: `calc(50% + ${x}px)`,
                                    top: `calc(50% + ${y}px)`,
                                    borderColor: world.color,
                                    boxShadow: isActive
                                        ? `0 0 25px ${world.color}55`
                                        : `0 0 10px ${world.color}33`,
                                }}
                            >
                                <div
                                    className="flex h-14 w-14 items-center justify-center rounded-full bg-slate-950/90"
                                    style={{
                                        backgroundImage: `radial-gradient(circle at 30% 20%, ${world.color}, transparent 55%)`,
                                    }}
                                >
                                    <span className="text-[10px] font-semibold tracking-[0.18em] text-slate-50">
                                        {world.label}
                                    </span>
                                </div>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Orbit rings + track nodes */}
            <div
                className="absolute inset-0 flex items-center justify-center pointer-events-none"
                style={orbitParallaxStyle}
            >
                <div
                    className={cn(
                        "relative h-[420px] w-[420px] pointer-events-auto",
                        fxEnabled && "orion-spin-orbits"
                    )}
                >
                    {/* Orbits */}
                    {orbitIndices.map((orbitIndex) => {
                        const size = 120 + orbitIndex * 60;
                        return (
                            <div
                                key={orbitIndex}
                                className="absolute rounded-full border border-cyan-400/25"
                                style={{
                                    width: size * 2,
                                    height: size * 2,
                                    left: "50%",
                                    top: "50%",
                                    transform: "translate(-50%, -50%)",
                                }}
                            />
                        );
                    })}

                    {/* Track nodes */}
                    {tracks.map((track) => {
                        const radius = 120 + track.orbitIndex * 60;
                        const angle = (track.angleDeg * Math.PI) / 180;
                        const x = Math.cos(angle) * radius;
                        const y = Math.sin(angle) * radius;
                        const progress = Math.round(track.progressPct);

                        return (
                            <button
                                key={track.id}
                                onMouseEnter={() => onTrackHover(track.id)}
                                onMouseLeave={() => onTrackHover(null)}
                                onClick={() => onTrackClick(track.id)}
                                className="absolute -translate-x-1/2 -translate-y-1/2"
                                style={{
                                    left: `calc(50% + ${x}px)`,
                                    top: `calc(50% + ${y}px)`,
                                }}
                            >
                                <div className="rounded-full border border-cyan-400/70 bg-slate-950/90 px-3 py-1.5 text-center text-[10px] tracking-[0.16em] text-slate-50 shadow-[0_0_16px_rgba(56,189,248,0.55)] hover:bg-cyan-500/10">
                                    <div className="truncate">{track.title}</div>
                                    <div className="mt-0.5 text-[9px] text-slate-400">
                                        {progress}% • {track.difficulty.toUpperCase()}
                                    </div>
                                </div>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Central planet stays in the middle */}
            <div
                className={cn(
                    "absolute flex items-center justify-center rounded-full border-2 border-cyan-300 shadow-[0_0_40px_rgba(56,189,248,0.8)]",
                    fxEnabled && "orion-planet-breathe"
                )}
                style={{
                    width: activeWorld.radius * 2,
                    height: activeWorld.radius * 2,
                    left: "50%",
                    top: "50%",
                    transform: "translate(-50%, -50%)",
                    backgroundImage: `radial-gradient(circle at 35% 25%, ${activeWorld.color}, #020617 55%)`,
                }}
            >
                <span className="text-xs font-semibold tracking-[0.22em]">
                    {activeWorld.label} WORLD
                </span>
            </div>
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
    const { setLayout } = useGameStore();

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

            {/* Later: quest/boss details, small log, etc. */}
            <div className="mt-auto flex flex-col gap-2">
                <button className="rounded-lg border border-cyan-400/70 bg-cyan-500/15 px-3 py-2 text-[11px] font-semibold tracking-[0.2em] text-cyan-100 shadow-[0_0_16px_rgba(34,211,238,0.7)] hover:bg-cyan-500/25">
                    WARP TO TRACK
                </button>
                <button
                    onClick={() => setLayout("cyberdeck")}
                    className="rounded-lg border border-slate-500/70 bg-slate-900/80 px-3 py-2 text-[10px] tracking-[0.18em] text-slate-300 hover:border-cyan-400/50 hover:text-cyan-100"
                >
                    OPEN IN CYBERDECK
                </button>
            </div>
        </div>
    );
}
