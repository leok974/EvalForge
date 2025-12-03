import React, { useState, useEffect } from 'react';
import { DeckPanel } from '../ui/DeckPanel';

export function RepoStatusPanel() {
    const [status, setStatus] = useState<'synced' | 'syncing' | 'error'>('synced');
    const [lastSync, setLastSync] = useState<string>('Just now');

    // In a real app, this would listen to the socket or poll /api/projects/status
    // For now we'll just mock it or check if any project is syncing
    useEffect(() => {
        const checkStatus = () => {
            fetch('/api/projects')
                .then(r => r.json())
                .then(data => {
                    if (Array.isArray(data)) {
                        const isSyncing = data.some((p: any) => p.sync_status === 'syncing' || p.sync_status === 'pending');
                        const hasError = data.some((p: any) => p.sync_status === 'error');

                        if (isSyncing) setStatus('syncing');
                        else if (hasError) setStatus('error');
                        else setStatus('synced');

                        // Find most recent sync
                        // setLastSync(...)
                    }
                })
                .catch(() => setStatus('error'));
        };

        checkStatus();
        const interval = setInterval(checkStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <DeckPanel title="REPO STATUS" className="h-24">
            <div className="flex flex-col justify-center h-full gap-2">
                <div className="flex items-center gap-3">
                    <div className={`h-3 w-3 rounded-full ${status === 'synced' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.6)]' :
                            status === 'syncing' ? 'bg-amber-500 animate-ping' :
                                'bg-rose-500'
                        }`} />
                    <div className="flex flex-col">
                        <span className={`text-xs font-bold tracking-widest ${status === 'synced' ? 'text-emerald-400' :
                                status === 'syncing' ? 'text-amber-400' :
                                    'text-rose-400'
                            }`}>
                            {status === 'synced' ? 'ALL SYSTEMS SYNCED' :
                                status === 'syncing' ? 'SYNC IN PROGRESS' :
                                    'SYNC ERROR DETECTED'}
                        </span>
                        <span className="text-[9px] text-slate-500 font-mono">
                            LAST UPDATE: {lastSync}
                        </span>
                    </div>
                </div>

                {/* Mini progress bar if syncing */}
                {status === 'syncing' && (
                    <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden mt-1">
                        <div className="h-full bg-amber-500 w-1/2 animate-pulse" />
                    </div>
                )}
            </div>
        </DeckPanel>
    );
}
