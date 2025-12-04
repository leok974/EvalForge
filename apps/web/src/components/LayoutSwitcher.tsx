import React, { useState } from 'react';
import { useCurrentLayout } from '../hooks/useCurrentLayout';
import { useLayoutUnlocks } from '../features/layouts/useLayoutUnlocks';
import { LayoutId } from '../features/layouts/layoutConfig';
import { cn } from '../lib/utils';

export function LayoutSwitcher() {
    const { layout, setLayout } = useCurrentLayout();
    const layouts = useLayoutUnlocks();
    const [isOpen, setIsOpen] = useState(false);

    const currentLayoutLabel = layouts.find(l => l.id === layout)?.label || layout.toUpperCase();

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="text-[10px] tracking-[0.22em] font-semibold flex items-center gap-1 text-zinc-400 hover:text-zinc-200"
                data-testid="layout-picker-trigger"
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
                    <div
                        className="absolute right-0 mt-2 min-w-[240px] rounded-xl border border-slate-700/80 bg-slate-950/95 shadow-xl z-50 backdrop-blur-md p-2"
                        data-testid="layout-picker"
                    >
                        <div className="mb-2 px-2 flex items-center justify-between gap-2">
                            <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                                Select Layout
                            </span>
                        </div>
                        <div className="grid grid-cols-1 gap-1">
                            {layouts.map((opt) => {
                                const isActive = layout === opt.id;
                                const isLocked = !opt.unlocked;

                                return (
                                    <button
                                        key={opt.id}
                                        type="button"
                                        data-testid={`layout-option-${opt.id}`}
                                        disabled={isLocked}
                                        onClick={() => {
                                            if (isLocked) return;
                                            setLayout(opt.id as LayoutId);
                                            setIsOpen(false);
                                        }}
                                        className={cn(
                                            "group flex flex-col items-start rounded-lg border px-3 py-2 text-left transition w-full",
                                            isActive
                                                ? "border-cyan-500/40 bg-cyan-950/20"
                                                : "border-transparent hover:bg-slate-800/50",
                                            isLocked
                                                ? "opacity-50 cursor-not-allowed"
                                                : "cursor-pointer"
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
                                            {isLocked && (
                                                <span className="text-[9px] uppercase tracking-wider text-amber-500/80">Locked</span>
                                            )}
                                        </div>
                                        <span className="mt-0.5 text-[10px] text-slate-500 group-hover:text-slate-400">
                                            {opt.description}
                                        </span>
                                        {isLocked && opt.lockedReason && (
                                            <span className="mt-1.5 text-[9px] text-amber-500/70 border-t border-amber-500/10 pt-1 w-full">
                                                {opt.lockedReason}
                                            </span>
                                        )}
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
