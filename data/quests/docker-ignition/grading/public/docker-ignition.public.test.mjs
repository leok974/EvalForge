import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Docker Ignition: verify setup", () => {
    const t = readText("workspace/hello.txt");
    mustNotContain(t, "TODO");
    mustContain(t, "docker-ok");
});
