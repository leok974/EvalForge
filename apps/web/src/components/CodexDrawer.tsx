import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface CodexEntry {
    id: string;
    title: string;
    world: string;
    tags: string[];
}

interface CodexContent {
    metadata: CodexEntry;
    content: string;
}

interface Props {
    isOpen: boolean;
    onClose: () => void;
    currentWorldId: string;
}

export function CodexDrawer({ isOpen, onClose, currentWorldId }: Props) {
    const [index, setIndex] = useState<CodexEntry[]>([]);
    const [selectedEntry, setSelectedEntry] = useState<CodexContent | null>(null);
    const [loading, setLoading] = useState(false);

    // 1. Fetch Index when Drawer Opens or World Changes
    useEffect(() => {
        if (isOpen) {
            setLoading(true);
            fetch(`/api/codex?world=${currentWorldId}`)
                .then(res => res.json())
                .then(data => {
                    setIndex(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error(err);
                    setLoading(false);
                });
        }
    }, [isOpen, currentWorldId]);

    // 2. Fetch Specific Entry Content
    const loadEntry = (id: string) => {
        setLoading(true);
        fetch(`/api/codex/${id}`)
            .then(res => res.json())
            .then(data => {
                setSelectedEntry(data);
                setLoading(false);
            })
            .catch(console.error);
    };

    const handleBack = () => {
        setSelectedEntry(null);
    };

    return (
        <>
            {/* Backdrop (Click to close) */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                    onClick={onClose}
                />
            )}

            {/* Drawer Panel */}
            <div className={`fixed inset-y-0 right-0 w-[500px] bg-zinc-950 border-l border-zinc-800 shadow-2xl transform transition-transform duration-300 z-50 flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>

                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-950">
                    <div className="flex items-center gap-2">
                        <span className="text-xl">📖</span>
                        <h2 className="text-cyan-500 font-bold tracking-wider font-mono">CODEX SYSTEM</h2>
                    </div>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">
                        ✕ ESC
                    </button>
                </div>

                {/* Body */}
                <div className="flex-1 overflow-y-auto p-6">
                    {loading && <div className="text-zinc-500 animate-pulse font-mono text-sm">ACCESSING ARCHIVES...</div>}

                    {!loading && !selectedEntry && (
                        // LIST VIEW
                        <div className="space-y-4">
                            <div className="text-xs font-mono text-zinc-600 uppercase border-b border-zinc-900 pb-2">
                                Available Knowledge: {currentWorldId}
                            </div>

                            {index.length === 0 && (
                                <div className="text-zinc-700 italic text-sm">No entries found for this world. Check data/codex/.</div>
                            )}

                            {index.map(entry => (
                                <div
                                    key={entry.id}
                                    onClick={() => loadEntry(entry.id)}
                                    className="group p-4 rounded-lg bg-zinc-900 border border-zinc-800 hover:border-cyan-500/50 hover:bg-zinc-800/50 cursor-pointer transition-all"
                                >
                                    <div className="font-bold text-zinc-300 group-hover:text-cyan-400 font-mono text-sm">
                                        {entry.title}
                                    </div>
                                    <div className="flex gap-2 mt-3">
                                        {entry.tags.map(t => (
                                            <span key={t} className="px-1.5 py-0.5 bg-black rounded text-[10px] text-zinc-500 uppercase tracking-tight border border-zinc-800">
                                                {t}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {!loading && selectedEntry && (
                        // DETAIL VIEW
                        <div className="animate-in fade-in slide-in-from-right-4 duration-300">
                            <button
                                onClick={handleBack}
                                className="text-xs text-zinc-500 hover:text-cyan-400 mb-6 flex items-center gap-1 font-mono"
                            >
                                ← BACK TO INDEX
                            </button>

                            <h1 className="text-2xl font-bold text-zinc-100 mb-2 font-mono">
                                {selectedEntry.metadata.title}
                            </h1>

                            <div className="flex gap-2 mb-8 border-b border-zinc-800 pb-4">
                                {selectedEntry.metadata.tags.map((t: string) => (
                                    <span key={t} className="text-cyan-600 text-xs font-mono">#{t}</span>
                                ))}
                            </div>

                            {/* Markdown Renderer */}
                            <div className="prose prose-invert prose-sm max-w-none prose-pre:bg-black prose-pre:border prose-pre:border-zinc-800 font-sans">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {selectedEntry.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}
