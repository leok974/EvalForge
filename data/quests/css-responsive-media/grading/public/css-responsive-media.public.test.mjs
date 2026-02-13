
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("responsive media queries", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, ".row"), "display", "flex");
  cssAssertDecl(cssFindBlock(css, ".grid"), "grid-template-columns", "repeat(3, 1fr)");

  assertMatches(css, /@media\s*\(\s*max-width\s*:\s*600px\s*\)\s*\{([\s\S]*)\}\s*$/m, "media query required");

  const mq = css.match(/@media\s*\(\s*max-width\s*:\s*600px\s*\)\s*\{([\s\S]*)\}\s*$/m);
  assert.ok(mq, "media query block");
  assertMatches(mq[1], /\.row\s*\{[\s\S]*flex-direction\s*:\s*column/i, "row becomes column");
  assertMatches(mq[1], /\.grid\s*\{[\s\S]*grid-template-columns\s*:\s*1fr/i, "grid becomes 1fr");

  assertNoTodo(css);
});
