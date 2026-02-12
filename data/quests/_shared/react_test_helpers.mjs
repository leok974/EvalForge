import React from "react";
import TestRenderer, { act as _act } from "react-test-renderer";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

/**
 * Create + mount a component under react-test-renderer within act().
 * Returns { renderer, root } where root is the ReactTestInstance.
 */
export function runComponent(Component, props = {}) {
    let renderer;
    _act(() => {
        renderer = TestRenderer.create(React.createElement(Component, props));
    });
    return { renderer, root: renderer.root };
}

/**
 * Wrap react-test-renderer act() so tests can update state deterministically.
 */
export function act(fn) {
    _act(fn);
}

/**
 * Find a node by data-testid within the given ReactTestInstance subtree.
 */
export function findByTestId(root, testId) {
    return root.findByProps({ "data-testid": testId });
}

/**
 * Find all nodes by data-testid within the given subtree.
 */
export function findAllByTestId(root, testId) {
    return root.findAllByProps({ "data-testid": testId });
}

/**
 * Flatten text content from a ReactTestInstance (or string/number).
 * Useful for assert.equal(textContent(node), "expected").
 */
export function textContent(node) {
    if (node == null) return "";
    if (typeof node === "string" || typeof node === "number") return String(node);
    if (Array.isArray(node)) return node.map(textContent).join("");
    if (typeof node === "object" && Array.isArray(node.children)) {
        return node.children.map(textContent).join("");
    }
    return "";
}

/**
 * Read a fixture file relative to the quest root.
 * Call from tests: readFixture(import.meta.url, "fixtures/users.json")
 */
export function readFixture(testMetaUrl, relPath) {
    // grading/public -> quest root is ../../
    const questRootUrl = new URL("../../", testMetaUrl);
    const absUrl = new URL(relPath, questRootUrl);
    const absPath = fileURLToPath(absUrl);

    const raw = fs.readFileSync(absPath, "utf8");
    try {
        return JSON.parse(raw);
    } catch {
        return raw;
    }
}
