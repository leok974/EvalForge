import { processFile } from "./utils.js";

async function main() {
    try {
        await processFile("input.txt");
        console.log("Processed input.txt -> output.txt");
    } catch (err) {
        console.error("Error:", err.message);
        process.exit(1);
    }
}

main();
