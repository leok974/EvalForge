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
                parent.type === 'termLink' // Don't nest
            ) {
                return;
            }

            const value = node.value as string;
            if (!value) return;

            // Find first matching term
            // We process one match per text node to avoid complexity, 
            // relying on re-visiting if we wanted exhaustiveness, but simple replacement is safer.
            // Actually, to handle multiple terms in one text node, we need to split the node.

            let bestMatch: { term: KeyTerm; index: number } | null = null;

            for (const termObj of sortedTerms) {
                // Simple case-insensitive match with boundary checks
                // We want to match "Term" or "terms" (plural)
                const escaped = termObj.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                // Bound by non-word chars or start/end of string
                const regex = new RegExp(`\\b${escaped}(s?)\\b`, 'i');

                const match = regex.exec(value);
                if (match) {
                    // If we found a match earlier in the string than current best, or same pos but longer
                    if (!bestMatch || match.index < bestMatch.index) {
                        bestMatch = { term: termObj, index: match.index };
                    }
                }
            }

            if (bestMatch) {
                const termObj = bestMatch.term;
                const escaped = termObj.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(`\\b${escaped}(s?)\\b`, 'i');
                const match = regex.exec(value); // Re-exec to get details

                if (!match) return; // Should not happen

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
                    children: [u('text', matchedText)] // Keep original casing/plurality
                }));

                if (after) {
                    newNodes.push(u('text', after));
                }

                // Replace current node with new nodes
                parent.children.splice(index, 1, ...newNodes);

                // Return index + newNodes.length to skip over the nodes we just added
                // (wrapping the matched term prevents infinite recursion on it)
                return index + newNodes.length;
            }
        });
    };
}
