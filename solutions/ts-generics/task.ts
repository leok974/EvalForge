// TS Generics
// Implement a generic pick function that preserves key order.

export function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
    const out = {} as Pick<T, K>;
    for (const k of keys) {
        out[k] = obj[k];
    }
    return out;
}
