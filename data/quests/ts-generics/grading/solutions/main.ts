export function wrap<T>(val: T): { value: T } {
    return { value: val };
}