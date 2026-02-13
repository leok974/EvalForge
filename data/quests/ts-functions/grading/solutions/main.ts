export function greet(name: string, title?: string): string {
    if (title) return `Hello, ${title} ${name}`;
    return `Hello, ${name}`;
}