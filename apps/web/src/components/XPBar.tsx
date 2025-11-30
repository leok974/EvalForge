import React, { useEffect, useState } from 'react';
import { ProgressUpdate } from '../hooks/useArcadeStream';

interface Props {
    user: string;
    lastProgress: ProgressUpdate | null;
}

interface Profile {
    total_xp: number;
    level: number;
}

export function XPBar({ user, lastProgress }: Props) {
    const [profile, setProfile] = useState<Profile>({ total_xp: 0, level: 1 });
    const [showToast, setShowToast] = useState(false);

    // 1. Fetch initial profile
    useEffect(() => {
        fetch(`/api/profile/${user}`)
            .then(res => res.json())
            .then(setProfile)
            .catch(console.error);
    }, [user]);

    // 2. React to Stream Updates
    useEffect(() => {
        if (lastProgress) {
            // Optimistic update
            setProfile(prev => ({
                total_xp: prev.total_xp + lastProgress.xp_gained,
                level: lastProgress.new_global_level
            }));

            // Trigger animation
            setShowToast(true);
            const timer = setTimeout(() => setShowToast(false), 3000);
            return () => clearTimeout(timer);
        }
    }, [lastProgress]);

    // Calculate Progress to next level (assuming 1000 XP per level)
    const xpInLevel = profile.total_xp % 1000;
    const percent = (xpInLevel / 1000) * 100;

    return (
        <div className="relative flex items-center gap-3">

            {/* Pop-up Toast for XP Gain */}
            {showToast && lastProgress && (
                <div className="absolute top-10 right-0 z-50 animate-bounce-in">
                    <div className="bg-cyan-900/90 border border-cyan-500 text-cyan-100 px-3 py-1.5 rounded shadow-xl text-xs font-mono font-bold flex flex-col items-center">
                        <span>+{lastProgress.xp_gained} XP</span>
                        {lastProgress.global_level_up && <span className="text-amber-400 animate-pulse">LEVEL UP!</span>}
                    </div>
                </div>
            )}

            {/* Level Badge */}
            <div className="flex flex-col items-end">
                <div className="text-[10px] text-zinc-500 font-mono leading-none">LVL</div>
                <div className="text-xl font-bold text-cyan-400 leading-none">{profile.level}</div>
            </div>

            {/* Bar Container */}
            <div className="w-32 h-2 bg-zinc-800 rounded-full overflow-hidden border border-zinc-700">
                <div
                    className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 transition-all duration-1000 ease-out"
                    style={{ width: `${percent}%` }}
                />
            </div>

            <div className="text-[10px] font-mono text-zinc-500 w-12 text-right">
                {xpInLevel}/1000
            </div>
        </div>
    );
}
