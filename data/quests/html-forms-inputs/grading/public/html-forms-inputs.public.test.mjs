
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("forms + inputs", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<form\b[^>]*data-testid=["']signup["'][^>]*action=["']\/submit["'][^>]*method=["']post["'][^>]*>/i);
  assertMatches(html, /<label\b[^>]*for=["']email["'][^>]*>\s*Email\s*<\/label>/i);
  assertMatches(html, /<input\b[^>]*id=["']email["'][^>]*name=["']email["'][^>]*type=["']email["'][^>]*required/i);
  assertMatches(html, /<select\b[^>]*id=["']role["'][^>]*name=["']role["'][^>]*>[\s\S]*<\/select>/i);
  assertMatches(html, /<option\b[^>]*value=["']student["'][^>]*>\s*student\s*<\/option>/i);
  assertMatches(html, /<option\b[^>]*value=["']mentor["'][^>]*>\s*mentor\s*<\/option>/i);
  assertMatches(html, /<button\b[^>]*type=["']submit["'][^>]*>\s*Join\s*<\/button>/i);
  assertNoTodo(html);
});
