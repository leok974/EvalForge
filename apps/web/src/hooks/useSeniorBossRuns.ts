import { useEffect, useState } from "react";
import type { SeniorBossRun, SeniorBossRunsResponse } from "../types";

export function useSeniorBossRuns() {
    const [items, setItems] = useState<SeniorBossRun[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;

        async function run() {
            try {
                setLoading(true);
                const resp = await fetch("http://localhost:8092/api/boss_runs/senior", {
                    // credentials: "include",
                });
                if (!resp.ok) throw new Error(`Boss runs failed: ${resp.status}`);
                const json = (await resp.json()) as SeniorBossRunsResponse;
                if (!cancelled) setItems(json.items);
            } catch (err: any) {
                if (!cancelled) setError(err?.message ?? "Unknown error");
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        run();
        return () => {
            cancelled = true;
        };
    }, []);

    return { items, loading, error };
}
