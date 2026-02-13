
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("media + embeds", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<video\b[^>]*data-testid=["']demo-video["'][^>]*controls[^>]*>/i);
  assertMatches(html, /<source\b[^>]*src=["']media\/demo\.mp4["'][^>]*type=["']video\/mp4["'][^>]*\/?>/i);
  assertMatches(html, /<iframe\b[^>]*data-testid=["']embed["'][^>]*src=["']https:\/\/example\.com\/embed["'][^>]*title=["']Demo Embed["'][^>]*><\/iframe>/i);
  assertNoTodo(html);
});
