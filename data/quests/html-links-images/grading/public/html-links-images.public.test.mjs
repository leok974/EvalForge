
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("links + images", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*>\s*Docs\s*<\/a>/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*href=["']https:\/\/example\.com\/docs["']/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*target=["']_blank["']/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*rel=["'][^"']*noopener[^"']*["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*src=["']assets\/logo\.png["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*alt=["']EvalForge logo["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*width=["']120["'][^>]*height=["']120["']/i);
  assertNoTodo(html);
});
