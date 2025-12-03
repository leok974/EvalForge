import React, { useEffect, useState } from 'react';
import { StreamContext } from '../hooks/useArcadeStream';
import { WorldIcon } from './WorldIcon';
import { fxEnabled } from "@/lib/featureFlags";

type Track = {
    id: string;
    name: string;
    world_id: string;
    source: 'fundamentals' | 'personal' | 'user-repo';
};

type UniverseData = {
    worlds: { id: string; name: string; icon: string }[];
    tracks: Track[];
};

interface Props {
    context: StreamContext;
    setContext: (ctx: StreamContext) => void;
    hasSkill: (key: string) => boolean;
    onOpenCodex?: () => void;
}

export function ContextSelector({ context, setContext, hasSkill, onOpenCodex }: Props) {
    const [universe, setUniverse] = useState<UniverseData | null>(null);

    useEffect(() => {
        fetch('/api/universe')
            .then(res => res.json())
            .then(data => setUniverse(data))
            .catch(err => console.error("Failed to load universe", err));
    }, []);

    if (!universe) return <div className="text-xs text-zinc-600 animate-pulse">LOADING UNIVERSE...</div>;

    // Filter tracks for current world
    const activeTracks = universe.tracks.filter(t => t.world_id === context.world_id);
    const activeWorld = universe.worlds.find(w => w.id === context.world_id);

    // Group by Source Pillar
    const myProjects = activeTracks.filter(t => t.source === 'personal' || t.source === 'user-repo');
    const fundamentals = activeTracks.filter(t => t.source === 'fundamentals');

    return (
        <div className="bg-zinc-900 border-b border-zinc-800 p-4 flex flex-col md:flex-row gap-4 justify-between items-center shadow-lg z-20">

            {/* Selector Controls */}
            <div className="flex gap-2 w-full md:w-auto items-center">

                {/* ACTIVE ICON INDICATOR */}
                <div className="w-8 h-8 flex items-center justify-center bg-zinc-900 border border-zinc-700 rounded text-cyan-400 shrink-0">
                    <WorldIcon iconName={activeWorld?.icon || 'box'} className="w-4 h-4" />
                </div>

                {/* World Selector */}
                <div className="relative">
                    <select
                        value={context.world_id}
                        onChange={(e) => setContext({ ...context, world_id: e.target.value, track_id: '' })}
                        className="appearance-none bg-black border border-zinc-700 text-zinc-300 text-sm rounded px-3 py-1.5 font-mono hover:border-cyan-500 focus:outline-none pr-8 cursor-pointer"
                    >
                        {universe.worlds.map(w => (
                            <option key={w.id} value={w.id}>{w.name}</option>
                        ))}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-zinc-500">
                        <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                    </div>
                </div>

                {/* Track Selector (Grouped) */}
                <div className="relative">
                    <select
                        value={context.track_id}
                        onChange={(e) => setContext({ ...context, track_id: e.target.value })}
                        className="appearance-none bg-black border border-zinc-700 text-zinc-300 text-sm rounded px-3 py-1.5 font-mono hover:border-cyan-500 focus:outline-none pr-8 cursor-pointer min-w-[200px]"
                    >
                        {activeTracks.length === 0 && <option value="">Select World First</option>}

                        {myProjects.length > 0 && (
                            <optgroup label="My Projects (BYOR)">
                                {myProjects.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                            </optgroup>
                        )}

                        {fundamentals.length > 0 && (
                            <optgroup label="Fundamentals">
                                {fundamentals.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                            </optgroup>
                        )}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-zinc-500">
                        <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                    </div>
                </div>
            </div>

            {/* Mode Switcher */}
            <div className="flex bg-black rounded p-1 border border-zinc-800">
                <button
                    onClick={() => setContext({ ...context, mode: 'judge' })}
                    className={`px-3 py-1 text-[10px] md:text-xs font-bold uppercase tracking-wider rounded transition-all ${context.mode === 'judge'
                        ? `bg-cyan-900 text-cyan-300 shadow-[0_0_10px_rgba(8,145,178,0.5)] ${fxEnabled ? 'deck-mode-pulse' : ''}`
                        : 'text-zinc-500 hover:text-zinc-300'
                        }`}
                >
                    JUDGE
                </button>
                <button
                    onClick={() => setContext({ ...context, mode: 'quest' })}
                    className={`px-3 py-1 text-[10px] md:text-xs font-bold uppercase tracking-wider rounded transition-all ${context.mode === 'quest'
                        ? `bg-cyan-900 text-cyan-300 shadow-[0_0_10px_rgba(8,145,178,0.5)] ${fxEnabled ? 'deck-mode-pulse' : ''}`
                        : 'text-zinc-500 hover:text-zinc-300'
                        }`}
                >
                    QUEST
                </button>

                {/* GATED: EXPLAIN AGENT */}
                <button
                    onClick={() => hasSkill('agent_explain') && setContext({ ...context, mode: 'explain' })}
                    className={`px-3 py-1 text-[10px] md:text-xs font-bold uppercase tracking-wider rounded transition-all ${context.mode === 'explain'
                        ? `bg-cyan-900 text-cyan-300 shadow-[0_0_10px_rgba(8,145,178,0.5)] ${fxEnabled ? 'deck-mode-pulse' : ''}`
                        : 'text-zinc-500 hover:text-zinc-300'
                        } ${!hasSkill('agent_explain') ? 'opacity-30 cursor-not-allowed' : ''}`}
                    title={!hasSkill('agent_explain') ? "Requires Mentor Protocol (Tier 2)" : ""}
                >
                    EXPLAIN {!hasSkill('agent_explain') && '🔒'}
                </button>

                {/* GATED: DEBUG AGENT */}
                <button
                    onClick={() => hasSkill('agent_debug') && setContext({ ...context, mode: 'debug' })}
                    className={`px-3 py-1 text-[10px] md:text-xs font-bold uppercase tracking-wider rounded transition-all ${context.mode === 'debug'
                        ? `bg-cyan-900 text-cyan-300 shadow-[0_0_10px_rgba(8,145,178,0.5)] ${fxEnabled ? 'deck-mode-pulse' : ''}`
                        : 'text-zinc-500 hover:text-zinc-300'
                        } ${!hasSkill('agent_debug') ? 'opacity-30 cursor-not-allowed' : ''}`}
                    title={!hasSkill('agent_debug') ? "Requires Debug Routine (Tier 3)" : ""}
                >
                    DEBUG {!hasSkill('agent_debug') && '🔒'}
                </button>

                {/* GATED: CODEX */}
                <button
                    onClick={() => hasSkill('codex_link') && onOpenCodex && onOpenCodex()}
                    className={`px-3 py-1 text-[10px] md:text-xs font-bold uppercase tracking-wider rounded transition-all text-zinc-500 hover:text-zinc-300 ${!hasSkill('codex_link') ? 'opacity-30 cursor-not-allowed' : ''}`}
                    title={!hasSkill('codex_link') ? "Requires Archive Uplink (Tier 1)" : ""}
                >
                    CODEX {!hasSkill('codex_link') && '🔒'}
                </button>
            </div>
        </div>
    );
}
