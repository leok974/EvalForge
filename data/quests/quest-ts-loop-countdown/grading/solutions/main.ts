export function countdown(start: number): number[] {
    const res: number[] = [];
    for (let i = start; i >= 0; i--) {
        res.push(i);
    }
    return res;
}