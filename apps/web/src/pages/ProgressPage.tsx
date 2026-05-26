/**
 * Sprint 22.5: Progress page — /arcade/progress
 * Per-world / per-track quest completion view.
 * Data source: GET /api/worlds/progress → { tracks: TrackProgress[] }
 */
import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, BarChart2, CheckCircle2, Circle, Clock } from 'lucide-react';

interface TrackProgress {
    world_slug: string;
    track_slug: string;
    label: string;
    progress: number;       // 0.0 – 1.0
    total_quests: number;
    completed_quests: number;
}

interface WorldGroup {
    world_slug: string;
    tracks: TrackProgress[];
    total_quests: number;
    completed_quests: number;
}

const WORLD_LABELS: Record<string, string> = {
    'world-python': 'Python',
    'world-sql': 'SQL',
    'world-web': 'Web',
    'world-js': 'JavaScript',
    'world-typescript': 'TypeScript',
    'world-git': 'Git',
    'world-agents': 'Agents',
    'world-cli': 'CLI',
    'world-docker': 'Docker',
    'world-infra': 'Infra',
    'world-react': 'React',
};

const ACTIVE_WORLDS = new Set([
    'world-python', 'world-sql', 'world-web', 'world-js', 'world-typescript', 'world-git',
]);

function worldLabel(slug: string): string {
    return WORLD_LABELS[slug] || slug.replace('world-', '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function worldEmoji(slug: string): string {
    const map: Record<string, string> = {
        'world-python': '🐍',
        'world-sql': '🗄️',
        'world-web': '🌐',
        'world-js': '☁️',
        'world-typescript': '🔷',
        'world-git': '🌿',
        'world-agents': '🤖',
        'world-cli': '⚡',
        'world-docker': '🐳',
        'world-react': '⚛️',
    };
    return map[slug] || '🌍';
}

function ProgressBar({ value, color = 'cyan' }: { value: number; color?: 'cyan' | 'violet' | 'emerald' }) {
    const pct = Math.round(value * 100);
    const colorClass =
        color === 'violet' ? 'bg-workshop-violet' :
        color === 'emerald' ? 'bg-emerald-500' :
        'bg-workshop-cyan';
    return (
        <div className="h-1.5 w-full rounded-full bg-white/8 overflow-hidden">
            <div
                className={`h-full rounded-full transition-all duration-500 ${colorClass}`}
                style={{ width: `${pct}%` }}
            />
        </div>
    );
}

export function ProgressPage() {
    const [tracks, setTracks] = useState<TrackProgress[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showAll, setShowAll] = useState(false);

    useEffect(() => {
        fetch('/api/worlds/progress')
            .then(r => {
                if (!r.ok) throw new Error(`HTTP ${r.status}`);
                return r.json();
            })
            .then(data => setTracks(data.tracks || []))
            .catch(err => setError(err.message || 'Failed to load progress'))
            .finally(() => setLoading(false));
    }, []);

    // Group by world
    const worldGroups = useMemo<WorldGroup[]>(() => {
        const map = new Map<string, TrackProgress[]>();
        for (const t of tracks) {
            if (!map.has(t.world_slug)) map.set(t.world_slug, []);
            map.get(t.world_slug)!.push(t);
        }
        return Array.from(map.entries()).map(([world_slug, wTracks]) => ({
            world_slug,
            tracks: wTracks,
            total_quests: wTracks.reduce((n, t) => n + t.total_quests, 0),
            completed_quests: wTracks.reduce((n, t) => n + t.completed_quests, 0),
        }));
    }, [tracks]);

    // Sort: active worlds first (in order), then others
    const activeOrder = ['world-python', 'world-sql', 'world-web', 'world-js', 'world-typescript', 'world-git'];
    const sortedGroups = useMemo(() => {
        const active = activeOrder.flatMap(w => worldGroups.filter(g => g.world_slug === w));
        const others = worldGroups.filter(g => !ACTIVE_WORLDS.has(g.world_slug));
        return [...active, ...others];
    }, [worldGroups]);

    const visibleGroups = showAll ? sortedGroups : sortedGroups.filter(g => ACTIVE_WORLDS.has(g.world_slug));
    const hiddenCount = sortedGroups.length - visibleGroups.length;

    // Summary band
    const totalQuests = worldGroups.reduce((n, g) => n + g.total_quests, 0);
    const totalCompleted = worldGroups.reduce((n, g) => n + g.completed_quests, 0);
    const activeCompleted = sortedGroups.filter(g => ACTIVE_WORLDS.has(g.world_slug)).reduce((n, g) => n + g.completed_quests, 0);
    const activeTotal = sortedGroups.filter(g => ACTIVE_WORLDS.has(g.world_slug)).reduce((n, g) => n + g.total_quests, 0);

    return (
        <main className="min-h-screen bg-workshop-bg text-workshop-text font-sans selection:bg-workshop-violet/20 relative">
            {/* Ambient gradient */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-[400px] bg-workshop-violet/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[400px] bg-workshop-cyan/5 blur-[120px]" />
            </div>

            {/* Page header */}
            <header className="relative z-10 border-b border-white/5 bg-workshop-bg/60 backdrop-blur-sm px-6 py-4">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Link
                            to="/arcade/workshop"
                            className="flex items-center gap-1 text-xs text-workshop-subtle hover:text-workshop-text transition-colors"
                        >
                            <ChevronLeft className="w-3.5 h-3.5" />
                            Workshop
                        </Link>
                        <span className="text-white/20">/</span>
                        <div className="flex items-center gap-2">
                            <BarChart2 className="w-4 h-4 text-workshop-violet" />
                            <h1 className="text-sm font-semibold tracking-wide">Progress</h1>
                        </div>
                    </div>
                    <span className="text-[10px] text-workshop-subtle font-mono uppercase tracking-wider">
                        Quest Completion
                    </span>
                </div>
            </header>

            {/* Content */}
            <div className="relative z-10 max-w-4xl mx-auto px-6 py-8 space-y-6">

                {/* Summary band */}
                {!loading && !error && tracks.length > 0 && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        <StatCard label="Completed" value={totalCompleted.toString()} sub="all worlds" />
                        <StatCard label="Total Quests" value={totalQuests.toString()} sub="all worlds" />
                        <StatCard label="Active Score" value={`${activeTotal > 0 ? Math.round((activeCompleted / activeTotal) * 100) : 0}%`} sub="active worlds" accent="violet" />
                        <StatCard label="Worlds Active" value={visibleGroups.length.toString()} sub={`of ${sortedGroups.length}`} />
                    </div>
                )}

                {/* States */}
                {loading && (
                    <div className="text-center py-16 text-workshop-subtle text-sm animate-pulse">
                        Loading progress…
                    </div>
                )}

                {error && (
                    <div className="rounded-xl border border-red-800/50 bg-red-950/20 px-4 py-3 text-sm text-red-400">
                        {error}
                    </div>
                )}

                {!loading && !error && tracks.length === 0 && (
                    <div className="text-center py-16 space-y-3">
                        <div className="text-4xl">🏕️</div>
                        <p className="text-workshop-subtle text-sm">No quests completed yet.</p>
                        <Link
                            to="/arcade/workshop"
                            className="inline-block mt-2 px-4 py-2 rounded-lg bg-workshop-cyan/10 border border-workshop-cyan/30 text-workshop-cyan text-xs font-medium hover:bg-workshop-cyan/20 transition-colors"
                        >
                            Go to Workshop →
                        </Link>
                    </div>
                )}

                {/* World groups */}
                {!loading && !error && visibleGroups.length > 0 && (
                    <div className="space-y-4">
                        {visibleGroups.map(group => (
                            <WorldCard key={group.world_slug} group={group} />
                        ))}

                        {hiddenCount > 0 && !showAll && (
                            <button
                                onClick={() => setShowAll(true)}
                                className="w-full py-3 rounded-xl border border-white/8 bg-workshop-panel text-xs text-workshop-subtle hover:text-workshop-text hover:border-white/20 transition-colors"
                            >
                                Show {hiddenCount} more world{hiddenCount === 1 ? '' : 's'} (inactive / experimental)
                            </button>
                        )}
                    </div>
                )}
            </div>
        </main>
    );
}

function StatCard({ label, value, sub, accent }: { label: string; value: string; sub: string; accent?: 'violet' | 'cyan' }) {
    const valClass = accent === 'violet' ? 'text-workshop-violet' : accent === 'cyan' ? 'text-workshop-cyan' : 'text-workshop-text';
    return (
        <div className="rounded-xl bg-workshop-panel border border-white/8 p-4 space-y-1">
            <div className={`text-2xl font-bold font-mono ${valClass}`}>{value}</div>
            <div className="text-xs font-medium text-workshop-text">{label}</div>
            <div className="text-[10px] text-workshop-subtle">{sub}</div>
        </div>
    );
}

function WorldCard({ group }: { group: WorldGroup }) {
    const [expanded, setExpanded] = useState(true);
    const pct = group.total_quests > 0 ? group.completed_quests / group.total_quests : 0;
    const isActive = ACTIVE_WORLDS.has(group.world_slug);

    return (
        <div className={`rounded-xl border ${isActive ? 'border-white/10' : 'border-white/5'} bg-workshop-panel overflow-hidden`}>
            {/* World header */}
            <button
                onClick={() => setExpanded(e => !e)}
                className="w-full flex items-center justify-between px-5 py-4 hover:bg-white/3 transition-colors"
            >
                <div className="flex items-center gap-3">
                    <span className="text-xl">{worldEmoji(group.world_slug)}</span>
                    <div className="text-left">
                        <div className="flex items-center gap-2">
                            <span className="font-semibold text-sm">{worldLabel(group.world_slug)}</span>
                            {!isActive && (
                                <span className="text-[9px] px-1.5 py-0.5 rounded-full border border-white/10 text-workshop-subtle uppercase tracking-wider">
                                    Inactive
                                </span>
                            )}
                        </div>
                        <div className="text-[11px] text-workshop-subtle mt-0.5">
                            {group.completed_quests} / {group.total_quests} quests · {Math.round(pct * 100)}%
                        </div>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    <div className="w-24 hidden sm:block">
                        <ProgressBar value={pct} color={pct === 1 ? 'emerald' : 'cyan'} />
                    </div>
                    <ChevronLeft
                        className={`w-4 h-4 text-workshop-subtle transition-transform duration-200 ${expanded ? '-rotate-90' : 'rotate-180'}`}
                    />
                </div>
            </button>

            {/* Track rows */}
            {expanded && (
                <div className="border-t border-white/5 divide-y divide-white/5">
                    {group.tracks.map(track => (
                        <TrackRow key={track.track_slug} track={track} worldSlug={group.world_slug} />
                    ))}
                </div>
            )}
        </div>
    );
}

function TrackRow({ track, worldSlug }: { track: TrackProgress; worldSlug: string }) {
    const pct = track.total_quests > 0 ? track.completed_quests / track.total_quests : 0;
    const done = pct === 1;
    const started = track.completed_quests > 0;

    return (
        <div className="flex items-center gap-4 px-5 py-3">
            {/* Status icon */}
            <div className="shrink-0">
                {done ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : started ? (
                    <Clock className="w-4 h-4 text-workshop-cyan" />
                ) : (
                    <Circle className="w-4 h-4 text-workshop-subtle/40" />
                )}
            </div>

            {/* Track info */}
            <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-3">
                    <span className={`text-xs font-medium truncate ${done ? 'text-emerald-400' : started ? 'text-workshop-text' : 'text-workshop-subtle'}`}>
                        {track.label}
                    </span>
                    <span className="text-[10px] font-mono text-workshop-subtle shrink-0">
                        {track.completed_quests}/{track.total_quests}
                    </span>
                </div>
                <div className="mt-1.5">
                    <ProgressBar value={pct} color={done ? 'emerald' : 'cyan'} />
                </div>
            </div>

            {/* Link to workshop (world context) */}
            <Link
                to={`/arcade/workshop?world=${worldSlug}&track=${track.track_slug}`}
                className="shrink-0 text-[10px] text-workshop-subtle hover:text-workshop-cyan transition-colors px-2 py-1 rounded border border-white/8 hover:border-workshop-cyan/30"
                title="Open in Workshop"
            >
                Go →
            </Link>
        </div>
    );
}
