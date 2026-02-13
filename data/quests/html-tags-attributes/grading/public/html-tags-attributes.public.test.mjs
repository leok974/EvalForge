
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("tags + attributes required", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<header\b[^>]*data-testid=["']header["'][^>]*>\s*<h1>\s*My Site\s*<\/h1>\s*<\/header>/i);
  assertMatches(html, /<section\b[^>]*id=["']profile["'][^>]*class=["'][^"']*\bcard\b[^"']*["'][^>]*data-testid=["']profile["'][^>]*>/i);
  assertMatches(html, /<p\b[^>]*class=["'][^"']*\btagline\b[^"']*["'][^>]*>\s*Building with HTML\s*<\/p>/i);
  assertMatches(html, /<footer\b[^>]*data-testid=["']footer["'][^>]*>\s*©\s*2026\s*<\/footer>/i);
  assertNoTodo(html);
});
