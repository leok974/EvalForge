import React from 'react';
import { cn } from '@/lib/utils';
import { ArrowRight, LayoutGrid, HelpCircle, Columns2, TableIcon } from 'lucide-react';

// ── Schema ──────────────────────────────────────────────────────────────────
export type QuickFixAction =
    | { kind: 'open_tab'; tab: 'query_result' | 'result' | 'results' | 'trace' | 'explain' | 'hints' | 'console'; label?: string }
    | { kind: 'jump_file'; path: string; line?: number; label?: string }
    | { kind: 'reveal_hint'; hintIndex: number; label?: string }   // 0-based
    | { kind: 'compare_columns'; expected: string[]; actual: string[]; label?: string };

export interface QuickFixCard {
    id: string;
    title: string;
    action: QuickFixAction;
}

// ── Generator (client-side, deterministic) ───────────────────────────────────
export function generateQuickFixes(opts: {
    evaluated_objectives: boolean;
    objective_results: Array<{ id: string; ok: boolean; detail?: string; kind?: string }>;
    sql_student_result?: { columns?: string[]; row_count?: number } | null;
    quest_expected_columns?: string[];  // from quest metadata if available
    entrypoint?: string;
}): QuickFixCard[] {
    const { evaluated_objectives, objective_results, sql_student_result, entrypoint = 'task.sql' } = opts;

    // Never show quick fixes for preview / reference runs
    if (!evaluated_objectives) return [];

    const failedObjectives = objective_results.filter(o => !o.ok);
    if (failedObjectives.length === 0) return [];

    const fixes: QuickFixCard[] = [];
    const seen = new Set<string>();

    const add = (fix: QuickFixCard) => {
        if (!seen.has(fix.id)) {
            seen.add(fix.id);
            fixes.push(fix);
        }
    };

    // Always: open Query Result so they see what they got
    add({
        id: 'open_query_result',
        title: 'See your output',
        action: { kind: 'open_tab', tab: 'result' },  // must match activeTerminalTab values
    });

    // Column mismatch: compare expected vs actual
    const colFailObj = failedObjectives.find(o =>
        ['obj_cols', 'obj_shape', 'obj_header_order', 'column_match', 'columns'].some(k => o.id?.includes(k) || o.kind?.includes(k))
    );
    const actualCols = sql_student_result?.columns ?? [];
    const expectedCols = opts.quest_expected_columns ?? [];

    if (colFailObj || (actualCols.length > 0 && expectedCols.length > 0 && JSON.stringify(actualCols) !== JSON.stringify(expectedCols))) {
        if (expectedCols.length > 0 && actualCols.length > 0) {
            add({
                id: 'compare_columns',
                title: 'Compare columns',
                action: { kind: 'compare_columns', expected: expectedCols, actual: actualCols },
            });
        }
        // Jump to the top of task.sql to fix SELECT list
        add({
            id: 'jump_task_sql',
            title: `Edit ${entrypoint}`,
            action: { kind: 'jump_file', path: entrypoint, line: 1 },
        });
        // Hint 1 covers column contract
        add({
            id: 'hint_col_contract',
            title: 'Hint: column contract',
            action: { kind: 'reveal_hint', hintIndex: 0 },
        });
    }

    // Missing ORDER BY
    const orderByFail = failedObjectives.find(o =>
        o.detail?.toLowerCase().includes('order') || o.id?.includes('order') || o.kind?.includes('order') || o.kind?.includes('sort')
    );
    if (orderByFail) {
        add({
            id: 'jump_for_order_by',
            title: `Edit ${entrypoint}`,
            action: { kind: 'jump_file', path: entrypoint, line: 1 },
        });
        // Hint 4 is "ORDER BY is not automatic"
        add({
            id: 'hint_order_by',
            title: 'Hint: ORDER BY',
            action: { kind: 'reveal_hint', hintIndex: 3 },
        });
    }

    // SQL runtime error: open Trace
    const hasRuntimeError = failedObjectives.some(o =>
        o.detail?.toLowerCase().includes('error') || o.kind === 'runtime'
    );
    if (hasRuntimeError) {
        add({
            id: 'open_trace',
            title: 'View SQL Trace',
            action: { kind: 'open_tab', tab: 'trace' },
        });
    }

    // Always offer Hints tab as last resort if not already added
    if (!seen.has('hint_col_contract') && !seen.has('hint_order_by')) {
        add({
            id: 'open_hints',
            title: 'Open Hints',
            action: { kind: 'open_tab', tab: 'hints' },
        });
    }

    return fixes;
}

