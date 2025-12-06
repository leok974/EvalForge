import { useNavigate } from 'react-router-dom';
import { useGameStore } from '@/store/gameStore';
import { ActiveTrackStatus } from '@/components/hud/ActiveTrackStatus';
import { OrionMap } from './OrionMap';
import { GameShellHeader } from '@/components/shell/GameShellHeader';
import { RightRailBossPracticeColumn } from "@/components/layout/RightRailBossPracticeColumn";
import { useEffect, useState } from 'react';
import { refreshWorldProgress } from '@/features/progress/trackProgress';

export function OrionLayout() {
    const [loaded, setLoaded] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        refreshWorldProgress()
            .then(() => setLoaded(true))
            .catch((err) => {
                console.warn('World progress bootstrap failed', err);
                setError(err as Error);
            });
    }, []);

    const navigate = useNavigate();
    const activeTrack = useGameStore((s) => s.activeTrack);

    const hasTrack = Boolean(activeTrack);

    const handleWarpToTrack = () => {
        if (!activeTrack) return;
        navigate('/workshop');
    };

    const handleOpenInCyberdeck = () => {
        if (!activeTrack) return;
        navigate('/cyberdeck');
    };

    return (
        <div className="flex h-screen flex-col bg-slate-950 text-slate-50 font-sans selection:bg-cyan-500/30">
            <GameShellHeader />

            <main className="flex flex-1 gap-4 px-6 pb-2 pt-2 overflow-hidden">
                <section className="flex-1 min-w-0 relative rounded-xl border border-slate-800/60 bg-slate-900/40 shadow-inner overflow-hidden">
                    {/* ✨ Twinkling stars behind the map */}
                    <div className="orion-starfield-layer" />

                    {/* Map sits above the starfield */}
                    <div className="relative h-full">
                        {/* Optional tiny status overlay */}
                        {!loaded && !error && (
                            <div className="absolute left-4 top-4 text-[10px] text-cyan-300/70 z-10">
                                Syncing star chart…
                            </div>
                        )}
                        {error && (
                            <div className="absolute left-4 top-4 text-[10px] text-rose-400/80 z-10">
                                Progress unavailable
                            </div>
                        )}
                        <OrionMap />
                    </div>
                </section>

                <aside className="w-[360px] flex-shrink-0 space-y-3 hidden lg:block">
                    <RightRailBossPracticeColumn mode="world" />
                </aside>
            </main>

            <footer className="flex items-center justify-between border-t border-slate-800 bg-slate-950/80 px-6 py-3 text-[11px] backdrop-blur-md">
                <ActiveTrackStatus />
                <div className="flex gap-3">
                    <button
                        type="button"
                        onClick={handleWarpToTrack}
                        disabled={!hasTrack}
                        className={`
              px-4 py-1.5 rounded-lg border text-[10px] tracking-[0.22em] font-semibold transition-all
              ${hasTrack
                                ? 'border-cyan-500/50 bg-cyan-500/10 text-cyan-100 hover:bg-cyan-500/20 hover:border-cyan-400 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                                : 'border-slate-800 bg-slate-900/40 text-slate-600 cursor-not-allowed'
                            }
            `}
                    >
                        Warp to Track
                    </button>

                    <button
                        type="button"
                        onClick={handleOpenInCyberdeck}
                        disabled={!hasTrack}
                        className={`
              px-4 py-1.5 rounded-lg border text-[10px] tracking-[0.22em] font-semibold transition-all
              ${hasTrack
                                ? 'border-sky-500/50 bg-sky-500/10 text-sky-100 hover:bg-sky-500/20 hover:border-sky-400 shadow-[0_0_12px_rgba(14,165,233,0.15)]'
                                : 'border-slate-800 bg-slate-900/40 text-slate-600 cursor-not-allowed'
                            }
            `}
                    >
                        Open in Cyberdeck
                    </button>
                </div>
            </footer>
        </div>
    );
}
