import React, { useState, useEffect } from 'react';

export function NetworkPanel() {
    const [ping, setPing] = useState(24);
    const [isOnline, setIsOnline] = useState(true);

    // Simulate network "noise" for the game feel
    useEffect(() => {
        const interval = setInterval(() => {
            // Fluctuate ping between 20ms and 60ms
            setPing(Math.floor(Math.random() * 40) + 20);
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="mb-6">
            <div className="text-[9px] uppercase tracking-widest text-zinc-600 mb-2 font-bold">
                Network Topology
            </div>

            {/* Status Box */}
            <div className={`p-3 rounded border ${isOnline ? 'border-emerald-900/50 bg-emerald-950/10' : 'border-red-900 bg-red-950/10'} transition-colors`}>
                <div className="flex justify-between items-center mb-2">
                    <span className="text-[10px] text-zinc-400">STATUS</span>
                    <span className={`text-xs font-bold ${isOnline ? 'text-emerald-500' : 'text-red-500'} animate-pulse`}>
                        {isOnline ? 'ONLINE' : 'OFFLINE'}
                    </span>
                </div>

                {/* Fake Ping Graph */}
                <div className="flex items-end gap-0.5 h-8 opacity-50">
                    {[...Array(15)].map((_, i) => (
                        <div
                            key={i}
                            className="w-full bg-emerald-500/50"
                            style={{ height: `${Math.random() * 100}%` }}
                        />
                    ))}
                </div>

                <div className="flex justify-between mt-1 text-[9px] font-mono text-zinc-600">
                    <span>US-CENTRAL1</span>
                    <span>{ping}ms</span>
                </div>
            </div>
        </div>
    );
}
