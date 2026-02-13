
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertMatches, assertNoTodo } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("debug + validate", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<meta\s+charset=["']utf-8["']\s*\/?>/i);
  assert.ok(!/<p>\s*<div>/i.test(html), "must not nest div inside p");

  const m = html.match(/<ul\b[^>]*data-testid=["']menu["'][^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(m, "menu ul");
  const li = (m[1].match(/<li\b[^>]*>[\s\S]*?<\/li>/gi) || []).map(s => s.replace(/<[^>]+>/g,"").trim());
  assert.deepEqual(li, ["Home","About"]);

  assertMatches(html, /<a\b[^>]*data-testid=["']home-link["'][^>]*href=["']\/home["'][^>]*>\s*Home\s*<\/a>/i);
  assertNoTodo(html);
});
