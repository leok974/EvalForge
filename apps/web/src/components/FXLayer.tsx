import React, { useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { useSettingsStore } from '../store/settingsStore';
import { useGameStore } from '../store/gameStore';
import { useGameSocket } from '../hooks/useGameSocket';
import { useSound } from '../hooks/useSound';
import { useBossStore } from '../store/bossStore';
import { ConfettiManager } from './fx/ConfettiManager';
import { FX } from '../lib/fx';
import { cn } from '../lib/utils';

interface Props {
    children: React.ReactNode;
}

export function FXLayer({ children }: Props) {
    const { crtMode, screenShake } = useSettingsStore();
    const layout = useGameStore((s) => s.layout);

    const controls = useAnimation();
    const lastEvent = useGameSocket();
    const { play } = useSound();
    const startBoss = useBossStore((s) => s.startBoss);

    useEffect(() => {
        if (!lastEvent) return;

        if (lastEvent.type === 'boss_spawn') {
            // Pass full spawn payload to store
            startBoss({
                bossId: lastEvent.boss_id || 'boss-reactor-core',
                name: lastEvent.name || 'Reactor Core Meltdown',
                difficulty: lastEvent.difficulty || 'normal',
                durationSeconds: lastEvent.duration_seconds || 30 * 60,
                hpPenaltyOnFail: lastEvent.hp_penalty_on_fail || 10,
                baseXpReward: lastEvent.base_xp_reward || 300,
            });

            play('boss');
            if (screenShake) {
                const intensity = layout === 'workshop' ? 20 : 10;
                controls.start({
                    x: [0, -intensity, intensity, -intensity, intensity, 0],
                    transition: { duration: 0.5 }
                });
            }

            // Optional: global FX tint/glitch via FX bus
            FX.emit('glitch', { intensity: 'high' });
        } else if (lastEvent.type === 'boss_result') {
            if (lastEvent.outcome === 'success') {
                play('success');
                FX.emit('confetti', { count: 150 });
                // Green tint handled by CSS class based on state if we tracked it, 
                // but for now we rely on the event triggering a transient effect if we had one.
                // The user requested explicit tint state.
                // I need to add state for tint/shake/glitch if I want persistent overlays.
                // But FXLayer currently uses `lastEvent` directly for some things.
                // Let's stick to the user's request of using local state for FX.
            } else {
                play('error');
                FX.emit('glitch', { intensity: 'high' });
                if (screenShake) {
                    controls.start({
                        x: [0, -10, 10, -10, 10, 0],
                        transition: { duration: 0.4 }
                    });
                }
            }
        } else if (lastEvent.type === 'sync_complete') {
            play('success');
            FX.emit('confetti', { count: 150 });
        } else if (lastEvent.type === 'quest_complete') {
            FX.emit('confetti', { count: 200, y: 0.3 });
        }
    }, [lastEvent, screenShake, controls, play, layout, startBoss]);

    // Helper to determine active FX classes based on lastEvent (transient)
    // In a real app we'd use a timeout to clear these, but for MVP we rely on the event being "fresh"
    // or we add a state. The user's code snippet used `setFxState`.
    // I should probably implement that state to be faithful to the request.

    // Let's add the state.
    const [fxState, setFxState] = React.useState({
        shake: false,
        glitch: false,
        tint: null as 'red' | 'green' | null,
    });

    useEffect(() => {
        if (!lastEvent) return;

        if (lastEvent.type === 'boss_spawn') {
            setFxState(s => ({ ...s, shake: true, tint: 'red' }));
            setTimeout(() => setFxState(s => ({ ...s, shake: false, tint: null })), 2000);
        } else if (lastEvent.type === 'boss_result') {
            if (lastEvent.outcome === 'success') {
                setFxState(s => ({ ...s, tint: 'green' }));
                setTimeout(() => setFxState(s => ({ ...s, tint: null })), 2000);
            } else {
                setFxState(s => ({ ...s, shake: true, glitch: true, tint: 'red' }));
                setTimeout(() => setFxState(s => ({ ...s, shake: false, glitch: false, tint: null })), 1000);
            }
        }
    }, [lastEvent]);

    const isCyberdeck = layout === 'cyberdeck';

    return (
        <div className={`relative w-full h-full overflow-hidden bg-black ${isCyberdeck && crtMode ? 'crt-aberration' : ''}`}>

            {/* 1. Main Content (Z-10) */}
            <motion.div animate={controls} className="w-full h-full relative z-10">
                {children}
            </motion.div>

            {/* --- THEME OVERLAYS (Z-0 to Z-20) --- */}

            {/* CYBERDECK (CRT) - z-20 */}
            {layout === 'cyberdeck' && crtMode && (
                <div className="absolute inset-0 pointer-events-none z-20 opacity-30 mix-blend-overlay"
                    style={{
                        backgroundImage: "linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06))",
                        backgroundSize: "100% 2px, 3px 100%"
                    }}
                />
            )}

            {/* NAVIGATOR (Stars) - z-0 (Background) */}
            {layout === 'navigator' && (
                <div className="absolute inset-0 pointer-events-none z-0">
                    <div className="absolute inset-0 bg-[radial-gradient(white_1px,transparent_1px)] [background-size:50px_50px] opacity-20" />
                    <div className="absolute inset-0 bg-gradient-to-b from-blue-950/40 to-transparent" />
                </div>
            )}

            {/* WORKSHOP (Grid) - z-0 (Background) */}
            {layout === 'workshop' && (
                <div className="absolute inset-0 pointer-events-none z-0 opacity-10"
                    style={{
                        backgroundImage: `linear-gradient(to right, #888 1px, transparent 1px), linear-gradient(to bottom, #888 1px, transparent 1px)`,
                        backgroundSize: '40px 40px'
                    }}
                />
            )}

            {/* BOSS EVENT TINT (Z-30) */}
            <div
                className={cn(
                    "absolute inset-0 pointer-events-none z-30 transition-opacity duration-500",
                    fxState.tint === 'red' ? "bg-red-500/20 mix-blend-overlay deck-boss-tint-red" : "",
                    fxState.tint === 'green' ? "bg-green-500/20 mix-blend-overlay deck-boss-tint-green" : "",
                    fxState.glitch ? "deck-boss-glitch" : "",
                    fxState.shake ? "deck-boss-shake" : ""
                )}
            />

            {/* Mount the Particle Engine */}
            <ConfettiManager />

        </div>
    );
}
