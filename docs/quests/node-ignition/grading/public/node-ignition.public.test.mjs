import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { greet } from "../../workspace/src/greet.js";

const CWD = fileURLToPath(new URL("../../workspace/", import.meta.url));

test("greet() trims and formats output exactly", () => {
    assert.equal(greet("Leo"), "Hello, Leo!", "EF_NODE_IGNITION_GREETING_FORMAT");
    assert.equal(greet("  Leo  "), "Hello, Leo!", "EF_NODE_IGNITION_GREETING_TRIM");
});

test("greet() throws on empty/whitespace-only", () => {
    assert.throws(() => greet("   "), /EMPTY_NAME/, "EF_NODE_IGNITION_GREETING_THROW_WS");
});

test("CLI prints greeting when arg provided", () => {
    const result = spawnSync(process.execPath, ["index.js", "Leo"], {
        cwd: CWD,
        encoding: "utf-8",
        shell: false
    });

    const stderr = (result.stderr ?? "").toString().trim();
    const stdout = (result.stdout ?? "").toString().trimEnd();

    assert.equal(result.status, 0, "EF_NODE_IGNITION_EXIT_0");
    assert.equal(stderr, "", "EF_NODE_IGNITION_STDERR_EMPTY");
    assert.equal(stdout, "Hello, Leo!", "EF_NODE_IGNITION_CLI_OUTPUT");
});

test("CLI prints usage + exits 2 when missing arg", () => {
    const result = spawnSync(process.execPath, ["index.js"], {
        cwd: CWD,
        encoding: "utf-8",
        shell: false
    });

    assert.equal(result.status, 2, "EF_NODE_IGNITION_EXIT_2");
    assert.match(
        (result.stderr ?? "").toString(),
        /Usage:\s*node index\.js <name>/,
        "EF_NODE_IGNITION_USAGE"
    );
});

test("CLI treats whitespace-only as missing (usage + exit 2)", () => {
    const result = spawnSync(process.execPath, ["index.js", "   "], {
        cwd: CWD,
        encoding: "utf-8",
        shell: false
    });

    assert.equal(result.status, 2, "EF_NODE_IGNITION_EXIT_2_WS");
    assert.match(
        (result.stderr ?? "").toString(),
        /Usage:\s*node index\.js <name>/,
        "EF_NODE_IGNITION_USAGE_WS"
    );
});
