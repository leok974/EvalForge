import React, { useState, useEffect } from 'react';
import { Search, Play, CheckCircle, XCircle, Loader, PlayCircle } from 'lucide-react';
import {
    getQASummary, getQAQuests, QASummary, QuestHealth,
    runQATest, pollQARun, QARunResponse,
    runBatchQATest, pollBatchQARun, getBatchQuestResults, QABatchRun
} from '../lib/qaApi';

export default function DevQA() {
    const [summary, setSummary] = useState<QASummary | null>(null);
    const [quests, setQuests] = useState<QuestHealth[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Run state
    const [selectedQuest, setSelectedQuest] = useState<QuestHealth | null>(null);
    const [activeRun, setActiveRun] = useState<QARunResponse | null>(null);
    const [runningQuests, setRunningQuests] = useState<Set<string>>(new Set());

    // Batch run state (Phase 8.1)
    const [batchRun, setBatchRun] = useState<QABatchRun | null>(null);
    const [showBatchModal, setShowBatchModal] = useState(false);
    const [batchResults, setBatchResults] = useState<any>(null);

    // Filters
    const [searchQuery, setSearchQuery] = useState('');
    const [worldFilter, setWorldFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState('');

    useEffect(() => {
        loadData();
    }, [worldFilter, statusFilter, searchQuery]);

    async function loadData() {
        try {
            setLoading(true);
            const [summaryData, questsData] = await Promise.all([
                getQASummary(),
                getQAQuests({
                    world_id: worldFilter || undefined,
                    status: statusFilter || undefined,
                    q: searchQuery || undefined
                })
            ]);

            setSummary(summaryData);
            setQuests(questsData.quests);
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load QA data');
            console.error('QA Dashboard error:', err);
        } finally {
            setLoading(false);
        }
    }

    async function handleRunTest(quest: QuestHealth, variant: 'starter' | 'solution' | 'integrity') {
        try {
            setRunningQuests(prev => new Set(prev).add(quest.slug));
            setSelectedQuest(quest);

            const { run_id } = await runQATest({ quest_id: quest.slug, variant });

            // Poll for updates
            await pollQARun(run_id, (run) => {
                setActiveRun(run);
            });

            // Refresh quest list after completion
            await loadData();
            setRunningQuests(prev => {
                const next = new Set(prev);
                next.delete(quest.slug);
                return next;
            });
        } catch (err) {
            console.error('Run test error:', err);
            setError(err instanceof Error ? err.message : 'Failed to run test');
            setRunningQuests(prev => {
                const next = new Set(prev);
                next.delete(quest.slug);
                return next;
            });
        }
    }

    async function handleRunTrack() {
        if (!worldFilter) {
            setError('Please select a world to run batch tests');
            return;
        }

        try {
            setError(null);
            const batch = await runBatchQATest(worldFilter, undefined, 'integrity');
            setBatchRun(batch);
            setShowBatchModal(true);
            setBatchResults(null);

            // Poll for progress
            await pollBatchQARun(batch.batch_id, (updatedBatch) => {
                setBatchRun(updatedBatch);
            });

            // Fetch detailed results
            const results = await getBatchQuestResults(batch.batch_id);
            setBatchResults(results);

            // Refresh quest list after completion
            await loadData();
        } catch (err) {
            console.error('Batch run error:', err);
            setError(err instanceof Error ? err.message : 'Failed to run batch test');
            setShowBatchModal(false);
        }
    }

    const getStatusBadge = (status: string) => {
        const styles = {
            healthy: 'bg-green-500/20 text-green-400 border-green-500/30',
            unhealthy: 'bg-red-500/20 text-red-400 border-red-500/30',
            running: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
            unknown: 'bg-gray-500/20 text-gray-400 border-gray-500/30'
        };

        return (
            <span className={`px-2 py-1 rounded text-xs border ${styles[status as keyof typeof styles] || styles.unknown}`}>
                {status.toUpperCase()}
            </span>
        );
    };

    if (loading && !summary) {
        return (
            <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto mb-4"></div>
                    <p className="text-gray-400">Loading QA Dashboard...</p>
                </div>
            </div>
        );
    }

    if (error && !summary) {
        return (
            <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
                <div className="text-center">
                    <p className="text-red-400 mb-4">❌ {error}</p>
                    <button
                        onClick={() => loadData()}
                        className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded transition"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-950 text-white p-6">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">Quest QA Dashboard</h1>
                <p className="text-gray-400">Content health monitoring and on-demand testing</p>
            </div>

            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                    <div className="text-gray-400 text-sm mb-1">Total Quests</div>
                    <div className="text-3xl font-bold">{summary?.global.quests_total || 0}</div>
                </div>

                <div className="bg-gray-900 border border-green-500/30 rounded-lg p-6">
                    <div className="text-gray-400 text-sm mb-1">Healthy</div>
                    <div className="text-3xl font-bold text-green-400">{summary?.global.healthy || 0}</div>
                </div>

                <div className="bg-gray-900 border border-red-500/30 rounded-lg p-6">
                    <div className="text-gray-400 text-sm mb-1">Unhealthy</div>
                    <div className="text-3xl font-bold text-red-400">{summary?.global.unhealthy || 0}</div>
                </div>

                <div className="bg-gray-900 border border-gray-500/30 rounded-lg p-6">
                    <div className="text-gray-400 text-sm mb-1">Unknown</div>
                    <div className="text-3xl font-bold text-gray-400">{summary?.global.unknown || 0}</div>
                </div>
            </div>

            {/* Filters */}
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 mb-6 flex flex-wrap gap-4">
                <div className="flex-1 min-w-[200px]">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search quests..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full bg-gray-800 border border-gray-700 rounded px-10 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
                        />
                    </div>
                </div>

                <select
                    value={worldFilter}
                    onChange={(e) => setWorldFilter(e.target.value)}
                    className="bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
                >
                    <option value="">All Worlds</option>
                    <option value="foundry">Foundry</option>
                    <option value="prism">Prism</option>
                    <option value="synapse">Synapse</option>
                </select>

                <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
                >
                    <option value="">All Status</option>
                    <option value="healthy">Healthy</option>
                    <option value="unhealthy">Unhealthy</option>
                    <option value="unknown">Unknown</option>
                </select>

                {/* Run Track Button */}
                <button
                    onClick={handleRunTrack}
                    disabled={!worldFilter || showBatchModal}
                    className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded flex items-center gap-2 transition"
                    title={!worldFilter ? 'Select a world first' : 'Run integrity check on all quests in world'}
                >
                    <PlayCircle className="w-4 h-4" />
                    Run World
                </button>
            </div>

            {/* Batch Progress Modal */}
            {showBatchModal && batchRun && (
                <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
                    <div className="bg-gray-900 border border-gray-700 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-auto">
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-4">World Integrity Check</h3>
                            <p className="text-gray-400 mb-4">
                                {batchRun.world_id} {batchRun.track_id && `/ ${batchRun.track_id}`}
                            </p>

                            {/* Progress Bar */}
                            <div className="mb-6">
                                <div className="flex justify-between text-sm text-gray-400 mb-2">
                                    <span>{batchRun.completed_quests} / {batchRun.total_quests} complete</span>
                                    <span>{batchRun.progress_percent}%</span>
                                </div>
                                <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                                    <div
                                        className="bg-cyan-500 h-full transition-all duration-300"
                                        style={{ width: `${batchRun.progress_percent}%` }}
                                    />
                                </div>
                            </div>

                            {/* Results Summary */}
                            {batchRun.status === 'finished' && (
                                <div className="space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="bg-green-500/10 border border-green-500/30 rounded p-4">
                                            <div className="text-green-400 text-2xl font-bold">{batchRun.passed_count}</div>
                                            <div className="text-gray-400 text-sm">Passed</div>
                                        </div>
                                        <div className="bg-red-500/10 border border-red-500/30 rounded p-4">
                                            <div className="text-red-400 text-2xl font-bold">{batchRun.failed_count}</div>
                                            <div className="text-gray-400 text-sm">Failed</div>
                                        </div>
                                    </div>

                                    {/* Per-quest results */}
                                    {batchResults && batchResults.quests.length > 0 && (
                                        <div>
                                            <h4 className="font-semibold mb-2">Quest Details:</h4>
                                            <div className="space-y-2 max-h-60 overflow-y-auto">
                                                {batchResults.quests.map((q: any) => (
                                                    <div
                                                        key={q.quest_slug}
                                                        className={`p-3 rounded border ${q.passed
                                                                ? 'bg-green-500/5 border-green-500/30'
                                                                : 'bg-red-500/5 border-red-500/30'
                                                            }`}
                                                    >
                                                        <div className="flex items-start gap-2">
                                                            {q.passed ? <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" /> : <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />}
                                                            <div className="flex-1 min-w-0">
                                                                <div className="font-mono text-sm">{q.quest_slug}</div>
                                                                {!q.passed && q.issues.length > 0 && (
                                                                    <ul className="mt-2 space-y-1 text-xs text-red-300">
                                                                        {q.issues.map((issue: string, i: number) => (
                                                                            <li key={i}>• {issue}</li>
                                                                        ))}
                                                                    </ul>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Loading state */}
                            {batchRun.status === 'running' && (
                                <div className="text-center py-8">
                                    <Loader className="w-8 h-8 text-cyan-500 animate-spin mx-auto mb-2" />
                                    <p className="text-gray-400">Running tests...</p>
                                </div>
                            )}

                            {/* Close button */}
                            <div className="mt-6 flex justify-end">
                                <button
                                    onClick={() => setShowBatchModal(false)}
                                    className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded transition"
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Quest Grid */}
            <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-800 border-b border-gray-700">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Quest</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">World/Track</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Language</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Last Run</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                        {quests.length === 0 ? (
                            <tr>
                                <td colSpan={6} className="px-6 py-8 text-center text-gray-400">
                                    No quests found matching filters
                                </td>
                            </tr>
                        ) : (
                            quests.map((quest) => (
                                <tr key={quest.slug} className="hover:bg-gray-800/50 transition">
                                    <td className="px-6 py-4">
                                        <div className="font-medium">{quest.title}</div>
                                        <div className="text-sm text-gray-500">{quest.slug}</div>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-400">
                                        {quest.world_id} / {quest.track_id}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-400">
                                        {quest.language}
                                    </td>
                                    <td className="px-6 py-4">
                                        {getStatusBadge(quest.health_status)}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-400">
                                        {quest.last_run_at ? new Date(quest.last_run_at).toLocaleString() : 'Never'}
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex gap-2">
                                            {runningQuests.has(quest.slug) ? (
                                                <div className="flex items-center gap-2 text-yellow-400">
                                                    <Loader className="w-4 h-4 animate-spin" />
                                                    <span className="text-xs">Running...</span>
                                                </div>
                                            ) : (
                                                <button
                                                    onClick={() => handleRunTest(quest, 'integrity')}
                                                    className="px-3 py-1 bg-cyan-600 hover:bg-cyan-700 rounded text-xs transition flex items-center gap-1"
                                                    title="Run Integrity Check"
                                                >
                                                    <Play className="w-3 h-3" />
                                                    Integrity
                                                </button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Results Modal */}
            {activeRun && selectedQuest && (
                <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-6" onClick={() => setActiveRun(null)}>
                    <div className="bg-gray-900 border border-gray-800 rounded-lg max-w-4xl w-full max-h-[80vh] overflow-auto" onClick={e => e.stopPropagation()}>
                        <div className="p-6 border-b border-gray-800 flex items-center justify-between">
                            <div>
                                <h2 className="text-xl font-bold">{selectedQuest.title}</h2>
                                <p className="text-sm text-gray-400">{activeRun.variant.toUpperCase()} Test Results</p>
                            </div>
                            <button onClick={() => setActiveRun(null)} className="text-gray-400 hover:text-white">✕</button>
                        </div>

                        <div className="p-6 space-y-4">
                            {/* Status */}
                            <div className="flex items-center gap-4">
                                <div className="flex items-center gap-2">
                                    {activeRun.result?.passed ? (
                                        <CheckCircle className="w-6 h-6 text-green-400" />
                                    ) : (
                                        <XCircle className="w-6 h-6 text-red-400" />
                                    )}
                                    <span className={`font-medium ${activeRun.result?.passed ? 'text-green-400' : 'text-red-400'}`}>
                                        {activeRun.result?.passed ? 'PASSED' : 'FAILED'}
                                    </span>
                                </div>
                                {activeRun.duration_ms && (
                                    <span className="text-sm text-gray-400">
                                        Duration: {activeRun.duration_ms}ms
                                    </span>
                                )}
                            </div>

                            {/* Issues (for integrity checks) */}
                            {activeRun.result?.issues && activeRun.result.issues.length > 0 && (
                                <div className="bg-red-500/10 border border-red-500/30 rounded p-4">
                                    <h3 className="font-medium text-red-400 mb-2">Issues Found:</h3>
                                    <ul className="list-disc list-inside space-y-1">
                                        {activeRun.result.issues.map((issue: string, i: number) => (
                                            <li key={i} className="text-sm text-red-300">{issue}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Logs */}
                            {activeRun.logs && (
                                <div>
                                    <h3 className="font-medium mb-2">Output:</h3>
                                    <pre className="bg-gray-950 border border-gray-800 rounded p-4 text-xs overflow-auto max-h-60">
                                        {activeRun.logs}
                                    </pre>
                                </div>
                            )}

                            {/* Raw Result (for debugging) */}
                            <details className="text-sm">
                                <summary className="cursor-pointer text-gray-400 hover:text-white">View Raw Result JSON</summary>
                                <pre className="bg-gray-950 border border-gray-800 rounded p-4 text-xs overflow-auto mt-2">
                                    {JSON.stringify(activeRun.result, null, 2)}
                                </pre>
                            </details>
                        </div>

                        <div className="p-6 border-t border-gray-800 flex justify-end gap-3">
                            <button
                                onClick={() => setActiveRun(null)}
                                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded transition"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
