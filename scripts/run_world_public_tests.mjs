#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { spawn, spawnSync } from "node:child_process";

// --- Helpers -------------------------------------------------------------

function arg(name) {
    const idx = process.argv.indexOf(name);
    return idx >= 0 ? process.argv[idx + 1] : null;
}

function usage() {
    console.error("Usage: node scripts/run_world_public_tests.mjs --questpack data/questpacks/cli_core.json [--mode student|solution]");
    process.exit(2);
}

// Capture stdout while streaming it to user, so we can parse result JSON
async function runDelegate(cmd, args, cwd) {
    return new Promise((resolve) => {
        const child = spawn(cmd, args, {
            stdio: ["inherit", "pipe", "inherit"],
            cwd: cwd || process.cwd(),
            env: process.env
        });

        let out = "";
        child.stdout.on("data", (chunk) => {
            process.stdout.write(chunk);
            out += chunk.toString();
        });

        child.on("exit", (code) => {
            let json = null;
            // Look for EF_RUNNER_RESULT_JSON={...}
            const match = out.match(/EF_RUNNER_RESULT_JSON=(.*)/);
            if (match) {
                try {
                    json = JSON.parse(match[1]);
                } catch (e) {
                    // ignore parse error, json remains null
                }
            }
            resolve({ code: code ?? 1, json, rawOutput: out });
        });
    });
}

function printSummaryAndExit(delegateResult) {
    const { code, json } = delegateResult;

    if (json) {
        // Modern runner output
        const passed = json.passed;
        const total = json.total;
        console.log(`\nEF_RUN_WORLD_SUMMARY: ${passed}/${total} public tests passed.`);
        // Force exit 1 if any failures, even if child exit code was 0 (shouldn't happen but safe)
        if (json.failed > 0 || json.errors.length > 0) process.exit(1);
        process.exit(0);
    } else {
        // Legacy fallback
        if (code === 0) {
            // We assume 100% pass if exit code 0 and no JSON (best effort)
            // Or strictly: we don't know totals.
            console.log(`\nEF_RUN_WORLD_SUMMARY: All tests passed (Legacy Mode).`);
            process.exit(0);
        } else {
            console.error(`\nEF_RUN_WORLD_SUMMARY: Tests failed (Legacy Mode). Exit code: ${code}`);
            process.exit(1);
        }
    }
}

// --- Main ----------------------------------------------------------------

