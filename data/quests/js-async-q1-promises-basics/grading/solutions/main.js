export function waitAndReturn(ms, val) {
    return new Promise(resolve => setTimeout(() => resolve(val), ms));
}