
import { useState, useCallback, useRef } from 'react';
import { useQuestStore } from '../store/questStore';
import { fetchCoachFeedback, CoachResponse, CoachRequest } from '../lib/coachApi';
import { useParams } from 'react-router-dom';

type CoachMode = 'explain' | 'debug';

interface UseCoachResult {
    data: CoachResponse | null;
    loading: boolean;
    error: string | null;
    invoke: () => Promise<void>;
    clear: () => void;
}

export function useCoach(mode: CoachMode): UseCoachResult {
    const { questId: questSlugFromUrl, worldSlug: worldSlugFromUrl } = useParams<{ questId: string; worldSlug: string }>();
    const [data, setData] = useState<CoachResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Store Access
    const lastRunResult = useQuestStore(s => s.lastRunResult);
    const editorFiles = useQuestStore(s => s.editorFiles);
    const editorActivePath = useQuestStore(s => s.editorActivePath);

    // Get worldSlug from URL or fall back to store
    // This handles both routes: /workshop/quests/:questId (no worldSlug in URL)
    // and /worlds/:worldSlug/quests/:questId (worldSlug in URL)
    const activeWorldSlugFromStore = useQuestStore(s => s.activeWorldSlug);
    const worldSlug = worldSlugFromUrl || activeWorldSlugFromStore;

    // Cache Ref: key -> response
    // Key = `${run_number}:${mode}`
    const cache = useRef<Record<string, CoachResponse>>({});

    const invoke = useCallback(async () => {
        // Validate context when invoked, not on mount
        if (!questSlugFromUrl || !worldSlug) {
            setError("Quest context missing");
            setLoading(false);
            return;
        }

        const runNumber = lastRunResult?.run_number || 'no-run';
        const cacheKey = `${runNumber}:${mode}`;

        if (cache.current[cacheKey]) {
            setData(cache.current[cacheKey]);
            return;
        }

        setLoading(true);
        setError(null);
        setData(null);

        try {
            // Build Context
            // Flatten files to array
            const workspaceFiles = Object.entries(editorFiles).map(([path, f]) => ({
                path,
                content: f.content
            }));

            // Selected path
            const selectedPaths = editorActivePath ? [editorActivePath] : [];

            // Failing tests text construction
            let failingTestsText = "";
            if (lastRunResult?.stderr) failingTestsText += `STDERR:\n${lastRunResult.stderr}\n`;
            if (lastRunResult?.stdout) failingTestsText += `STDOUT:\n${lastRunResult.stdout}\n`;
            if (lastRunResult?.test_summary?.failures) {
                failingTestsText += "\nTEST FAILURES:\n";
                lastRunResult.test_summary.failures.forEach((f: any) => {
                    failingTestsText += `- ${f.name}: ${f.message}\n`;
                });
            }

            const payload: CoachRequest = {
                // Let backend decide or force? User said "Auto mode picks debug if failed"
                // Actually user said: "Auto mode picks debug if last run failed... Cache by ... mode"
                // But the hook takes a specific mode ('explain' or 'debug').
                // If the user clicked "Explain", we should force 'explain'.
                // If the user clicked "Debug", we should force 'debug'.
                // If we want "Auto", we pass 'auto'.
                // The Panel usually knows what it wants.
                // Let's pass the requested mode.
                // UNLESS the prompt implies we should be smart. 
                // "Auto mode picks debug if last run failed" -> This logic is for the 'auto' backend mode.
                // But here we are explicit.
                // Let's pass the mode from the hook arg, but map to schema.
                // Wait, Schema has 'explain' | 'debug' | 'auto'.
                // If I pass 'explain', backend forces explain.
                // I will pass the mode as requested.
                mode: mode === 'debug' ? 'debug' : 'explain',

                world: worldSlug,
                quest_slug: questSlugFromUrl,
                student_mode: true, // Always true in Workshop for now
                runner_result: lastRunResult,
                failing_tests_text: failingTestsText,
                selected_paths: selectedPaths,
                workspace_files: workspaceFiles
            };

            const response = await fetchCoachFeedback(payload);

            // Cache it
            cache.current[cacheKey] = response;
            setData(response);

        } catch (e: any) {
            setError(e.message || "Coach request failed");
        } finally {
            setLoading(false);
        }
    }, [questSlugFromUrl, worldSlug, mode, lastRunResult, editorFiles, editorActivePath]);

    const clear = useCallback(() => {
        setData(null);
        setError(null);
    }, []);

    return { data, loading, error, invoke, clear };
}