async function main() {
    const questpackPath = arg("--questpack");
    if (!questpackPath) usage();

    const root = process.cwd();
    const qpAbs = path.resolve(root, questpackPath);
    if (!fs.existsSync(qpAbs)) {
        console.error(`EF_RUN_WORLD_MISSING_QUESTPACK: not found: ${qpAbs}`);
        process.exit(2);
    }

    const questpack = JSON.parse(fs.readFileSync(qpAbs, "utf8"));
    const packBase = path.basename(questpackPath).toLowerCase();

    // --- Slug Extraction -------------------------------------------------

    function extractSlugFromQuestPath(p) {
        if (!p || typeof p !== "string") return null;
        const norm = p.replace(/\\/g, "/");
        const parts = norm.split("/").filter(Boolean);
        return parts.length ? parts[parts.length - 1] : null;
    }

    function extractSlugs(json) {
        const list = [];
        const push = (s) => { if (typeof s === "string" && s.trim()) list.push(s.trim()); };

        const handleItem = (it) => {
            if (!it) return;
            if (typeof it === "string") return push(it);
            if (typeof it === "object") {
                if (typeof it.slug === "string") return push(it.slug);
                if (typeof it.quest_path === "string") return push(extractSlugFromQuestPath(it.quest_path));
                if (typeof it.questPath === "string") return push(extractSlugFromQuestPath(it.questPath));
            }
        };

        if (json && typeof json === "object" && !Array.isArray(json)) {
            if (Array.isArray(json.quests)) {
                for (const it of json.quests) handleItem(it);
            } else if (Array.isArray(json.entries)) {
                for (const it of json.entries) handleItem(it);
            }
        } else if (Array.isArray(json)) {
            for (const it of json) handleItem(it);
        }
        return list;
    }

    const slugs = Array.from(new Set(extractSlugs(questpack))).filter(Boolean);
    const slugsToCheck = slugs; // Alias for cleaner checks

    // --- Dispatch Logic --------------------------------------------------

    const mode = arg("--mode") || "starter";

    // Helper to run python runner
    async function dispatchPython(runnerName) {
        let pythonBin = process.env.PYTHON || process.env.PYTHON_BIN || "python";

        // Try to pick python3/py if default is missing or generic
        // (Simple heuristic, or trust environment)

        const args = [runnerName, "--questpack", questpackPath, "--mode", mode];
        const only = arg("--only-slug");
        if (only) args.push("--only-slug", only);

        const res = await runDelegate(pythonBin, args, root);
        printSummaryAndExit(res);
    }

    // 1. CLI
    const looksCli = packBase.includes("cli") || (slugs.length > 0 && slugs.every(s => s.startsWith("cli-")));
    if (looksCli) {
        const args = ["scripts/run_cli_questpack.mjs", "--questpack", questpackPath, "--mode", mode];
        if (arg("--only-slug")) args.push("--only-slug", arg("--only-slug"));

        const res = await runDelegate(process.execPath, args, root);
        printSummaryAndExit(res);
    }

    // 2. TS
    const looksTs = packBase.includes("typescript") || packBase.includes("ts-") || packBase.includes("prism_ts") || (slugs.length > 0 && slugs.every(s => s.startsWith("ts-")));
    if (looksTs) {
        const args = ["scripts/run_ts_questpack.mjs", "--questpack", questpackPath, "--mode", mode];
        if (arg("--only-slug")) args.push("--only-slug", arg("--only-slug"));

        const res = await runDelegate(process.execPath, args, root);
        printSummaryAndExit(res);
    }

    // 3. Git
    const looksGit = packBase.includes("git") || (slugs.length > 0 && slugs.every(s => s.startsWith("git-")));
    if (looksGit) {
        const args = ["scripts/run_git_questpack.mjs", "--questpack", questpackPath, "--mode", mode];
        if (arg("--only-slug")) args.push("--only-slug", arg("--only-slug"));

        const res = await runDelegate(process.execPath, args, root);
        printSummaryAndExit(res);
    }

    // 4. ML
    function isMlQuestpack(p) {
        const b = path.basename(p);
        return b.startsWith("ml_") || b.includes("ml_core");
    }
    if (isMlQuestpack(questpackPath)) {
        await dispatchPython("scripts/run_ml_questpack.py");
    }

    // 5. Python / Agents
    const looksPython = packBase.includes("python") || packBase.includes("foundry") || (slugs.length > 0 && slugs.every(s => s.startsWith("python-")));
    const looksAgents = packBase.includes("agents") || (slugs.length > 0 && slugs.every(s => s.startsWith("agents-")));

    if (looksPython || looksAgents) {
        const script = looksAgents ? "scripts/run_agents_questpack.py" : "scripts/run_python_questpack.py";
        await dispatchPython(script);
    }

    // 6. SQL
    const looksSql = packBase.includes("sql") || (slugs.length > 0 && slugs.every(s => s.startsWith("sql-")));
    if (looksSql) {
        await dispatchPython("scripts/run_sql_questpack.py");
    }

    // 7. Web
    const looksWeb = (p, sList) => {
        const b = path.basename(p).toLowerCase();
        if (b.includes("web_html") || b.includes("web_css") || b.startsWith("web_")) return true;
        return sList.some(s => s.startsWith("html-") || s.startsWith("css-"));
    };
    if (looksWeb(questpackPath, slugs)) {
        const args = ["scripts/run_web_questpack.mjs", "--questpack", questpackPath, "--mode", mode];
        if (arg("--only-slug")) args.push("--only-slug", arg("--only-slug"));

        const res = await runDelegate(process.execPath, args, root);
        printSummaryAndExit(res);
    }

    // --- Default Node Runner Loop -----------------------------------------
    // If no specialized runner, we run `node --test` for each slug.
    // Handles: Node, React, Infra (often), Labs

    if (slugs.length === 0) {
        console.error("EF_RUN_WORLD_NO_SLUGS: could not extract quest slugs");
        process.exit(2);
    }

    let totalQuests = 0;
    let passedQuests = 0;
    let failedQuests = 0;
    const errors = [];
    const slugResults = [];

    for (const slug of slugs) {
        // Filter by only-slug if present
        if (arg("--only-slug") && arg("--only-slug") !== slug) continue;

        totalQuests++;

        const questDir = path.join(root, "data", "quests", slug);
        const pubDir = path.join(questDir, "grading", "public");

        let testFiles = [];
        if (fs.existsSync(pubDir)) {
            testFiles = fs.readdirSync(pubDir)
                .filter(f => f.endsWith(".mjs") || f.endsWith(".js") || f.endsWith(".ts"))
                .filter(f => f.includes(".test."))
                .map(f => path.join(pubDir, f));
        }

        if (testFiles.length === 0) {
            console.error(`EF_RUN_WORLD_NO_PUBLIC_TESTS: ${slug}`);
            failedQuests++;
            slugResults.push({ slug, status: "failed", error: "No public tests" });
            continue;
        }

        // Swap Logic: Generic (copy all from grading/solutions to workspace)
        const wsDir = path.join(questDir, "workspace");
        const solDir = path.join(questDir, "grading", "solutions");
        let backups = [];

        if (mode === "solution" && fs.existsSync(solDir)) {
            try {
                const solFiles = fs.readdirSync(solDir);
                for (const f of solFiles) {
                    const src = path.join(solDir, f);
                    const dst = path.join(wsDir, f);

                    // Skip if directory (for now, simplistic)
                    if (fs.statSync(src).isDirectory()) continue;

                    if (fs.existsSync(dst)) {
                        const bak = dst + ".bak";
                        fs.copyFileSync(dst, bak);
                        backups.push({ dst, bak });
                    } else {
                        backups.push({ dst, bak: null }); // Track new files
                    }
                    fs.copyFileSync(src, dst);
                }
            } catch (e) {
                console.error(`EF_SWAP_FAIL: ${e.message}`);
            }
        }

        // Run Tests
        let slugFail = false;
        for (const tf of testFiles) {
            const childRef = spawnSync(process.execPath, ["--test", tf], {
                stdio: "inherit",
                cwd: questDir,
            });

            if (childRef.status !== 0) {
                slugFail = true;
                errors.push(`${slug}: ${path.basename(tf)} failed`);
            }
        }

        // Restore
        if (backups.length > 0) {
            for (const b of backups) {
                try {
                    if (b.bak && fs.existsSync(b.bak)) {
                        fs.copyFileSync(b.bak, b.dst);
                        fs.unlinkSync(b.bak);
                    } else if (b.bak === null && fs.existsSync(b.dst)) {
                        fs.unlinkSync(b.dst);
                    }
                } catch (e) { }
            }
        }

        if (slugFail) {
            failedQuests++;
            slugResults.push({ slug, status: "failed" });
        } else {
            passedQuests++;
            slugResults.push({ slug, status: "passed" });
        }
    }

    console.log(`\nEF_RUN_WORLD_SUMMARY: ${passedQuests}/${totalQuests} quests passed.`);

    // Also emit JSON for audit script consistency from this "Parent Runner acting as Runner"
    const resultJson = {
        total: totalQuests,
        passed: passedQuests,
        failed: failedQuests,
        errors,
        slugs: slugResults
    };
    console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(resultJson)}`);

    process.exit(failedQuests === 0 ? 0 : 1);
}

main().catch(err => {
    console.error("EF_RUN_WORLD_FATAL:", err);
    process.exit(1);
});
