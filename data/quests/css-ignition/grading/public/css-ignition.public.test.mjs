
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("css ignition", () => {
  const css = normLF(readText(WS, "style.css"));
  const body = cssFindBlock(css, "body");
  cssAssertDecl(body, "background", "#111");
  cssAssertDecl(body, "color", "#eee");
  cssAssertDecl(body, "font-family", "system-ui");

  const c = cssFindBlock(css, ".container");
  cssAssertDecl(c, "max-width", "800px");
  cssAssertDecl(c, "margin", "0 auto");

  const h1 = cssFindBlock(css, "h1");
  cssAssertDecl(h1, "font-size", "2rem");

  assertNoTodo(css);
});
