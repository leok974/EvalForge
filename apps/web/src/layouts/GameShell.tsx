import React from 'react';
import { useGameStore } from '../store/gameStore';
import { CyberdeckLayout } from './CyberdeckLayout';
import DevUI from '../pages/DevUI'; // The main content
// Temporary internal import to avoid circular deps if LayoutSwitcher isn't exported yet
import { LayoutSwitcher } from '../components/LayoutSwitcher';

export function GameShell() {
    const layout = useGameStore((s) => s.layout);

    // We wrap the DevUI (Terminal) inside the chosen layout
    // In the future, 'DevUI' might be split into smaller widgets passed to specific layout slots

    const content = <DevUI />;

    switch (layout) {
        case 'navigator':
            return (
                <div className="h-screen flex items-center justify-center bg-black text-white">
                    <div className="text-center">
                        <h1 className="text-2xl font-bold mb-2">NAVIGATOR INTERFACE</h1>
                        <p className="text-zinc-500 text-sm">Star Map Module Not Loaded.</p>
                        <div className="mt-4"><LayoutSwitcher /></div> {/* Allow switching back */}
                    </div>
                </div>
            );
        case 'workshop':
            return (
                <div className="h-screen flex items-center justify-center bg-stone-900 text-amber-100">
                    <div className="text-center">
                        <h1 className="text-2xl font-bold mb-2">ISOMETRIC WORKSHOP</h1>
                        <p className="text-stone-500 text-sm">Construction Grid Offline.</p>
                        <div className="mt-4"><LayoutSwitcher /></div>
                    </div>
                </div>
            );
        case 'cyberdeck':
        default:
            return <CyberdeckLayout>{content}</CyberdeckLayout>;
    }
}
