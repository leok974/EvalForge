
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("semantic layout", () => {
  const html = normLF(readText(WS, "index.html"));
  for (const tag of ["header","nav","main","aside","footer"]) {
    assertMatches(html, new RegExp(`<${tag}\\b`, "i"), `missing <${tag}>`);
  }
  assertMatches(html, /<nav\b[^>]*aria-label=["']Primary["'][^>]*>/i);
  assertMatches(html, /<article\b[^>]*data-testid=["']article["'][^>]*>\s*<h2>\s*News\s*<\/h2>\s*<\/article>/i);
  assertNoTodo(html);
});
