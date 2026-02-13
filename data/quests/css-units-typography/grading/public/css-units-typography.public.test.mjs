
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("units + typography", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "html"), "font-size", "16px");
  cssAssertDecl(cssFindBlock(css, "h1"), "font-size", "2rem");
  cssAssertDecl(cssFindBlock(css, "p"), "line-height", "1.5");
  cssAssertDecl(cssFindBlock(css, ".caption"), "font-size", "0.875rem");
  assertNoTodo(css);
});
