import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-async', async (t) => {
    const { stdout } = await runNode(WS_DIR, 'index.js');
    const lines = stdout.trim().split(/[\r\n]+/);
    assert.deepStrictEqual(lines, ['Steps: 1', 'Steps: 2']);
});