
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("colors + backgrounds", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "body"), "background-color", "#0b1020");

  const heroBlock = cssFindBlock(css, ".hero");
  assertMatches(heroBlock, /background\s*:\s*linear-gradient/i, "hero must use linear-gradient");
  cssAssertDecl(heroBlock, "color", "#fff");

  assertNoTodo(css);
});
