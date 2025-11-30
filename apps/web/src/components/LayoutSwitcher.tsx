import React from 'react';
import { useGameStore, LayoutId } from '../store/gameStore';

export function LayoutSwitcher() {
    const { layout, setLayout } = useGameStore();

    return (
        <div className="flex items-center gap-2">
            <span className="text-[9px] text-zinc-600 font-mono tracking-widest uppercase hidden md:inline">
                INTERFACE::
            </span>
            <select
                value={layout}
                onChange={(e) => setLayout(e.target.value as LayoutId)}
                className="bg-black/20 border border-zinc-800 text-zinc-500 text-[10px] uppercase tracking-wider rounded px-2 py-1 hover:border-banana-400 hover:text-banana-400 focus:outline-none transition-colors cursor-pointer"
            >
                <option value="cyberdeck">CYBERDECK v1</option>
                <option value="navigator">NAVIGATOR (Alpha)</option>
                <option value="workshop">WORKSHOP (Alpha)</option>
            </select>
        </div>
    );
}
