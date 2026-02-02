/**
 * Phase 9.1: Codex Drawer Component
 * Side drawer for viewing Codex documentation entries
 */
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { fetchCodex, type CodexEntry } from '../../lib/codexApi';

export interface CodexDrawerProps {
    isOpen: boolean;
    activeRef: string | null;
    onClose: () => void;
}

export function CodexDrawer({ isOpen, activeRef, onClose }: CodexDrawerProps) {
    const [content, setContent] = useState<CodexEntry | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!activeRef || !isOpen) {
            return;
        }

        async function loadCodex() {
            setLoading(true);
            setError(null);

            try {
                const entry = await fetchCodex(activeRef);
                setContent(entry);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load codex entry');
                setContent(null);
            } finally {
                setLoading(false);
            }
        }

        loadCodex();
    }, [activeRef, isOpen]);

    if (!isOpen) {
        return null;
    }

    return (
        <>
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-black/50 z-40 transition-opacity"
                onClick={onClose}
            />

            {/* Drawer */}
            <div className="fixed right-0 top-0 bottom-0 w-full md:w-2/3 lg:w-1/2 bg-white dark:bg-gray-900 
                      shadow-xl z-50 overflow-y-auto transform transition-transform">
                {/* Header */}
                <div className="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 
                        px-6 py-4 flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                        {loading ? 'Loading...' : content?.title || 'Codex'}
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                        aria-label="Close"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Content */}
                <div className="px-6 py-6">
                    {loading && (
                        <div className="flex items-center justify-center py-12">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                        </div>
                    )}

                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 
                            rounded-lg p-4">
                            <h3 className="text-red-800 dark:text-red-200 font-semibold mb-2">
                                Error Loading Codex Entry
                            </h3>
                            <p className="text-red-700 dark:text-red-300 text-sm">{error}</p>
                        </div>
                    )}

                    {content && !loading && !error && (
                        <div className="prose prose-sm max-w-none dark:prose-invert">
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                components={{
                                    code({ node, inline, className, children, ...props }) {
                                        return inline ? (
                                            <code className={className} {...props}>
                                                {children}
                                            </code>
                                        ) : (
                                            <code
                                                className={`${className} block bg-gray-100 dark:bg-gray-800 p-4 rounded overflow-x-auto`}
                                                {...props}
                                            >
                                                {children}
                                            </code>
                                        );
                                    },
                                }}
                            >
                                {content.md}
                            </ReactMarkdown>

                            {/* Metadata footer */}
                            <div className="mt-8 pt-4 border-t border-gray-200 dark:border-gray-700">
                                <p className="text-xs text-gray-500 dark:text-gray-400">
                                    Reference: <code className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                                        {content.ref}
                                    </code>
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}
