import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import fs from 'node:fs';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-fs-path', async (t) => {
    // Restore fixture just in case
    fs.writeFileSync(path.join(WS_DIR, 'input.txt'), 'hello world');
    if (fs.existsSync(path.join(WS_DIR, 'output.txt'))) fs.unlinkSync(path.join(WS_DIR, 'output.txt'));

    await runNode(WS_DIR, 'index.js');
    
    assert.ok(fs.existsSync(path.join(WS_DIR, 'output.txt')), 'output.txt missing');
    const content = fs.readFileSync(path.join(WS_DIR, 'output.txt'), 'utf8');
    assert.strictEqual(content, 'HELLO WORLD');
});