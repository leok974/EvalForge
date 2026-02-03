import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("tests/math.test.js contains assertions", async () => {
    const content = await fs.readFile(path.join(starterDir, "tests/math.test.js"), "utf-8");
    // Rudimentary check that they uncommented or wrote assert code
    // The starter has // TODO
    // We check for "assert.equal" or "assert.strictEqual"
    assert.match(content, /assert\.(equal|strictEqual|deepEqual)/, "EF_TEST_ASSERTION_PRESENT: Test file should contain assertions");
});
