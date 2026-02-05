import React from 'react';
import { AlertTriangle, Info, Lightbulb, FileText, AlertOctagon } from 'lucide-react';
import { cn } from '@/lib/utils';

export type CalloutVariant = 'note' | 'tip' | 'important' | 'warning' | 'caution' | 'info';

interface CalloutProps {
    variant: CalloutVariant;
    title?: string;
    children: React.ReactNode;
    className?: string;
}

const styles: Record<string, { icon: any; color: string; border: string; bg: string }> = {
    note: { icon: Info, color: 'text-blue-500', border: 'border-blue-500/50', bg: 'bg-blue-500/10' },
    info: { icon: Info, color: 'text-blue-500', border: 'border-blue-500/50', bg: 'bg-blue-500/10' }, // Alias for note
    tip: { icon: Lightbulb, color: 'text-emerald-500', border: 'border-emerald-500/50', bg: 'bg-emerald-500/10' },
    important: { icon: FileText, color: 'text-violet-500', border: 'border-violet-500/50', bg: 'bg-violet-500/10' },
    warning: { icon: AlertTriangle, color: 'text-amber-500', border: 'border-amber-500/50', bg: 'bg-amber-500/10' },
    caution: { icon: AlertOctagon, color: 'text-red-500', border: 'border-red-500/50', bg: 'bg-red-500/10' },
};

export function Callout({ variant, title, children, className }: CalloutProps) {
    const style = styles[variant.toLowerCase()] || styles.note;
    const Icon = style.icon;

    return (
        <div className={cn(`my-4 rounded-lg border-l-4 p-4 ${style.border} ${style.bg}`, className)}>
            <div className="flex items-start gap-3">
                <Icon className={`w-5 h-5 shrink-0 mt-0.5 ${style.color}`} />
                <div className="min-w-0 flex-1 space-y-2">
                    {title && <div className={`font-semibold ${style.color}`}>{title}</div>}
                    <div className="text-sm text-foreground/90 leading-relaxed">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
}
