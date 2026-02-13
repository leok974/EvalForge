import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-middleware', async (t) => {
    const { stdout } = await runNode(WS_DIR, 'index.js');
    // Solution 5*2=10 +1=11
    assert.strictEqual(stdout.trim(), '11');
});