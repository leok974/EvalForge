import React, { useState, useEffect } from 'react';
import { DeckPanel } from '../ui/DeckPanel';

interface ProjectSummary {
    id: string;
    name: string;
    repo_url: string;
    sync_status: 'pending' | 'syncing' | 'ok' | 'error';
    last_sync_at: string | null;
    summary_data: { stack?: string[] };
}

export function ProjectPayloadPanel() {
    const [projects, setProjects] = useState<ProjectSummary[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch('/api/projects')
            .then(r => r.json())
            .then(data => {
                if (Array.isArray(data)) setProjects(data);
            })
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return (
        <DeckPanel title="PAYLOAD" className="h-64 flex flex-col min-h-0">
            <div className="flex-1 overflow-y-auto scrollbar-hide space-y-2">
                {loading && <div className="text-[10px] text-slate-500 animate-pulse">Scanning payloads...</div>}

                {!loading && projects.length === 0 && (
                    <div className="text-[10px] text-slate-500 italic">No active payloads.</div>
                )}

                {projects.map(p => (
                    <div key={p.id} className="group relative border border-slate-800/60 bg-slate-900/40 p-2 rounded hover:border-cyan-500/50 hover:bg-cyan-900/10 transition-all cursor-pointer">
                        <div className="flex justify-between items-start mb-1">
                            <span className="text-[11px] font-bold text-slate-200 group-hover:text-cyan-300 transition-colors">
                                {p.name}
                            </span>
                            <span className={`text-[9px] font-mono uppercase ${p.sync_status === 'ok' ? 'text-emerald-500' : 'text-amber-500'}`}>
                                {p.sync_status}
                            </span>
                        </div>
                        <div className="text-[9px] text-slate-500 font-mono truncate mb-1.5 opacity-60">
                            {p.repo_url}
                        </div>
                        <div className="flex flex-wrap gap-1">
                            {p.summary_data?.stack?.slice(0, 3).map(tech => (
                                <span key={tech} className="text-[8px] px-1 py-0.5 bg-slate-950 border border-slate-800 rounded text-cyan-600/80 font-mono uppercase">
                                    {tech}
                                </span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer Action */}
            <div className="mt-2 pt-2 border-t border-slate-800/50 flex justify-between items-center">
                <span className="text-[9px] text-slate-600 font-mono">CAPACITY: {projects.length}/5</span>
                <button className="text-[9px] text-cyan-500 hover:text-cyan-300 uppercase tracking-wider font-bold transition-colors">
                    + LOAD NEW
                </button>
            </div>
        </DeckPanel>
    );
}