// ── UI ────────────────────────────────────────────────────────────────────────
interface QuickFixBarProps {
    fixes: QuickFixCard[];
    onAction: (action: QuickFixAction) => void;
    expectedColumns?: string[];
}

function ColDiff({ expected, actual }: { expected: string[]; actual: string[] }) {
    return (
        <div className="flex gap-4 text-xs font-mono mt-1">
            <div>
                <div className="text-zinc-500 mb-1 uppercase tracking-wide text-[9px]">Expected</div>
                {expected.map((c, i) => (
                    <div key={i} className={cn("px-1.5 py-0.5 rounded mb-0.5", actual.includes(c) ? "text-emerald-400" : "text-red-400 bg-red-900/20")}>
                        {c}
                    </div>
                ))}
            </div>
            <div>
                <div className="text-zinc-500 mb-1 uppercase tracking-wide text-[9px]">Your output</div>
                {actual.map((c, i) => (
                    <div key={i} className={cn("px-1.5 py-0.5 rounded mb-0.5", expected.includes(c) ? "text-emerald-400" : "text-amber-400 bg-amber-900/20")}>
                        {c}
                    </div>
                ))}
            </div>
        </div>
    );
}

function actionIcon(action: QuickFixAction) {
    switch (action.kind) {
        case 'open_tab': return action.tab === 'hints' ? <HelpCircle className="w-3 h-3" /> : <TableIcon className="w-3 h-3" />;
        case 'jump_file': return <ArrowRight className="w-3 h-3" />;
        case 'reveal_hint': return <HelpCircle className="w-3 h-3" />;
        case 'compare_columns': return <Columns2 className="w-3 h-3" />;
        default: return <LayoutGrid className="w-3 h-3" />;
    }
}

export function QuickFixBar({ fixes, onAction }: QuickFixBarProps) {
    const [expandedId, setExpandedId] = React.useState<string | null>(null);
    if (!fixes || fixes.length === 0) return null;

    return (
        <div className="border-b border-zinc-800 bg-zinc-950/60 px-3 py-2 flex flex-wrap items-center gap-2 shrink-0">
            <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 mr-1">Quick fixes</span>
            {fixes.map(fix => {
                const isExpanded = expandedId === fix.id;
                const isCompare = fix.action.kind === 'compare_columns';
                return (
                    <div key={fix.id} className="relative">
                        <button
                            onClick={() => {
                                if (isCompare) {
                                    setExpandedId(isExpanded ? null : fix.id);
                                } else {
                                    setExpandedId(null);
                                    onAction(fix.action);
                                }
                            }}
                            className={cn(
                                "flex items-center gap-1.5 px-2 py-1 rounded text-[11px] font-medium border transition-all",
                                "bg-zinc-900 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:border-zinc-600 hover:text-zinc-100"
                            )}
                        >
                            {actionIcon(fix.action)}
                            {fix.title}
                        </button>
                        {isCompare && isExpanded && fix.action.kind === 'compare_columns' && (
                            <div className="absolute top-full left-0 mt-1 z-50 bg-zinc-900 border border-zinc-700 rounded-lg p-3 shadow-xl w-52 animate-in slide-in-from-top-1">
                                <ColDiff expected={fix.action.expected} actual={fix.action.actual} />
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
}
