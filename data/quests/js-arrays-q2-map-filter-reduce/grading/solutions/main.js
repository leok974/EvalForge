export function doubleAll(arr) {
    return arr.map(x => x * 2);
}
export function getEvens(arr) {
    return arr.filter(x => x % 2 === 0);
}
export function sumAll(arr) {
    return arr.reduce((acc, x) => acc + x, 0);
}