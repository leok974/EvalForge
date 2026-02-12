import fs from "node:fs/promises";
import fssync from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync } from "node:child_process";

function parseArgs(argv) {
    const out = {
        questpack: null,
        mode: "student", // student | solution
        onlySlug: null,
        debug: false,
    };
    for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a === "--questpack") out.questpack = argv[++i];
        else if (a === "--mode") out.mode = argv[++i];
        else if (a === "--only-slug") out.onlySlug = argv[++i];
        else if (a === "--debug") out.debug = true;
        else throw new Error(`Unknown arg: ${a}`);
    }
    if (!out.questpack) throw new Error("Missing --questpack <path>");
    if (!["student", "solution"].includes(out.mode)) {
        throw new Error(`Invalid --mode ${out.mode} (expected student|solution)`);
    }
    return out;
}

async function readJson(p) {
    const raw = await fs.readFile(p, "utf8");
    return JSON.parse(raw);
}

function basenameFromQuestPath(qp) {
    const norm = qp.replace(/\\/g, "/").replace(/\/+$/, "");
    return norm.split("/").at(-1);
}

function extractSlugs(questpackJson) {
    const items =
        Array.isArray(questpackJson)
            ? questpackJson
            : Array.isArray(questpackJson.quests)
                ? questpackJson.quests
                : Array.isArray(questpackJson.entries)
                    ? questpackJson.entries
                    : null;

    if (!items) {
        throw new Error("Questpack JSON shape not recognized (expected array, or {quests:[...]}, or {entries:[...]}).");
    }

    const slugs = [];
    for (const it of items) {
        if (typeof it === "string") slugs.push(basenameFromQuestPath(it));
        else if (it?.slug) slugs.push(it.slug);
        else if (it?.quest_path) slugs.push(basenameFromQuestPath(it.quest_path));
        else throw new Error(`Cannot extract slug from questpack entry: ${JSON.stringify(it)}`);
    }
    return slugs;
}

async function listPublicTests(questDir) {
    const pubDir = path.join(questDir, "grading", "public");
    if (!fssync.existsSync(pubDir)) {
        throw new Error(`Missing grading/public: ${pubDir}`);
    }
    const files = await fs.readdir(pubDir);
    const tests = files
        .filter((f) => f.endsWith(".mjs") || f.endsWith(".js") || f.endsWith(".ts"))
        .filter((f) => f.includes(".test.") || f.includes(".public.test."))
        .map((f) => path.join(pubDir, f))
        .sort((a, b) => a.localeCompare(b));
    if (tests.length === 0) {
        throw new Error(`No public test files found in ${pubDir}`);
    }
    return tests;
}

function findWorkspaceFolder(questDir) {
    const ws = path.join(questDir, "workspace");
    if (fssync.existsSync(ws)) return { dir: ws, name: "workspace" };
    const starter = path.join(questDir, "starter");
    if (fssync.existsSync(starter)) return { dir: starter, name: "starter" };
    throw new Error(`No workspace/ or starter/ found in ${questDir}`);
}

async function copyDir(src, dst) {
    await fs.mkdir(dst, { recursive: true });
    const entries = await fs.readdir(src, { withFileTypes: true });
    for (const e of entries) {
        const s = path.join(src, e.name);
        const d = path.join(dst, e.name);
        if (e.isDirectory()) await copyDir(s, d);
        else if (e.isFile()) await fs.copyFile(s, d);
    }
}

