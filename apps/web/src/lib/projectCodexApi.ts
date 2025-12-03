/**
 * API helpers for Project Codex
 */

export interface ProjectCodexSummary {
    slug: string;
    name: string;
    tagline: string;
    worlds: string[];
    tags: string[];
    doc_types: string[];
    codex_status: "complete" | "partial" | "missing_docs";
}

export interface ProjectCodexDoc {
    doc_type: string;
    title: string;
    body_md: string;
    tags: string[];
}

export interface ProjectCodexBundle {
    project: ProjectCodexSummary;
    docs: ProjectCodexDoc[];
}

export async function getProjectCodexProjects(): Promise<ProjectCodexSummary[]> {
    const res = await fetch('/api/project_codex/projects');
    if (!res.ok) {
        throw new Error(`Failed to fetch projects: ${res.statusText}`);
    }
    return res.json();
}

export async function getProjectCodexBundle(slug: string): Promise<ProjectCodexBundle> {
    const res = await fetch(`/api/project_codex/projects/${slug}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch project bundle for ${slug}: ${res.statusText}`);
    }
    return res.json();
}
