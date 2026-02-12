export function greet(name) {
    if (typeof name !== "string") {
        throw new Error("EF_NODE_IGNITION_INVALID_TYPE: name must be a string");
    }

    const trimmed = name.trim();
    if (!trimmed) {
        throw new Error("EF_NODE_IGNITION_EMPTY_NAME: name is required");
    }

    return `Hello, ${trimmed}!`;
}
