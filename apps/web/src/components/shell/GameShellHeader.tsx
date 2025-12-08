import React, { useState } from 'react';
import { useGameStore } from '@/store/gameStore';
import { useSettingsStore } from '@/store/settingsStore';
import { useAuth } from '@/hooks/useAuth';
import { SettingsModal } from '@/components/SettingsModal';
import { AvatarSelector } from '@/components/AvatarSelector';
import { ProjectsPanel } from '@/components/ProjectsPanel';
import { BossHud } from '@/components/BossHud';
import {
    Layout,
    Settings,
    Shield,
    Cpu,
    Wifi,
    Battery,
    Battery,
    User
} from 'lucide-react';
import { useSeniorProgress } from '@/hooks/useSeniorProgress';

export function GameShellHeader() {
    const { layout, setLayout } = useGameStore();
    const { crtMode } = useSettingsStore();
    const { user } = useAuth();
    const { data: senior } = useSeniorProgress();

    // Local state for modals
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isAvatarOpen, setIsAvatarOpen] = useState(false);
    const [isLayoutOpen, setIsLayoutOpen] = useState(false);
    const [isProjectsOpen, setIsProjectsOpen] = useState(false);

    return (
        <>
            <header className="h-14 border-b border-zinc-800 bg-zinc-900/50 flex items-center justify-between px-4 sticky top-0 z-50 backdrop-blur-md w-full">

                {/* Left: Brand & Mode Switcher */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-3 text-cyan-400">
                        <img src="/branding/logo.png" alt="EvalForge" className="h-9 w-auto rounded-full object-contain" />
                        <span className={`text-sm font-semibold tracking-[0.25em] ${crtMode ? 'crt-aberration' : ''}`}>EVALFORGE</span>
                    </div>

                    <div className="h-6 w-px bg-zinc-800" />

                    {/* Layout Switcher */}
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
                                    onClick={() => { setLayout('orion'); setIsLayoutOpen(false); }}
                                    className={`w-full text-left px-3 py-2 text-xs rounded transition-colors ${layout === 'orion' ? 'bg-zinc-800 text-purple-400' : 'text-zinc-400 hover:bg-zinc-800 hover:text-purple-400'}`}
                                >
                                    ORION
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
                    {/* Senior Progress Badge */}
                    {senior && (
                        <div className="hidden lg:flex items-center gap-2 text-[10px] uppercase tracking-wide mr-2">
                            <span className="rounded-full bg-emerald-900/40 border border-emerald-500/30 px-2 py-0.5 text-emerald-400 font-mono shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                                Bosses {senior.senior_bosses_cleared}/{senior.total_senior_bosses}
                            </span>
                            {senior.legendary_trials_completed > 0 && (
                                <span className="rounded-full bg-amber-900/40 border border-amber-500/30 px-2 py-0.5 text-amber-400 font-mono shadow-[0_0_10px_rgba(245,158,11,0.2)] animate-pulse">
                                    Legendary {senior.legendary_trials_completed}
                                </span>
                            )}
                        </div>
                    )}

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

            {/* Modals are managed here so they work across all layouts */}
            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
            <AvatarSelector isOpen={isAvatarOpen} onClose={() => setIsAvatarOpen(false)} />
            <ProjectsPanel user={user} isOpen={isProjectsOpen} onClose={() => setIsProjectsOpen(false)} />
        </>
    );
}
