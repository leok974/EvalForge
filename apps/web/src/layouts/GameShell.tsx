import React from 'react';
import { useGameStore } from '../store/gameStore';
import { CyberdeckLayout } from './CyberdeckLayout';
import DevUI from '../pages/DevUI'; // The main content
import { LayoutSwitcher } from '../components/LayoutSwitcher';
import { BossHud } from '../components/BossHud';

export function GameShell() {
    const layout = useGameStore((s) => s.layout);

    const content = <DevUI />;

    switch (layout) {
        case 'navigator':
            return (
                <>
                    <BossHud />
                    <div className="h-screen flex items-center justify-center bg-black text-white">
                        <div className="text-center">
                            <h1 className="text-2xl font-bold mb-2">NAVIGATOR INTERFACE</h1>
                            <p className="text-zinc-500 text-sm">Star Map Module Not Loaded.</p>
                            <div className="mt-4"><LayoutSwitcher /></div>
                        </div>
                    </div>
                </>
            );
        case 'workshop':
            return (
                <>
                    <BossHud />
                    <div className="h-screen flex items-center justify-center bg-stone-900 text-amber-100">
                        <div className="text-center">
                            <h1 className="text-2xl font-bold mb-2">ISOMETRIC WORKSHOP</h1>
                            <p className="text-stone-500 text-sm">Construction Grid Offline.</p>
                            <div className="mt-4"><LayoutSwitcher /></div>
                        </div>
                    </div>
                </>
            );
        case 'cyberdeck':
        default:
            return (
                <>
                    <BossHud />
                    <CyberdeckLayout>{content}</CyberdeckLayout>
                </>
            );
    }
}
