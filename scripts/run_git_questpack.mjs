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
    if (out.mode === "starter") out.mode = "student"; // Alias for world runner compatibility
    if (!["student", "solution"].includes(out.mode)) {
        throw new Error(`Invalid --mode ${out.mode} (expected student|solution)`);
    }
    return out;
}

// Reuse logic from cli_runner for basics
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
        throw new Error("Questpack JSON shape not recognized.");
    }

    const slugs = [];
    for (const it of items) {
        if (typeof it === "string") slugs.push(basenameFromQuestPath(it));
        else if (it?.slug) slugs.push(it.slug);
        else if (it?.quest_path) slugs.push(basenameFromQuestPath(it.quest_path));
    }
    return slugs;
}

async function listPublicTests(questDir) {
    const pubDir = path.join(questDir, "grading", "public");
    if (!fssync.existsSync(pubDir)) throw new Error(`Missing grading/public: ${pubDir}`);
    const files = await fs.readdir(pubDir);
    const tests = files
        .filter((f) => f.endsWith(".mjs") || f.endsWith(".js") || f.endsWith(".ts"))
        .filter((f) => f.includes(".test.") || f.includes(".public.test."))
        .map((f) => path.join(pubDir, f))
        .sort();
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
    const questDir = path.join(repoRoot, "data", "quests", slug);
    if (!fssync.existsSync(questDir)) throw new Error(`Quest dir missing: ${questDir}`);

    const tests = await listPublicTests(questDir);
    const wsInfo = findWorkspaceFolder(questDir);

    const tmpBase = await fs.mkdtemp(path.join(os.tmpdir(), `ef-git-${slug}-`));
    const tmpWs = path.join(tmpBase, wsInfo.name); // This is where student works
    await copyDir(wsInfo.dir, tmpWs);

    // Env definition moved up
    const env = {
        ...process.env,
        EF_WORKSPACE_OVERRIDE: tmpWs,
        EF_QUEST_SLUG: slug,
        // Override git identity for tests
        GIT_AUTHOR_NAME: "EvalForge Bot",
        GIT_AUTHOR_EMAIL: "bot@evalforge.app",
        GIT_COMMITTER_NAME: "EvalForge Bot",
        GIT_COMMITTER_EMAIL: "bot@evalforge.app",
    };

    if (process.platform === "win32") {
        const gitVars = ["GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL"];
        env.WSLENV = (process.env.WSLENV ? process.env.WSLENV + ":" : "") + gitVars.join(":");
    }

    // Copy solutions if needed
    if (mode === "solution") {
        const solDir = path.join(questDir, "grading", "solutions");
        if (fssync.existsSync(solDir)) {
            await copyDir(solDir, tmpWs);

            // If there's a generator script, run it
            const genScript = path.join(tmpWs, "solution_generator.js");
            if (fssync.existsSync(genScript)) {
                // console.log(`Running solution generator: ${genScript}`);
                const genRes = spawnSync(process.execPath, [genScript], {
                    cwd: tmpWs,
                    env,
                    stdio: "inherit"
                });
                if (genRes.status !== 0) {
                    console.error("Solution generator failed");
                    return false;
                }
                // Cleanup generator
                try { await fs.unlink(genScript); } catch { }
            }
        } else {
            console.warn(`(warn) No solution found at solutions/${slug}`);
        }
    }

    const args = ["--test", ...tests];

    const res = spawnSync(process.execPath, args, {
        cwd: repoRoot,
        env,
        encoding: "utf8",
        shell: false
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

    console.log(`=== Running ${slugs.length} Git quests from ${opts.questpack} in ${opts.mode} mode ===`);

    let pass = 0;
    const results = [];
    for (const slug of slugs) {
        const ok = await runQuest({ slug, mode: opts.mode, debug: opts.debug });
        results.push({ slug, status: ok ? "passed" : "failed" });
        if (!ok) process.exitCode = 1;
        else pass++;
    }

    const summary = {
        total: slugs.length,
        passed: pass,
        failed: slugs.length - pass,
        errors: [],
        slugs: results
    };

    console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(summary)}`);

    if (process.exitCode === 1) {
        console.log(`\n❌ Git questpack FAILED (${pass}/${slugs.length} passed)`);
        process.exit(process.exitCode);
    } else {
        console.log(`\n✅ Git questpack OK (${pass}/${slugs.length} passed)`);
    }
}

main().catch((err) => {
    console.error("Runner error:", err?.stack || err);
    process.exit(1);
});
