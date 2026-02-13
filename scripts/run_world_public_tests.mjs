#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

function arg(name) {
    const idx = process.argv.indexOf(name);
    return idx >= 0 ? process.argv[idx + 1] : null;
}

function usage() {
    console.error("Usage: node scripts/run_world_public_tests.mjs --questpack data/questpacks/cli_core.json");
    process.exit(2);
}

const questpackPath = arg("--questpack");
if (!questpackPath) usage();

const root = process.cwd();
const qpAbs = path.resolve(root, questpackPath);
if (!fs.existsSync(qpAbs)) {
    console.error(`EF_RUN_WORLD_MISSING_QUESTPACK: not found: ${qpAbs}`);
    process.exit(2);
}

const questpack = JSON.parse(fs.readFileSync(qpAbs, "utf8"));

// --- CLI questpack dispatch ----------------------------------------------
function extractSlugsFromPack(pack) {
    const items =
        Array.isArray(pack) ? pack :
            Array.isArray(pack.quests) ? pack.quests :
                Array.isArray(pack.entries) ? pack.entries :
                    null;
    if (!items) return [];
    return items.map((it) => {
        if (typeof it === "string") return path.basename(it.replace(/\\/g, "/"));
        if (it?.slug) return it.slug;
        if (it?.quest_path) return path.basename(it.quest_path.replace(/\\/g, "/"));
        return null;
    }).filter(Boolean);
}

const slugsToCheck = extractSlugsFromPack(questpack);
const packBase = path.basename(questpackPath).toLowerCase();
const looksCli =
    packBase.includes("cli") ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("cli-")));

if (looksCli) {
    const runnerPath = path.resolve(root, "scripts/run_cli_questpack.mjs");
    const args = [
        runnerPath,
        "--questpack",
        questpackPath,
        "--mode",
        arg("--mode") || "starter",
    ];

    const onlySlug = arg("--only-slug"); // Not typically supported by world runner yet, but future proofing
    if (onlySlug) args.push("--only-slug", onlySlug);

    // Check for debug flag in raw args since arg() helper is simple
    if (process.argv.includes("--debug")) args.push("--debug");

    const res = spawnSync(process.execPath, args, { stdio: "inherit" });
    process.exit(res.status ?? 1);
}

const looksTs =
    packBase.includes("typescript") ||
    packBase.includes("ts-") ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("ts-")));

if (looksTs) {
    const runnerPath = path.resolve(root, "scripts/run_ts_questpack.mjs");
    const args = [
        runnerPath,
        "--questpack",
        questpackPath,
        "--mode",
        arg("--mode") || "starter",
    ];

    const onlySlug = arg("--only-slug");
    if (onlySlug) args.push("--only-slug", onlySlug);

    if (process.argv.includes("--debug")) args.push("--debug");

    const res = spawnSync(process.execPath, args, { stdio: "inherit" });
    process.exit(res.status ?? 1);
}

const looksGit =
    packBase.includes("git") ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("git-")));

if (looksGit) {
    const runnerPath = path.resolve(root, "scripts/run_git_questpack.mjs");
    const args = [
        runnerPath,
        "--questpack",
        questpackPath,
        "--mode",
        arg("--mode") || "starter",
    ];

    const onlySlug = arg("--only-slug");
    if (onlySlug) args.push("--only-slug", onlySlug);

    if (process.argv.includes("--debug")) args.push("--debug");

    const res = spawnSync(process.execPath, args, { stdio: "inherit" });
    process.exit(res.status ?? 1);
}

// --- Shared Python helper for Python & SQL dispatchers ---
function pickPythonBin() {
    const env = process.env.PYTHON || process.env.PYTHON_BIN;
    if (env && env.trim()) return env.trim();

    const candidates = ["python", "python3", "py"];
    for (const c of candidates) {
        const probeArgs = c === "py" ? ["-3", "--version"] : ["--version"];
        const r = spawnSync(c, probeArgs, { stdio: "pipe" });
        if (r.status === 0) return c;
    }
    return "python";
}

const looksPython =
    packBase.includes("python_") ||
    packBase.includes("foundry_python") ||
    packBase === "python_systems.json" ||
    packBase === "foundry_python.json" ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("python-")));

const looksAgents =
    packBase.includes("agents_") ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("agents-")));

function isMlQuestpack(questpackPath) {
    const base = path.basename(questpackPath);
    return (
        base === "ml_core.json" ||
        base === "ml_core.upgraded.json" ||
        base.startsWith("ml_") ||
        questpackPath.includes("/ml_") ||
        questpackPath.includes("\\ml_")
    );
}

if (isMlQuestpack(questpackPath)) {
    const python = pickPythonBin();
    const mode = arg("--mode") || "student";
    const onlySlug = arg("--only-slug");
    const args = ["scripts/run_ml_questpack.py", questpackPath, "--mode", mode];
    if (onlySlug) args.push("--only-slug", onlySlug);
    const rc = spawnSync(python, args, { stdio: "inherit" });
    process.exit(rc.status ?? 1);
}

if (looksPython || looksAgents) {
    // Python dispatch: use pytest runner
    const py = pickPythonBin();
    const args = [];

    if (py === "py") args.push("-3");

    if (looksAgents) {
        args.push("scripts/run_agents_questpack.py");
    } else {
        args.push("scripts/run_python_questpack.py");
    }

    args.push("--questpack", questpackPath, "--mode", arg("--mode") || "student");

    const onlySlug = arg("--only-slug");
    if (onlySlug) args.push("--only-slug", onlySlug);

    const res = spawnSync(py, args, { stdio: "inherit" });
    process.exit(res.status ?? 1);
}

