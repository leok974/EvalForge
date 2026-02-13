
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("cascade + inheritance", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "body"), "color", "#222");
  cssAssertDecl(cssFindBlock(css, "p"), "color", "inherit");
  cssAssertDecl(cssFindBlock(css, ".muted"), "color", "#666");
  assertNoTodo(css);
});
