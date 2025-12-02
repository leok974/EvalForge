import React, { useEffect, useState } from 'react';
import { User, Terminal, Code, Cpu, Shield, Zap, Circle } from 'lucide-react';

type Avatar = {
    id: string;
    name: string;
    description: string;
    required_level: number;
    rarity: string;
    visual_type: string;
    visual_data: string;
    is_locked: boolean;
    is_equipped: boolean;
};

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

// Map visual_data to Lucide icons for "icon" type
const ICON_MAP: Record<string, any> = {
    user: User,
    terminal: Terminal,
    code: Code,
    cpu: Cpu,
    shield: Shield,
    zap: Zap,
    circle: Circle
};

export function AvatarSelector({ isOpen, onClose }: Props) {
    const [avatars, setAvatars] = useState<Avatar[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState<string | null>(null);

    useEffect(() => {
        if (!isOpen) return;
        (async () => {
            try {
                setLoading(true);
                setError(null);
                const res = await fetch('/api/avatars');
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data = await res.json();
                setAvatars(data.avatars ?? data);
            } catch (err: any) {
                console.error(err);
                setError('Failed to load avatars');
            } finally {
                setLoading(false);
            }
        })();
    }, [isOpen]);

    const equip = async (id: string) => {
        try {
            setSubmitting(id);
            const res = await fetch('/api/avatars/equip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ avatar_id: id }),
            });
            if (!res.ok) {
                const text = await res.text().catch(() => '');
                throw new Error(text || 'Failed to equip avatar');
            }

            // Optimistic update
            setAvatars((prev) =>
                prev.map((a) => ({ ...a, is_equipped: a.id === id })),
            );

            // Force a reload of the user session to update the header
            // In a real app we'd update the global store, but this works for now
            window.location.reload();

        } catch (err) {
            console.error(err);
            // optionally toast
        } finally {
            setSubmitting(null);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <div className="bg-zinc-950 border border-zinc-800 rounded-xl w-full max-w-4xl p-6 shadow-2xl flex flex-col max-h-[90vh]">
                <div className="flex justify-between items-center mb-6 border-b border-zinc-800 pb-4">
                    <h2 className="font-mono text-lg font-bold text-zinc-100 flex items-center gap-2">
                        <span className="text-2xl">🎭</span> AVATAR CLOSET <span className="text-zinc-600 text-sm font-normal ml-2">// IDENTITY MATRIX</span>
                    </h2>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors p-2 hover:bg-zinc-900 rounded-full">
                        ✕
                    </button>
                </div>

                {loading && (
                    <div className="flex-1 flex items-center justify-center text-zinc-500 font-mono animate-pulse">
                        SCANNING IDENTITY DATABASE...
                    </div>
                )}

                {error && (
                    <div className="p-4 bg-red-950/30 border border-red-900/50 text-red-400 rounded-lg font-mono text-sm">
                        ERROR: {error}
                    </div>
                )}

                {!loading && !error && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 overflow-y-auto pr-2 custom-scrollbar">
                        {avatars.map((avatar) => {
                            const disabled = avatar.is_locked || submitting === avatar.id;
                            const Icon = ICON_MAP[avatar.visual_data] || User;

                            return (
                                <button
                                    key={avatar.id}
                                    disabled={disabled}
                                    onClick={() => equip(avatar.id)}
                                    className={`group relative p-4 rounded-xl border text-left transition-all duration-300 flex flex-col gap-3 ${avatar.is_equipped
                                            ? 'border-emerald-500/50 bg-emerald-950/20 shadow-[0_0_20px_rgba(16,185,129,0.1)]'
                                            : avatar.is_locked
                                                ? 'border-zinc-800 bg-zinc-900/50 opacity-60 cursor-not-allowed grayscale'
                                                : 'border-zinc-800 bg-zinc-900/30 hover:bg-zinc-800 hover:border-cyan-500/30 hover:shadow-[0_0_15px_rgba(6,182,212,0.1)]'
                                        }`}
                                >
                                    <div className="flex justify-between items-start">
                                        {/* Avatar Preview */}
                                        <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-colors ${avatar.is_equipped ? 'border-emerald-500 bg-emerald-950' :
                                                avatar.is_locked ? 'border-zinc-700 bg-zinc-800' : 'border-cyan-500/30 bg-zinc-900 group-hover:border-cyan-400'
                                            }`}>
                                            {avatar.visual_type === 'icon' ? (
                                                <Icon className={`w-6 h-6 ${avatar.is_equipped ? 'text-emerald-400' :
                                                        avatar.is_locked ? 'text-zinc-600' : 'text-cyan-400'
                                                    }`} />
                                            ) : (
                                                <div className={`w-full h-full rounded-full ${avatar.visual_data}`} />
                                            )}
                                        </div>

                                        {/* Status Badge */}
                                        {avatar.is_equipped && (
                                            <span className="px-2 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase tracking-wider">
                                                Active
                                            </span>
                                        )}
                                        {avatar.is_locked && (
                                            <span className="px-2 py-1 rounded-full bg-zinc-800 border border-zinc-700 text-zinc-500 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1">
                                                🔒 Lvl {avatar.required_level}
                                            </span>
                                        )}
                                    </div>

                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className={`font-bold font-mono text-sm ${avatar.is_equipped ? 'text-white' : 'text-zinc-300'}`}>
                                                {avatar.name}
                                            </span>
                                            <span className={`text-[10px] px-1.5 py-0.5 rounded border ${avatar.rarity === 'legendary' ? 'border-amber-500/30 text-amber-400 bg-amber-950/30' :
                                                    avatar.rarity === 'epic' ? 'border-purple-500/30 text-purple-400 bg-purple-950/30' :
                                                        avatar.rarity === 'rare' ? 'border-blue-500/30 text-blue-400 bg-blue-950/30' :
                                                            'border-zinc-700 text-zinc-500 bg-zinc-900'
                                                } uppercase tracking-wider`}>
                                                {avatar.rarity}
                                            </span>
                                        </div>
                                        <p className="text-xs text-zinc-500 leading-relaxed">
                                            {avatar.description}
                                        </p>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
