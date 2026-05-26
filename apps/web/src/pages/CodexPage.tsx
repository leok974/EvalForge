/**
 * Sprint 22.5: Codex page — /arcade/codex
 * Embedded codex browser: client-side search over /api/codex/index/structure,
 * world filter chips, section grouping, CodexDrawer detail view.
 */
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Search, BookOpen, ChevronLeft, X } from 'lucide-react';
import { fetchCodexIndex, CodexSection } from '../lib/codexApi';
import { CodexDrawer } from '../components/codex/CodexDrawer';

// Active worlds that have codex content worth surfacing in the nav.
const ACTIVE_WORLD_ORDER = [
    'world-python',
    'world-sql',
    'world-web',
    'world-js',
    'world-typescript',
    'world-git',
];

const WORLD_LABELS: Record<string, string> = {
    'world-python': 'Python',
    'world-sql': 'SQL',
    'world-web': 'Web',
    'world-js': 'JavaScript',
    'world-typescript': 'TypeScript',
    'world-git': 'Git',
};

function worldLabel(slug: string): string {
    return WORLD_LABELS[slug] || slug.replace('world-', '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
    const [debounced, setDebounced] = useState(value);
    useEffect(() => {
        const timer = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);
    return debounced;
}

export function CodexPage() {
    const [sections, setSections] = useState<CodexSection[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [query, setQuery] = useState('');
    const [activeWorld, setActiveWorld] = useState<string>('all');
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [drawerRef, setDrawerRef] = useState<string | null>(null);

    const debouncedQuery = useDebounce(query, 250);

    useEffect(() => {
        fetchCodexIndex()
            .then(data => setSections(data.sections))
            .catch(err => setError(err.message || 'Failed to load codex index'))
            .finally(() => setLoading(false));
    }, []);

    // Derive sorted world list from actual data + prefer active-world order
    const worlds = useMemo(() => {
        const seen = new Set<string>();
        const ordered: string[] = [];
        // First pass: active worlds in preferred order
        for (const w of ACTIVE_WORLD_ORDER) {
            if (sections.some(s => s.world === w)) {
                seen.add(w);
                ordered.push(w);
            }
        }
        // Second pass: any remaining worlds from index
        for (const s of sections) {
            if (!seen.has(s.world)) {
                seen.add(s.world);
                ordered.push(s.world);
            }
        }
        return ordered;
    }, [sections]);

    // Filtered + searched sections
    const visible = useMemo(() => {
        const q = debouncedQuery.trim().toLowerCase();
        return sections
            .filter(s => {
                if (activeWorld !== 'all' && s.world !== activeWorld) return false;
                if (!q) return true;
                return s.pages.some(p => p.title.toLowerCase().includes(q) || p.id.toLowerCase().includes(q));
            })
            .map(s => ({
                ...s,
                pages: debouncedQuery.trim()
                    ? s.pages.filter(p => p.title.toLowerCase().includes(debouncedQuery.trim().toLowerCase()) || p.id.toLowerCase().includes(debouncedQuery.trim().toLowerCase()))
                    : s.pages,
            }))
            .filter(s => s.pages.length > 0);
    }, [sections, activeWorld, debouncedQuery]);

    const totalResults = useMemo(() => visible.reduce((n, s) => n + s.pages.length, 0), [visible]);

    const handleOpenEntry = useCallback((id: string) => {
        setDrawerRef(`codex:${id}`);
        setDrawerOpen(true);
    }, []);

    const handleOpenCodex = useCallback((ref: string) => {
        setDrawerRef(ref);
        setDrawerOpen(true);
    }, []);

    // Sprint 22.6: h-full overflow-y-auto instead of min-h-screen — fixes scroll inside FXLayer.
    return (
        <main className="h-full overflow-y-auto bg-workshop-bg text-workshop-text font-sans selection:bg-workshop-violet/20 relative">
            {/* Ambient gradient */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-[400px] bg-workshop-cyan/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[400px] bg-workshop-violet/5 blur-[120px]" />
            </div>

            {/* Page header */}
            <header className="relative z-10 border-b border-white/5 bg-workshop-bg/60 backdrop-blur-sm px-6 py-4">
                <div className="max-w-5xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Link
                            to="/arcade/workshop"
                            className="flex items-center gap-1 text-xs text-workshop-subtle hover:text-workshop-text transition-colors"
                        >
                            <ChevronLeft className="w-3.5 h-3.5" />
                            Workshop
                        </Link>
                        <span className="text-white/20">/</span>
                        <div className="flex items-center gap-2">
                            <BookOpen className="w-4 h-4 text-workshop-cyan" />
                            <h1 className="text-sm font-semibold tracking-wide">Codex</h1>
                        </div>
                    </div>
                    <span className="text-[10px] text-workshop-subtle font-mono uppercase tracking-wider">
                        Knowledge Base
                    </span>
                </div>
            </header>

            {/* Content */}
            <div className="relative z-10 max-w-5xl mx-auto px-6 py-8 space-y-6">

                {/* Search bar */}
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-workshop-subtle" />
                    <input
                        type="text"
                        placeholder="Search documentation…"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        autoFocus
                        className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-workshop-panel border border-white/10 text-sm text-workshop-text placeholder:text-workshop-subtle focus:outline-none focus:border-workshop-cyan/50 focus:ring-1 focus:ring-workshop-cyan/30 transition-all"
                    />
                    {query && (
                        <button
                            onClick={() => setQuery('')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-workshop-subtle hover:text-workshop-text"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    )}
                </div>

                {/* World filter chips */}
                <div className="flex flex-wrap gap-2">
                    <button
                        onClick={() => setActiveWorld('all')}
                        className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
                            activeWorld === 'all'
                                ? 'bg-workshop-violet/20 text-workshop-violet border-workshop-violet/40'
                                : 'bg-workshop-panel text-workshop-subtle border-white/10 hover:text-workshop-text hover:border-white/20'
                        }`}
                    >
                        All Worlds
                    </button>
                    {worlds.map(w => (
                        <button
                            key={w}
                            onClick={() => setActiveWorld(w === activeWorld ? 'all' : w)}
                            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
                                activeWorld === w
                                    ? 'bg-workshop-cyan/20 text-workshop-cyan border-workshop-cyan/40'
                                    : 'bg-workshop-panel text-workshop-subtle border-white/10 hover:text-workshop-text hover:border-white/20'
                            }`}
                        >
                            {worldLabel(w)}
                        </button>
                    ))}
                </div>

                {/* Status / result count */}
                {!loading && !error && debouncedQuery && (
                    <p className="text-xs text-workshop-subtle">
                        {totalResults === 0 ? 'No results' : `${totalResults} result${totalResults === 1 ? '' : 's'}`}
                        {' '}for <span className="text-workshop-text font-medium">"{debouncedQuery}"</span>
                    </p>
                )}

                {/* States */}
                {loading && (
                    <div className="text-center py-16 text-workshop-subtle text-sm animate-pulse">
                        Loading codex index…
                    </div>
                )}

                {error && (
                    <div className="rounded-xl border border-red-800/50 bg-red-950/20 px-4 py-3 text-sm text-red-400">
                        {error}
                    </div>
                )}

                {!loading && !error && visible.length === 0 && (
                    <div className="text-center py-16 text-workshop-subtle text-sm">
                        No entries found.{activeWorld !== 'all' && (
                            <> <button onClick={() => setActiveWorld('all')} className="text-workshop-cyan hover:underline ml-1">Clear world filter</button></>
                        )}
                    </div>
                )}

                {/* Results: grouped by section */}
                {!loading && !error && visible.length > 0 && (
                    <div className="space-y-8">
                        {visible.map((section, idx) => (
                            <div key={`${section.world}-${section.section}-${idx}`}>
                                {/* Section header */}
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="h-px flex-1 bg-white/5" />
                                    <div className="flex items-center gap-2">
                                        <span className="text-[10px] font-bold uppercase tracking-widest text-workshop-subtle">
                                            {worldLabel(section.world)}
                                        </span>
                                        <span className="text-white/20">·</span>
                                        <span className="text-[10px] font-medium uppercase tracking-wider text-workshop-subtle/70">
                                            {(section.section || 'General').replace(/-/g, ' ')}
                                        </span>
                                    </div>
                                    <div className="h-px flex-1 bg-white/5" />
                                </div>

                                {/* Page cards */}
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                    {section.pages.map(page => (
                                        <button
                                            key={page.id}
                                            onClick={() => handleOpenEntry(page.id)}
                                            className="text-left group p-4 rounded-xl bg-workshop-panel border border-white/8 hover:border-workshop-cyan/30 hover:bg-workshop-panel/80 transition-all shadow-sm"
                                        >
                                            <div className="font-medium text-sm text-workshop-text group-hover:text-workshop-cyan transition-colors leading-snug">
                                                {page.title}
                                            </div>
                                            <div className="mt-1.5 text-[10px] font-mono text-workshop-subtle/60 truncate">
                                                {page.id}
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* CodexDrawer for detail view */}
            <CodexDrawer
                isOpen={drawerOpen}
                activeRef={drawerRef}
                onClose={() => setDrawerOpen(false)}
                onOpenCodex={handleOpenCodex}
            />
        </main>
    );
}
