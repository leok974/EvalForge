import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { SettingsModal } from '@/components/SettingsModal';
import { AvatarSelector } from '@/components/AvatarSelector';
import { ProjectsPanel } from '@/components/ProjectsPanel';
import { BossHud } from '@/components/BossHud';
import {
    Settings,
    Shield,
    Cpu,
    Wifi,
    Battery,
    User
} from 'lucide-react';
import { useSeniorProgress } from '@/hooks/useSeniorProgress';

// Sprint 22: Layout switcher removed — Workshop is the only layout.
// crtMode removed — Cyberdeck (its only consumer) was deleted.

export function GameShellHeader() {
    const { user } = useAuth();
    const { data: senior } = useSeniorProgress();

    // Local state for modals
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isAvatarOpen, setIsAvatarOpen] = useState(false);
    const [isProjectsOpen, setIsProjectsOpen] = useState(false);

    return (
        <>
            <header className="h-14 border-b border-zinc-800 bg-zinc-900/50 flex items-center justify-between px-4 sticky top-0 z-50 backdrop-blur-md w-full">

                {/* Left: Brand */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-3 text-cyan-400">
                        <img src="/branding/logo.png" alt="EvalForge" className="h-9 w-auto rounded-full object-contain" />
                        <span className="text-sm font-semibold tracking-[0.25em]">EVALFORGE</span>
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
