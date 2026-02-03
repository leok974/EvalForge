import fs from "node:fs/promises";
import path from "node:path";

export async function processFile(fileName) {
    const filePath = path.join(process.cwd(), fileName);
    const content = await fs.readFile(filePath, "utf-8");
    const uppercased = content.toUpperCase();
    await fs.writeFile(path.join(process.cwd(), "output.txt"), uppercased);
}
