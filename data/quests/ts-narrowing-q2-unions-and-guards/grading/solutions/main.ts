export function format(val: string | number): string {
    if (typeof val === "number") {
        return `Value: ${val}`;
    }
    return val.toUpperCase();
}