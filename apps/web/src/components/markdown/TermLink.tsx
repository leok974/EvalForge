import React, { useState } from 'react';
import { cn } from '@/lib/utils';
import { KeyTerm } from '@/components/quests/TutorialPanel';

interface TermLinkProps {
    term: string;
    codexRef?: string;
    children: React.ReactNode;
    onOpenCodex: (ref: string) => void;
    className?: string;
    // We strictly might not have the full term object here, but we can try to look it up 
    // or pass minimal info. The plugin passes term and codexRef.
    // Ideally, we'd look up the definition from a context, but for now we rely on 
    // what's passed or just show a generic "Open Codex" tooltip.
}

export function TermLink({ term, codexRef, children, onOpenCodex, className }: TermLinkProps) {
    const [showTooltip, setShowTooltip] = useState(false);

    return (
        <span
            className={cn(
                "relative inline-block cursor-pointer",
                "text-blue-600 dark:text-blue-400 font-medium hover:underline decoration-blue-300 underline-offset-2",
                className
            )}
            onClick={(e) => {
                e.stopPropagation();
                if (codexRef) onOpenCodex(codexRef);
            }}
            onMouseEnter={() => setShowTooltip(true)}
            onMouseLeave={() => setShowTooltip(false)}
        >
            {children}

            {showTooltip && (
                <span className="absolute z-50 bottom-full left-1/2 transform -translate-x-1/2 mb-2 
        px-3 py-2 bg-gray-900 text-white text-xs rounded shadow-lg whitespace-nowrap pointer-events-none">
                    Click to open Codex
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
                </span>
            )}
        </span>
    );
}
