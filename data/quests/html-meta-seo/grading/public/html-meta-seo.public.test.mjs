
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches, assertTagText } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("meta + seo", () => {
  const html = normLF(readText(WS, "index.html"));
  assertTagText(html, "title", "EvalForge Web Quest");
  assertMatches(html, /<meta\s+name=["']description["']\s+content=["']EvalForge web training quest\.[\"']\s*\/?>/i);
  assertMatches(html, /<link\s+rel=["']canonical["']\s+href=["']https:\/\/example\.com\/quest["']\s*\/?>/i);
  assertMatches(html, /<meta\s+property=["']og:title["']\s+content=["']EvalForge["']\s*\/?>/i);
  assertNoTodo(html);
});
