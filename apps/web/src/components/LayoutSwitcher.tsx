import React, { useState } from 'react';
import { useGameStore, LayoutId } from '../store/gameStore';
import { LAYOUTS } from '../lib/layouts';
import { cn } from '../lib/utils';

export function LayoutSwitcher() {
    const { layout, setLayout } = useGameStore();
    const [isOpen, setIsOpen] = useState(false);

    const currentLayoutLabel = LAYOUTS.find(l => l.id === layout)?.label || layout.toUpperCase();

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="text-[10px] tracking-[0.22em] font-semibold flex items-center gap-1 text-zinc-400 hover:text-zinc-200"
            >
                LAYOUT: <span className="text-cyan-400">{currentLayoutLabel.toUpperCase()}</span>
                <span className="text-[8px] ml-1">▼</span>
            </button>

            {isOpen && (
                <>
                    <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsOpen(false)}
                    />
                    <div className="absolute right-0 mt-2 min-w-[160px] rounded-lg border border-slate-700/70 bg-slate-950/95 shadow-xl z-50 backdrop-blur-md">
                        {LAYOUTS.map((l) => (
                            <button
                                key={l.id}
                                onClick={() => {
                                    setLayout(l.id);
                                    setIsOpen(false);
                                }}
                                className={cn(
                                    "w-full px-4 py-2 text-left text-[11px] tracking-wider hover:bg-cyan-500/10 transition-colors block",
                                    l.id === layout ? "text-cyan-300 font-medium" : "text-zinc-400"
                                )}
                            >
                                {l.label.toUpperCase()}
                            </button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}
