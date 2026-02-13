import shutil
from pathlib import Path
import textwrap

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = REPO_ROOT / "data" / "quests"
SHARED_HELPERS = REPO_ROOT / "data" / "_shared"

QUESTS = [
    {
        "slug": "node-ignition",
        "readme": "# Node Ignition\n\nWrite a Node.js script `index.js` that prints `Hello Node` to stdout.",
        "starter": "console.log('TODO');",
        "solution": "console.log('Hello Node');",
        "test": """
import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-ignition', async (t) => {
    const { stdout } = await runNode(WS_DIR, 'index.js');
    assert.strictEqual(stdout.trim(), 'Hello Node');
});
"""
    },
    {
        "slug": "node-modules",
        "readme": "# Modules\n\n1. Create `math.js` that exports an `add(a, b)` function (CommonJS).\n2. In `index.js`, require it and print the result of `add(5, 3)`.",
        "starter": "// index.js\nconst math = require('./math');\nconsole.log(math.add(5, 3));",
        "starter_math": "// math.js\nexports.add = (a, b) => { return 0; };",
        "solution": "// index.js\nconst math = require('./math');\nconsole.log(math.add(5, 3));",
        "solution_math": "// math.js\nexports.add = (a, b) => a + b;",
        "test": """
import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import fs from 'node:fs';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-modules', async (t) => {
    // Check math.js exists
    assert.ok(fs.existsSync(path.join(WS_DIR, 'math.js')), 'math.js must exist');
    
    const { stdout } = await runNode(WS_DIR, 'index.js');
    assert.strictEqual(stdout.trim(), '8');
});
"""
    },
    {
        "slug": "node-npm",
        "readme": "# npm\n\nInitialize a `package.json` file with `name` set to `node-npm-quest`.",
        "starter": "// index.js",
        "solution": "// index.js",
        "extra_files": {"package.json": '{\n  "name": "todo"\n}'}, 
        "extra_solutions": {"package.json": '{\n  "name": "node-npm-quest",\n  "version": "1.0.0"\n}'},
        "test": """
import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import fs from 'node:fs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-npm', async (t) => {
    const pkgPath = path.join(WS_DIR, 'package.json');
    assert.ok(fs.existsSync(pkgPath), 'package.json must exist');
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    assert.strictEqual(pkg.name, 'node-npm-quest');
});
"""
    },
    {
        "slug": "node-env-config",
        "readme": "# Environment Variables\n\nRead `APP_PORT` from environment variables and print `Running on <APP_PORT>`.\nUse default `8080` if not set.",
        "starter": "const port = 3000;\nconsole.log(`Running on ${port}`);",
        "solution": "const port = process.env.APP_PORT || 8080;\nconsole.log(`Running on ${port}`);",
        "test": """
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
"""
    },
    {
        "slug": "node-async",
        "readme": "# Async\n\nWrite an `async` function `run()` that prints `Steps: 1` then awaits 10ms then prints `Steps: 2`.",
        "starter": "function run() {\n console.log('Steps: 1');\n}",
        "solution": "async function run() {\n console.log('Steps: 1');\n await new Promise(r => setTimeout(r, 10));\n console.log('Steps: 2');\n}\nrun();",
        "test": """
import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-async', async (t) => {
    const { stdout } = await runNode(WS_DIR, 'index.js');
    const lines = stdout.trim().split(/[\\r\\n]+/);
    assert.deepStrictEqual(lines, ['Steps: 1', 'Steps: 2']);
});
"""
    },
    {
        "slug": "node-fs-path",
        "readme": "# FS & Path\n\nRead content from `input.txt`. Uppercase it. Write to `output.txt`.\nUse `path.join` to resolve paths safely.",
        "starter": "const fs = require('fs');\n// TODO",
        "solution": "const fs = require('fs');\nconst path = require('path');\nconst inp = path.join(__dirname, 'input.txt');\nconst out = path.join(__dirname, 'output.txt');\nconst content = fs.readFileSync(inp, 'utf8');\nfs.writeFileSync(out, content.toUpperCase());",
        "fixtures": {"input.txt": "hello world"},
        "test": """
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
"""
    },
    {
        "slug": "node-http",
        "readme": "# HTTP Server\n\nStart an HTTP server on port 3000 that responds with `Hello HTTP` to any request.",
        "starter": "const http = require('http');\n// TODO",
        "solution": """
const http = require('http');
const server = http.createServer((req, res) => {
  res.end('Hello HTTP');
});
server.listen(3000, () => { console.log('Listening'); });
""",
        "test": """
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
"""
    },
    {
        "slug": "node-middleware",
        "readme": "# Middleware Pattern\n\nImplement `apply(value, fns)` that passes value through an array of functions.\nEach function takes `v` and returns modified `v`.",
        "starter": "function apply(val, fns) {\n  return val; \n}\nconsole.log(apply(1, [v => v+1]));",
        "solution": "function apply(val, fns) {\n  return fns.reduce((acc, fn) => fn(acc), val);\n}\nconsole.log(apply(5, [v => v*2, v => v+1]));",
        "test": """
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
"""
    },
    {
        "slug": "node-testing",
        "readme": "# Testing\n\nUse `node:assert` to assert that `1 + 1 === 2`.",
        "starter": "const assert = require('node:assert');\n// TODO",
        "solution": "const assert = require('node:assert');\nassert.strictEqual(1 + 1, 2);\nconsole.log('Passed');",
        "test": """
import { test } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { runNode } from '../../../_shared/node_test_helpers.mjs';

const QUEST_DIR = path.resolve(import.meta.dirname, '../../');
const WS_DIR = path.join(QUEST_DIR, 'workspace');

test('node-testing', async (t) => {
    const { stdout } = await runNode(WS_DIR, 'index.js');
    assert.match(stdout, /Passed/);
});
"""
    },
    {
        "slug": "node-deploy-basics",
        "readme": "# Deploy Basics\n\nCreate a `Procfile` with content `web: node index.js`.\nAnd `index.js` printing `Starting app...`",
        "starter": "",
        "solution": "console.log('Starting app...');",
        "extra_files": {"Procfile": "web: echo TODO"},
        "extra_solutions": {"Procfile": "web: node index.js"},
        "test": """
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
"""
    }
]

