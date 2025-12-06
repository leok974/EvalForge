import React from 'react';
import { useGameStore } from '../store/gameStore';
import { useSettingsStore } from '../store/settingsStore';
import { BossHistoryPanel } from '../components/BossHistoryPanel';
import { PracticeGauntletCard } from '../components/practice/PracticeGauntletCard';
import { Clock } from 'lucide-react';
import { GameShellHeader } from '../components/shell/GameShellHeader';

interface Props {
    children: React.ReactNode;
}

export function CyberdeckLayout({ children }: Props) {
    const { crtMode } = useSettingsStore();

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100 font-mono selection:bg-cyan-900 selection:text-cyan-100 flex flex-col">

            {/* --- HEADER --- */}
            <GameShellHeader />

            {/* --- MAIN CONTENT --- */}
            <div className="flex-1 flex overflow-hidden">

                {/* Left Sidebar */}
                <aside className="w-64 border-r border-zinc-800 bg-zinc-900/30 hidden lg:flex flex-col">
                    <div className="p-4 space-y-6 flex-1 overflow-y-auto">

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

                        {/* Practice Gauntlet */}
                        <div>
                            <PracticeGauntletCard />
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

        </div>
    );
}