const looksSql =
    packBase.includes("sql") ||
    (slugsToCheck.length > 0 && slugsToCheck.every((s) => String(s).startsWith("sql-")));

if (looksSql) {
    // SQL dispatch: use Python runner with pytest + sqlite3
    const py = pickPythonBin();
    const args = [];

    if (py === "py") args.push("-3");

    args.push("scripts/run_sql_questpack.py", "--questpack", questpackPath, "--mode", arg("--mode") || "student");

    const onlySlug = arg("--only-slug");
    if (onlySlug) args.push("--only-slug", onlySlug);

    const res = spawnSync(py, args, { stdio: "inherit" });
    process.exit(res.status ?? 1);
}

// -------------------------------------------------------------------------


function extractSlugFromQuestPath(p) {
    if (!p || typeof p !== "string") return null;
    const norm = p.replace(/\\/g, "/");
    const parts = norm.split("/").filter(Boolean);
    return parts.length ? parts[parts.length - 1] : null;
}

function extractSlugs(questpackJson) {
    const slugs = [];

    const push = (s) => {
        if (typeof s === "string" && s.trim()) slugs.push(s.trim());
    };

    const handleItem = (it) => {
        if (!it) return;

        // string style: ["infra-ignition", ...]
        if (typeof it === "string") return push(it);

        if (typeof it === "object") {
            // canonical style: { slug: "agents-ignition", ... }
            if (typeof it.slug === "string") return push(it.slug);

            // quest_path style: { quest_path: "docs/quests/agents-ignition" }
            if (typeof it.quest_path === "string") {
                const s = extractSlugFromQuestPath(it.quest_path);
                if (s) return push(s);
            }

            // tolerate camelCase too
            if (typeof it.questPath === "string") {
                const s = extractSlugFromQuestPath(it.questPath);
                if (s) return push(s);
            }
        }
    };

    // wrapper style: { world_id, track_id, title, quests:[...] }
    if (questpackJson && typeof questpackJson === "object" && !Array.isArray(questpackJson)) {
        if (Array.isArray(questpackJson.quests)) {
            for (const it of questpackJson.quests) handleItem(it);
            return slugs;
        }
    }

    // array style: [...]
    if (Array.isArray(questpackJson)) {
        for (const it of questpackJson) handleItem(it);
        return slugs;
    }

    return slugs;
}

const slugs = Array.from(new Set(extractSlugs(questpack))).filter(Boolean);
if (slugs.length === 0) {
    console.error("EF_RUN_WORLD_NO_SLUGS: could not extract quest slugs from questpack JSON");
    process.exit(2);
}

function listPublicTests(slug) {
    const qDir = path.join(root, "data", "quests", slug);
    const pubDir = path.join(qDir, "grading", "public");
    if (!fs.existsSync(pubDir)) return [];
    return fs
        .readdirSync(pubDir)
        .filter((f) => f.endsWith(".test.mjs"))
        .map((f) => path.join(pubDir, f));
}

let total = 0;
let failed = 0;

const mode = arg("--mode") || "starter"; // starter | solution

for (const slug of slugs) {
    const tests = listPublicTests(slug);
    if (tests.length === 0) {
        console.error(`EF_RUN_WORLD_NO_PUBLIC_TESTS: ${slug}`);
        failed++;
        continue;
    }

    const questDir = path.join(root, "data", "quests", slug);

    // Detect task file extension (.sh or .mjs)
    let taskFilename = "task.sh";
    if (fs.existsSync(path.join(questDir, "workspace", "task.mjs"))) {
        taskFilename = "task.mjs";
    }

    const workspaceTask = path.join(questDir, "workspace", taskFilename);
    const solutionTask = path.join(questDir, "grading", "solutions", taskFilename);
    const backupTask = path.join(questDir, "workspace", taskFilename + ".bak");

    let swapped = false;
    if (mode === "solution") {
        if (fs.existsSync(solutionTask)) {
            try {
                if (fs.existsSync(workspaceTask)) {
                    fs.copyFileSync(workspaceTask, backupTask);
                }
                fs.copyFileSync(solutionTask, workspaceTask);
                swapped = true;
            } catch (e) {
                console.error(`EF_RUN_WORLD_SWAP_FAIL: ${slug} -> ${e.message}`);
            }
        } else {
            console.warn(`EF_RUN_WORLD_NO_SOLUTION: ${slug} (running starter)`);
        }
    }

    for (const testFile of tests) {
        total++;
        const res = spawnSync(process.execPath, ["--test", testFile], { stdio: "inherit" });
        if (res.status !== 0) {
            failed++;
            console.error(`EF_RUN_WORLD_TEST_FAIL: ${slug} -> ${path.relative(root, testFile)}`);
        }
    }

    if (swapped) {
        try {
            if (fs.existsSync(backupTask)) {
                fs.copyFileSync(backupTask, workspaceTask);
                fs.unlinkSync(backupTask);
            } else {
                // If there was no original task.sh, maybe we should remove the solution? 
                // But normally workspace has task.sh. Let's just unlink workspaceTask if backup didn't exist?
                // Safest to leave it or unlink if we created it from scratch.
                // Assuming workspace always has task.sh for CLI quests.
                fs.unlinkSync(workspaceTask);
            }
        } catch (e) {
            console.error(`EF_RUN_WORLD_RESTORE_FAIL: ${slug} -> ${e.message}`);
        }
    }
}

if (failed) {
    console.error(`\nEF_RUN_WORLD_SUMMARY: ${failed}/${total} public tests failed.`);
    process.exit(1);
} else {
    console.log(`\nEF_RUN_WORLD_SUMMARY: ${total} public tests passed.`);
    process.exit(0);
}
