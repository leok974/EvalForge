import React, { useState, useEffect } from 'react';
import { AvatarDisplay, AvatarDef } from './AvatarDisplay';
import { useAuth } from '../hooks/useAuth';

interface ExtendedAvatar extends AvatarDef {
    is_locked: boolean;
    is_equipped: boolean;
    required_level: number;
    description: string;
}

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export function AvatarSelector({ isOpen, onClose }: Props) {
    const { user, refresh } = useAuth();
    const [avatars, setAvatars] = useState<ExtendedAvatar[]>([]);
    const [loading, setLoading] = useState(false);

    // Load Catalog
    useEffect(() => {
        if (isOpen && user) {
            setLoading(true);
            fetch('/api/avatars')
                .then(r => r.json())
                .then(data => {
                    setAvatars(data);
                    setLoading(false);
                });
        }
    }, [isOpen, user]);

    const handleEquip = async (avatarId: string) => {
        try {
            const res = await fetch('/api/avatars/equip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ avatar_id: avatarId })
            });

            if (res.ok) {
                // Optimistic update
                setAvatars(prev => prev.map(av => ({
                    ...av,
                    is_equipped: av.id === avatarId
                })));
                // Refresh global user state to update header immediately
                refresh();
            }
        } catch (e) {
            console.error("Equip failed", e);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-zinc-950 border border-zinc-800 rounded-xl w-full max-w-4xl h-[80vh] shadow-2xl flex flex-col overflow-hidden">

                {/* Header */}
                <div className="p-6 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                    <div>
                        <h2 className="text-white font-bold text-xl tracking-wide font-mono">IDENTITY MATRIX</h2>
                        <div className="text-zinc-500 text-xs mt-1">Customize your digital appearance</div>
                    </div>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">✕ ESC</button>
                </div>

                {/* Grid */}
                <div className="flex-1 overflow-y-auto p-6 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {loading && <div className="text-zinc-500 col-span-full text-center py-20 animate-pulse">LOADING ASSETS...</div>}

                    {avatars.map(av => (
                        <div
                            key={av.id}
                            onClick={() => !av.is_locked && handleEquip(av.id)}
                            className={`
                relative p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-3 group
                ${av.is_equipped
                                    ? 'bg-zinc-900 border-cyan-500 shadow-[0_0_20px_rgba(34,211,238,0.1)]'
                                    : av.is_locked
                                        ? 'bg-black border-zinc-800 opacity-50 cursor-not-allowed grayscale'
                                        : 'bg-black border-zinc-800 hover:border-zinc-600 cursor-pointer hover:bg-zinc-900'
                                }
              `}
                        >
                            <AvatarDisplay avatar={av} size="lg" />

                            <div className="text-center">
                                <div className={`font-bold text-sm ${av.is_equipped ? 'text-cyan-400' : 'text-zinc-300'}`}>
                                    {av.name}
                                </div>
                                <div className="text-[10px] text-zinc-500 mt-1 line-clamp-1">{av.description}</div>
                            </div>

                            {/* Status Badge */}
                            <div className="mt-auto pt-2">
                                {av.is_equipped ? (
                                    <span className="text-[10px] font-bold text-cyan-500 bg-cyan-950/50 px-2 py-1 rounded border border-cyan-900">
                                        EQUIPPED
                                    </span>
                                ) : av.is_locked ? (
                                    <span className="text-[10px] font-bold text-red-500 bg-red-950/30 px-2 py-1 rounded border border-red-900 flex items-center gap-1 justify-center">
                                        🔒 LVL {av.required_level}
                                    </span>
                                ) : (
                                    <span className="text-[10px] font-bold text-zinc-500 group-hover:text-white transition-colors">
                                        SELECT
                                    </span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
