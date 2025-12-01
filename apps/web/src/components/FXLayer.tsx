import React, { useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { useSettingsStore } from '../store/settingsStore';
import { useGameStore } from '../store/gameStore';
import { useGameSocket } from '../hooks/useGameSocket';
import { useSound } from '../hooks/useSound';
import { useBossStore } from '../store/bossStore';
import { ConfettiManager } from './fx/ConfettiManager';
import { FX } from '../lib/fx';

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
        } else if (lastEvent.type === 'sync_complete') {
            play('success');
            FX.emit('confetti', { count: 150 });
        } else if (lastEvent.type === 'quest_complete') {
            FX.emit('confetti', { count: 200, y: 0.3 });
        }
    }, [lastEvent, screenShake, controls, play, layout, startBoss]);

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
            {lastEvent?.type === 'boss_spawn' && (
                <div className={`absolute inset-0 pointer-events-none z-30 animate-pulse opacity-20 ${layout === 'cyberdeck' ? 'bg-red-500' :
                    layout === 'navigator' ? 'bg-purple-500' : 'bg-orange-500'
                    }`} />
            )}

            {/* Mount the Particle Engine */}
            <ConfettiManager />

        </div>
    );
}
