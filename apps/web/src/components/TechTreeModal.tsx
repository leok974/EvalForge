import React, { useState } from 'react';
import { useSkills, SkillNode } from '../hooks/useSkills';
import { useAuth } from '../hooks/useAuth';

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export function TechTreeModal({ isOpen, onClose }: Props) {
    const { user } = useAuth();
    const { skills, skillPoints, unlockSkill } = useSkills(user);
    const [purchasing, setPurchasing] = useState<string | null>(null);

    if (!isOpen) return null;

    const handleUnlock = async (skill: SkillNode) => {
        if (!skill.can_unlock || skill.is_unlocked) return;

        setPurchasing(skill.id);
        await unlockSkill(skill.id);
        setPurchasing(null);
    };

    // Group by Tier for layout
    const tiers = [1, 2, 3];

    return (
        <div className="fixed inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-4">
            <div className="w-full max-w-5xl h-[85vh] bg-nano-900 border border-zinc-800 rounded-xl shadow-2xl flex flex-col overflow-hidden relative">

                {/* Background Circuit Effect */}
                <div className="absolute inset-0 opacity-10 pointer-events-none"
                    style={{ backgroundImage: 'radial-gradient(#FACC15 1px, transparent 1px)', backgroundSize: '40px 40px' }}
                />

                {/* Header */}
                <div className="p-6 border-b border-zinc-800 flex justify-between items-center bg-black/40 z-10">
                    <div>
                        <h2 className="text-2xl font-bold text-white font-mono tracking-widest flex items-center gap-3">
                            <span className="text-banana-400 text-3xl">🧬</span> CYBERNETICS LAB
                        </h2>
                        <div className="text-zinc-500 text-xs mt-1">Augment your development capabilities.</div>
                    </div>
                    <div className="flex items-center gap-6">
                        <div className="text-right">
                            <div className="text-[10px] text-zinc-500 uppercase tracking-widest">Available SP</div>
                            <div className="text-2xl font-bold text-banana-400 font-mono">{skillPoints}</div>
                        </div>
                        <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors text-xl">✕</button>
                    </div>
                </div>

                {/* The Tree */}
                <div className="flex-1 overflow-y-auto p-8 relative z-10">
                    <div className="flex flex-col gap-12">

                        {tiers.map(tier => (
                            <div key={tier} className="relative">
                                {/* Tier Label */}
                                <div className="absolute -left-4 -top-6 text-[10px] font-bold text-zinc-700 uppercase tracking-widest">
                                    Tier 0{tier} Clearance
                                </div>

                                {/* Connector Line (Vertical) */}
                                {tier < 3 && (
                                    <div className="absolute left-1/2 -bottom-12 w-px h-12 bg-zinc-800 -translate-x-1/2" />
                                )}

                                <div className="flex justify-center gap-8 flex-wrap">
                                    {skills.filter(s => s.tier === tier).map(skill => (
                                        <SkillCard
                                            key={skill.id}
                                            skill={skill}
                                            onUnlock={() => handleUnlock(skill)}
                                            isPurchasing={purchasing === skill.id}
                                        />
                                    ))}
                                </div>
                            </div>
                        ))}

                    </div>
                </div>
            </div>
        </div>
    );
}

function SkillCard({ skill, onUnlock, isPurchasing }: { skill: SkillNode, onUnlock: () => void, isPurchasing: boolean }) {
    // Visual State Logic
    let statusClass = "border-zinc-800 bg-zinc-900/50 opacity-60 grayscale"; // Locked
    let btnText = `LOCKED (${skill.cost} SP)`;
    let btnClass = "bg-zinc-800 text-zinc-600 cursor-not-allowed";

    if (skill.is_unlocked) {
        statusClass = "border-cyan-500/50 bg-cyan-950/20 shadow-[0_0_15px_rgba(34,211,238,0.1)]"; // Owned
        btnText = "INSTALLED";
        btnClass = "bg-cyan-900/50 text-cyan-400 border border-cyan-800";
    } else if (skill.can_unlock) {
        statusClass = "border-banana-500 bg-banana-900/10 shadow-[0_0_20px_rgba(250,204,21,0.1)] animate-pulse-slow"; // Buyable
        btnText = isPurchasing ? "INSTALLING..." : `UNLOCK (-${skill.cost} SP)`;
        btnClass = "bg-banana-500 hover:bg-banana-400 text-black font-bold shadow-lg shadow-banana-500/20";
    }

    return (
        <div className={`w-64 p-4 rounded-xl border-2 flex flex-col gap-3 transition-all duration-300 ${statusClass}`}>
            <div className="flex justify-between items-start">
                <div className="text-xs font-bold text-zinc-500 uppercase tracking-wider">{skill.category}</div>
                {skill.is_unlocked && <div className="text-cyan-400 text-xs">●</div>}
            </div>

            <div>
                <div className={`font-bold text-lg font-mono ${skill.is_unlocked ? 'text-white' : 'text-zinc-400'}`}>
                    {skill.name}
                </div>
                <div className="text-xs text-zinc-500 leading-relaxed mt-1 h-10">
                    {skill.description}
                </div>
            </div>

            <button
                onClick={onUnlock}
                disabled={!skill.can_unlock || skill.is_unlocked || isPurchasing}
                className={`w-full py-2 rounded text-xs tracking-wider transition-all ${btnClass}`}
            >
                {btnText}
            </button>
        </div>
    );
}
