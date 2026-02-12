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
        .filter((f) => f.endsWith(".mjs") || f.endsWith(".js"))
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
    const tmpBase = await fs.mkdtemp(path.join(os.tmpdir(), `ef-cli-${slug}-`));
    const tmpWs = path.join(tmpBase, wsInfo.name);
    await copyDir(wsInfo.dir, tmpWs);

    // Overlay solutions (if present)
    if (mode === "solution") {
        const solDir = path.join(repoRoot, "solutions", slug);
        if (!fssync.existsSync(solDir)) {
            throw new Error(`Missing solutions/${slug} (mode=solution)`);
        }
        await copyDir(solDir, tmpWs);
    }

    const env = {
        ...process.env,
        EF_WORKSPACE_OVERRIDE: tmpWs,
        EF_QUEST_SLUG: slug,
    };

    const args = ["--test", ...tests];

    const res = spawnSync(process.execPath, args, {
        cwd: repoRoot,
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

    console.log(`=== Running ${slugs.length} CLI quests from ${opts.questpack} in ${opts.mode} mode ===`);

    let pass = 0;
    for (const slug of slugs) {
        const ok = await runQuest({ slug, mode: opts.mode, debug: opts.debug });
        if (!ok) process.exitCode = 1;
        else pass++;
    }

    if (process.exitCode === 1) {
        console.log(`\n❌ CLI questpack FAILED (${pass}/${slugs.length} passed)`);
        process.exit(process.exitCode);
    } else {
        console.log(`\n✅ CLI questpack OK (${pass}/${slugs.length} passed)`);
    }
}

main().catch((err) => {
    console.error("Runner error:", err?.stack || err);
    process.exit(1);
});
