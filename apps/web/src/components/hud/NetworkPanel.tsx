import React, { useState, useEffect } from 'react';
import { DeckPanel } from '../ui/DeckPanel';

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
        <DeckPanel title="NETWORK" className="h-48">
            <div className="flex flex-col h-full justify-between">
                {/* Status Header */}
                <div className="flex justify-between items-center mb-2">
                    <span className="text-[10px] text-slate-500 font-hud tracking-wider">STATUS</span>
                    <span className={`text-[10px] font-bold tracking-widest ${isOnline ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.5)]' : 'text-rose-500'} animate-pulse`}>
                        {isOnline ? 'ONLINE' : 'OFFLINE'}
                    </span>
                </div>

                {/* Ping Graph Visualization */}
                <div className="flex items-end gap-[2px] h-20 opacity-80 border-b border-cyan-900/30 pb-1">
                    {[...Array(20)].map((_, i) => {
                        const height = Math.random() * 100;
                        return (
                            <div
                                key={i}
                                className="w-full bg-gradient-to-t from-cyan-500/20 to-cyan-400/60 rounded-t-[1px]"
                                style={{ height: `${height}%` }}
                            />
                        );
                    })}
                </div>

                {/* Footer Info */}
                <div className="flex justify-between mt-2 text-[9px] font-mono text-slate-400">
                    <span className="text-cyan-600">US-CENTRAL1</span>
                    <span className="text-cyan-300">{ping}ms</span>
                </div>

                {/* Decorative Hex/Grid bits */}
                <div className="absolute bottom-2 right-2 w-8 h-8 border-r border-b border-cyan-500/20 rounded-br-lg pointer-events-none" />
            </div>
        </DeckPanel>
    );
}
