import React from 'react';
import { useGameStore } from '../store/gameStore';
import { CyberdeckLayout as CyberdeckLayoutV1 } from './CyberdeckLayout';
import { CyberdeckLayout as CyberdeckLayoutV2 } from '../components/layouts/CyberdeckLayout';
import DevUI from '../pages/DevUI'; // The main content
import { LayoutSwitcher } from '../components/LayoutSwitcher';
import { BossHud } from '../components/BossHud';
import { LAYOUTS } from '../lib/layouts';

const USE_CYBERDECK_V2 = import.meta.env.VITE_LAYOUT_CYBERDECK_V2 === '1' || import.meta.env.VITE_LAYOUT_CYBERDECK_V2 === 'true';

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
        case 'orion':
            // Dynamic import to avoid circular deps if needed, but for now direct import via registry is fine
            // We need to import OrionLayout here or use the component from registry
            // Since registry has the component, we can just use that if we refactored GameShell to use registry fully.
            // But for now, let's just add the case.
            // We need to import OrionLayout at top of file first.
            const OrionLayoutComponent = LAYOUTS.find(l => l.id === 'orion')?.component;
            if (OrionLayoutComponent) {
                return <OrionLayoutComponent>{content}</OrionLayoutComponent>;
            }
            return <div>Orion Layout Not Found</div>;
        case 'cyberdeck':
        default:
            return (
                <>
                    <BossHud />
                    {USE_CYBERDECK_V2 ? (
                        <CyberdeckLayoutV2>{content}</CyberdeckLayoutV2>
                    ) : (
                        <CyberdeckLayoutV1>{content}</CyberdeckLayoutV1>
                    )}
                </>
            );
    }
}
