import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-http', async (t) => {
    const child = spawn(process.execPath, ['index.js'], { cwd: WS_DIR });
    
    // Give it time to start
    await new Promise(r => setTimeout(r, 1000));
    
    try {
        const res = await fetch('http://localhost:3000');
        const text = await res.text();
        assert.strictEqual(text, 'Hello HTTP');
    } finally {
        child.kill();
    }
});