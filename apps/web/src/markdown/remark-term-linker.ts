import { visit } from 'unist-util-visit';
import { u } from 'unist-builder';
import type { Node, Parent } from 'unist';

interface KeyTerm {
    id: string;
    term: string;
    codex_ref?: string;
}

interface Options {
    keyTerms: KeyTerm[];
}

export function remarkTermLinker(options: Options) {
    const { keyTerms } = options;

    // Build matcher regex once
    // Sort by length desc to match longest terms first
    const sortedTerms = [...keyTerms]
        .filter(t => t.term && t.codex_ref)
        .sort((a, b) => b.term.length - a.term.length);

    return (tree: Node) => {
        visit(tree, 'text', (node: any, index: number | undefined, parent: Parent | undefined) => {
            if (!parent || index === undefined) return;

            // Skip if parent is already a link or code
            if (
                parent.type === 'link' ||
                parent.type === 'linkReference' ||
                parent.type === 'code' ||
                parent.type === 'inlineCode' ||
                parent.type === 'termLink' || // Don't nest
                parent.type === 'heading' // Don't link in headings (Phase 9.4-C)
            ) {
                return;
            }

            const value = node.value as string;
            if (!value) return;

            // Find first matching term
            let bestMatch: { term: KeyTerm; index: number } | null = null;

            for (const termObj of sortedTerms) {
                const escaped = termObj.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(`\\b${escaped}(s?)\\b`, 'i');
                const match = regex.exec(value);
                if (match) {
                    if (!bestMatch || match.index < bestMatch.index) {
                        bestMatch = { term: termObj, index: match.index };
                    }
                }
            }

            if (bestMatch) {
                const termObj = bestMatch.term;
                const escaped = termObj.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(`\\b${escaped}(s?)\\b`, 'i');
                const match = regex.exec(value);

                if (!match) return;

                const startIndex = match.index;
                const endIndex = startIndex + match[0].length;

                const before = value.slice(0, startIndex);
                const matchedText = value.slice(startIndex, endIndex);
                const after = value.slice(endIndex);

                const newNodes: Node[] = [];

                if (before) {
                    newNodes.push(u('text', before));
                }

                newNodes.push(u('termLink', {
                    term: termObj.term,
                    codexRef: termObj.codex_ref,
                    children: [u('text', matchedText)]
                }));

                if (after) {
                    newNodes.push(u('text', after));
                }

                parent.children.splice(index, 1, ...newNodes);

                // Resume visitation at the 'after' node (or next node if no after)
                // If we inserted [before, link, after], after is at index + 2.
                // If we inserted [link, after], after is at index + 1.
                // Generally, after is at index + newNodes.length - 1.
                // If we return this index, visitor visits it next.
                return index + newNodes.length - (after ? 1 : 0);
            }
        });
    };
}
