import React from 'react';
import { StreamContext } from '../hooks/useArcadeStream';
import { WorldIcon } from './WorldIcon';
import { fxEnabled } from "@/lib/featureFlags";
import { useWorkshopCatalog } from '../features/workshop/WorkshopCatalogContext';

interface Props {
    context: StreamContext;
    setContext: (ctx: StreamContext) => void;
    hasSkill: (key: string) => boolean;
    onOpenCodex?: () => void;
}

export function ContextSelector({ context, setContext, hasSkill, onOpenCodex }: Props) {
    const {
        worlds,
        loading,
        resolveWorldName,
        getTracksForWorld,
        resolveTrackName,
        nameMode,
        toggleNameMode
    } = useWorkshopCatalog();

    if (loading) return <div className="text-xs text-zinc-600 animate-pulse">LOADING WORKSHOP...</div>;

    // Filter tracks for current world using catalog
    // If context.world_id is set, get tracks for it.
    const activeTracks = context.world_id ? getTracksForWorld(context.world_id) : [];

    return (
        <div className="bg-zinc-900 border-b border-zinc-800 p-4 flex flex-col md:flex-row gap-4 justify-between items-center shadow-lg z-20">

            {/* Selector Controls */}
            <div className="flex gap-2 w-full md:w-auto items-center">

                {/* ACTIVE ICON INDICATOR */}
                <div className="w-8 h-8 flex items-center justify-center bg-zinc-900 border border-zinc-700 rounded text-cyan-400 shrink-0">
                    <WorldIcon iconName={'box'} className="w-4 h-4" />
                </div>

                {/* World Selector */}
                <div className="relative">
                    <select
                        value={context.world_id}
                        onChange={(e) => setContext({ ...context, world_id: e.target.value, track_id: '' })}
                        className="appearance-none bg-black border border-zinc-700 text-zinc-300 text-sm rounded px-3 py-1.5 font-mono hover:border-cyan-500 focus:outline-none pr-8 cursor-pointer min-w-[160px]"
                    >
                        {worlds.length === 0 && <option value="">No Active Worlds</option>}
                        {worlds.map(w => (
                            <option key={w.world_id} value={w.world_id}>
                                {resolveWorldName(w)}
                            </option>
                        ))}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-zinc-500">
                        <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                    </div>
                </div>

                {/* Track Selector */}
                <div className="relative">
                    <select
                        value={context.track_id}
                        onChange={(e) => setContext({ ...context, track_id: e.target.value })}
                        className="appearance-none bg-black border border-zinc-700 text-zinc-300 text-sm rounded px-3 py-1.5 font-mono hover:border-cyan-500 focus:outline-none pr-8 cursor-pointer min-w-[200px]"
                    >
                        {activeTracks.length === 0 && <option value="">Select World First</option>}
                        {activeTracks.length > 0 && <option value="">All Tracks</option>}

                        {/* Flattened list for now, preserving grouping if needed later */}
                        {activeTracks.map(t => (
                            <option key={t.track_id} value={t.track_id}>
                                {resolveTrackName(t)}
                            </option>
                        ))}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-zinc-500">
                        <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                    </div>
                </div>

                {/* Names Toggle (Small) */}
                <button
                    onClick={toggleNameMode}
                    className="ml-2 px-2 py-1 text-[10px] uppercase font-bold text-zinc-500 hover:text-cyan-400 border border-transparent hover:border-zinc-700 rounded transition-colors"
                    title={`Switch to ${nameMode === 'lore' ? 'Real' : 'Lore'} Names`}
                >
                    {nameMode === 'lore' ? 'LORE' : 'REAL'}
                </button>
            </div>

            {/* Mode Switcher - REMOVED (Moved to WorkshopToolsPanel) */}
        </div>
    );
}

