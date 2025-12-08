import { useEffect, useState } from "react";
import type { SeniorProgressResponse } from "../types";

export function useSeniorProgress() {
    const [data, setData] = useState<SeniorProgressResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;

        async function run() {
            try {
                setLoading(true);
                const resp = await fetch("http://localhost:8092/api/profile/senior_progress", {
                    // credentials: "include", // Assuming local dev, maybe generic proxy handles this?
                    // Previous components use generic fetch or axios. Assuming proxy setup.
                    // But strict fetch needs full URL if no proxy.
                    // Existing agent is on 8092. Frontend likely proxies or CORS.
                    // I will use /api/ structure assuming proxy.
                });

                // Actually best to check if valid response.
                // If 404/500, handle gracefully.
                if (!resp.ok) {
                    // fallback
                    console.warn("Senior progress fetch failed", resp.status);
                    throw new Error(`Senior progress failed: ${resp.status}`);
                }

                const json = (await resp.json()) as SeniorProgressResponse;
                if (!cancelled) {
                    setData(json);
                }
            } catch (err: any) {
                if (!cancelled) {
                    setError(err?.message ?? "Unknown error");
                }
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        run();
        return () => {
            cancelled = true;
        };
    }, []);

    return { data, loading, error };
}
