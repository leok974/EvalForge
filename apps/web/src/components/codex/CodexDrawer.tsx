/**
 * Phase 9.1: Codex Drawer Component
 * Side drawer for viewing Codex documentation entries
 */
import React, { useState, useEffect, useMemo } from 'react';
import { createPortal } from 'react-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { fetchCodex, CodexEntry, fetchCodexIndex, CodexIndex } from '@/lib/codexApi';
import { MarkdownSurface } from '../markdown/MarkdownSurface';

export interface CodexDrawerProps {
    isOpen: boolean;
    activeRef: string | null;
    onClose: () => void;
    onOpenCodex?: (ref: string) => void;
    questSlug?: string;
}

export function CodexDrawer({ isOpen, activeRef, onClose, onOpenCodex, questSlug }: CodexDrawerProps) {
    const [content, setContent] = useState<CodexEntry | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [index, setIndex] = useState<CodexIndex | null>(null);
    const [activeTab, setActiveTab] = useState<string>('foundry'); // Default world
    const [searchQuery, setSearchQuery] = useState('');

    // UX Refs
    const drawerRef = React.useRef<HTMLDivElement>(null);
    const scrollRef = React.useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (isOpen) {
            loadCodex();
            loadIndex();

            // Lock body scroll
            document.body.style.overflow = 'hidden';

            // Restore scroll position
            if (questSlug && scrollRef.current) {
                const key = `codex_scroll_${questSlug}`;
                const saved = localStorage.getItem(key);
                if (saved) {
                    // Small timeout to allow content render
                    setTimeout(() => {
                        if (scrollRef.current) scrollRef.current.scrollTop = parseInt(saved, 10);
                    }, 50);
                }
            }
        } else {
            document.body.style.overflow = '';
        }

        return () => {
            document.body.style.overflow = '';
        };
    }, [isOpen, activeRef, questSlug]);

    // Save scroll position on close or unmount
    useEffect(() => {
        return () => {
            if (isOpen && questSlug && scrollRef.current) {
                const key = `codex_scroll_${questSlug}`;
                localStorage.setItem(key, scrollRef.current.scrollTop.toString());
            }
        };
    }, [isOpen, questSlug]);

    // Also save periodically or on scroll? On close is safer for now. 
    // Actually, if they close via prop change, the cleanup above runs. UseEffect cleanup runs before re-run.

    // ESC Key Handler
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, onClose]);

    const loadIndex = async () => {
        if (index) return;
        try {
            const data = await fetchCodexIndex(); // Ensure this is imported
            setIndex(data);
        } catch (err) {
            console.error('Failed to load codex index', err);
        }
    };

    const loadCodex = async () => {
        if (!activeRef) return;

        setLoading(true);
        setError(null);
        try {
            // If home, we don't fetch content, we just show the index
            // But we can create a fake context for "Codex Library" title
            if (activeRef === 'codex:home') {
                setContent({ ref: 'codex:home', title: 'Codex Library', md: '', path: 'home' });
                setLoading(false);
                return;
            }

            const data = await fetchCodex(activeRef);
            setContent(data);
        } catch (err) {
            console.error('Codex fetch error:', err);
            setError(err instanceof Error ? err.message : 'Failed to load content');
        } finally {
            setLoading(false);
        }
    };

    // Extract unique worlds for tabs
    const worlds = useMemo(() => {
        if (!index) return [];
        const w = new Set(index.sections.map(s => s.world));
        return Array.from(w).sort();
    }, [index]);

    // Filtered sections for the active tab
    const filteredSections = useMemo(() => {
        if (!index) return [];
        return index.sections.filter(s => {
            if (s.world !== activeTab && s.world !== 'general') return false; // Show general in all tabs? Or separate? Let's keep separate tabs.
            if (s.world !== activeTab) return false;

            if (!searchQuery) return true;
            // Search filter
            const hasMatchingPage = s.pages.some(p => p.title.toLowerCase().includes(searchQuery.toLowerCase()));
            return hasMatchingPage;
        }).map(s => ({
            ...s,
            pages: searchQuery ? s.pages.filter(p => p.title.toLowerCase().includes(searchQuery.toLowerCase())) : s.pages
        })).filter(s => s.pages.length > 0);
    }, [index, activeTab, searchQuery]);

    if (!isOpen) return null;

    const isHome = activeRef === 'codex:home' || !activeRef;

    const drawerContent = (
        <>
            {/* Blur overlay */}
            <div
                className="fixed inset-0 z-[80] bg-black/40 backdrop-blur-sm transition-opacity"
                onClick={() => {
                    if (questSlug && scrollRef.current) {
                        const key = `codex_scroll_${questSlug}`;
                        localStorage.setItem(key, scrollRef.current.scrollTop.toString());
                    }
                    onClose();
                }}
                aria-hidden="true"
            />

            {/* Drawer panel */}
            <div
                ref={drawerRef}
                className="fixed right-0 top-0 z-[90] h-dvh w-[520px] max-w-[90vw] bg-slate-950/90 border-l border-slate-800 flex flex-col shadow-2xl"
                role="dialog"
                aria-modal="true"
            >

                {/* Header: never scrolls */}
                <div className="shrink-0 px-6 py-4 border-b border-slate-700 flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-slate-100">
                        {loading ? 'Loading...' : (isHome ? 'Codex Library' : content?.title)}
                    </h2>
                    <div className="flex items-center space-x-2">
                        {!isHome && onOpenCodex && (
                            <button
                                onClick={() => onOpenCodex('codex:home')}
                                className="px-3 py-1.5 text-sm text-blue-400 hover:text-blue-300 hover:bg-slate-800/50 rounded-md transition-colors"
                            >
                                📚 Library
                            </button>
                        )}
                        <button
                            onClick={() => {
                                if (questSlug && scrollRef.current) {
                                    const key = `codex_scroll_${questSlug}`;
                                    localStorage.setItem(key, scrollRef.current.scrollTop.toString());
                                }
                                onClose();
                            }}
                            className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-slate-100"
                            aria-label="Close"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Body: MUST scroll */}
                <div
                    ref={scrollRef}
                    className="flex-1 min-h-0 overflow-y-auto px-6 py-6"
                >
                    {loading && (
                        <div className="flex items-center justify-center py-12">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                        </div>
                    )}

                    {!loading && !error && (
                        <>
                            {isHome ? (
                                // Library View
                                <div className="space-y-6">
                                    {/* Search */}
                                    <input
                                        type="text"
                                        placeholder="Search documentation..."
                                        className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-md text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        value={searchQuery}
                                        onChange={e => setSearchQuery(e.target.value)}
                                        autoFocus
                                    />

                                    {/* World Tabs */}
                                    <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
                                        {worlds.map(w => (
                                            <button
                                                key={w}
                                                onClick={() => setActiveTab(w)}
                                                className={`px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${activeTab === w
                                                    ? 'bg-blue-600 text-white'
                                                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-slate-200'
                                                    }`}
                                            >
                                                {w.charAt(0).toUpperCase() + w.slice(1)}
                                            </button>
                                        ))}
                                    </div>

                                    {/* Grouped Sections */}
                                    <div className="space-y-8">
                                        {filteredSections.map((section, idx) => (
                                            <div key={`${section.world}-${section.section}-${idx}`}>
                                                <h3 className="text-lg font-medium text-slate-200 mb-3 ml-1 border-l-4 border-blue-500 pl-3">
                                                    {section.section.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                                </h3>
                                                <div className="grid grid-cols-1 gap-3">
                                                    {section.pages.map(page => (
                                                        <button
                                                            key={page.id}
                                                            onClick={() => onOpenCodex && onOpenCodex(`codex:${page.id}`)}
                                                            className="text-left p-3 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-slate-700 hover:border-blue-500/50 transition-all group"
                                                        >
                                                            <div className="font-medium text-slate-300 group-hover:text-blue-300 transition-colors">
                                                                {page.title}
                                                            </div>
                                                            <div className="text-xs text-slate-500 mt-1 font-mono">
                                                                {page.id}
                                                            </div>
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        ))}
                                        {filteredSections.length === 0 && (
                                            <div className="text-center py-12 text-slate-500">
                                                No entries found for this world.
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ) : (
                                // Detail View
                                <>
                                    {content ? (
                                        <>
                                            <MarkdownSurface md={content.md} />

                                            {/* Metadata footer */}
                                            <div className="mt-8 pt-4 border-t border-slate-700">
                                                <p className="text-xs text-slate-500">
                                                    Reference: <code className="text-xs bg-slate-800 px-2 py-1 rounded text-slate-300">
                                                        {content.ref}
                                                    </code>
                                                </p>
                                            </div>
                                        </>
                                    ) : (
                                        <div className="text-slate-400 italic">
                                            No content available.
                                        </div>
                                    )}
                                </>
                            )}
                        </>
                    )}

                    {error && !loading && (
                        <div className="p-4 rounded-md bg-red-900/20 border border-red-800">
                            <h3 className="text-lg font-medium text-red-400 mb-2">Error Loading Codex Entry</h3>
                            <p className="text-red-300 text-sm">{error}</p>
                        </div>
                    )}
                </div>

                {/* Optional Footer */}
                {content && !isHome && (
                    <div className="shrink-0 px-6 py-3 border-t border-slate-800 text-xs text-slate-400">
                        <div className="flex items-center justify-between">
                            <span>Codex Entry</span>
                            <span className="font-mono">{content.path}</span>
                        </div>
                    </div>
                )}
            </div>
        </>
    );

    // Portal to document.body to avoid clipping
    return createPortal(drawerContent, document.body);
}
