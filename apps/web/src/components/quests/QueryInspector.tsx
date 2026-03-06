import React, { useState, useMemo, useEffect } from 'react';
import { useQuestStore } from '@/store/questStore';
import { Database, Clock, TerminalSquare, AlertCircle, Info, Table2, Layers, ChevronRight, ChevronDown, Copy, Search, Download } from 'lucide-react';

function TraceRow({ entry, index, defaultExpanded = false, forceExpanded = false }: { entry: any, index: number, defaultExpanded?: boolean, forceExpanded?: boolean }) {
    const [expanded, setExpanded] = useState(defaultExpanded);
    const [sqlView, setSqlView] = useState<'raw' | 'stripped'>('raw');

    // Auto-expand if forced (e.g. error)
    useEffect(() => {
        if (forceExpanded) setExpanded(true);
    }, [forceExpanded]);

    const hasError = !!entry.error;
    const isSetup = entry.phase === 'setup';
    const firstLine = entry.sql.split('\n')[0].substring(0, 100) + (entry.sql.length > 100 ? '...' : '');

    const handleCopy = (e: React.MouseEvent, text: string) => {
        e.stopPropagation();
        navigator.clipboard.writeText(text);
    };

    return (
        <div className={`flex flex-col text-xs rounded border transition-colors ${hasError ? 'border-red-900/50 bg-red-950/10' : 'border-zinc-800/50 bg-black/20 hover:bg-black/40'}`}>
            {/* Row Header */}
            <div
                className="flex items-center justify-between p-2 cursor-pointer select-none"
                onClick={() => setExpanded(!expanded)}
            >
                <div className="flex items-center gap-2 overflow-hidden flex-1">
                    {expanded ? <ChevronDown className="w-3 h-3 text-zinc-500 shrink-0" /> : <ChevronRight className="w-3 h-3 text-zinc-500 shrink-0" />}

                    <span className={`px-1.5 py-0.5 rounded text-[9px] uppercase font-bold tracking-wider shrink-0
                        ${isSetup ? 'bg-zinc-800 text-zinc-400' : hasError ? 'bg-red-900/40 text-red-400 border border-red-800/50' : 'bg-cyan-900/40 text-cyan-400 border border-cyan-800/50'}
                    `}>
                        {entry.phase}
                    </span>

                    <span className="text-zinc-500 text-[10px] shrink-0"><Clock className="w-3 h-3 inline mr-1" />{entry.elapsed_ms}ms</span>

                    <span className="text-zinc-400 font-mono truncate hidden md:inline-block">
                        {firstLine}
                    </span>

                    {entry.row_count !== null && !hasError && (
                        <span className="text-zinc-500 text-[10px] shrink-0 ml-auto">~ {entry.row_count} rows</span>
                    )}
                </div>
                {hasError && <AlertCircle className="w-4 h-4 text-red-500 shrink-0 ml-2" />}
            </div>

            {/* Expanded Body */}
            {expanded && (
                <div className="p-2 border-t border-zinc-800/50 bg-black/40 flex flex-col gap-2">
                    {hasError && (
                        <div className="flex items-start gap-2 p-2 bg-red-950/40 text-red-400 border border-red-900/50 rounded mb-2 font-mono text-[10px]">
                            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <div className="flex-1 whitespace-pre-wrap">{entry.error}</div>
                        </div>
                    )}

                    <div className="relative group">
                        {entry.sql_stripped && entry.sql_stripped !== entry.sql && (
                            <div className="flex gap-1 mb-1 relative z-10">
                                <button
                                    onClick={(e) => { e.stopPropagation(); setSqlView('raw'); }}
                                    className={`text-[9px] uppercase font-bold px-2 py-0.5 rounded ${sqlView === 'raw' ? 'bg-zinc-700 text-white' : 'text-zinc-500 hover:text-zinc-300'}`}
                                >Raw SQL</button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); setSqlView('stripped'); }}
                                    className={`text-[9px] uppercase font-bold px-2 py-0.5 rounded ${sqlView === 'stripped' ? 'bg-zinc-700 text-white' : 'text-zinc-500 hover:text-zinc-300'}`}
                                >Checked SQL</button>
                            </div>
                        )}
                        <pre className="p-2 bg-zinc-950 border border-zinc-800/80 rounded text-zinc-300 font-mono overflow-x-auto whitespace-pre-wrap word-break-all text-[11px]">
                            {sqlView === 'raw' ? entry.sql : (entry.sql_stripped || entry.sql)}
                        </pre>
                        <button
                            onClick={(e) => handleCopy(e, sqlView === 'raw' ? entry.sql : (entry.sql_stripped || entry.sql))}
                            className="absolute top-2 right-2 p-1.5 bg-zinc-800 hover:bg-zinc-700 rounded text-zinc-400 opacity-0 group-hover:opacity-100 transition-opacity"
                            title="Copy SQL"
                        >
                            <Copy className="w-3 h-3" />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export interface QueryInspectorProps {
    activeTabOverride?: 'trace' | 'result' | 'explain';
}

export function QueryInspector({ activeTabOverride }: QueryInspectorProps) {
    const lastRunResult = useQuestStore((s) => s.lastRunResult);
    const [internalTab, setInternalTab] = useState<'trace' | 'result' | 'explain'>('trace');
    const activeTab = activeTabOverride || internalTab;
    const [searchQuery, setSearchQuery] = useState('');
    const [isSetupCollapsed, setIsSetupCollapsed] = useState(true);

    const { artifacts } = (lastRunResult as any) || {};
    const trace = artifacts?.sql_trace || [];
    const studentResult = artifacts?.sql_student_result;
    const explain = artifacts?.sql_explain;

    const filteredTrace = useMemo(() => {
        if (!searchQuery) return trace;
        const q = searchQuery.toLowerCase();
        return trace.filter((t: any) => t.sql.toLowerCase().includes(q) || (t.error && t.error.toLowerCase().includes(q)));
    }, [trace, searchQuery]);

    const setupCount = filteredTrace.filter((t: any) => t.phase === 'setup').length;
    const nonSetupTrace = filteredTrace.filter((t: any) => t.phase !== 'setup');
    const setupTrace = filteredTrace.filter((t: any) => t.phase === 'setup');

    if (!lastRunResult || !(lastRunResult as any).artifacts) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center p-4 text-center text-zinc-500 h-full bg-[#09090b]">
                <Database className="w-8 h-8 mb-2 opacity-50" />
                <div className="font-bold uppercase tracking-wider text-[10px]">Query Inspector</div>
                <div className="text-xs opacity-70">Run a SQL task to capture execution traces.</div>
            </div>
        );
    }

    const handleCopyCsv = () => {
        if (!studentResult || !studentResult.columns || !studentResult.rows) return;
        const header = studentResult.columns.join(',');
        const rows = studentResult.rows.map((r: any[]) => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(','));
        navigator.clipboard.writeText([header, ...rows].join('\n'));
    };

    const handleCopyJson = () => {
        if (!studentResult || !studentResult.columns || !studentResult.rows) return;
        const data = studentResult.rows.map((r: any[]) => {
            const rowObj: any = {};
            studentResult.columns.forEach((c: string, i: number) => {
                rowObj[c] = r[i];
            });
            return rowObj;
        });
        navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    };

    return (
        <div className="flex-1 flex flex-col h-full bg-[#09090b] font-mono min-w-0">
            {/* Header / Tabs (Only show if not overridden by parent) */}
            {!activeTabOverride && (
                <div className="flex items-center justify-between border-b border-zinc-800/50 bg-black/20 shrink-0 relative z-20">
                    <div className="flex items-center overflow-x-auto hide-scrollbar">
                        <button
                            onClick={() => setInternalTab('trace')}
                            className={`px-4 py-2 text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                ${internalTab === 'trace' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                        >
                            <TerminalSquare className="w-3 h-3" /> Trace ({trace.length})
                        </button>
                        <button
                            onClick={() => setInternalTab('result')}
                            className={`px-4 py-2 text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                ${internalTab === 'result' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                        >
                            <Table2 className="w-3 h-3" /> Result
                        </button>
                        <button
                            onClick={() => setInternalTab('explain')}
                            className={`px-4 py-2 text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                ${internalTab === 'explain' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                        >
                            <Layers className="w-3 h-3" /> Explain
                        </button>
                    </div>

                    {/* Search / Actions area based on tab */}
                    <div className="pr-3 flex items-center gap-2">
                        {internalTab === 'trace' && (
                            <div className="relative flex items-center">
                                <Search className="w-3 h-3 absolute left-2 text-zinc-500" />
                                <input
                                    type="text"
                                    placeholder="Filter SQL..."
                                    value={searchQuery}
                                    onChange={e => setSearchQuery(e.target.value)}
                                    className="bg-zinc-900 border border-zinc-800 rounded text-[10px] pl-6 pr-2 py-1 text-zinc-300 focus:outline-none focus:border-zinc-700 w-32 transition-colors"
                                />
                            </div>
                        )}
                        {internalTab === 'result' && studentResult?.rows?.length > 0 && (
                            <div className="flex gap-1">
                                <button onClick={handleCopyCsv} className="text-zinc-500 hover:text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded px-2 py-1 flex items-center gap-1 text-[10px] uppercase font-bold" title="Copy CSV"><Download className="w-3 h-3" /> CSV</button>
                                <button onClick={handleCopyJson} className="text-zinc-500 hover:text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded px-2 py-1 flex items-center gap-1 text-[10px] uppercase font-bold" title="Copy JSON"><Copy className="w-3 h-3" /> JSON</button>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Actions area when tabs are hidden (moved to top of content) */}
            {activeTabOverride && (
                <div className="flex justify-end p-2 bg-black/10 border-b border-zinc-800/50 shrink-0">
                    <div className="flex items-center gap-2">
                        {activeTab === 'trace' && (
                            <div className="relative flex items-center">
                                <Search className="w-3 h-3 absolute left-2 text-zinc-500" />
                                <input
                                    type="text"
                                    placeholder="Filter SQL..."
                                    value={searchQuery}
                                    onChange={e => setSearchQuery(e.target.value)}
                                    className="bg-zinc-900 border border-zinc-800 rounded text-[10px] pl-6 pr-2 py-1 text-zinc-300 focus:outline-none focus:border-zinc-700 w-32 transition-colors"
                                />
                            </div>
                        )}
                        {activeTab === 'result' && studentResult?.rows?.length > 0 && (
                            <div className="flex gap-1">
                                <button onClick={handleCopyCsv} className="text-zinc-500 hover:text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded px-2 py-1 flex items-center gap-1 text-[10px] uppercase font-bold" title="Copy CSV"><Download className="w-3 h-3" /> CSV</button>
                                <button onClick={handleCopyJson} className="text-zinc-500 hover:text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded px-2 py-1 flex items-center gap-1 text-[10px] uppercase font-bold" title="Copy JSON"><Copy className="w-3 h-3" /> JSON</button>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Content Body */}
            <div className="flex-1 overflow-auto p-3 relative min-h-0 bg-[#09090b]">
                {activeTab === 'trace' && (
                    <div className="space-y-2 h-full">
                        {filteredTrace.length === 0 ? (
                            <div className="text-center text-zinc-500 italic mt-8 text-xs">No matching trace entries.</div>
                        ) : (
                            <div className="flex flex-col gap-2 pb-4">
                                {/* Group Setup rows */}
                                {setupCount > 0 && (
                                    <div className="flex flex-col border border-zinc-800/50 rounded overflow-hidden">
                                        <div
                                            className="bg-black/40 hover:bg-zinc-900/60 p-2 flex items-center justify-between cursor-pointer select-none text-xs text-zinc-400"
                                            onClick={() => setIsSetupCollapsed(!isSetupCollapsed)}
                                        >
                                            <div className="flex items-center gap-2 font-bold tracking-wider uppercase text-[10px]">
                                                {isSetupCollapsed ? <ChevronRight className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                                                Setup Phase ({setupCount} queries)
                                            </div>
                                        </div>
                                        {!isSetupCollapsed && (
                                            <div className="p-2 gap-2 flex flex-col bg-black/20 border-t border-zinc-800/50">
                                                {setupTrace.map((entry: any, i: number) => (
                                                    <TraceRow key={`setup-${i}`} entry={entry} index={i} forceExpanded={!!entry.error} />
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Remainder (Student & Assert) */}
                                {nonSetupTrace.map((entry: any, i: number) => (
                                    <TraceRow
                                        key={`main-${i}`}
                                        entry={entry}
                                        index={i}
                                        defaultExpanded={true}
                                        forceExpanded={!!entry.error}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'result' && (
                    <div className="space-y-3 h-full flex flex-col animate-in fade-in slide-in-from-left-1 min-h-0">
                        {lastRunResult && !studentResult && (lastRunResult as any).exit_code !== 0 ? (
                            <div className="flex flex-col items-center justify-center p-8 border border-zinc-800 rounded bg-black/40 text-center gap-3">
                                <AlertCircle className="w-8 h-8 text-zinc-600" />
                                <div className="text-zinc-400 text-sm">No student result produced.</div>
                                <div className="text-zinc-500 text-xs max-w-sm">The execution failed before a query result could be fetched. Check the Trace tab for SQL syntax/runtime errors.</div>
                            </div>
                        ) : !studentResult ? (
                            <div className="text-zinc-500 text-xs italic">No SELECT output found in student task.</div>
                        ) : (
                            <>
                                {studentResult.note && (
                                    <div className="flex gap-2 items-center text-[10px] text-cyan-400/80 bg-cyan-950/20 p-2 border border-cyan-900/30 rounded shrink-0 leading-relaxed">
                                        <Info className="w-3 h-3" /> {studentResult.note}
                                        {studentResult.rows?.length === 25 && " (Preview truncated to 25 rows)"}
                                    </div>
                                )}
                                <div className="flex-1 overflow-auto rounded border border-zinc-800 bg-black/20" style={{ minHeight: 0 }}>
                                    <table className="w-full text-left border-collapse text-xs">
                                        <thead className="bg-zinc-900 border-b border-zinc-800 sticky top-0 z-10">
                                            <tr>
                                                <th className="px-3 py-2 border-r border-zinc-800 text-zinc-500 font-bold uppercase tracking-wider whitespace-nowrap w-8">#</th>
                                                {studentResult.columns?.map((c: string, i: number) => (
                                                    <th key={i} className="px-3 py-2 text-zinc-300 font-bold uppercase tracking-wider whitespace-nowrap border-r border-zinc-800/50 last:border-r-0">
                                                        {c}
                                                    </th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {studentResult.rows?.length === 0 ? (
                                                <tr>
                                                    <td colSpan={(studentResult.columns?.length || 0) + 1} className="px-3 py-4 text-center text-zinc-500 italic">
                                                        (No rows returned)
                                                    </td>
                                                </tr>
                                            ) : (
                                                studentResult.rows?.map((row: any[], ri: number) => (
                                                    <tr key={ri} className="hover:bg-zinc-800/50 transition-colors border-b border-zinc-800/30 last:border-b-0">
                                                        <td className="px-3 py-1.5 border-r border-zinc-800/30 text-zinc-600 font-mono text-[10px]">
                                                            {ri + 1}
                                                        </td>
                                                        {row.map((cell: any, ci: number) => (
                                                            <td key={ci} className="px-3 py-1.5 border-r border-zinc-800/30 last:border-r-0 text-zinc-300 whitespace-nowrap overflow-hidden text-ellipsis max-w-[200px]" title={String(cell)}>
                                                                {cell === null ? (
                                                                    <span className="text-zinc-600 italic font-mono text-[10px]">NULL</span>
                                                                ) : (
                                                                    String(cell)
                                                                )}
                                                            </td>
                                                        ))}
                                                    </tr>
                                                ))
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </>
                        )}
                    </div>
                )}

                {activeTab === 'explain' && (
                    <div className="space-y-3 h-full animate-in fade-in slide-in-from-left-1 min-h-0">
                        {!explain ? (
                            <div className="text-zinc-500 text-xs italic">No EXPLAIN PLAN available. Only SELECT queries are planned, or the query failed.</div>
                        ) : (
                            <div className="flex flex-col h-full gap-3">
                                <div className="shrink-0 p-3 bg-black/40 rounded border border-zinc-800/50 relative group">
                                    <div className="text-[10px] font-bold text-zinc-500 mb-2 uppercase tracking-wider flex justify-between">
                                        <span>Statement Analyzed ({explain.engine})</span>
                                    </div>
                                    <pre className="text-xs text-zinc-300 font-mono whitespace-pre-wrap">{explain.statement}</pre>
                                    <button
                                        onClick={() => navigator.clipboard.writeText(explain.statement)}
                                        className="absolute top-2 right-2 p-1 bg-zinc-800 hover:bg-zinc-700 rounded text-zinc-400 opacity-0 group-hover:opacity-100 transition-opacity"
                                        title="Copy Statement"
                                    >
                                        <Copy className="w-3 h-3" />
                                    </button>
                                </div>
                                <div className="flex-1 overflow-auto rounded border border-zinc-800 min-h-0 bg-black/20 flex flex-col relative group">
                                    <div className="px-3 py-2 bg-zinc-900 border-b border-zinc-800 sticky top-0 z-10 flex justify-between items-center shrink-0">
                                        <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Execution Tree</span>
                                        <button
                                            onClick={() => navigator.clipboard.writeText((explain.plan_rows || []).join('\n'))}
                                            className="flex items-center gap-1 text-[10px] uppercase font-bold text-zinc-500 hover:text-zinc-300 transition-opacity"
                                            title="Copy Plan"
                                        >
                                            <Copy className="w-3 h-3" /> Copy
                                        </button>
                                    </div>
                                    <div className="p-3 space-y-1 overflow-auto">
                                        {explain.plan_rows?.length === 0 && (
                                            <div className="text-zinc-500 italic px-2 text-xs">No plan output.</div>
                                        )}
                                        {explain.plan_rows?.map((row: string, i: number) => {
                                            // Collapse repeated SQLite SCAN prefixes visually
                                            let displayRow = row;
                                            const indent = (row.match(/^\s*/)?.[0]?.length || 0) * 8;

                                            // Slight prettification for SQLite EXPLAIN QUERY PLAN
                                            if (displayRow.includes('SCAN TABLE')) {
                                                displayRow = displayRow.replace('SCAN TABLE', 'SCAN');
                                            } else if (displayRow.includes('SEARCH TABLE')) {
                                                displayRow = displayRow.replace('SEARCH TABLE', 'SEARCH');
                                            }

                                            return (
                                                <div key={i} className="text-xs font-mono text-zinc-300 whitespace-pre hover:bg-zinc-800/50 px-2 py-0.5 rounded transition-colors" style={{ paddingLeft: (indent + 8) + 'px' }}>
                                                    {displayRow.trim()}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div >
    );
}
