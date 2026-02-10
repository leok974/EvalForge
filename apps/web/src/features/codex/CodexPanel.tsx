import React, { useState, useEffect, useMemo } from 'react';
import { BookOpen, Search, History, Bookmark, ArrowLeft, Filter, Globe } from 'lucide-react'; // Added icons
import { cn } from '../../lib/utils';
import { CodexMarkdown } from './CodexMarkdown';
import { fetchQuest, QuestSummary } from '../../lib/questsApi';
import { fetchCodex, fetchCodexIndex, CodexEntry, CodexIndex } from '../../lib/codexApi';
import { useOpenCodex } from '../../hooks/useOpenCodex';

interface CodexPanelProps {
    initialTerm?: string;
    questSlug?: string;
}

export const CodexPanel: React.FC<CodexPanelProps> = ({ initialTerm, questSlug }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [activeTerm, setActiveTerm] = useState<string | null>(initialTerm || null);
    const [history, setHistory] = useState<string[]>([]);

    // Data State
    const [questTerms, setQuestTerms] = useState<NonNullable<QuestSummary['key_terms']>>([]);
    const [codexIndex, setCodexIndex] = useState<CodexIndex | null>(null);
    const [activeWorldFilter, setActiveWorldFilter] = useState<string | 'all'>('all');

    // Content State
    const [termContent, setTermContent] = useState<CodexEntry | null>(null);
    const [loadingTerm, setLoadingTerm] = useState(false);
    const [termError, setTermError] = useState<string | null>(null);

    // Persistent Recents (LocalStorage)
    const [recents, setRecents] = useState<string[]>(() => {
        try {
            return JSON.parse(localStorage.getItem('codex_recents') || '[]');
        } catch {
            return [];
        }
    });

    const openCodex = useOpenCodex();

    // 1. Fetch Codex Index on Mount (for Filters/Search)
    useEffect(() => {
        console.log("🏁 [CodexPanel] Mounted. initialTerm:", initialTerm);
        fetchCodexIndex().then(idx => {
            console.log("📚 [CodexPanel] Index Loaded:", idx);
            setCodexIndex(idx);
        }).catch(console.error);
    }, []);

    // 2. Fetch Quest Terms on Slug Change (Fix 3)
    useEffect(() => {
        if (questSlug) {
            fetchQuest(questSlug).then(q => {
                setQuestTerms(q.key_terms || []);
            }).catch(e => {
                console.error("Failed to load quest context", e);
                setQuestTerms([]);
            });
        } else {
            setQuestTerms([]);
        }
    }, [questSlug]);

    // 3. Load Active Term Content
    useEffect(() => {
        console.log("🔄 [CodexPanel] useEffect activeTerm changed:", activeTerm);
        if (activeTerm) {
            setLoadingTerm(true);
            setTermContent(null);
            setTermError(null);

            // Add to history if unique
            setHistory(prev => {
                if (prev[prev.length - 1] !== activeTerm) return [...prev, activeTerm];
                return prev;
            });

            // Add to recents
            setRecents(prev => {
                const newRecents = [activeTerm, ...prev.filter(t => t !== activeTerm)].slice(0, 10);
                localStorage.setItem('codex_recents', JSON.stringify(newRecents));
                return newRecents;
            });

            console.log("🚀 [CodexPanel] fetching content for:", activeTerm);
            fetchCodex(activeTerm)
                .then(data => {
                    console.log("✅ [CodexPanel] fetch success:", data);
                    setTermContent(data);
                })
                .catch(err => {
                    console.error("❌ [CodexPanel] fetch error:", err);
                    setTermError(err.message || "Failed to load term. Please try again.");
                    setTermContent(null); // Ensure content is cleared
                })
                .finally(() => setLoadingTerm(false));
        }
    }, [activeTerm]);

    // Update active term if prop changes (deep link)
    useEffect(() => {
        if (initialTerm) setActiveTerm(initialTerm);
    }, [initialTerm]);

    const handleTermClick = (termRef: string) => {
        console.log("👉 [CodexPanel] handleTermClick:", termRef);
        // Ensure consistent state reset
        setLoadingTerm(true);
        setTermError(null);
        openCodex(termRef);
        setActiveTerm(termRef);
    };

    const handleBack = () => {
        setActiveTerm(null);
        // Clear param from URL?
        // Ideally yes, but tricky to do cleanly without hook support for clearing.
        // For now, local back is fine.
    };

    // Derived World List
    const worlds = useMemo(() => {
        if (!codexIndex) return [];
        const w = new Set(codexIndex.sections.map(s => s.world));
        return Array.from(w);
    }, [codexIndex]);

    // Filtered Results Calculation
    // If searching -> filter index pages
    // If not searching -> show categories? Or just World filter effect?
    // User wants "World Pills" to filter list/search.

    const filteredPages = useMemo(() => {
        if (!codexIndex) return []; // Allow empty search if filtering by world

        let pages = codexIndex.sections.flatMap(s => s.pages);

        // World Filter
        if (activeWorldFilter !== 'all') {
            pages = pages.filter(p => p.world === activeWorldFilter);
        }

        // Search Query
        if (searchQuery) {
            const q = searchQuery.toLowerCase();
            pages = pages.filter(p => p.title.toLowerCase().includes(q) || p.id.includes(q));
        }

        return pages;
    }, [codexIndex, searchQuery, activeWorldFilter]);


    // SEARCH VIEW
    if (!activeTerm) {
        return (
            <div className="h-full flex flex-col font-mono text-sm bg-slate-950/50">
                {/* Search Header */}
                <div className="p-4 border-b border-white/5 space-y-3 bg-black/20">
                    <div className="relative">
                        <Search className="absolute left-3 top-2.5 w-4 h-4 text-zinc-500" />
                        <input
                            type="text"
                            placeholder="Search Codex..."
                            className="w-full bg-zinc-900/80 border border-white/10 rounded-md py-2 pl-9 pr-4 text-zinc-300 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    {/* World Pills (Fix 4) */}
                    {worlds.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                            <button
                                onClick={() => {
                                    console.log("🔘 [CodexPanel] Clicked Filter Pill: all");
                                    setActiveWorldFilter('all');
                                }}
                                className={cn(
                                    "px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-full border transition-all",
                                    activeWorldFilter === 'all'
                                        ? "bg-cyan-950/50 text-cyan-300 border-cyan-500/30"
                                        : "bg-zinc-900/50 text-zinc-500 border-zinc-800 hover:border-zinc-700"
                                )}
                            >
                                All
                            </button>
                            {worlds.map(w => (
                                <button
                                    key={w}
                                    data-testid={`codex-world-pill-${w}`}
                                    onClick={() => {
                                        console.log("🔘 [CodexPanel] Clicked Filter Pill:", w);
                                        setActiveWorldFilter(w)
                                    }}
                                    className={cn(
                                        "px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-full border transition-all",
                                        activeWorldFilter === w
                                            ? "bg-cyan-950/50 text-cyan-300 border-cyan-500/30"
                                            : "bg-zinc-900/50 text-zinc-500 border-zinc-800 hover:border-zinc-700"
                                    )}
                                >
                                    {w.replace(/^world-/, '')}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                    {/* Search Results OR Filtered List */}
                    {(searchQuery || activeWorldFilter !== 'all') ? (
                        <div>
                            <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 mb-3 block">
                                {filteredPages.length} Results
                            </h3>
                            <div className="space-y-1">
                                {filteredPages.map(p => (
                                    <button
                                        key={p.id}
                                        onClick={() => handleTermClick(`codex:${p.id}`)} // Assuming ID is usable ref
                                        className="block w-full text-left px-3 py-2 bg-zinc-900/30 hover:bg-zinc-800 border border-transparent hover:border-zinc-700 rounded text-zinc-300 transition-colors"
                                    >
                                        <div className="font-bold text-xs">{p.title}</div>
                                        <div className="text-[10px] text-zinc-500 flex items-center gap-2">
                                            <span className="uppercase">{p.world}</span>
                                            <span>•</span>
                                            <span>{p.section}</span>
                                        </div>
                                    </button>
                                ))}
                                {filteredPages.length === 0 && (
                                    <div className="text-zinc-600 italic text-center py-4">No entries found.</div>
                                )}
                            </div>
                        </div>
                    ) : (
                        <>
                            {/* Contextual Terms (Fix 3) */}
                            {questSlug && questTerms.length > 0 && (
                                <div>
                                    <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-600/80 mb-3 flex items-center gap-2">
                                        <Bookmark className="w-3 h-3" />
                                        For this Quest
                                    </h3>
                                    <div className="grid grid-cols-1 gap-2">
                                        {questTerms.map((term, idx) => (
                                            <button
                                                key={term.id || `term-${idx}`}
                                                onClick={() => term.codex_ref && handleTermClick(term.codex_ref)}
                                                disabled={!term.codex_ref}
                                                className="text-left p-2 bg-cyan-950/10 border border-cyan-900/20 rounded hover:bg-cyan-900/30 transition-colors group"
                                            >
                                                <div className="text-cyan-200/90 text-xs font-bold">{term.term}</div>
                                                {term.one_liner && (
                                                    <div className="text-[10px] text-cyan-600/70 truncate group-hover:text-cyan-500/80">{term.one_liner}</div>
                                                )}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Recents */}
                            {recents.length > 0 && (
                                <div>
                                    <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 mb-3 flex items-center gap-2">
                                        <History className="w-3 h-3" />
                                        Recent
                                    </h3>
                                    <div className="space-y-1">
                                        {recents.map(r => (
                                            <button key={r} onClick={() => handleTermClick(r)} className="block w-full text-left px-2 py-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-white/5 rounded transition-colors truncate text-xs">
                                                {r.replace('codex:', '')}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Browse All (Fallback if no search) */}
                            <div className="mt-8">
                                <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-600 mb-3 flex items-center gap-2">
                                    <Globe className="w-3 h-3" />
                                    Browse Index
                                </h3>
                                <div className="text-[10px] text-zinc-500">
                                    Use search or filters to find specific entries.
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </div>
        );
    }

    // TERM VIEW
    return (
        <div className="h-full flex flex-col font-mono bg-slate-950/50">
            {/* Header */}
            <div className="flex items-center gap-2 p-3 border-b border-white/5 bg-black/20 text-zinc-400 sticky top-0 z-10 backdrop-blur">
                <button
                    onClick={handleBack}
                    className="p-1 hover:bg-white/10 rounded transition-colors"
                >
                    <ArrowLeft className="w-4 h-4" />
                </button>
                <span className="text-xs font-bold text-zinc-300 truncate flex-1 leading-none">
                    {termContent?.title || activeTerm?.replace('codex:', '')}
                </span>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 scroll-smooth">
                {loadingTerm ? (
                    <div className="flex flex-col items-center justify-center py-10 gap-2 opacity-50">
                        <div className="w-4 h-4 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                        <div className="text-xs text-cyan-500 uppercase tracking-widest">Decrypting...</div>
                    </div>
                ) : termError ? (
                    <div className="flex flex-col items-center justify-center py-10 gap-4">
                        <div className="p-4 border border-red-900/30 bg-red-950/10 text-red-400 text-xs rounded max-w-md">
                            <strong className="block mb-1">DATA CORRUPTED</strong>
                            {termError}
                            <div className="text-[10px] text-red-500/70 mt-2">
                                Term: <code className="bg-red-950/30 px-1 rounded">{activeTerm}</code>
                            </div>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={() => {
                                    setTermError(null);
                                    setLoadingTerm(true);
                                    fetchCodex(activeTerm!)
                                        .then(data => setTermContent(data))
                                        .catch(err => setTermError(err.message || "Failed to load term."))
                                        .finally(() => setLoadingTerm(false));
                                }}
                                className="px-3 py-1.5 bg-cyan-900/30 hover:bg-cyan-900/50 border border-cyan-700/50 text-cyan-300 text-xs rounded transition-colors"
                            >
                                Retry
                            </button>
                            <button
                                onClick={handleBack}
                                className="px-3 py-1.5 bg-zinc-900/30 hover:bg-zinc-800 border border-zinc-700/50 text-zinc-300 text-xs rounded transition-colors"
                            >
                                Back to Search
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <CodexMarkdown
                            markdown={termContent?.md || ''}
                            overrideTitle={termContent?.title}
                        />
                    </div>
                )}
            </div>
        </div>
    );
};
