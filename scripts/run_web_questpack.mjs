// scripts/run_web_questpack.mjs
import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

function argValue(flag) {
    const i = process.argv.indexOf(flag);
    if (i === -1) return null;
    return process.argv[i + 1] ?? null;
}

const questpackPath = argValue("--questpack");
const mode = argValue("--mode") ?? "student";
const onlySlug = argValue("--only-slug");

if (!questpackPath) {
    console.error("Usage: node scripts/run_web_questpack.mjs --questpack <path> --mode student|solution [--only-slug <slug>]");
    process.exit(2);
}

function loadQuestpack(p) {
    const raw = fsSync.readFileSync(p, "utf8");
    const json = JSON.parse(raw);
    if (Array.isArray(json)) {
        // legacy quest_path list
        return json.map((q) => ({
            slug: String(q.quest_path).split("/").pop(),
        }));
    }
    if (json && Array.isArray(json.quests)) return json.quests;
    throw new Error("Unsupported questpack format");
}

async function listPublicTests(questDir) {
    const pubDir = path.join(questDir, "grading", "public");
    try {
        const items = await fs.readdir(pubDir);
        return items
            .filter((f) => f.endsWith(".public.test.mjs") || f.endsWith(".test.mjs"))
            .map((f) => path.join(pubDir, f));
    } catch {
        return [];
    }
}

async function swapSolutionsIntoWorkspace(questDir) {
    const ws = path.join(questDir, "workspace");
    const sol = path.join(questDir, "grading", "solutions");

    // Copy every file from grading/solutions -> workspace (same name)
    const backups = [];
    const files = await fs.readdir(sol);
    for (const f of files) {
        const src = path.join(sol, f);
        const dst = path.join(ws, f);

        const srcStat = await fs.stat(src);
        if (!srcStat.isFile()) continue;

        let old = null;
        try {
            old = await fs.readFile(dst, "utf8");
        } catch {
            old = null;
        }
        const next = await fs.readFile(src, "utf8");
        await fs.writeFile(dst, next, "utf8");
        backups.push({ dst, old });
    }
    return backups;
}

async function restoreBackups(backups) {
    for (const b of backups) {
        if (b.old === null) {
            try { await fs.unlink(b.dst); } catch { }
        } else {
            await fs.writeFile(b.dst, b.old, "utf8");
        }
    }
}

function runNodeTest(testFiles) {
    return new Promise((resolve) => {
        const child = spawn(process.execPath, ["--test", ...testFiles], {
            stdio: "inherit",
            env: process.env,
        });
        child.on("exit", (code) => resolve(code ?? 1));
    });
}

async function main() {
    const quests = loadQuestpack(questpackPath)
        .map((q) => ({ slug: q.slug ?? q.quest_path?.split("/").pop() }))
        .filter((q) => q.slug);

    const filtered = onlySlug ? quests.filter((q) => q.slug === onlySlug) : quests;

    if (filtered.length === 0) {
        console.error("EF_RUN_WORLD_NO_QUESTS: no quests found (check questpack)");
        process.exit(1);
    }

    let passed = 0;
    let failed = 0;

    for (const q of filtered) {
        const questDir = path.resolve("data", "quests", q.slug);
        const tests = await listPublicTests(questDir);
        if (tests.length === 0) {
            console.error(`EF_WEB_NO_PUBLIC_TESTS: ${q.slug}`);
            failed++;
            continue;
        }

        let backups = [];
        try {
            if (mode === "solution") {
                backups = await swapSolutionsIntoWorkspace(questDir);
            }

            const code = await runNodeTest(tests);
            if (code === 0) passed++;
            else failed++;
        } finally {
            if (mode === "solution" && backups.length) {
                await restoreBackups(backups);
            }
        }
    }

    const summary = {
        total: passed + failed,
        passed,
        failed,
        errors: [],
        slugs: []
    };
    console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(summary)}`);

    console.log(`EF_RUN_WORLD_SUMMARY: passed=${passed} failed=${failed} total=${passed + failed}`);
    process.exit(failed === 0 ? 0 : 1);
}

main().catch((e) => {
    console.error("EF_WEB_RUNNER_ERROR:", e?.stack ?? String(e));
    process.exit(1);
});
