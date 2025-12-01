import { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { FX } from '../../lib/fx';
import { useSettingsStore } from '../../store/settingsStore';

export function ConfettiManager() {
    const { particles } = useSettingsStore(); // toggle from Settings

    useEffect(() => {
        // subscribe returns an unsubscribe fn
        const unsubscribe = FX.subscribe((type, payload) => {
            if (!particles) return;

            if (type === 'confetti') {
                const { x = 0.5, y = 0.5, count = 120 } = (payload || {}) as any;

                // Clamp count to prevent lag
                const safeCount = Math.min(count, 300);

                confetti({
                    particleCount: safeCount,
                    spread: 70,
                    origin: { x, y },
                    zIndex: 9999,
                    colors: ['#FACC15', '#22D3EE', '#FFFFFF'], // banana/cyan/white
                    ticks: 200,
                });
            }

            // you can handle 'glitch' or 'shockwave' here later if needed
        });

        return () => { unsubscribe(); };
    }, [particles]);

    return null;
}
