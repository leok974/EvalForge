export async function safeJson<T>(res: Response): Promise<{ ok: boolean; status: number; data: T | null; raw?: string | null }> {
    const text = await res.text();
    let data: T | null = null;
    try {
        if (text) data = JSON.parse(text);
    } catch (e) {
        // Parsing failed
    }

    if (!res.ok) {
        // Even if we parsed JSON error details, overall success is false
        return { ok: false, status: res.status, data, raw: data ? null : text };
    }

    // Success case
    return { ok: true, status: res.status, data, raw: null };
}
