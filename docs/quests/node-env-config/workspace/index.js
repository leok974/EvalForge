import { config } from "./config.js";

console.log(`Server starting on port ${config.port}`);
console.log(`Connected to database at ${config.dbUrl}`);
