import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useGameStore } from '../store/gameStore';

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
    const [selectedWorld, setSelectedWorld] = useState<string>('All');

    // Hook into Game Store for XP
    const addXp = useGameStore((s) => s.addXp);

    // 1. Fetch Index when Drawer Opens or World Filter Changes
    useEffect(() => {
        if (isOpen) {
            setLoading(true);
            const query = selectedWorld === 'All' ? '' : `?world=${selectedWorld}`;
            fetch(`/api/codex${query}`)
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
    }, [isOpen, selectedWorld]);

    // Mark as read logic
    useEffect(() => {
        if (selectedEntry) {
            // Award XP for "Studying" (Debounced/Once per session logic ideally)
            // For MVP: Just a small toast or visual feedback
            // In a real app, we'd check if already read.
            // addXp(10); // Uncomment to enable XP gain on read
        }
    }, [selectedEntry, addXp]);

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

    // Custom Renderer for Code Blocks
    const MarkdownComponents = {
        code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
                <div className="relative group">
                    <div className="absolute top-0 right-0 bg-zinc-800 text-[10px] px-2 py-1 text-zinc-400 rounded-bl opacity-0 group-hover:opacity-100 transition-opacity uppercase">
                        {match[1]}
                    </div>
                    <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                            margin: '1rem 0',
                            borderRadius: '0.5rem',
                            backgroundColor: '#09090b', // zinc-950
                            border: '1px solid #27272a', // zinc-800
                            fontSize: '0.8rem',
                        }}
                        {...props}
                    >
                        {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                </div>
            ) : (
                <code className="bg-zinc-800 text-banana-300 px-1 py-0.5 rounded text-xs font-mono" {...props}>
                    {children}
                </code>
            );
        }
    };

    const WORLDS = ['All', 'world-python', 'world-js', 'world-sql', 'world-infra', 'world-agents', 'world-git', 'world-ml', 'world-evalforge'];

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
            <div className={`fixed inset-y-0 right-0 w-[600px] bg-zinc-950 border-l border-zinc-800 shadow-2xl transform transition-transform duration-300 z-50 flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>

                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-950">
                    <div className="flex items-center gap-2">
                        <span className="text-xl">📖</span>
                        <h2 className="text-cyan-500 font-bold tracking-wider font-mono">CODEX SYSTEM</h2>
                    </div>
                    {/* XP Reward Badge */}
                    {selectedEntry && (
                        <div className="text-[10px] bg-cyan-900/30 text-cyan-400 px-2 py-1 rounded border border-cyan-800">
                            READING MODE (+10 XP)
                        </div>
                    )}
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">
                        ✕ ESC
                    </button>
                </div>

                {/* Body */}
                <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-zinc-800">
                    {loading && <div className="text-zinc-500 animate-pulse font-mono text-sm">ACCESSING ARCHIVES...</div>}

                    {!loading && !selectedEntry && (
                        // LIST VIEW
                        <div className="space-y-4">
                            <div className="flex flex-wrap gap-2 pb-4 border-b border-zinc-900">
                                {WORLDS.map(w => (
                                    <button
                                        key={w}
                                        onClick={() => setSelectedWorld(w)}
                                        className={`px-2 py-1 text-[10px] uppercase tracking-wider rounded border transition-colors ${selectedWorld === w
                                                ? 'bg-cyan-950 text-cyan-400 border-cyan-800'
                                                : 'bg-zinc-900 text-zinc-500 border-zinc-800 hover:border-zinc-700 hover:text-zinc-300'
                                            }`}
                                    >
                                        {w.replace('world-', '')}
                                    </button>
                                ))}
                            </div>

                            <div className="text-xs font-mono text-zinc-600 uppercase">
                                Available Knowledge: {selectedWorld.toUpperCase()}
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
                                    <div className="flex flex-wrap gap-2 mt-3 items-center">
                                        <span className="px-1.5 py-0.5 bg-zinc-950 text-zinc-400 rounded text-[9px] uppercase border border-zinc-800">
                                            {entry.world}
                                        </span>
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

                            <h1 className="text-2xl font-bold text-white mb-2 font-mono tracking-tight">
                                {selectedEntry.metadata.title}
                            </h1>

                            {/* Metadata Pills */}
                            <div className="flex flex-wrap gap-2 mb-8 border-b border-zinc-800 pb-4">
                                <span className="px-2 py-0.5 bg-zinc-800 text-zinc-400 text-[10px] uppercase rounded">
                                    {selectedEntry.metadata.world}
                                </span>
                                {selectedEntry.metadata.tags.map((t: string) => (
                                    <span key={t} className="px-2 py-0.5 bg-cyan-950 text-cyan-400 text-[10px] uppercase rounded border border-cyan-900/50">
                                        #{t}
                                    </span>
                                ))}
                            </div>

                            {/* The "Ask Agent" Action Bar */}
                            <div className="mb-8 p-4 bg-zinc-900/50 border border-zinc-800 rounded-lg flex items-center justify-between">
                                <div className="text-xs text-zinc-500">
                                    Need clarification on this topic?
                                </div>
                                <button
                                    className="bg-zinc-800 hover:bg-banana-500 hover:text-black text-zinc-300 text-xs px-3 py-1.5 rounded transition-all font-bold flex items-center gap-2"
                                    onClick={() => {
                                        // TODO: Dispatch event to open Chat with context
                                        onClose();
                                        // You would ideally update the input state in DevUI via a global store action
                                    }}
                                >
                                    <span>💬</span> ASK MENTOR
                                </button>
                            </div>

                            {/* Enhanced Markdown Renderer */}
                            <div className="prose prose-invert prose-sm max-w-none 
                                prose-headings:font-mono prose-headings:text-banana-400
                                prose-strong:text-white
                                prose-blockquote:border-l-cyan-500 prose-blockquote:bg-cyan-950/20 prose-blockquote:text-cyan-100 prose-blockquote:py-2 prose-blockquote:px-4 prose-blockquote:not-italic prose-blockquote:rounded-r
                                font-sans">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={MarkdownComponents} // <--- Inject Highlighter
                                >
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
