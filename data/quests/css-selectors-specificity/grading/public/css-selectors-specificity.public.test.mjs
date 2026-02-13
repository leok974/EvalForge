
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("selectors + specificity", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, ".btn"), "padding", "10px");
  cssAssertDecl(cssFindBlock(css, ".btn.primary"), "background", "#4f46e5");
  cssAssertDecl(cssFindBlock(css, "#cta.btn.primary"), "border", "2px solid #fff");
  assertNoTodo(css);
});
