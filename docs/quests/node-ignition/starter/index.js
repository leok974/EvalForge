import { greet } from "./src/greet.js";

const raw = process.argv[2];

// TODO:
// - If missing/blank: print usage to stderr and exit(2)
// - Else: print greet(name) to stdout

console.log(greet(raw));
