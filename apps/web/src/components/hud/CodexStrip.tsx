import React, { useState, useEffect } from 'react';
import { DeckPanel } from '../ui/DeckPanel';

export function CodexStrip() {
    const [stats, setStats] = useState({ total: 0, worlds: 0, recent: 0 });

    useEffect(() => {
        // Mock stats for now, or fetch from an endpoint if available
        // Ideally we'd have a /api/codex/stats endpoint
        fetch('/api/codex')
            .then(r => r.json())
            .then(data => {
                if (Array.isArray(data)) {
                    setStats({
                        total: data.length,
                        worlds: new Set(data.map((d: any) => d.world)).size,
                        recent: data.length // Just showing total for now
                    });
                }
            })
            .catch(console.error);
    }, []);

    return (
        <DeckPanel title="CODEX" className="flex-1 flex flex-col min-h-0">
            <div className="flex-1 flex flex-col justify-center items-center gap-2">
                <div className="text-center">
                    <div className="text-2xl font-bold text-slate-200 font-hud tracking-widest drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]">
                        {stats.total}
                    </div>
                    <div className="text-[9px] text-slate-500 uppercase tracking-[0.2em] font-mono">
                        ENTRIES INDEXED
                    </div>
                </div>

                <div className="w-full px-4">
                    <div className="h-px bg-gradient-to-r from-transparent via-slate-700 to-transparent my-2" />
                </div>

                <div className="flex gap-4 text-center">
                    <div>
                        <div className="text-xs font-bold text-cyan-400">{stats.worlds}</div>
                        <div className="text-[8px] text-slate-600 uppercase">WORLDS</div>
                    </div>
                    <div>
                        <div className="text-xs font-bold text-emerald-400">ONLINE</div>
                        <div className="text-[8px] text-slate-600 uppercase">STATUS</div>
                    </div>
                </div>
            </div>

            <div className="mt-auto pt-2 border-t border-slate-800/50">
                <button className="w-full text-[9px] text-slate-400 hover:text-cyan-400 uppercase tracking-widest transition-colors flex items-center justify-center gap-1">
                    <span>ACCESS DATABASE</span>
                    <span>→</span>
                </button>
            </div>
        </DeckPanel>
    );
}
