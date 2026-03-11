import React from 'react';
import { cn } from '@/lib/utils';
import { Rocket, CheckSquare, Zap, AlertTriangle, Info, BookOpen, GitMerge, ShieldAlert } from 'lucide-react';

export type BriefingCardVariant = 'mission' | 'requirements' | 'workflow' | 'watch' | 'overview';

interface BriefingCardProps {
    variant: BriefingCardVariant;
    title: string;
    children: React.ReactNode;
    className?: string;
}

const variantConfig = {
    mission: {
        icon: Rocket,
        baseColor: 'cyan',
        bg: 'bg-cyan-950/10',
        border: 'border-cyan-500/20',
        titleColor: 'text-cyan-400',
        accentBg: 'bg-cyan-500/10',
    },
    requirements: {
        icon: CheckSquare,
        baseColor: 'emerald',
        bg: 'bg-emerald-950/10',
        border: 'border-emerald-500/20',
        titleColor: 'text-emerald-400',
        accentBg: 'bg-emerald-500/10',
    },
    workflow: {
        icon: GitMerge,
        baseColor: 'violet',
        bg: 'bg-violet-950/10',
        border: 'border-violet-500/20',
        titleColor: 'text-violet-400',
        accentBg: 'bg-violet-500/10',
    },
    watch: {
        icon: ShieldAlert,
        baseColor: 'amber',
        bg: 'bg-amber-950/10',
        border: 'border-amber-500/20',
        titleColor: 'text-amber-400',
        accentBg: 'bg-amber-500/10',
    },
    overview: {
        icon: BookOpen,
        baseColor: 'zinc',
        bg: 'bg-zinc-900/40',
        border: 'border-zinc-800',
        titleColor: 'text-zinc-50',
        accentBg: 'bg-zinc-800/50',
    },
};

export function BriefingCard({ variant, title, children, className }: BriefingCardProps) {
    const config = variantConfig[variant] || variantConfig.overview;
    const Icon = config.icon;

    return (
        <div className={cn(
            "group relative rounded-xl border p-5 transition-all duration-300",
            "backdrop-blur-sm",
            config.bg,
            config.border,
            "hover:bg-zinc-900/60 hover:border-zinc-700",
            className
        )}>
            {/* Glossy Overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/[0.03] to-transparent pointer-events-none" />
            
            <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">
                    <div className={cn(
                        "p-2 rounded-lg shrink-0",
                        config.accentBg,
                        config.titleColor
                    )}>
                        <Icon className="w-4 h-4" />
                    </div>
                    <h3 className={cn(
                        "text-sm font-bold uppercase tracking-widest",
                        config.titleColor
                    )}>
                        {title}
                    </h3>
                </div>

                <div className="text-sm leading-relaxed text-zinc-300 prose prose-sm prose-invert max-w-none 
                    prose-p:text-zinc-300 prose-headings:text-zinc-100 prose-strong:text-zinc-200 
                    prose-code:text-amber-300 prose-code:bg-zinc-800/60 prose-code:px-1 prose-code:rounded">
                    {children}
                </div>
            </div>
            
            {/* Subtle corner accent */}
            <div className={cn(
                "absolute top-0 right-0 w-16 h-16 bg-gradient-to-bl from-white/[0.02] to-transparent",
                "pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"
            )} />
        </div>
    );
}
