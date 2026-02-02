import { visit } from 'unist-util-visit';
import { u } from 'unist-builder';
import type { Node, Parent } from 'unist';

export function remarkCoachCallouts() {
    return (tree: Node) => {
        visit(tree, 'heading', (node: any, index: number | undefined, parent: Parent | undefined) => {
            if (!parent || index === undefined) return;

            // Ensure strictly 7-section template headings match if needed, 
            // but for now we look for specific strings.
            const children = node.children || [];
            const textNode = children.find((c: any) => c.type === 'text');
            if (!textNode) return;

            const headingText = (textNode.value as string).trim().toLowerCase();
            let variant: 'info' | 'warning' | null = null;
            let title = '';

            if (headingText.includes('common mistakes')) {
                variant = 'warning';
                title = 'Common Mistakes';
            } else if (headingText.includes('run vs submit')) {
                variant = 'info';
                title = 'Run vs Submit';
            }

            if (variant) {
                // Found a target header.
                // We want to wrap this header and all subsequent siblings UNTIL the next header 
                // of the same or lower depth (higher precedence).

                const depth = node.depth;
                const siblings = parent.children;
                const start = index; // Include the header inside the callout? or just body?
                // Usually callout has a title. If we include header, we can use it as title logic or hide it.
                // Let's include the header so the Callout component can decide (or we strip it).
                // Actually, "Smart styling" says: "detect heading... wrap section body".
                // Let's wrap everything including the header, but maybe the Callout component handles specific rendering.
                // Or better: valid Markdown structure usually implies the header starts the section.

                let end = start + 1;
                while (end < siblings.length) {
                    const sibling = siblings[end];
                    if (sibling.type === 'heading' && (sibling as any).depth <= depth) {
                        break;
                    }
                    end++;
                }

                // Extract nodes to wrap
                const nodesToWrap = siblings.slice(start + 1, end); // Exclude header from content, use header as Title trigger

                // If we want to hide the original header, we can remove it or replace it.
                // Let's replace the header + body with a callout node.

                const calloutNode = u('callout', {
                    variant,
                    title,
                    children: nodesToWrap
                });

                // Replace [header, ...body] with [callout]
                parent.children.splice(start, (end - start), calloutNode);

                // Skip the new node
                return index + 1;
            }
        });
    };
}
