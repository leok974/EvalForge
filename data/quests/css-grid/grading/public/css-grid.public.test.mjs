
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("grid", () => {
  const css = normLF(readText(WS, "style.css"));
  const grid = cssFindBlock(css, ".grid");
  cssAssertDecl(grid, "display", "grid");
  cssAssertDecl(grid, "grid-template-columns", "repeat(3, 1fr)");
  cssAssertDecl(grid, "gap", "12px");
  assertNoTodo(css);
});
