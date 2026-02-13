
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("accessibility basics", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<img\b[^>]*data-testid=["']avatar["'][^>]*alt=["'][^"']+["'][^>]*>/i, "img needs alt");
  assertMatches(html, /<button\b[^>]*data-testid=["']close["'][^>]*aria-label=["']Close dialog["'][^>]*>\s*X\s*<\/button>/i);
  assertMatches(html, /<label\b[^>]*for=["']name["'][^>]*>\s*Name\s*<\/label>/i);
  assertMatches(html, /<input\b[^>]*id=["']name["'][^>]*name=["']name["'][^>]*>/i);
  assertNoTodo(html);
});
