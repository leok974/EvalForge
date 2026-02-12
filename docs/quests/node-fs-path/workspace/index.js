import { processFile } from "./utils.js";

async function main() {
    try {
        await processFile("input.txt");
        console.log("Processed input.txt -> output.txt");
    } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        console.error("Error:", msg);
        process.exit(1);
    }
}

main();
