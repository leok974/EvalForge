import React from 'react';
import { NanoLogo } from '../components/Branding';
import { LayoutSwitcher } from '../components/LayoutSwitcher';
import { GameToast } from '../components/GameToast';
import { NetworkPanel } from '../components/hud/NetworkPanel';
import { EventLog } from '../components/hud/EventLog';

// Props allow us to inject the main "Terminal" content (DevUI)
interface Props {
    children: React.ReactNode;
}

export function CyberdeckLayout({ children }: Props) {
    return (
        <div className="h-screen w-screen bg-nano-900 text-zinc-100 flex flex-col font-mono overflow-hidden selection:bg-banana-500 selection:text-black relative">

            {/* 0. Background Effects (Scanlines/Grid) */}
            <div className="absolute inset-0 pointer-events-none z-0 opacity-20"
                style={{ backgroundImage: 'radial-gradient(#3f3f46 1px, transparent 1px)', backgroundSize: '24px 24px' }}
            />

            {/* 1. TOP HUD */}
            <header className="flex-none flex items-center justify-between px-4 py-2 border-b border-nano-800 bg-nano-900/95 backdrop-blur z-50">
                <div className="flex items-center gap-6">
                    <NanoLogo />
                    <div className="h-4 w-px bg-zinc-800" />
                    <LayoutSwitcher />
                </div>

                {/* Placeholder for future top-level stats */}
                <div className="text-[10px] text-zinc-600 font-mono">
                    SYS.STATUS: <span className="text-emerald-500">OPTIMAL</span>
                </div>
            </header>

            {/* 2. MAIN VIEWPORT */}
            <div className="flex flex-1 relative z-10 overflow-hidden">

                {/* Left Panel: Network / Telemetry */}
                <aside className="hidden xl:flex w-64 flex-col border-r border-nano-800 bg-black/40 p-4 gap-4">
                    {/* 1. Real Network Stats */}
                    <NetworkPanel />

                    {/* 2. Real Event Log */}
                    <EventLog />

                    {/* 3. Static Footer */}
                    <div className="mt-auto pt-4 border-t border-zinc-800 text-[9px] text-zinc-700 text-center">
                        EVALFORGE v2.0.4<br />SECURE CONNECTION
                    </div>
                </aside>

                {/* Center: The Terminal (Injected Content) */}
                <main className="flex-1 relative flex flex-col min-w-0">
                    {children}
                </main>

            </div>

            {/* 3. Global Overlays */}
            <GameToast />
        </div>
    );
}
