
import { useCallback, useState } from "react";
import {
    submitQuestSolution,
    QuestSubmitResult,
} from "@/lib/questsApi";
import {
    broadcastQuestUpdate,
    broadcastQuestUnlocks,
} from "@/lib/questsEvents";

import { useGameStore } from "@/store/gameStore";

interface UseQuestSubmissionOptions {
    questSlug: string | null;
    defaultLanguage?: string;
}

export function useQuestSubmission(opts: UseQuestSubmissionOptions) {
    const { questSlug, defaultLanguage } = opts;
    const setBossesUnlocked = useGameStore((state) => state.setBossesUnlocked);

    const [loading, setLoading] = useState(false);
    const [lastResult, setLastResult] = useState<QuestSubmitResult | null>(
        null
    );
    const [error, setError] = useState<string | null>(null);

    const submit = useCallback(
        async (code: string, language?: string) => {
            if (!questSlug) {
                setError("No active quest selected.");
                return;
            }
            setLoading(true);
            setError(null);
            try {
                const result = await submitQuestSolution(
                    questSlug,
                    code,
                    language ?? defaultLanguage
                );
                setLastResult(result);

                // Broadcast to QuestBoard / others
                broadcastQuestUpdate(result.quest);

                if (result.unlock_events && result.unlock_events.length > 0) {
                    broadcastQuestUnlocks(result.quest, result.unlock_events);
                }

                // Sync profile flags (bosses unlocked)
                if (result.profile?.flags?.bosses_unlocked) {
                    const bosses = result.profile.flags.bosses_unlocked as string[];
                    setBossesUnlocked(bosses);
                }

                return result;
            } catch (err: any) {
                console.error("Quest submission failed", err);
                setError(err.message ?? "Submission failed");
                throw err;
            } finally {
                setLoading(false);
            }
        },
        [questSlug, defaultLanguage]
    );

    return {
        submit,
        loading,
        lastResult,
        error,
    };
}
