// TS Arrays
// Clean a list of scores: handle non-numbers, round, bound 0..100, unique, sort.

export function cleanScores(scores: unknown): number[] {
    if (!Array.isArray(scores)) return [];

    const valid = scores
        .filter((x) => typeof x === "number" && Number.isFinite(x))
        .map((x) => Math.round(x))
        .filter((x) => x >= 0 && x <= 100);

    const unique = Array.from(new Set(valid));
    unique.sort((a, b) => a - b);

    return unique;
}
