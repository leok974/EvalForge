import React, { useState } from 'react';
import { useGameStore } from '../store/gameStore';
import { useSettingsStore } from '../store/settingsStore';
import { useAuth } from '../hooks/useAuth';
import { SettingsModal } from '../components/SettingsModal';
import { AvatarSelector } from '../components/AvatarSelector';
import { BossHud } from '../components/BossHud';
import { BossHistoryPanel } from '../components/BossHistoryPanel';
import { PracticeGauntletCard } from '../components/practice/PracticeGauntletCard';
import {
    Terminal,
    Layout,
    Settings,
    Shield,
    Cpu,
    Wifi,
    Battery,
    Clock,
    Menu,
    User
} from 'lucide-react';

interface Props {
    children: React.ReactNode;
}

import { ProjectsPanel } from '../components/ProjectsPanel';

export function CyberdeckLayout({ children }: Props) {
    const { layout, setLayout } = useGameStore();
    const { crtMode } = useSettingsStore();
    const { user } = useAuth();
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isAvatarOpen, setIsAvatarOpen] = useState(false);
    const [isLayoutOpen, setIsLayoutOpen] = useState(false);
    const [isProjectsOpen, setIsProjectsOpen] = useState(false);

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100 font-mono selection:bg-cyan-900 selection:text-cyan-100 flex flex-col">

            {/* --- HEADER --- */}
            <header className="h-14 border-b border-zinc-800 bg-zinc-900/50 flex items-center justify-between px-4 sticky top-0 z-50 backdrop-blur-md">

                {/* Left: Brand & Mode Switcher */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-3 text-cyan-400">
                        <img src="/branding/logo.png" alt="EvalForge" className="h-9 w-auto rounded-full object-contain" />
                        <span className={`text-sm font-semibold tracking-[0.25em] ${crtMode ? 'crt-aberration' : ''}`}>EVALFORGE</span>
                    </div>

                    <div className="h-6 w-px bg-zinc-800" />

                    <div
                        className="relative h-full flex items-center"
                        onMouseEnter={() => setIsLayoutOpen(true)}
                        onMouseLeave={() => setIsLayoutOpen(false)}
                    >
                        <button
                            className={`flex items-center gap-2 text-xs font-bold transition-colors uppercase tracking-wider ${isLayoutOpen ? 'text-white' : 'text-zinc-400 hover:text-white'}`}
                        >
                            <Layout className="w-4 h-4" />
                            {layout}
                        </button>

                        {/* Dropdown with safe hover gap (pt-2) */}
                        <div
                            className={`absolute top-full left-0 w-48 pt-2 transition-all duration-200 origin-top-left ${isLayoutOpen ? 'opacity-100 translate-y-0 visible' : 'opacity-0 -translate-y-2 invisible pointer-events-none'}`}
                        >
                            <div className="bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl overflow-hidden p-1 flex flex-col gap-1">
                                <button
                                    onClick={() => { setLayout('cyberdeck'); setIsLayoutOpen(false); }}
                                    className={`w-full text-left px-3 py-2 text-xs rounded transition-colors ${layout === 'cyberdeck' ? 'bg-zinc-800 text-cyan-400' : 'text-zinc-400 hover:bg-zinc-800 hover:text-cyan-400'}`}
                                >
                                    CYBERDECK
                                </button>
                                <button
                                    onClick={() => { setLayout('navigator'); setIsLayoutOpen(false); }}
                                    className={`w-full text-left px-3 py-2 text-xs rounded transition-colors ${layout === 'navigator' ? 'bg-zinc-800 text-purple-400' : 'text-zinc-400 hover:bg-zinc-800 hover:text-purple-400'}`}
                                >
                                    NAVIGATOR
                                </button>
                                <button
                                    onClick={() => { setLayout('workshop'); setIsLayoutOpen(false); }}
                                    className={`w-full text-left px-3 py-2 text-xs rounded transition-colors ${layout === 'workshop' ? 'bg-zinc-800 text-orange-400' : 'text-zinc-400 hover:bg-zinc-800 hover:text-orange-400'}`}
                                >
                                    WORKSHOP
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="h-6 w-px bg-zinc-800" />

                    <button
                        onClick={() => setIsProjectsOpen(true)}
                        className="flex items-center gap-2 text-xs font-bold text-zinc-400 hover:text-white transition-colors uppercase tracking-wider"
                    >
                        <span>🚀</span> PROJECTS
                    </button>
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

                    {user && (
                        <>
                            <button
                                onClick={() => setIsAvatarOpen(true)}
                                className="flex items-center gap-2 hover:opacity-80 transition-opacity cursor-pointer"
                                title="Change Avatar"
                            >
                                {user.avatar_url ? (
                                    <img
                                        src={user.avatar_url}
                                        alt={user.name}
                                        className="w-8 h-8 rounded-full border-2 border-cyan-500/50"
                                    />
                                ) : (
                                    <div className="w-8 h-8 rounded-full border-2 border-cyan-500/50 bg-zinc-800 flex items-center justify-center">
                                        <User className="w-4 h-4 text-cyan-400" />
                                    </div>
                                )}
                                <span className="text-xs text-zinc-300 hidden lg:inline">{user.name}</span>
                            </button>
                            <div className="h-6 w-px bg-zinc-800" />
                        </>
                    )}

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


            {/* Settings Modal */}
            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />

            {/* Avatar Selector Modal */}
            <AvatarSelector isOpen={isAvatarOpen} onClose={() => setIsAvatarOpen(false)} />

            {/* Projects Panel */}
            <ProjectsPanel user={user} isOpen={isProjectsOpen} onClose={() => setIsProjectsOpen(false)} />

        </div>
    );
}
