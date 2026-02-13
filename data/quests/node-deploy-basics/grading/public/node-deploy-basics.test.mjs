import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import fs from 'node:fs';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-deploy-basics', async (t) => {
    const proc = fs.readFileSync(path.join(WS_DIR, 'Procfile'), 'utf8');
    assert.match(proc, /web: node index.js/);
    
    const { stdout } = await runNode(WS_DIR, 'index.js');
    assert.match(stdout, /Starting app/);
});