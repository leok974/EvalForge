export function greet(name) {
    const n = String(name ?? "").trim();
    if (!n) throw new Error("EF_NODE_IGNITION_EMPTY_NAME");
    return `Hello, ${n}!`;
}
