import { greet } from "./src/greet.js";

function printUsage() {
    console.error("Usage: node index.js <name>");
}

const raw = process.argv[2];
const name = typeof raw === "string" ? raw.trim() : "";

if (!name) {
    printUsage();
    process.exit(2);
}

try {
    // greet() trims internally too, but we already used trim to enforce CLI "missing" behavior.
    console.log(greet(raw));
} catch (err) {
    // Treat "empty/invalid name" as usage error (exit 2).
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes("EF_NODE_IGNITION_EMPTY_NAME") || msg.includes("EF_NODE_IGNITION_INVALID_TYPE")) {
        printUsage();
        process.exit(2);
    }
    // Unexpected error: surface and fail.
    console.error(msg);
    process.exit(1);
}
