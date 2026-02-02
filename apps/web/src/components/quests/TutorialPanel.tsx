/**
 * Phase 9.1: Tutorial Panel Component
 * Renders quest tutorials with key terms and Codex links
 */
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { remarkTermLinker } from '../../markdown/remark-term-linker';
import { remarkCoachCallouts } from '../../markdown/remark-coach-callouts';
import { TermLink } from '../markdown/TermLink';
import { Callout } from '../markdown/Callout';
import { CodeBlock } from '../markdown/CodeBlock';

export interface KeyTerm {
    id: string;
    term: string;
    one_liner?: string;
    codex_ref?: string;
    tags?: string[];
}

export interface TutorialPanelProps {
    tutorialMd: string;
    keyTerms: KeyTerm[];
    codexRefs: string[];
    onOpenCodexRef: (ref: string) => void;
    onPasteCode?: (code: string) => void;
}

export function TutorialPanel({
    tutorialMd,
    keyTerms,
    codexRefs,
    onOpenCodexRef,
    onPasteCode
}: TutorialPanelProps) {
    // Memoize plugins to avoid re-creating on every render
    const plugins = React.useMemo(() => {
        return [
            remarkGfm,
            [remarkTermLinker, { keyTerms }],
            remarkCoachCallouts
        ];
    }, [keyTerms]);

    const components = React.useMemo(() => ({
        // Custom Code Block (with Copy + optional Paste)
        code({ node, inline, className, children, ...props }: any) {
            if (inline) {
                return (
                    <code className={className} {...props}>
                        {children}
                    </code>
                );
            }
            return (
                <CodeBlock
                    className={className}
                    onPaste={onPasteCode ? () => onPasteCode(String(children).replace(/\n$/, '')) : undefined}
                    canPaste={!!onPasteCode}
                    {...props}
                >
                    {children}
                </CodeBlock>
            );
        },
        // Custom Term Links (from remark-term-linker)
        termLink({ term, codexRef, children }: any) {
            return (
                <TermLink
                    term={term}
                    codexRef={codexRef}
                    onOpenCodex={(ref) => {
                        console.log('🔗 CLICKED TERM LINK:', ref);
                        if (onOpenCodexRef) onOpenCodexRef(ref);
                    }}
                >
                    {children}
                </TermLink>
            );
        },
        // Custom Callouts (from remark-coach-callouts)
        callout({ variant, title, children }: any) {
            return (
                <Callout variant={variant} title={title}>
                    {children}
                </Callout>
            );
        }
    }), [onPasteCode, onOpenCodexRef]);

    return (
        <div className="tutorial-panel overflow-y-auto p-6 max-w-4xl mx-auto">
            {/* Tutorial Markdown */}
            <div className="prose prose-sm max-w-none dark:prose-invert mb-8">
                <ReactMarkdown
                    remarkPlugins={plugins as any}
                    components={components as any}
                >
                    {tutorialMd}
                </ReactMarkdown>
            </div>

            {/* Key Terms Section */}
            {keyTerms && keyTerms.length > 0 && (
                <div className="mb-8">
                    <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
                        Key Terms
                    </h3>
                    <div className="flex flex-wrap gap-2">
                        {keyTerms.map((term) => (
                            <button
                                key={term.id}
                                onClick={() => term.codex_ref && onOpenCodexRef(term.codex_ref)}
                                className="px-3 py-2 bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-200 dark:hover:bg-blue-900/50 
                           text-blue-900 dark:text-blue-100 rounded-lg transition-colors
                           cursor-pointer group relative"
                                title={term.one_liner}
                                disabled={!term.codex_ref}
                            >
                                <span className="font-medium">{term.term}</span>
                                {term.one_liner && (
                                    <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 
                                   px-3 py-2 bg-gray-900 text-white text-xs rounded whitespace-nowrap
                                   opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none
                                   max-w-xs z-50">
                                        {term.one_liner}
                                    </span>
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Codex References Section */}
            {codexRefs && codexRefs.length > 0 && (
                <div>
                    <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
                        Related Codex Entries
                    </h3>
                    <div className="flex flex-col gap-2">
                        {codexRefs.map((ref) => {
                            // Extract display name from ref (e.g., "glossary/python/print" -> "print")
                            const displayName = ref.split('/').pop()?.replace(/-/g, ' ') || ref;

                            return (
                                <button
                                    key={ref}
                                    onClick={() => onOpenCodexRef(`codex:${ref}`)}
                                    className="text-left px-4 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700
                             rounded-lg transition-colors flex items-center gap-2"
                                >
                                    <svg
                                        className="w-4 h-4 text-gray-600 dark:text-gray-400"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                                        />
                                    </svg>
                                    <span className="text-gray-900 dark:text-gray-100 capitalize">{displayName}</span>
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}
