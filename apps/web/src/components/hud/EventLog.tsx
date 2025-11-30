import React, { useEffect, useState } from 'react';
import { useGameSocket, GameEvent } from '../../hooks/useGameSocket';

export function EventLog() {
    const lastEvent = useGameSocket();
    const [logs, setLogs] = useState<{ time: string, msg: string, color: string }[]>([]);

    // Initialize with boot message
    useEffect(() => {
        addLog("System Boot Sequence Initiated", "text-zinc-500");
        setTimeout(() => addLog("Connected to EvalForge Core", "text-cyan-600"), 500);
    }, []);

    // Listen for Real Events
    useEffect(() => {
        if (lastEvent) {
            if (lastEvent.type === 'boss_spawn') {
                addLog(`WARNING: ${lastEvent.title}`, "text-red-500");
            } else if (lastEvent.type === 'sync_complete') {
                addLog(`SUCCESS: ${lastEvent.title}`, "text-emerald-400");
            } else if (lastEvent.type === 'sync_progress' && lastEvent.percent === 5) {
                addLog(`SYNC STARTED: ${lastEvent.project_id}`, "text-banana-400");
            }
        }
    }, [lastEvent]);

    const addLog = (msg: string, color: string) => {
        const time = new Date().toLocaleTimeString([], { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
        setLogs(prev => [{ time, msg, color }, ...prev].slice(0, 8)); // Keep last 8
    };

    return (
        <div className="flex-1 flex flex-col min-h-0">
            <div className="text-[9px] uppercase tracking-widest text-zinc-600 mb-2 font-bold">
                Event Stream
            </div>
            <div className="flex-1 overflow-hidden relative">
                {/* Scanline overlay */}
                <div className="absolute inset-0 pointer-events-none bg-gradient-to-b from-transparent via-transparent to-black/20 z-10" />

                <ul className="space-y-1.5">
                    {logs.map((log, i) => (
                        <li key={i} className={`text-[10px] font-mono flex gap-2 ${i === 0 ? 'opacity-100' : 'opacity-60'}`}>
                            <span className="text-zinc-600 shrink-0">[{log.time}]</span>
                            <span className={`truncate ${log.color}`}>{log.msg}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
