import React, { useState } from 'react';
import { QuickFix } from '@/lib/questsApi';
import { Lightbulb, Check, Copy, ArrowRight, X } from 'lucide-react';
import { useToast } from '@/lib/toast';

interface QuickFixBarProps {
    fixes: QuickFix[];
    onApplyPatch: (fix: QuickFix) => void;
    onNavigate: (fix: QuickFix) => void;
    readOnly?: boolean;
}

export const QuickFixBar: React.FC<QuickFixBarProps> = ({ fixes, onApplyPatch, onNavigate, readOnly }) => {
    const { addToast } = useToast();
    const [selectedFix, setSelectedFix] = useState<QuickFix | null>(null);

    if (!fixes || fixes.length === 0) return null;

    const handleCopy = (text: string) => {
        navigator.clipboard.writeText(text);
        addToast({ type: 'success', title: 'Copied', message: 'Snippet copied to clipboard' });
        setSelectedFix(null);
    };

    const handleApply = (fix: QuickFix) => {
        if (readOnly) return;
        onApplyPatch(fix);
        addToast({ type: 'success', title: 'Applied', message: fix.title });
        setSelectedFix(null);
    };

    const handleNav = (fix: QuickFix) => {
        onNavigate(fix);
        setSelectedFix(null);
    };

    return (
        <div className="bg-blue-50/50 border-b border-blue-100 p-2 flex flex-col gap-2">
            {/* Chips Row */}
            <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-medium text-blue-600 flex items-center gap-1">
                    <Lightbulb size={12} />
                    Quick Fixes:
                </span>
                {fixes.map((fix) => (
                    <button
                        key={fix.id}
                        onClick={() => setSelectedFix(selectedFix?.id === fix.id ? null : fix)}
                        className={`
                            px-2 py-1 text-xs rounded-full border transition-colors flex items-center gap-1
                            ${selectedFix?.id === fix.id
                                ? 'bg-blue-100 border-blue-300 text-blue-800'
                                : 'bg-white border-blue-200 text-slate-700 hover:bg-blue-50'}
                        `}
                    >
                        {fix.title}
                    </button>
                ))}
            </div>

            {/* Expanded Details Panel */}
            {selectedFix && (
                <div className="bg-white border border-blue-200 rounded p-3 shadow-sm animate-in slide-in-from-top-2">
                    <div className="flex justify-between items-start mb-2">
                        <div>
                            <h4 className="font-semibold text-sm text-slate-800">{selectedFix.title}</h4>
                            <p className="text-xs text-slate-500 mt-0.5">{selectedFix.why}</p>
                        </div>
                        <button
                            onClick={() => setSelectedFix(null)}
                            className="text-slate-400 hover:text-slate-600"
                        >
                            <X size={14} />
                        </button>
                    </div>

                    <div className="flex items-center gap-2 mt-3">
                        {selectedFix.kind === 'apply_patch' && (
                            <button
                                onClick={() => handleApply(selectedFix)}
                                disabled={readOnly}
                                className={`
                                    flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium text-white
                                    ${readOnly ? 'bg-slate-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}
                                `}
                                title={readOnly ? "Exit replay mode to apply fixes" : "Apply this fix"}
                            >
                                <Check size={14} />
                                {readOnly ? 'Apply (Disabled in Replay)' : 'Apply Fix'}
                            </button>
                        )}

                        {selectedFix.kind === 'copy_snippet' && selectedFix.snippet && (
                            <button
                                onClick={() => handleCopy(selectedFix.snippet!)}
                                className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200"
                            >
                                <Copy size={14} />
                                Copy Snippet
                            </button>
                        )}

                        {(selectedFix.kind === 'navigate' || selectedFix.locator) && (
                            <button
                                onClick={() => handleNav(selectedFix)}
                                className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium bg-white text-slate-700 hover:bg-slate-50 border border-slate-200"
                            >
                                <ArrowRight size={14} />
                                Jump to Code
                            </button>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};