def scaffold_quest(q):
    slug = q["slug"]
    print(f"Scaffolding {slug}...")
    
    quest_dir = DATA_QUESTS / slug
    quest_dir.mkdir(parents=True, exist_ok=True)
    
    # Dirs
    (quest_dir / "workspace").mkdir(exist_ok=True)
    (quest_dir / "grading" / "public").mkdir(parents=True, exist_ok=True)
    (quest_dir / "grading" / "solutions").mkdir(parents=True, exist_ok=True)
    
    # 1. Workspace
    (quest_dir / "workspace" / "README.md").write_text(q["readme"], encoding="utf-8")
    
    starter_file = q.get("starter_file", "index.js")
    (quest_dir / "workspace" / starter_file).write_text(q["starter"], encoding="utf-8")
    
    if "starter_math" in q:
        (quest_dir / "workspace" / "math.js").write_text(q["starter_math"], encoding="utf-8")
        
    if "extra_files" in q:
        for fname, content in q["extra_files"].items():
            (quest_dir / "workspace" / fname).write_text(content, encoding="utf-8")
            
    if "fixtures" in q:
         for fname, content in q["fixtures"].items():
            (quest_dir / "workspace" / fname).write_text(content, encoding="utf-8")

    # 2. Solutions
    (quest_dir / "grading" / "solutions" / starter_file).write_text(q["solution"], encoding="utf-8")
    
    if "solution_math" in q:
        (quest_dir / "grading" / "solutions" / "math.js").write_text(q["solution_math"], encoding="utf-8")

    if "extra_solutions" in q:
        for fname, content in q["extra_solutions"].items():
            (quest_dir / "grading" / "solutions" / fname).write_text(content, encoding="utf-8")

    # 3. Tests
    test_file = quest_dir / "grading" / "public" / f"{slug}.test.mjs"
    test_file.write_text(q["test"].strip(), encoding="utf-8")

def main():
    for q in QUESTS:
        scaffold_quest(q)
    print("Scaffolded 10 Node quests.")

if __name__ == "__main__":
    main()
