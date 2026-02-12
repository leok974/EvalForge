// TS Generics
// Implement a typed pick() helper using keyof + generics.

export function pick<T extends object, K extends keyof T>(
    obj: T,
    keys: readonly K[]
): Pick<T, K> {
    // TODO: build a new object containing only these keys
    const out = {} as Pick<T, K>;

    for (const k of keys) {
        out[k] = obj[k];
    }

    return out;
}
