
import fs from "node:fs";
import path from "node:path";

export function readText(rel) {
  const p = path.resolve(process.cwd(), rel);
  if (!fs.existsSync(p)) {
      throw new Error(`File not found: ${rel}`);
  }
  return fs.readFileSync(p, "utf8").replace(/\r\n/g, "\n");
}

export function mustContain(text, needle) {
  if (!text.includes(needle)) throw new Error(`Missing: ${needle}`);
}

export function mustMatch(text, re, msg = "Pattern missing") {
  if (!re.test(text)) throw new Error(msg);
}

export function mustNotContain(text, needle) {
  if (text.includes(needle)) throw new Error(`Should not contain: ${needle}`);
}
