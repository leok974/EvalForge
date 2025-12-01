import React, { useState, useEffect } from 'react';
import { useBossStore } from '../store/bossStore';
import { useGameStore } from '../store/gameStore';
import { FX } from '../lib/fx';

export function BossPanel() {
    const { status, bossId, encounterId, setBossResolved } = useBossStore();
    const { damageIntegrity, addXp } = useGameStore();
    const [code, setCode] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [bossData, setBossData] = useState<any>(null);

    // Fetch boss details on mount
    useEffect(() => {
        if (bossId) {
            fetch('/api/boss/current')
                .then(res => res.json())
                .then(data => {
                    if (data.active) {
                        setBossData(data);
                    }
                });
        }
    }, [bossId]);

    // Effect to set starting code once data is loaded
    useEffect(() => {
        if (bossData?.starting_code && !code) {
            setCode(bossData.starting_code);
        }
    }, [bossData]);

    const handleSubmit = async () => {
        if (!encounterId) return;
        setSubmitting(true);

        try {
            const res = await fetch('/api/boss/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ encounterId, code }),
            });
            const result = await res.json();

            if (result.status === 'success') {
                setBossResolved('success');
                FX.emit('confetti', { count: 200 });
                // Play success sound
                // addXp handled by backend, but we can optimistically update or re-fetch profile
            } else if (result.status === 'failed') {
                setBossResolved('failed');
                FX.emit('glitch', { intensity: 'high' });
                damageIntegrity(20); // Sync with backend logic
            } else {
                // Still active (e.g. multiple attempts allowed?)
                // If the backend says 'active', maybe we just show feedback.
                // But the prompt implies "Submit" resolves it.
            }
        } catch (e) {
            console.error(e);
        } finally {
            setSubmitting(false);
        }
    };

    if (status !== 'active') return null;

    return (
        <div className="flex flex-col h-full bg-black/90 text-red-100 p-6 border-l-4 border-red-600">
            <h2 className="text-3xl font-bold mb-2 text-red-500 animate-pulse">BOSS ENCOUNTER</h2>
            <div className="mb-4">
                <h3 className="text-xl font-mono">{bossData?.boss_id || 'Unknown Boss'}</h3>
                <p className="text-sm text-red-300 opacity-80">Time is running out.</p>
            </div>

            <div className="flex-1 flex flex-col gap-4">
                <div className="bg-zinc-900 p-4 rounded border border-red-900/50">
                    <h4 className="font-bold mb-2">Objective</h4>
                    <p className="font-mono text-sm">
                        {bossData?.technical_objective || "Defeat the boss by solving the challenge."}
                    </p>
                </div>

                <textarea
                    className="flex-1 bg-black border border-red-800 p-4 font-mono text-sm focus:outline-none focus:border-red-500 text-zinc-300"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="// Write your solution here..."
                />

                <button
                    onClick={handleSubmit}
                    disabled={submitting}
                    className="bg-red-600 hover:bg-red-500 text-white font-bold py-3 px-6 rounded shadow-[0_0_15px_rgba(220,38,38,0.5)] transition-all disabled:opacity-50"
                >
                    {submitting ? 'COMPILING...' : 'EXECUTE ATTACK'}
                </button>
            </div>
        </div>
    );
}
