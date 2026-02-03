import test from "node:test";
import assert from "node:assert/strict";
import { greet } from "../../starter/src/greet.js";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const CWD = fileURLToPath(new URL("../../starter/", import.meta.url));

test("greet() formats output exactly", () => {
    assert.equal(
        greet("Leo"),
        "Hello, Leo!",
        "EF_NODE_IGNITION_GREETING_FORMAT: greet('Leo') must be 'Hello, Leo!'"
    );
});

test("CLI prints greeting when arg provided", () => {
    const result = spawnSync(process.execPath, ["index.js", "Leo"], {
        cwd: CWD,
        encoding: "utf-8",
        shell: false
    });

    if (result.error) {
        console.error("Spawn error:", result.error);
    }

    const stderr = result.stderr ? result.stderr.toString().trim() : "";
    const stdout = result.stdout ? result.stdout.toString().trimEnd() : "";

    assert.equal(stderr, "", "EF_NODE_IGNITION_STDERR_EMPTY: should not write to stderr on success");
    assert.equal(
        stdout,
        "Hello, Leo!",
        "EF_NODE_IGNITION_CLI_OUTPUT: expected 'Hello, Leo!'"
    );
});

test("CLI prints usage + exits 2 when missing arg", () => {
    const result = spawnSync(process.execPath, ["index.js"], {
        cwd: CWD,
        encoding: "utf-8",
        shell: false
    });

    assert.equal(result.status, 2, "EF_NODE_IGNITION_EXIT_2: missing arg must exit with code 2");

    const stderr = result.stderr ? result.stderr.toString() : "";
    assert.match(
        stderr,
        /Usage:\s*node index\.js <name>/,
        "EF_NODE_IGNITION_USAGE: usage message must be printed to stderr"
    );
});
