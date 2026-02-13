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
    const questDir = path.join(repoRoot, "data", "quests", slug); // Correct path
    if (!fssync.existsSync(questDir)) {
        throw new Error(`Quest dir missing: ${questDir}`);
    }

    const tests = await listPublicTests(questDir);
    const wsInfo = findWorkspaceFolder(questDir);

    // Temp isolated workspace (preserve basename: starter vs workspace)
    const tmpBase = await fs.mkdtemp(path.join(os.tmpdir(), `ef-ts-${slug}-`));
    const tmpWs = path.join(tmpBase, wsInfo.name);
    await copyDir(wsInfo.dir, tmpWs);

    // Solution Mode Swap logic
    if (mode === "solution") {
        // Standard path: grading/solutions
        const solDir = path.join(questDir, "grading", "solutions");
        if (fssync.existsSync(solDir)) {
            await copyDir(solDir, tmpWs);
        } else {
            // Fallback to legacy root (optional, but let's stick to standard)
            // throw new Error(`Missing grading/solutions for ${slug}`);
            console.warn(`(warn) No solution found at grading/solutions`);
        }
    }

    // ... (rest of execution logic remains similar, but ensure we capture output)

    // Tests (COPY strategy is good)
    const tmpGradingPublic = path.join(tmpBase, "grading", "public");
    await copyDir(path.join(questDir, "grading", "public"), tmpGradingPublic);

    const env = {
        ...process.env,
        EF_WORKSPACE_OVERRIDE: tmpWs,
        EF_QUEST_SLUG: slug,
    };

    const copiedTests = tests.map(t => path.join(tmpGradingPublic, path.basename(t)));

    // We use node --test with loader
    // If using typescript, we might need --import tsx 
    // BUT 'tsx' might not be in path if just 'npm install'.
    // Better to rely on npx or absolute path? 
    // Or just assume 'node --import tsx' works if in devDependencies.
    const args = ["--import", "tsx", "--test", ...copiedTests];

    const res = spawnSync(process.execPath, args, {
        cwd: repoRoot,
        env,
        encoding: "utf8",
        shell: false
        // win32 shell:false avoids quoting issues sometimes, but might need true for PATH?
        // usually false is safer if executable is absolute. process.execPath is absolute.
    });

    const ok = res.status === 0;

    // Cleanup
    if (!debug) {
        try { await fs.rm(tmpBase, { recursive: true, force: true }); } catch { }
    }

    return { ok, error: ok ? null : (res.stderr || res.stdout) };
}

async function main() {
    const opts = parseArgs(process.argv);
    const pack = await readJson(opts.questpack);
    let slugs = extractSlugs(pack);

    if (opts.onlySlug) slugs = slugs.filter((s) => s === opts.onlySlug);

    console.log(`=== Running ${slugs.length} TS quests from ${opts.questpack} in ${opts.mode} mode ===`);

    let pass = 0;
    const results = [];

    for (const slug of slugs) {
        let ok = false;
        let err = null;
        try {
            const res = await runQuest({ slug, mode: opts.mode, debug: opts.debug });
            ok = res.ok;
            err = res.error;
        } catch (e) {
            err = e.message;
        }

        if (ok) {
            console.log(`✅ PASS: ${slug}`);
            pass++;
            results.push({ slug, status: "passed" });
        } else {
            console.log(`❌ FAIL: ${slug}`);
            if (err) console.error(err);
            results.push({ slug, status: "failed", error: err });
            process.exitCode = 1;
        }
    }

    const summary = {
        total: slugs.length,
        passed: pass,
        failed: slugs.length - pass,
        errors: [],
        slugs: results
    };

    console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(summary)}`); // CRITICAL for audit

    if (process.exitCode === 1) {
        console.log(`\n❌ TS questpack FAILED (${pass}/${slugs.length} passed)`);
    } else {
        console.log(`\n✅ TS questpack OK (${pass}/${slugs.length} passed)`);
    }
}

main().catch((err) => {
    console.error("Runner error:", err?.stack || err);
    process.exit(1);
});
