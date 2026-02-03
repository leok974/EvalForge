import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("top.txt contains top 2 names with counts", async () => {
    await runSh(WS);
    const out = readText(WS, "outputs/top.txt").replace(/\r/g, "").trim().split("\n");
    assert.deepEqual(out, ["leo 3", "maya 2"], "EF_CLI_PIPES_TOP2: expected 'leo 3' then 'maya 2'");
});
