import React, { useState } from 'react';
import { useCurrentLayout } from '../hooks/useCurrentLayout';
import { cn } from '../lib/utils';

const LAYOUT_PATHS: Record<string, string> = {
    // Both just reload current page logic effectively, layout is global state now
    // But we might want to allow them to act as navigation if we are NOT in workshop?
    // For now, let's just make them switch the state. 
    // Actually, "Layouts should swap the shell composition".
    // The user requirement says "Switching persists on refresh". 
    // So we just update the context.
    orion: '#',
    cyberdeck: '#',
};

export function LayoutSwitcher() {
    const { layout, setLayout } = useCurrentLayout();

    // Hardcoded options as per requirements
    const options = [
        { id: 'orion', label: 'Orion: Map', description: 'World map + guided progression' },
        { id: 'cyberdeck', label: 'Cyberdeck: Bench', description: 'Terminal-first engineering bench' }
    ] as const;

    const [isOpen, setIsOpen] = useState(false);

    // Current label
    const currentOption = options.find(o => o.id === layout) || options[0];

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="text-[10px] tracking-[0.22em] font-semibold flex items-center gap-1 text-zinc-400 hover:text-zinc-200"
                data-testid="layout-picker-trigger"
            >
                VIEW: <span className="text-cyan-400">{currentOption.label.toUpperCase()}</span>
                <span className="text-[8px] ml-1">▼</span>
            </button>

            {isOpen && (
                <>
                    <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsOpen(false)}
                    />
                    <div
                        className="absolute right-0 mt-2 min-w-[240px] rounded-xl border border-slate-700/80 bg-slate-950/95 shadow-xl z-50 backdrop-blur-md p-2"
                        data-testid="layout-picker"
                    >
                        <div className="mb-2 px-2 flex items-center justify-between gap-2">
                            <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                                Select View
                            </span>
                        </div>
                        <div className="grid grid-cols-1 gap-1">
                            {options.map((opt) => {
                                const isActive = layout === opt.id;

                                return (
                                    <button
                                        key={opt.id}
                                        type="button"
                                        data-testid={`layout-option-${opt.id}`}
                                        onClick={() => {
                                            setLayout(opt.id as any);
                                            setIsOpen(false);
                                        }}
                                        className={cn(
                                            "group flex flex-col items-start rounded-lg border px-3 py-2 text-left transition w-full",
                                            isActive
                                                ? "border-cyan-500/40 bg-cyan-950/20"
                                                : "border-transparent hover:bg-slate-800/50",
                                            "cursor-pointer"
                                        )}
                                    >
                                        <div className="flex w-full items-center justify-between gap-2">
                                            <span className={cn(
                                                "text-[11px] font-semibold tracking-wide",
                                                isActive ? "text-cyan-300" : "text-slate-200"
                                            )}>
                                                {opt.label}
                                            </span>
                                            {isActive && (
                                                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.8)]" />
                                            )}
                                        </div>
                                        <span className="mt-0.5 text-[10px] text-slate-500 group-hover:text-slate-400">
                                            {opt.description}
                                        </span>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
