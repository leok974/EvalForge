import React, { useState } from 'react';
import { useGameStore } from '../store/gameStore';
import { useSettingsStore } from '../store/settingsStore';
import { SettingsModal } from '../components/SettingsModal';
import { BossHud } from '../components/BossHud';
import { BossHistoryPanel } from '../components/BossHistoryPanel';
import {
    Terminal,
    Layout,
    Settings,
    Shield,
    Cpu,
    Wifi,
    Battery,
    Clock,
    Menu
} from 'lucide-react';

interface Props {
    children: React.ReactNode;
}

export function CyberdeckLayout({ children }: Props) {
    const { layout, setLayout } = useGameStore();
    const { crtMode } = useSettingsStore();
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100 font-mono selection:bg-cyan-900 selection:text-cyan-100 flex flex-col">

            {/* --- HEADER --- */}
            <header className="h-14 border-b border-zinc-800 bg-zinc-900/50 flex items-center justify-between px-4 sticky top-0 z-50 backdrop-blur-md">

                {/* Left: Brand & Mode Switcher */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-cyan-400">
                        <Terminal className="w-5 h-5" />
                        <span className={`font-bold tracking-widest ${crtMode ? 'crt-aberration' : ''}`}>EVALFORGE</span>
                    </div>

                    <div className="h-6 w-px bg-zinc-800" />

                    <div className="relative group">
                        <button className="flex items-center gap-2 text-xs font-bold text-zinc-400 hover:text-white transition-colors uppercase tracking-wider">
                            <Layout className="w-4 h-4" />
                            {layout}
                        </button>

                        {/* Dropdown */}
                        <div className="absolute top-full left-0 mt-2 w-48 bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-all transform origin-top-left scale-95 group-hover:scale-100">
                            <div className="p-1">
                                <button onClick={() => setLayout('cyberdeck')} className="w-full text-left px-3 py-2 text-xs hover:bg-zinc-800 rounded text-zinc-400 hover:text-cyan-400 transition-colors">
                                    CYBERDECK
                                </button>
                                <button onClick={() => setLayout('navigator')} className="w-full text-left px-3 py-2 text-xs hover:bg-zinc-800 rounded text-zinc-400 hover:text-purple-400 transition-colors">
                                    NAVIGATOR
                                </button>
                                <button onClick={() => setLayout('workshop')} className="w-full text-left px-3 py-2 text-xs hover:bg-zinc-800 rounded text-zinc-400 hover:text-orange-400 transition-colors">
                                    WORKSHOP
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Center: Boss HUD */}
                <div className="flex-1 flex justify-center">
                    <BossHud />
                </div>

                {/* Right: Status Indicators */}
                <div className="flex items-center gap-6 text-xs font-bold text-zinc-500">
                    <div className="flex items-center gap-2 hidden md:flex">
                        <Shield className="w-3 h-3 text-emerald-500" />
                        <span>SECURE</span>
                    </div>
                    <div className="flex items-center gap-2 hidden md:flex">
                        <Cpu className="w-3 h-3 text-cyan-500" />
                        <span>ONLINE</span>
                    </div>
                    <div className="flex items-center gap-2 hidden md:flex">
                        <Wifi className="w-3 h-3" />
                        <span>50ms</span>
                    </div>
                    <div className="flex items-center gap-2 hidden md:flex">
                        <Battery className="w-3 h-3" />
                        <span>100%</span>
                    </div>

                    <div className="h-6 w-px bg-zinc-800" />

                    <button
                        onClick={() => setIsSettingsOpen(true)}
                        className="p-2 hover:bg-zinc-800 rounded-full transition-colors text-zinc-400 hover:text-white"
                    >
                        <Settings className="w-4 h-4" />
                    </button>
                </div>
            </header>

            {/* --- MAIN CONTENT --- */}
            <div className="flex-1 flex overflow-hidden">

                {/* Left Sidebar (Optional, for now just a placeholder or navigation) */}
                <aside className="w-64 border-r border-zinc-800 bg-zinc-900/30 hidden lg:flex flex-col">
                    <div className="p-4 space-y-6">

                        <div>
                            <div className={`text-[9px] uppercase tracking-widest text-zinc-600 mb-2 font-bold ${crtMode ? 'crt-aberration' : ''}`}>
                                Network Topology
                            </div>
                            <div className="space-y-1">
                                <div className="text-xs text-zinc-400 hover:text-cyan-400 cursor-pointer py-1 px-2 rounded hover:bg-zinc-800/50 transition-colors">Localhost</div>
                                <div className="text-xs text-zinc-500 py-1 px-2">Staging (Offline)</div>
                                <div className="text-xs text-zinc-500 py-1 px-2">Production (Offline)</div>
                            </div>
                        </div>

                        <div>
                            <div className={`text-[9px] uppercase tracking-widest text-zinc-600 mb-2 font-bold ${crtMode ? 'crt-aberration' : ''}`}>
                                Active Modules
                            </div>
                            <div className="space-y-1">
                                <div className="text-xs text-emerald-400/80 py-1 px-2 bg-emerald-950/20 rounded border border-emerald-900/50">Auth Service</div>
                                <div className="text-xs text-emerald-400/80 py-1 px-2 bg-emerald-950/20 rounded border border-emerald-900/50">Database Shard</div>
                                <div className="text-xs text-emerald-400/80 py-1 px-2 bg-emerald-950/20 rounded border border-emerald-900/50">Event Bus</div>
                            </div>
                        </div>

                        {/* Boss History */}
                        <div>
                            <BossHistoryPanel />
                        </div>

                    </div>

                    <div className="mt-auto p-4 border-t border-zinc-800">
                        <div className="flex items-center gap-3 text-zinc-500">
                            <Clock className="w-4 h-4" />
                            <span className="text-xs">UPTIME: 04:20:69</span>
                        </div>
                    </div>
                </aside>

                {/* Content Area */}
                <main className="flex-1 overflow-y-auto relative">
                    {children}
                </main>

            </div>

            {/* Settings Modal */}
            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />

        </div>
    );
}
