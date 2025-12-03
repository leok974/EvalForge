import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useGameStore } from '../store/gameStore';
import { getProjectCodexProjects, getProjectCodexBundle, ProjectCodexSummary, ProjectCodexBundle, ProjectCodexDoc } from '../lib/projectCodexApi';
import { TagPill } from './ui/TagPill';

// Types for System Codex
interface CodexEntry {
    id: string;
    title: string;
    world: string;
    tags: string[];
    source?: string;
    project_id?: string;
}

interface CodexContent {
    metadata: CodexEntry;
    content: string;
}

// Types for Project Codex
type DocType = 'overview' | 'architecture' | 'data_model' | 'infra' | 'observability' | 'agents' | 'quest_hooks';

type Mode = 'project-list' | 'project-detail';

interface Props {
    isOpen: boolean;
    onClose: () => void;
    currentWorldId: string;
}

export function CodexDrawer({ isOpen, onClose, currentWorldId }: Props) {
    // System Codex State
    const [index, setIndex] = useState<CodexEntry[]>([]);
    const [selectedEntry, setSelectedEntry] = useState<CodexContent | null>(null);
    const [selectedWorld, setSelectedWorld] = useState<string>('All');

    // Project Codex State
    const [mode, setMode] = useState<Mode>('project-list');
    const [selectedProject, setSelectedProject] = useState<ProjectCodexSummary | null>(null);
    const [activeTab, setActiveTab] = useState<DocType>('overview');
    const [projectBundle, setProjectBundle] = useState<ProjectCodexBundle | null>(null);
    const [projects, setProjects] = useState<ProjectCodexSummary[]>([]);

    // Shared State
    const [loading, setLoading] = useState(false);
    const [activeTopTab, setActiveTopTab] = useState<'system' | 'project'>('system');

    const addXp = useGameStore((s) => s.addXp);

    // Fetch System Codex Index
    useEffect(() => {
        if (isOpen && activeTopTab === 'system') {
            setLoading(true);
            fetch(`/api/codex`)
                .then(res => res.json())
                .then(data => {
                    setIndex(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error(err);
                    setLoading(false);
                });
        }
    }, [isOpen, activeTopTab]);

    // Fetch Project Codex List
    useEffect(() => {
        if (isOpen && activeTopTab === 'project' && mode === 'project-list') {
            setLoading(true);
            getProjectCodexProjects()
                .then(data => {
                    setProjects(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error(err);
                    setLoading(false);
                });
        }
    }, [isOpen, activeTopTab, mode]);

    // Load System Codex Entry
    const loadEntry = (id: string) => {
        setLoading(true);
        fetch(`/api/codex/${id}`)
            .then(res => res.json())
            .then(data => {
                setSelectedEntry(data);
                setLoading(false);
            })
            .catch(console.error);
    };

    // Load Project Bundle
    const handleOpenProject = async (project: ProjectCodexSummary) => {
        setSelectedProject(project);
        setMode('project-detail');
        setActiveTab('overview');
        setLoading(true);

        try {
            const bundle = await getProjectCodexBundle(project.slug);
            setProjectBundle(bundle);
            setLoading(false);
        } catch (err) {
            console.error(err);
            setLoading(false);
        }
    };

    const handleBackToProjects = () => {
        setMode('project-list');
        setSelectedProject(null);
        setProjectBundle(null);
    };

    const handleBackToIndex = () => {
        setSelectedEntry(null);
    };

    //Filter System Codex
    const filteredEntries = index.filter(entry => {
        if (activeTopTab === 'system') {
            if (entry.source === 'project') return false;
            if (selectedWorld !== 'All' && entry.world !== selectedWorld && entry.world !== 'general') return false;
            return true;
        }
        return false;
    });

    // Label for doc type tabs
    const labelForDocType = (docType: string): string => {
        const labels: Record<string, string> = {
            'overview': 'Overview',
            'architecture': 'Architecture',
            'data_model': 'Data Model',
            'infra': 'Infra',
            'observability': 'Observability',
            'agents': 'Agents',
            'quest_hooks': 'Quest Hooks'
        };
        return labels[docType] || docType;
    };

    // Markdown Components
    const MarkdownComponents = {
        code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
                <div className="relative group">
                    <div className="absolute top-0 right-0 bg-zinc-800 text-[10px] px-2 py-1 text-zinc-400 rounded-bl opacity-0 group-hover:opacity-100 transition-opacity uppercase">
                        {match[1]}
                    </div>
                    <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                            margin: '1rem 0',
                            borderRadius: '0.5rem',
                            backgroundColor: '#09090b',
                            border: '1px solid #27272a',
                            fontSize: '0.8rem',
                        }}
                        {...props}
                    >
                        {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                </div>
            ) : (
                <code className="bg-zinc-900 px-1.5 py-0.5 rounded text-cyan-400 text-xs border border-zinc-800" {...props}>
                    {children}
                </code>
            );
        },
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-zinc-950 border border-zinc-800 rounded-xl w-full max-w-4xl h-[85vh] shadow-2xl overflow-hidden flex flex-col">

                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                    <h2 className="text-cyan-500 font-bold tracking-wider font-mono flex items-center gap-2">
                        <span className="text-xl">📚</span> CODEX DATABASE
                    </h2>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">✕ ESC</button>
                </div>

                {/* Top-Level Tabs */}
                <div className="flex border-b border-zinc-800">
                    <button
                        onClick={() => {
                            setActiveTopTab('system');
                            setSelectedEntry(null);
                        }}
                        className={`flex-1 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${activeTopTab === 'system' ? 'text-cyan-400 border-b-2 border-cyan-500' : 'text-zinc-500 hover:text-zinc-300'}`}
                    >
                        System Codex
                    </button>
                    <button
                        onClick={() => {
                            setActiveTopTab('project');
                            setMode('project-list');
                            setSelectedEntry(null);
                        }}
                        className={`flex-1 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${activeTopTab === 'project' ? 'text-cyan-400 border-b-2 border-cyan-500' : 'text-zinc-500 hover:text-zinc-300'}`}
                    >
                        Project Codex
                    </button>
                </div>

                {/* Body */}
                <div className="flex-1 overflow-auto p-6">
                    {activeTopTab === 'system' && (
                        <>
                            {!selectedEntry ? (
                                <div>
                                    {/* World Filter */}
                                    <div className="mb-4 flex gap-2 flex-wrap">
                                        {['All', 'world-python', 'world-js', 'world-sql', 'world-git', 'world-infra'].map((w) => (
                                            <button
                                                key={w}
                                                onClick={() => setSelectedWorld(w)}
                                                className={`px-3 py-1 rounded text-xs uppercase tracking-wider transition-colors ${selectedWorld === w ? 'bg-cyan-900 text-cyan-100' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
                                            >
                                                {w}
                                            </button>
                                        ))}
                                    </div>

                                    {/* Entry List */}
                                    <div className="space-y-3">
                                        {filteredEntries.map((entry) => (
                                            <button
                                                key={entry.id}
                                                onClick={() => loadEntry(entry.id)}
                                                className="w-full text-left bg-zinc-900 border border-zinc-800 p-4 rounded-lg hover:border-cyan-700 transition-all group"
                                            >
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <div className="font-bold text-zinc-200 group-hover:text-cyan-400 transition-colors">{entry.title}</div>
                                                        <div className="flex flex-wrap gap-2 mt-2">
                                                            <span className="px-1.5 py-0.5 bg-zinc-950 text-zinc-400 rounded text-[9px] uppercase border border-zinc-800">{entry.world}</span>
                                                            {entry.tags.slice(0, 3).map((tag) => (
                                                                <span key={tag} className="px-1.5 py-0.5 bg-zinc-950 text-green-500 rounded text-[9px]">#{tag}</span>
                                                            ))}
                                                        </div>
                                                    </div>
                                                    <div className="text-cyan-500 group-hover:translate-x-1 transition-transform">→</div>
                                                </div>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    {/* Back Button */}
                                    <button onClick={handleBackToIndex} className="text-xs text-zinc-500 hover:text-zinc-300 mb-4 flex items-center gap-1">
                                        <span>←</span> Back to Index
                                    </button>

                                    {/* Entry Content */}
                                    <div className="prose prose-invert max-w-none">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]} components={MarkdownComponents}>
                                            {selectedEntry.content}
                                        </ReactMarkdown>
                                    </div>
                                </div>
                            )}
                        </>
                    )}

                    {activeTopTab === 'project' && (
                        <>
                            {mode === 'project-list' ? (
                                <div>
                                    <h3 className="text-sm font-semibold tracking-[0.3em] text-zinc-500 mb-4">SELECT A PROJECT</h3>
                                    <div className="space-y-3">
                                        {projects.map((p) => (
                                            <button
                                                key={p.slug}
                                                onClick={() => handleOpenProject(p)}
                                                className="w-full rounded-xl border border-zinc-800 bg-zinc-900/40 px-4 py-3 text-left hover:border-cyan-700 transition-all"
                                            >
                                                <div className="flex items-center justify-between mb-1">
                                                    <span className="text-sm font-medium text-zinc-200">{p.name}</span>
                                                    <span className="text-[10px] uppercase tracking-[0.2em] text-zinc-500">
                                                        {p.codex_status}
                                                    </span>
                                                </div>
                                                <p className="text-xs text-zinc-500 line-clamp-2 mb-2">{p.tagline || 'No description'}</p>
                                                <div className="flex flex-wrap gap-1.5">
                                                    {p.tags.map((tag) => (
                                                        <TagPill key={tag} variant="default" className="text-[9px] px-2 py-0.5">
                                                            {tag}
                                                        </TagPill>
                                                    ))}
                                                </div>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                projectBundle && (
                                    <div className="flex flex-col h-full">
                                        {/* Project Detail Header */}
                                        <div className="flex items-center justify-between mb-3">
                                            <button
                                                className="text-[11px] font-medium text-zinc-500 hover:text-zinc-300 inline-flex items-center gap-1"
                                                onClick={handleBackToProjects}
                                            >
                                                <span>←</span>
                                                <span>Back to Projects</span>
                                            </button>
                                            <div className="flex items-center gap-2">
                                                <span className="text-xs font-semibold text-zinc-300">{projectBundle.project.name}</span>
                                                <div className="flex flex-wrap gap-1">
                                                    {projectBundle.project.worlds?.map((w) => (
                                                        <TagPill key={w} variant="world">
                                                            {w.replace("world-", "").toUpperCase()}
                                                        </TagPill>
                                                    ))}
                                                    <TagPill variant="docType">
                                                        {activeTab.toUpperCase()}
                                                    </TagPill>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Doc Type Tabs */}
                                        <div className="flex gap-2 mb-4 border-b border-zinc-800 overflow-x-auto pb-2">
                                            {(['overview', 'architecture', 'data_model', 'infra', 'observability', 'agents', 'quest_hooks'] as DocType[]).map((tab) => {
                                                const hasDoc = projectBundle.docs.some((d) => d.doc_type === tab);
                                                return (
                                                    <button
                                                        key={tab}
                                                        disabled={!hasDoc}
                                                        onClick={() => setActiveTab(tab)}
                                                        className={`pb-2 px-3 text-xs uppercase tracking-[0.2em] whitespace-nowrap transition-colors ${activeTab === tab ? 'border-b-2 border-cyan-500 text-cyan-400' : hasDoc ? 'text-zinc-500 hover:text-zinc-300' : 'text-zinc-700 cursor-not-allowed'
                                                            }`}
                                                    >
                                                        {labelForDocType(tab)}
                                                    </button>
                                                );
                                            })}
                                        </div>

                                        {/* Doc Content */}
                                        <div className="flex-1 overflow-auto">
                                            {(() => {
                                                const activeDoc = projectBundle.docs.find((d) => d.doc_type === activeTab);
                                                if (activeDoc) {
                                                    return (
                                                        <div className="prose prose-invert max-w-none text-xs leading-relaxed">
                                                            <ReactMarkdown remarkPlugins={[remarkGfm]} components={MarkdownComponents}>
                                                                {activeDoc.body_md}
                                                            </ReactMarkdown>
                                                        </div>
                                                    );
                                                } else {
                                                    return (
                                                        <div className="text-xs text-zinc-600 italic">
                                                            No documentation yet for this section. Seed a <code className="bg-zinc-900 px-1.5 py-0.5 rounded text-cyan-500">doc_type: {activeTab}</code> doc for <code className="bg-zinc-900 px-1.5 py-0.5 rounded text-cyan-500">{projectBundle.project.slug}</code>.
                                                        </div>
                                                    );
                                                }
                                            })()}
                                        </div>
                                    </div>
                                )
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
