
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  readText, normLF, compactWS, assertNoTodo, assertMatches, assertTagText, findOpenTag, hasAttr
} from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("html-ignition: skeleton + app", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /^<!DOCTYPE html>\n/i, "doctype must be first line");
  const openHtml = findOpenTag(html, "html");
  hasAttr(openHtml, "lang", "en");
  assertMatches(html, /<meta\s+charset=["']utf-8["']\s*\/?>/i, "meta charset utf-8");
  assertMatches(html, /<meta\s+name=["']viewport["']\s+content=["']width=device-width,\s*initial-scale=1["']\s*\/?>/i, "meta viewport");
  assertTagText(html, "title", "EvalForge HTML");
  assertMatches(html, /<main\b[^>]*data-testid=["']app["'][^>]*>[\s\S]*?<\/main>/i, "main data-testid=app");
  assertMatches(html, /<main\b[^>]*data-testid=["']app["'][^>]*>\s*Hello,\s*Web\s*<\/main>/i, "app text exact");
  assertNoTodo(html);
});
