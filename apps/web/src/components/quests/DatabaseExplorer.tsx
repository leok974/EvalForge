import React, { useState, useEffect } from 'react';
import { Database, Table2, Columns, Eye, RefreshCw, ChevronRight, ChevronDown, Loader2 } from 'lucide-react';
import { DbIntrospection, introspectDb, previewTable, DbPreview } from '@/lib/questsApi';
import { cn } from '@/lib/utils';

interface DatabaseExplorerProps {
    questId: string;
}

export function DatabaseExplorer({ questId }: DatabaseExplorerProps) {
    const [data, setData] = useState<DbIntrospection | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [expandedSchemas, setExpandedSchemas] = useState<Record<string, boolean>>({ "public": true });
    const [expandedTables, setExpandedTables] = useState<Record<string, boolean>>({});
    
    const [preview, setPreview] = useState<{ table: string; data: DbPreview } | null>(null);
    const [previewLoading, setPreviewLoading] = useState(false);

    const loadData = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await introspectDb(questId);
            setData(result);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, [questId]);

    const toggleSchema = (name: string) => {
        setExpandedSchemas(prev => ({ ...prev, [name]: !prev[name] }));
    };

    const toggleTable = (name: string) => {
        setExpandedTables(prev => ({ ...prev, [name]: !prev[name] }));
    };

    const handlePreview = async (schema: string, table: string) => {
        setPreviewLoading(true);
        try {
            const result = await previewTable(questId, table, schema);
            setPreview({ table, data: result });
        } catch (e: any) {
            alert(`Failed to preview ${table}: ${e.message}`);
        } finally {
            setPreviewLoading(false);
        }
    };

    if (loading && !data) {
        return (
            <div className="p-8 flex flex-col items-center justify-center text-zinc-500 gap-3">
                <Loader2 className="w-6 h-6 animate-spin text-cyan-500" />
                <span className="text-xs font-mono uppercase tracking-widest">Introspecting DB...</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-6 text-red-400 text-xs font-mono bg-red-950/20 rounded-lg border border-red-900/30 m-4">
                <p className="font-bold mb-1">INTROSPECTION_ERROR</p>
                <p>{error}</p>
                <button onClick={loadData} className="mt-4 flex items-center gap-2 text-red-300 hover:text-white">
                    <RefreshCw className="w-3 h-3" /> Retry
                </button>
            </div>
        );
    }

    if (!data || data.schemas.length === 0) {
        return (
            <div className="p-8 text-center text-zinc-500">
                <Database className="w-12 h-12 mx-auto mb-4 opacity-20" />
                <p className="text-sm">No tables found in this context.</p>
                <button onClick={loadData} className="mt-4 text-xs text-cyan-500 hover:underline">Refresh</button>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full bg-zinc-950/50">
            {/* Header */}
            <div className="p-3 border-b border-white/5 flex items-center justify-between bg-zinc-900/30">
                <div className="flex items-center gap-2">
                    <Database className="w-4 h-4 text-cyan-400" />
                    <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Explorer</span>
                    <span className={cn(
                        "text-[9px] px-1.5 py-0.5 rounded border leading-none font-mono",
                        data.engine === 'postgres' ? "bg-indigo-950/30 border-indigo-500/50 text-indigo-300" : "bg-zinc-800 border-zinc-700 text-zinc-400"
                    )}>
                        {data.engine.toUpperCase()}
                    </span>
                </div>
                <button 
                    onClick={loadData} 
                    title="Refresh Schema"
                    className="p-1 hover:bg-white/5 rounded transition-colors text-zinc-500 hover:text-cyan-400"
                >
                    <RefreshCw className={cn("w-3.5 h-3.5", loading && "animate-spin")} />
                </button>
            </div>

            {/* Tree View */}
            <div className="flex-1 overflow-y-auto p-2 space-y-1 select-none">
                {data.schemas.map(schema => (
                    <div key={schema.name} className="space-y-1">
                        <button 
                            onClick={() => toggleSchema(schema.name)}
                            className="flex items-center gap-1.5 w-full text-left p-1 rounded hover:bg-white/5 group transition-colors"
                        >
                            {expandedSchemas[schema.name] ? <ChevronDown className="w-3 h-3 text-zinc-600" /> : <ChevronRight className="w-3 h-3 text-zinc-600" />}
                            <span className="text-xs font-semibold text-zinc-400 group-hover:text-zinc-200">{schema.name}</span>
                        </button>

                        {expandedSchemas[schema.name] && (
                            <div className="pl-4 space-y-1">
                                {schema.tables.map(table => (
                                    <div key={table.name} className="space-y-1">
                                        <div className="flex items-center justify-between group rounded hover:bg-white/5 pr-1">
                                            <button 
                                                onClick={() => toggleTable(table.name)}
                                                className="flex items-center gap-2 flex-1 text-left p-1"
                                            >
                                                <Table2 className="w-3.5 h-3.5 text-cyan-600/70" />
                                                <span className="text-xs text-zinc-300 group-hover:text-white truncate">{table.name}</span>
                                            </button>
                                            <button 
                                                onClick={() => handlePreview(schema.name, table.name)}
                                                title="Preview Rows"
                                                className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-cyan-500/20 text-cyan-500 transition-all"
                                            >
                                                {previewLoading && preview?.table === table.name ? <Loader2 className="w-3 h-3 animate-spin" /> : <Eye className="w-3 h-3" />}
                                            </button>
                                        </div>

                                        {expandedTables[table.name] && (
                                            <div className="pl-5 py-1 space-y-1 border-l border-white/5 ml-2.5">
                                                {table.columns.map(col => (
                                                    <div key={col.name} className="flex items-center gap-2 py-0.5 px-1 group">
                                                        <Columns className="w-3 h-3 text-zinc-700 group-hover:text-zinc-500" />
                                                        <span className="text-[11px] text-zinc-400 group-hover:text-zinc-300 truncate">{col.name}</span>
                                                        <span className="text-[9px] font-mono text-zinc-600 ml-auto">{col.type}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Preview Modal/Overlay */}
            {preview && (
                <div className="absolute inset-x-2 bottom-2 max-h-[60%] bg-zinc-900 border border-white/10 rounded-lg shadow-2xl flex flex-col z-50 animate-in slide-in-from-bottom-4 duration-200 overflow-hidden">
                    <div className="p-2 border-b border-white/5 flex items-center justify-between bg-zinc-800/50">
                        <div className="flex items-center gap-2">
                            <Eye className="w-3.5 h-3.5 text-cyan-400" />
                            <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-300">{preview.table}</span>
                            <span className="text-[9px] text-zinc-500 font-mono">({preview.data.row_count} rows)</span>
                        </div>
                        <button 
                            onClick={() => setPreview(null)}
                            className="p-1 hover:bg-white/10 rounded text-zinc-400 hover:text-white"
                        >
                            <ChevronDown className="w-4 h-4" />
                        </button>
                    </div>
                    <div className="flex-1 overflow-auto bg-black/20">
                        <table className="w-full text-left text-[11px] font-mono border-collapse">
                            <thead className="sticky top-0 bg-zinc-900 z-10 shadow-sm">
                                <tr>
                                    {preview.data.columns.map(col => (
                                        <th key={col} className="px-3 py-1.5 border-b border-white/10 text-zinc-500 font-bold uppercase tracking-tighter whitespace-nowrap bg-zinc-900/80 backdrop-blur-sm">
                                            {col}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {preview.data.rows.map((row, i) => (
                                    <tr key={i} className="hover:bg-cyan-500/5 transition-colors border-b border-white/5">
                                        {row.map((cell, j) => (
                                            <td key={j} className="px-3 py-1 text-zinc-400 whitespace-nowrap">
                                                {cell === null ? <span className="text-zinc-700 italic">null</span> : String(cell)}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
