import fs from "node:fs";
import path from "node:path";
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

function readJson(p) {
    const raw = fs.readFileSync(p, "utf8");
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

function listPublicTests(questDir) {
    const pubDir = path.join(questDir, "grading", "public");
    if (!fs.existsSync(pubDir)) {
        throw new Error(`Missing grading/public: ${pubDir}`);
    }
    const files = fs.readdirSync(pubDir)
        .filter((f) => f.endsWith(".mjs") || f.endsWith(".js"))
        .filter((f) => f.includes(".test.") || f.includes(".public.test."))
        .map((f) => path.join(pubDir, f))
        .sort((a, b) => a.localeCompare(b));
    if (files.length === 0) {
        throw new Error(`No public test files found in ${pubDir}`);
    }
    return files;
}

/**
 * Swap solutions in-place: copy files from grading/solutions/ into workspace/,
 * saving backups so they can be restored after the test run.
 */
function swapInSolution(questDir) {
    const solDir = path.join(questDir, "grading", "solutions");
    const wsDir = path.join(questDir, "workspace");
    const backups = [];

    if (!fs.existsSync(solDir)) return backups; // No solution dir — skip

    const solFiles = fs.readdirSync(solDir);
    for (const f of solFiles) {
        const src = path.join(solDir, f);
        const dst = path.join(wsDir, f);
        if (fs.statSync(src).isDirectory()) continue; // Skip subdirs for now

        if (fs.existsSync(dst)) {
            const bak = dst + ".bak";
            fs.copyFileSync(dst, bak);
            backups.push({ dst, bak });
        } else {
            backups.push({ dst, bak: null }); // New file — restore by deleting
        }
        fs.copyFileSync(src, dst);
    }
    return backups;
}

function restoreBackups(backups) {
    for (const b of backups) {
        try {
            if (b.bak && fs.existsSync(b.bak)) {
                fs.copyFileSync(b.bak, b.dst);
                fs.unlinkSync(b.bak);
            } else if (b.bak === null && fs.existsSync(b.dst)) {
                fs.unlinkSync(b.dst);
            }
        } catch { }
    }
}

function runQuest({ slug, mode, debug }) {
    const repoRoot = process.cwd();
    const questDir = path.join(repoRoot, "data", "quests", slug);
    if (!fs.existsSync(questDir)) {
        throw new Error(`Quest dir missing: ${questDir}`);
    }

    const tests = listPublicTests(questDir);

    // In-place solution swap (same approach as run_world_public_tests.mjs generic runner)
    let backups = [];
    if (mode === "solution") {
        backups = swapInSolution(questDir);
    }

    let ok = true;
    for (const tf of tests) {
        const res = spawnSync(process.execPath, ["--test", tf], {
            stdio: "inherit",
            cwd: questDir, // Run from quest root so relative paths in test helpers resolve correctly
        });

        if (res.status !== 0) {
            ok = false;
        }
    }

    // Restore workspace to original state
    if (backups.length > 0) {
        restoreBackups(backups);
    }

    if (!ok) {
        console.error(`\n❌ FAIL: ${slug}`);
    } else if (debug) {
        console.log(`✅ PASS: ${slug}`);
    }

    return ok;
}

function main() {
    const opts = parseArgs(process.argv);
    const pack = readJson(opts.questpack);
    let slugs = extractSlugs(pack);

    if (opts.onlySlug) slugs = slugs.filter((s) => s === opts.onlySlug);

    console.log(`=== Running ${slugs.length} CLI quests from ${opts.questpack} in ${opts.mode} mode ===`);

    let pass = 0;
    for (const slug of slugs) {
        let ok;
        try {
            ok = runQuest({ slug, mode: opts.mode, debug: opts.debug });
        } catch (err) {
            console.error(`\nRunner error: ${err?.stack || err}`);
            ok = false;
        }
        if (!ok) process.exitCode = 1;
        else pass++;
    }

    const total = slugs.length;
    if (process.exitCode === 1) {
        console.log(`\n❌ CLI questpack FAILED (${pass}/${total} passed)`);
        const resultJson = { total, passed: pass, failed: total - pass, errors: [], slugs: [] };
        console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(resultJson)}`);
        process.exit(1);
    } else {
        console.log(`\n✅ CLI questpack OK (${pass}/${total} passed)`);
        const resultJson = { total, passed: pass, failed: 0, errors: [], slugs: [] };
        console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(resultJson)}`);
    }
}

main();
