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
    // Strip 'codex:' prefix (handling duplicates like 'codex:codex:...')
    const id = ref.replace(/^(codex:)+/, '');

    // Call detail endpoint (now supports slashes via backend fix)
    // Backend expects ?ref=codex:...
    // Add 10s timeout to prevent hanging
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    try {
        const response = await fetch(`/api/codex?ref=codex:${id}`, { signal: controller.signal });
        clearTimeout(timeoutId);

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `Failed to fetch codex entry: ${response.statusText}`);
        }

        const data = await response.json();

        // Backend returns { metadata: {...}, content: "..." }
        // We map it to CodexEntry interface: { ref, title, md, path }
        return {
            ref: ref,
            title: data.metadata?.title || data.title || id,
            md: data.md || data.content || data.body_markdown || '',
            path: id
        };
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}

export interface CodexSection {
    world: string;
    section: string;
    pages: {
        id: string;
        title: string;
        world: string;
        section: string;
    }[];
}

export interface CodexIndex {
    sections: CodexSection[];
}

export async function fetchCodexIndex(): Promise<CodexIndex> {
    const response = await fetch('/api/codex/index/structure');
    if (!response.ok) {
        throw new Error(`Failed to fetch codex index: ${response.statusText}`);
    }
    return await response.json();
}
