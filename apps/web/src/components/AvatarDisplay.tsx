import React from 'react';
// Lucide icons map
import { User, Terminal, Code, Cpu, Ghost, ShieldAlert } from 'lucide-react';

export type AvatarVisualType = 'icon' | 'image' | 'css';

export interface AvatarDef {
    id: string;
    name: string;
    visual_type: AvatarVisualType;
    visual_data: string;
    rarity?: string;
}

const SIZE_CLASSES = {
    sm: "w-6 h-6 text-xs",
    md: "w-10 h-10 text-base",
    lg: "w-16 h-16 text-2xl",
    xl: "w-24 h-24 text-4xl"
};

interface Props {
    avatar: AvatarDef;
    size?: keyof typeof SIZE_CLASSES;
    className?: string;
}

export function AvatarDisplay({ avatar, size = "md", className = "" }: Props) {
    const containerClass = `rounded-full flex items-center justify-center shrink-0 overflow-hidden transition-all ${SIZE_CLASSES[size]} ${className}`;

    // --- 1. CSS GENERATIVE AVATARS ---
    if (avatar.visual_type === 'css') {
        if (avatar.visual_data === 'neon-pulse') {
            return (
                <div className={`${containerClass} bg-cyan-950 border-2 border-cyan-400 relative shadow-[0_0_15px_rgba(34,211,238,0.5)]`}>
                    <div className="absolute inset-0 bg-cyan-400/20 animate-pulse" />
                    <Ghost className="relative z-10 text-cyan-100 w-[60%] h-[60%]" />
                </div>
            );
        }
        if (avatar.visual_data === 'glitch') {
            return (
                <div className={`${containerClass} bg-red-950 border-2 border-red-500 relative`}>
                    <div className="absolute inset-0 bg-red-500/10 animate-pulse" />
                    <ShieldAlert className="relative z-10 text-red-500 w-[60%] h-[60%] animate-bounce" />
                    {/* Glitch Overlay */}
                    <div className="absolute top-0 left-0 w-full h-1 bg-red-500/50 animate-ping" style={{ animationDuration: '0.2s' }} />
                </div>
            );
        }
    }

    // --- 2. IMAGE AVATARS ---
    if (avatar.visual_type === 'image') {
        return (
            <div className={`${containerClass} bg-zinc-900 border border-zinc-700`}>
                <img src={avatar.visual_data} alt={avatar.name} className="w-full h-full object-cover" />
            </div>
        );
    }

    // --- 3. ICON AVATARS (Default) ---
    const IconMap: Record<string, any> = {
        user: User,
        terminal: Terminal,
        code: Code,
        cpu: Cpu,
    };
    const IconComponent = IconMap[avatar.visual_data] || User;

    // Rarity Colors
    const rarityColors: Record<string, string> = {
        common: "bg-zinc-800 text-zinc-400 border-zinc-700",
        rare: "bg-emerald-950 text-emerald-400 border-emerald-800",
        epic: "bg-purple-950 text-purple-400 border-purple-800",
        legendary: "bg-amber-950 text-amber-400 border-amber-600 shadow-lg shadow-amber-900/20"
    };

    const styleClass = rarityColors[avatar.rarity || 'common'] || rarityColors['common'];

    return (
        <div className={`${containerClass} border ${styleClass}`}>
            <IconComponent className="w-[60%] h-[60%]" />
        </div>
    );
}
