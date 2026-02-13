import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-env-config', async (t) => {
    // Case 1: Default
    const r1 = await runNode(WS_DIR, 'index.js', [], { APP_PORT: null });
    assert.match(r1.stdout, /Running on 8080/);

    // Case 2: Custom
    const r2 = await runNode(WS_DIR, 'index.js', [], { APP_PORT: '9090' });
    assert.match(r2.stdout, /Running on 9090/);
});