export function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}