async function runQuest({ slug, mode, debug }) {
    const repoRoot = process.cwd();
    const questDir = path.join(repoRoot, "docs", "quests", slug);
    if (!fssync.existsSync(questDir)) {
        throw new Error(`Quest dir missing: ${questDir}`);
    }

    const tests = await listPublicTests(questDir);
    const wsInfo = findWorkspaceFolder(questDir);

    // Temp isolated workspace (preserve basename: starter vs workspace)
    const tmpBase = await fs.mkdtemp(path.join(os.tmpdir(), `ef-ts-${slug}-`));
    const tmpWs = path.join(tmpBase, wsInfo.name);
    await copyDir(wsInfo.dir, tmpWs);

    // Overlay solutions (if present)
    if (mode === "solution") {
        const solDir = path.join(repoRoot, "solutions", slug);
        if (!fssync.existsSync(solDir)) {
            // Check if solution file is provided directly in solutions/slug/task.ts
            // But usually we dump files there. 
            // If missing -> fail in solution mode
            throw new Error(`Missing solutions/${slug} (mode=solution)`);
        }
        await copyDir(solDir, tmpWs);
    }

    // Set env var to point tests to the temp workspace
    // Tests must conform to "workspaceDirFromTestFile" logic and respect EF_WORKSPACE_OVERRIDE
    // OR we can pass it via another env var if needed. 
    // The previous CLI updates to _shared/cli_test_utils.mjs handle EF_WORKSPACE_OVERRIDE.
    // Assuming TS tests use similar logic or we need to update them.
    // TS tests likely import from "../../workspace/task.ts". which is relative.
    // IF tests are relying on RELATIVE imports from the test file location (in grading/public),
    // then moving the workspace elsewhere breaks those imports unless we use a loader/resolver hook 
    // OR we copy the tests to a location relative to the temp workspace?
    //
    // WAIT. If the test file is executed from its original location `docs/quests/ts-ign/grading/public/test.mjs`,
    // and it does `import { x } from "../../workspace/task.ts"`, that import resolves relative to the test file.
    // So it will import the ORIGINAL workspace file, not the temp execution one!
    //
    // For CLI tests, we used `runSh({ ws })` where `ws` was a path. The test logic used that path.
    // But for TS, we are IMPORTING the code under test.
    // 
    // To solve this for unit tests that import:
    // We must COPY the test file into the temp structure as well, maintaining the relative path relationship.
    // OR use a module alias/loader.
    //
    // Strategy: Copy grading/public -> temp/grading/public. Run tests from THERE.
    // This allows relative imports `../../workspace` to resolve to `temp/workspace`.

    const tmpGradingPublic = path.join(tmpBase, "grading", "public");
    await copyDir(path.join(questDir, "grading", "public"), tmpGradingPublic);

    const env = {
        ...process.env,
        EF_WORKSPACE_OVERRIDE: tmpWs, // Just in case
        EF_QUEST_SLUG: slug,
    };

    // We run the COPIED tests
    const copiedTests = tests.map(t => path.join(tmpGradingPublic, path.basename(t)));

    // Use node --import tsx --test
    const args = ["--import", "tsx", "--test", ...copiedTests];

    const res = spawnSync(process.execPath, args, {
        cwd: repoRoot, // Run from root so node_modules are found? using tsx should handle it
        env,
        encoding: "utf8",
        shell: false,
    });

    const ok = res.status === 0;
    if (!ok) {
        console.error(`\n❌ FAIL: ${slug}`);
        if (res.stdout) console.error(res.stdout);
        if (res.stderr) console.error(res.stderr);
    } else if (debug) {
        console.log(`✅ PASS: ${slug}`);
    }

    if (!debug) {
        // cleanup temp dir
        try {
            await fs.rm(tmpBase, { recursive: true, force: true });
        } catch { }
    } else {
        console.log(`(debug) kept temp workspace at: ${tmpWs}`);
    }

    return ok;
}

async function main() {
    const opts = parseArgs(process.argv);
    const pack = await readJson(opts.questpack);
    let slugs = extractSlugs(pack);

    if (opts.onlySlug) slugs = slugs.filter((s) => s === opts.onlySlug);

    console.log(`=== Running ${slugs.length} TS quests from ${opts.questpack} in ${opts.mode} mode ===`);

    let pass = 0;
    for (const slug of slugs) {
        const ok = await runQuest({ slug, mode: opts.mode, debug: opts.debug });
        if (!ok) process.exitCode = 1;
        else pass++;
    }

    if (process.exitCode === 1) {
        console.log(`\n❌ TS questpack FAILED (${pass}/${slugs.length} passed)`);
        process.exit(process.exitCode);
    } else {
        console.log(`\n✅ TS questpack OK (${pass}/${slugs.length} passed)`);
    }
}

main().catch((err) => {
    console.error("Runner error:", err?.stack || err);
    process.exit(1);
});
