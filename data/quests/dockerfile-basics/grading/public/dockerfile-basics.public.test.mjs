import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain, mustMatch } from "./_h.mjs";

test("Dockerfile basics: required directives present", () => {
  const t = readText("workspace/Dockerfile");

  mustNotContain(t, "TODO");
  mustMatch(t, /^FROM\s+node:20-alpine/m, "Expected FROM node:20-alpine");
  mustContain(t, "WORKDIR /app");
  mustMatch(t, /COPY\s+package\*\.json\s+\.\//m, "Expected COPY package*.json ./");
  mustMatch(t, /RUN\s+npm\s+ci/i, "Expected npm ci");
  mustContain(t, "COPY . .");
  mustContain(t, "EXPOSE 3000");
  mustContain(t, 'CMD ["node","server.js"]');

  // sanity: FROM should be first instruction (ignoring comments/blank lines)
  const first = t.split("\n").find((l) => l.trim() && !l.trim().startsWith("#"));
  assert.ok(first.startsWith("FROM "), "FROM must be first instruction");
});
