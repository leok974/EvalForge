
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("flexbox", () => {
  const css = normLF(readText(WS, "style.css"));
  const row = cssFindBlock(css, ".row");
  cssAssertDecl(row, "display", "flex");
  cssAssertDecl(row, "justify-content", "space-between");
  cssAssertDecl(row, "align-items", "center");
  cssAssertDecl(row, "gap", "12px");
  assertNoTodo(css);
});
