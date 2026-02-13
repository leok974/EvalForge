// data/_shared/web_test_helpers.mjs
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";

export function readText(rootDir, relPath) {
    const p = path.resolve(rootDir, relPath);
    return fs.readFileSync(p, "utf8");
}

export function normLF(s) {
    return String(s).replace(/\r\n/g, "\n");
}

export function compactWS(s) {
    return normLF(s).replace(/[ \t]+/g, " ").replace(/\n{3,}/g, "\n\n").trim();
}

export function assertNoTodo(s, msg = "Should not contain TODO") {
    assert.ok(!/TODO/i.test(s), msg);
}

export function assertIncludes(haystack, needle, msg) {
    assert.ok(haystack.includes(needle), msg ?? `Expected to include: ${needle}`);
}

export function assertMatches(haystack, re, msg) {
    assert.ok(re.test(haystack), msg ?? `Expected to match: ${String(re)}`);
}

/**
 * Find the first tag open like <tag ...>
 * Returns the raw match string.
 */
export function findOpenTag(html, tagName) {
    const re = new RegExp(`<${tagName}\\b[^>]*>`, "i");
    const m = normLF(html).match(re);
    assert.ok(m, `Expected <${tagName}> open tag`);
    return m[0];
}

export function hasAttr(tagOpen, attr, expectedValue) {
    const re = new RegExp(`\\b${attr}\\s*=\\s*["']([^"']+)["']`, "i");
    const m = tagOpen.match(re);
    assert.ok(m, `Expected attribute ${attr}=... on ${tagOpen}`);
    if (expectedValue !== undefined) {
        assert.equal(m[1], expectedValue, `Expected ${attr}="${expectedValue}"`);
    }
    return true;
}

export function assertTagText(html, tagName, expectedText) {
    const re = new RegExp(`<${tagName}\\b[^>]*>([\\s\\S]*?)<\\/${tagName}>`, "i");
    const m = normLF(html).match(re);
    assert.ok(m, `Expected <${tagName}>...</${tagName}>`);
    const inner = compactWS(m[1]);
    assert.equal(inner, expectedText, `Expected ${tagName} text to equal "${expectedText}"`);
}

export function cssFindBlock(css, selector) {
    const esc = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const re = new RegExp(`${esc}\\s*\\{([\\s\\S]*?)\\}`, "m");
    const m = normLF(css).match(re);
    assert.ok(m, `Expected CSS block for selector: ${selector}`);
    return m[1];
}

export function cssAssertDecl(blockBody, prop, value) {
    const escProp = prop.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const escVal = value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const re = new RegExp(`\\b${escProp}\\s*:\\s*${escVal}\\s*;?`, "i");
    assert.ok(re.test(blockBody), `Expected declaration: ${prop}: ${value}`);
}
