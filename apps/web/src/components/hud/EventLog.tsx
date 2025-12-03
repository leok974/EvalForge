import React, { useEffect, useState, useRef } from 'react';
import { useGameSocket, GameEvent } from '../../hooks/useGameSocket';
import { DeckPanel } from '../ui/DeckPanel';
import { fxEnabled } from "@/lib/featureFlags";

export function EventLog() {
    const lastEvent = useGameSocket();
    const [logs, setLogs] = useState<{ id: string, time: string, msg: string, color: string }[]>([]);
    const lastSeenRef = useRef<string | null>(null);

    // Initialize with boot message
    useEffect(() => {
        addLog("System Boot Sequence Initiated", "text-slate-500");
        setTimeout(() => addLog("Connected to EvalForge Core", "text-cyan-400"), 500);
    }, []);

    // Listen for Real Events
    useEffect(() => {
        if (lastEvent) {
            if (lastEvent.type === 'boss_spawn') {
                addLog(`WARNING: ${lastEvent.title}`, "text-rose-400 drop-shadow-[0_0_5px_rgba(244,63,94,0.5)]");
            } else if (lastEvent.type === 'sync_complete') {
                addLog(`SUCCESS: ${lastEvent.title}`, "text-emerald-400");
            } else if (lastEvent.type === 'sync_progress' && lastEvent.percent === 5) {
                addLog(`SYNC STARTED: ${lastEvent.project_id}`, "text-amber-300");
            }
        }
    }, [lastEvent]);

    // FX: Track new items
    useEffect(() => {
        if (!logs.length) return;
        if (!lastSeenRef.current) {
            lastSeenRef.current = logs[0].id;
            return;
        }
        if (logs[0].id !== lastSeenRef.current) {
            lastSeenRef.current = logs[0].id;
        }
    }, [logs]);

    const addLog = (msg: string, color: string) => {
        const time = new Date().toLocaleTimeString([], { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
        const id = Math.random().toString(36).substr(2, 9);
        setLogs(prev => [{ id, time, msg, color }, ...prev].slice(0, 12)); // Keep last 12
    };

    return (
        <DeckPanel title="EVENT FEED" className="flex-1 min-h-0 flex flex-col">
            <div className="flex-1 overflow-hidden relative">
                <ul className="space-y-1.5 h-full overflow-y-auto scrollbar-hide p-1">
                    {logs.map((log, i) => {
                        const isNewest = i === 0 && fxEnabled && log.id === lastSeenRef.current;
                        return (
                            <li key={log.id} className={`text-[10px] font-mono flex gap-2 rounded px-1 ${i === 0 ? 'opacity-100' : 'opacity-70'
                                } ${isNewest ? 'deck-event-flash' : ''}`}>
                                <span className="text-slate-600 shrink-0">[{log.time}]</span>
                                <span className={`truncate ${log.color}`}>{log.msg}</span>
                            </li>
                        );
                    })}
                    {logs.length === 0 && (
                        <li className="text-[10px] text-slate-700 font-mono italic">No events logged.</li>
                    )}
                </ul>
            </div>
        </DeckPanel>
    );
}
