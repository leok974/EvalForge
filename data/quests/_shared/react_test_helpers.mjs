import React from 'react';
import TestRenderer from 'react-test-renderer';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

// Re-export act for convenience
export const act = TestRenderer.act;

/**
 * Mounts a component using react-test-renderer
 * @param {Function} Component - The React component to render
 * @param {Object} props - Props to pass to the component
 * @returns {Object} { root, toJSON, instance }
 */
export function runComponent(Component, props = {}) {
    let root;
    act(() => {
        root = TestRenderer.create(React.createElement(Component, props));
    });
    return {
        root: root.root,
        toJSON: () => root.toJSON(),
        instance: root.getInstance()
    };
}

/**
 * Finds a single node by data-testid. Throws if not found or multiple found.
 * @param {Object} root - The TestInstance root
 * @param {string} testID - The data-testid value
 * @returns {Object} The found TestInstance
 */
export function findByTestId(root, testID) {
    try {
        return root.findByProps({ 'data-testid': testID });
    } catch (e) {
        throw new Error(`TestID "${testID}" not found or ambiguous: ${e.message}`);
    }
}

/**
 * Reads a JSON fixture file
 * @param {string} wsDir - Workspace directory
 * @param {string} relPath - Relative path to fixture (e.g. "fixtures/data.json")
 * @returns {any} Parsed JSON content
 */
export function readFixture(wsDir, relPath) {
    const p = path.join(wsDir, relPath);
    return JSON.parse(fs.readFileSync(p, 'utf8'));
}

/**
 * Reads a text file
 * @param {string} wsDir 
 * @param {string} relPath 
 */
export function readText(wsDir, relPath) {
    return fs.readFileSync(path.join(wsDir, relPath), 'utf8');
}

/**
 * Fail helper with custom message prefix support if needed, 
 * or just standard assert.fail
 */
export const fail = assert.fail;
