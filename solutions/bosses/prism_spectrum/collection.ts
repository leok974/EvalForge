export type KeyOf<T, K extends keyof T> = T[K] & (string | number | symbol);

/**
 * pluck: takes an array of objects and returns an array of the selected field.
 */
export function pluck<T, K extends keyof T>(
    items: readonly T[],
    key: K
): Array<T[K]> {
    return items.map((item) => item[key]);
}

/**
 * indexBy: creates a lookup table keyed by a specific property of T.
 */
export function indexBy<T, K extends keyof T>(
    items: readonly T[],
    key: K
): Record<KeyOf<T, K>, T> {
    const result = {} as Record<KeyOf<T, K>, T>;

    for (const item of items) {
        const id = item[key] as KeyOf<T, K>;
        result[id] = item;
    }

    return result;
}

/**
 * groupBy: groups items into arrays keyed by a specific property.
 */
export function groupBy<T, K extends keyof T>(
    items: readonly T[],
    key: K
): Record<KeyOf<T, K>, T[]> {
    const result = {} as Record<KeyOf<T, K>, T[]>;

    for (const item of items) {
        const id = item[key] as KeyOf<T, K>;
        if (!result[id]) {
            result[id] = [];
        }
        result[id].push(item);
    }

    return result;
}

/**
 * mergeById: merges two collections by id, preferring incoming entries
 * but preserving existing fields via shallow merge.
 */
export function mergeById<T extends Record<string, unknown>, K extends keyof T>(
    existing: readonly T[],
    incoming: readonly T[],
    key: K
): T[] {
    const byId = indexBy(existing, key);

    for (const item of incoming) {
        const id = item[key] as KeyOf<T, K>;
        const prev = byId[id];
        byId[id] = prev ? { ...prev, ...item } : item;
    }

    return Object.values(byId);
}

/**
 * ensureUnique: remove duplicates by key, keeping the *last* occurrence.
 */
export function ensureUnique<T, K extends keyof T>(
    items: readonly T[],
    key: K
): T[] {
    const byId = indexBy(items, key);
    return Object.values(byId);
}
