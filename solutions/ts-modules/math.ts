// TS Modules - math helpers

export function sum(nums: number[]): number {
    return nums.reduce((a, b) => a + b, 0);
}

export function toCents(dollars: number): number {
    // 1.005 * 100 is slightly less than 100.5 due to float precision
    // We add a small epsilon to push it over.
    return Math.round(dollars * 100 + 1e-9);
}
