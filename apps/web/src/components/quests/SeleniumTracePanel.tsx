import React from 'react';

interface SeleniumStep {
    step: number;
    action: string;
    label: string;
    selector?: string;
    url?: string;
    status: 'started' | 'passed' | 'failed';
    error?: string;
}

interface SeleniumTracePanelProps {
    steps: SeleniumStep[];
}

const ACTION_ICONS: Record<string, string> = {
    navigate: '🌐',
    find: '🔍',
    click: '🖱️',
    type: '⌨️',
    wait: '⏳',
    assert: '✔️',
};

const STATUS_COLORS: Record<string, string> = {
    passed: 'text-emerald-400',
    failed: 'text-red-400',
    started: 'text-amber-400',
};

const STATUS_ICONS: Record<string, string> = {
    passed: '✅',
    failed: '❌',
    started: '⏳',
};

export function SeleniumTracePanel({ steps }: SeleniumTracePanelProps) {
    if (!steps || steps.length === 0) return null;

    return (
        <div className="mt-3 border border-zinc-700/50 rounded-lg overflow-hidden">
            {/* Header */}
            <div className="flex items-center gap-2 px-3 py-2 bg-zinc-800/80 border-b border-zinc-700/50">
                <span className="text-xs font-semibold text-cyan-400 font-mono tracking-wider">▶ Automation Trace</span>
                <span className="ml-auto text-[10px] text-zinc-500 font-mono">{steps.length} step{steps.length !== 1 ? 's' : ''}</span>
            </div>

            {/* Steps */}
            <div className="divide-y divide-zinc-800">
                {steps.map((step) => (
                    <div
                        key={step.step}
                        className={`flex items-start gap-3 px-3 py-2 text-xs font-mono ${
                            step.status === 'failed' ? 'bg-red-950/20' : 'bg-zinc-900/50'
                        }`}
                    >
                        {/* Step number */}
                        <span className="text-zinc-600 w-4 text-right shrink-0 mt-0.5">{step.step}</span>

                        {/* Status icon */}
                        <span className="shrink-0 mt-0.5">{STATUS_ICONS[step.status] || '⏳'}</span>

                        {/* Action icon + label */}
                        <div className="flex-1 min-w-0">
                            <span className={`${STATUS_COLORS[step.status] || 'text-zinc-300'}`}>
                                {ACTION_ICONS[step.action] || '⚙️'} {step.label}
                            </span>

                            {/* Selector if present */}
                            {step.selector && (
                                <div className="mt-0.5 text-zinc-500 truncate">
                                    selector: <span className="text-violet-400">{step.selector}</span>
                                </div>
                            )}

                            {/* Failure details */}
                            {step.status === 'failed' && step.error && (
                                <div className="mt-1 text-red-400/80 break-words">
                                    ↳ {step.error}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
