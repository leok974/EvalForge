import { greet } from "./src/greet.js";

const raw = process.argv[2];
const name = String(raw ?? "").trim();

if (!name) {
    console.error("Usage: node index.js <name>");
    process.exit(2);
}

console.log(greet(name));
