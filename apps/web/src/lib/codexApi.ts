/**
 * Phase 9.1: Codex API Client
 * Fetch Codex documentation entries safely
 */

export interface CodexEntry {
    ref: string;
    title: string;
    md: string;
    path: string;
}

/**
 * Fetch a Codex entry by reference
 * @param ref - Codex reference (e.g., "codex:glossary/python/print")
 * @returns Codex entry with markdown content
 */
export async function fetchCodex(ref: string): Promise<CodexEntry> {
    const response = await fetch(`/api/codex?ref=${encodeURIComponent(ref)}`);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `Failed to fetch codex entry: ${response.statusText}`);
    }

    return response.json();
}
