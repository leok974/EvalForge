import React from 'react';
import { Diagnostic } from '@/lib/questsApi';
import { AlertTriangle, XCircle, MousePointerClick } from 'lucide-react';

interface ProblemsPanelProps {
    diagnostics: Diagnostic[];
    onDiagnosticClick: (path: string, line: number) => void;
}

export function ProblemsPanel({ diagnostics, onDiagnosticClick }: ProblemsPanelProps) {
    if (!diagnostics || diagnostics.length === 0) return null;

    return (
        <div className="border-t border-zinc-800 bg-[#09090b] flex flex-col shrink-0 font-mono h-32">
            <div className="px-3 py-1.5 border-b border-zinc-800/50 flex justify-between items-center bg-black/20">
                <span className="text-[10px] font-bold uppercase tracking-widest text-amber-500 flex items-center gap-2">
                    <AlertTriangle className="w-3 h-3" /> Problems ({diagnostics.length})
                </span>
            </div>
            <div className="flex-1 overflow-auto p-0">
                {diagnostics.map((d, i) => (
                    <button
                        key={i}
                        onClick={() => onDiagnosticClick(d.path, d.line)}
                        className="w-full text-left px-3 py-1.5 border-b border-zinc-800/30 hover:bg-zinc-800/50 transition-colors flex items-start gap-2 group"
                    >
                        {d.severity === 'error' ? (
                            <XCircle className="w-3 h-3 text-red-500 mt-0.5 shrink-0" />
                        ) : (
                            <AlertTriangle className="w-3 h-3 text-amber-500 mt-0.5 shrink-0" />
                        )}
                        <span className="text-zinc-500 text-xs shrink-0">{d.path}:{d.line}</span>
                        <span className="text-zinc-300 text-xs truncate group-hover:text-zinc-100">{d.message}</span>
                    </button>
                ))}
            </div>
        </div>
    );
}
