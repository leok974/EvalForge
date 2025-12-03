import React, { useState, useEffect } from 'react';
import { User } from '../hooks/useAuth';
import { useGameSocket } from '../hooks/useGameSocket';

type Project = {
    id: string;
    name: string;
    repo_url: string;
    sync_status: 'pending' | 'syncing' | 'ok' | 'error';
    last_sync_at: string | null;
    summary_data: { stack?: string[]; files_indexed?: number };
    codex_status?: 'complete' | 'partial' | 'missing_docs';
};

type Track = {
    id: string;
    title: string;
    description: string;
    world_id: string;
};

interface Props {
    user: User | null;
    isOpen: boolean;
    onClose: () => void;
}

export function ProjectsPanel({ user, isOpen, onClose }: Props) {
    const [projects, setProjects] = useState<Project[]>([]);
    const [academyTracks, setAcademyTracks] = useState<Track[]>([]);
    const [newRepoUrl, setNewRepoUrl] = useState('');
    const [isSyncing, setIsSyncing] = useState(false);

    // Listen to socket for live updates
    const lastEvent = useGameSocket();
    const [progressMap, setProgressMap] = useState<Record<string, { msg: string; pct: number; eta?: number }>>({});

    // Load Projects when opened
    useEffect(() => {
        if (user && isOpen) {
            // 1. Fetch User Projects
            fetch('/api/projects')
                .then(r => {
                    if (!r.ok) throw new Error(r.statusText);
                    return r.json();
                })
                .then(data => {
                    if (Array.isArray(data)) {
                        setProjects(data);
                    } else {
                        console.error("Projects API returned non-array:", data);
                        setProjects([]);
                    }
                })
                .catch(err => {
                    console.error("Failed to load projects:", err);
                    setProjects([]);
                });

            // 2. Fetch Academy Tracks
            fetch('/api/universe')
                .then(r => r.json())
                .then(data => {
                    if (data.tracks && Array.isArray(data.tracks)) {
                        setAcademyTracks(data.tracks);
                    }
                })
                .catch(err => console.error("Failed to load universe:", err));
        }
    }, [user, isOpen]);

    // Handle socket events
    useEffect(() => {
        if (lastEvent && lastEvent.type === 'sync_progress' && lastEvent.project_id) {
            setProgressMap(prev => ({
                ...prev,
                [lastEvent.project_id!]: {
                    msg: lastEvent.message || 'Processing...',
                    pct: lastEvent.percent || 0,
                    eta: lastEvent.eta_seconds
                }
            }));
        }
        // Refresh list on completion
        if (lastEvent && lastEvent.type === 'sync_complete' && lastEvent.project_id) {
            fetch('/api/projects').then(r => r.json()).then(setProjects);
            // Clear progress for this project
            setProgressMap(prev => {
                const updated = { ...prev };
                delete updated[lastEvent.project_id!];
                return updated;
            });
        }
    }, [lastEvent]);

    const handleAddProject = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newRepoUrl) return;

        setIsSyncing(true);
        try {
            // 1. Create the project entry
            const res = await fetch('/api/projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repo_url: newRepoUrl })
            });

            if (!res.ok) {
                const error = await res.json();
                alert(error.detail || 'Failed to add project');
                return;
            }

            const newProj = await res.json();

            // 2. Trigger the "Analysis" sync immediately
            const syncRes = await fetch(`/api/projects/${newProj.id}/sync`, { method: 'POST' });
            if (!syncRes.ok) {
                console.error('Sync failed:', await syncRes.text());
            }

            // 3. Refresh the list to show the new data (and tags)
            const listRes = await fetch('/api/projects');
            setProjects(await listRes.json());
            setNewRepoUrl('');
        } catch (e) {
            console.error("Failed to add project", e);
            alert('Failed to add project. Check console for details.');
        } finally {
            setIsSyncing(false);
        }
    };

    const handleReSync = async (projectId: string) => {
        // Optimistic Update
        setProjects(prev => prev.map(p =>
            p.id === projectId ? { ...p, sync_status: 'pending' } : p
        ));

        // Trigger Sync
        try {
            await fetch(`/api/projects/${projectId}/sync`, { method: 'POST' });
        } catch (e) {
            console.error("Sync failed", e);
        }
    };

    // Helper to format time
    const formatTime = (seconds?: number) => {
        if (seconds === undefined || seconds === null) return '';
        if (seconds < 60) return '< 1m left';
        const mins = Math.ceil(seconds / 60);
        return `~${mins}m left`;
    };

    const hasIncomplete = projects.some(
        (p) => p.codex_status && p.codex_status !== "complete"
    );

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            {/* Modal Container */}
            <div className="bg-zinc-950 border border-zinc-800 rounded-xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">

                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                    <h2 className="text-cyan-500 font-bold tracking-wider font-mono flex items-center gap-2">
                        <span className="text-xl">🚀</span> PROJECT DASHBOARD
                    </h2>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">✕ ESC</button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto flex-1 space-y-8">
                    {/* SECTION: SYNCED REPOSITORIES */}
                    <div>
                        <h3 className="text-xs font-bold text-cyan-600 uppercase tracking-widest mb-4 border-b border-zinc-800 pb-2 flex justify-between items-center">
                            <span>📡 Synced Repositories</span>
                            <span className="text-[10px] bg-cyan-950 text-cyan-400 px-2 py-0.5 rounded-full">{projects.length}</span>
                        </h3>

                        {hasIncomplete && (
                            <div className="mb-3 rounded-lg border border-amber-500/40 bg-amber-500/5 px-3 py-2 text-[11px] text-amber-100">
                                Some projects have incomplete Project Codex entries.
                                For best results, add <code>README.md</code> and
                                <code> ARCHITECTURE.md</code> to your repos, then run <b>Sync</b> again.
                            </div>
                        )}

                        <div className="space-y-3 mb-8">
                            {projects.length === 0 && (
                                <div className="text-zinc-600 italic text-sm text-center border border-dashed border-zinc-800 rounded p-8">
                                    No projects linked yet. Add your first repo below.
                                </div>
                            )}
                            {projects.map(p => {
                                const progress = progressMap[p.id];
                                const isBusy = p.sync_status === 'pending' || p.sync_status === 'syncing' || (progress && progress.pct < 100);

                                return (
                                    <div key={p.id} className="bg-zinc-900 border border-zinc-800 p-4 rounded-lg flex flex-col gap-3 group hover:border-zinc-700 transition-all">
                                        <div className="flex justify-between items-center">
                                            <div>
                                                <div className="font-bold text-zinc-200 text-lg">{p.name}</div>
                                                <div className="text-xs text-zinc-500 font-mono mb-2">{p.repo_url}</div>
                                                <div className="flex gap-2">
                                                    {p.summary_data && p.summary_data.stack && p.summary_data.stack.map((s: string) => (
                                                        <span key={s} className="px-1.5 py-0.5 bg-black rounded text-[10px] text-cyan-600 uppercase border border-zinc-800 tracking-wide font-bold">
                                                            {s}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-4">
                                                {/* Status Badge */}
                                                <div className="text-right">
                                                    {isBusy ? (
                                                        <div className="flex flex-col items-end">
                                                            <div className="flex items-center gap-2 text-amber-500">
                                                                <span className="text-[10px] font-mono animate-pulse">
                                                                    {progress ? progress.msg : 'QUEUED'}
                                                                </span>
                                                                <div className="h-2 w-2 rounded-full bg-amber-500 animate-ping" />
                                                            </div>
                                                            {/* ETA Display */}
                                                            {progress?.eta !== undefined && progress.eta > 0 && (
                                                                <div className="text-[9px] text-zinc-500 font-mono mt-0.5">
                                                                    {formatTime(progress.eta)}
                                                                </div>
                                                            )}
                                                        </div>
                                                    ) : (
                                                        <div className={`text-xs font-bold uppercase tracking-wider ${p.sync_status === 'ok' ? 'text-emerald-500' : 'text-red-500'}`}>
                                                            {p.sync_status === 'ok' ? 'SYNCED' : 'ERROR'}
                                                        </div>
                                                    )}
                                                    <div className="text-[10px] text-zinc-600 font-mono mt-1">
                                                        {p.last_sync_at ? new Date(p.last_sync_at).toLocaleTimeString() : 'Never'}
                                                    </div>
                                                </div>

                                                {/* RE-SYNC BUTTON */}
                                                <button
                                                    onClick={() => handleReSync(p.id)}
                                                    disabled={isBusy}
                                                    className="bg-zinc-800 hover:bg-zinc-700 text-zinc-400 p-2 rounded border border-zinc-700 transition-colors disabled:opacity-50"
                                                    title="Re-sync Repository"
                                                >
                                                    {/* Refresh Icon */}
                                                    <svg className={`w-4 h-4 ${isBusy ? 'animate-spin' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>

                                        {/* Progress Bar (Only visible during sync) */}
                                        {isBusy && progress && (
                                            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-amber-500 transition-all duration-300"
                                                    style={{ width: `${progress.pct}%` }}
                                                />
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>

                        {/* Add Project Form */}
                        <form onSubmit={handleAddProject} className="bg-zinc-900/50 p-4 rounded-lg border border-zinc-800">
                            <label className="block text-xs font-mono text-zinc-500 mb-2 uppercase tracking-widest">Link GitHub Repository</label>
                            <div className="flex gap-2">
                                <input
                                    type="url"
                                    placeholder="https://github.com/username/repo"
                                    value={newRepoUrl}
                                    onChange={e => setNewRepoUrl(e.target.value)}
                                    className="flex-1 bg-black border border-zinc-700 rounded px-3 py-2 text-sm text-zinc-200 focus:border-cyan-500 focus:outline-none font-mono"
                                    required
                                />
                                <button
                                    type="submit"
                                    disabled={isSyncing}
                                    className="bg-cyan-900 hover:bg-cyan-800 text-cyan-100 px-6 py-2 rounded text-xs font-bold transition-colors disabled:opacity-50 border border-cyan-700"
                                >
                                    {isSyncing ? 'ANALYZING...' : 'ADD PROJECT'}
                                </button>
                            </div>

                            <div className="mt-3 rounded-lg border border-zinc-800 bg-zinc-900/40 px-3 py-2 text-[11px] text-zinc-500">
                                <div className="font-medium text-xs mb-1 text-zinc-400">
                                    Tip: Get a rich Project Codex
                                </div>
                                <ul className="list-disc list-inside space-y-1">
                                    <li>Include a clear <code>README.md</code>.</li>
                                    <li>Add <code>ARCHITECTURE.md</code> or <code>docs/architecture.md</code>.</li>
                                    <li>Check in <code>docker-compose.yml</code> or infra docs if you have them.</li>
                                </ul>
                                <p className="mt-1">
                                    EvalForge reads these files to auto-build your project documentation,
                                    quests, and bosses.
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}
