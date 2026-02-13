
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("position + z-index", () => {
  const css = normLF(readText(WS, "style.css"));
  const modal = cssFindBlock(css, ".modal");
  cssAssertDecl(modal, "position", "fixed");
  cssAssertDecl(modal, "inset", "0");
  cssAssertDecl(modal, "z-index", "1000");

  const tip = cssFindBlock(css, ".tooltip");
  cssAssertDecl(tip, "position", "absolute");
  cssAssertDecl(tip, "z-index", "1100");

  const fab = cssFindBlock(css, ".fab");
  cssAssertDecl(fab, "position", "fixed");
  cssAssertDecl(fab, "right", "16px");
  cssAssertDecl(fab, "bottom", "16px");

  assertNoTodo(css);
});
