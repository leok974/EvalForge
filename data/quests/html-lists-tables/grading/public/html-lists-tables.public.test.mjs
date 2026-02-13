
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("lists + tables", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<ul\b[^>]*data-testid=["']task-list["'][^>]*>[\s\S]*?<\/ul>/i);
  const m = html.match(/<ul\b[^>]*data-testid=["']task-list["'][^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(m, "task-list ul exists");
  const li = (m[1].match(/<li\b[^>]*>[\s\S]*?<\/li>/gi) || []).map(s => s.replace(/<[^>]+>/g,"").trim());
  assert.deepEqual(li, ["Learn","Build","Ship"]);

  assertMatches(html, /<table\b[^>]*data-testid=["']scores["'][^>]*>[\s\S]*?<\/table>/i);
  assertMatches(html, /<th>\s*Name\s*<\/th>\s*<th>\s*Score\s*<\/th>/i);
  assertMatches(html, /<td>\s*Alice\s*<\/td>\s*<td>\s*10\s*<\/td>/i);
  assertMatches(html, /<td>\s*Bob\s*<\/td>\s*<td>\s*8\s*<\/td>/i);
  assertNoTodo(html);
});
