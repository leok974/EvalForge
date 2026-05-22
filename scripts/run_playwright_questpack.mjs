#!/usr/bin/env node
/**
 * scripts/run_playwright_questpack.mjs
 *
 * CI runner for Playwright questpacks.
 * Executes each quest's spec file inside the backend Docker container
 * (where Chromium and mock-cms are available).
 *
 * Usage:
 *   node scripts/run_playwright_questpack.mjs --questpack data/questpacks/playwright_ignition.json --mode solution
 *   node scripts/run_playwright_questpack.mjs --questpack data/questpacks/playwright_ignition.json --mode student
 */

import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { spawnSync, execSync } from "node:child_process";

// ---------------------------------------------------------------------------
// CLI Arg parsing
// ---------------------------------------------------------------------------

function arg(name) {
    const idx = process.argv.indexOf(name);
    return idx >= 0 ? process.argv[idx + 1] : null;
}

function usage() {
    console.error("Usage: node scripts/run_playwright_questpack.mjs --questpack <path> [--mode student|solution] [--only-slug <slug>]");
    process.exit(2);
}

// ---------------------------------------------------------------------------
// Questpack slug extraction (mirrors run_world_public_tests.mjs logic)
// ---------------------------------------------------------------------------

function basenameFromPath(p) {
    return p.replace(/\\/g, "/").replace(/\/+$/, "").split("/").at(-1);
}

function extractSlugs(pack) {
    const items = Array.isArray(pack) ? pack
        : Array.isArray(pack.quests) ? pack.quests
        : Array.isArray(pack.entries) ? pack.entries
        : null;
    if (!items) throw new Error("Unrecognised questpack shape");
    return items.map(it => {
        if (typeof it === "string") return basenameFromPath(it);
        if (it?.slug) return it.slug;
        if (it?.quest_path) return basenameFromPath(it.quest_path);
        throw new Error(`Cannot extract slug from: ${JSON.stringify(it)}`);
    });
}

// ---------------------------------------------------------------------------
// Docker container detection
// ---------------------------------------------------------------------------

function findBackendContainer() {
    // Try compose-style name first, then label search
    const candidates = ["evalforge-backend", "evalforge_backend", "backend"];
    for (const name of candidates) {
        const r = spawnSync("docker", ["inspect", "--format", "{{.State.Running}}", name], {
            encoding: "utf8",
            stdio: ["ignore", "pipe", "ignore"],
        });
        if (r.status === 0 && r.stdout.trim() === "true") return name;
    }
    // Fall back to label query
    const r2 = spawnSync("docker", ["ps", "--filter", "label=com.docker.compose.service=backend", "--format", "{{.Names}}"], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
    });
    const name = r2.stdout.trim().split("\n")[0];
    if (name) return name;
    return null;
}

// ---------------------------------------------------------------------------
// Run a single spec inside the backend container
// ---------------------------------------------------------------------------

function runSpecInContainer(container, specContent, mode) {
    // 1. Create temp dir on host so we can write the spec
    const tmpHost = fs.mkdtempSync(path.join(os.tmpdir(), "ef-pw-ci-"));
    const specPath = path.join(tmpHost, "quest.spec.ts");
    const configPath = path.join(tmpHost, "playwright.config.ts");
    const pkgPath = path.join(tmpHost, "package.json");

    try {
        fs.writeFileSync(specPath, specContent, "utf8");
        fs.writeFileSync(configPath, [
            "import { defineConfig } from '@playwright/test';",
            "export default defineConfig({",
            "  testDir: '.',",
            "  timeout: 30000,",
            "  use: {",
            "    headless: true,",
            "    baseURL: 'http://mock-cms:8765',",
            "    launchOptions: {",
            "      executablePath: '/usr/bin/chromium',",
            "      args: ['--no-sandbox', '--disable-setuid-sandbox'],",
            "    },",
            "  },",
            "  reporter: 'list',",
            "});",
        ].join("\n"), "utf8");
        fs.writeFileSync(pkgPath, JSON.stringify({
            name: "ef-pw-ci",
            version: "1.0.0",
            dependencies: { "@playwright/test": "^1.40.0" }
        }), "utf8");

        // 2. Copy files into container temp dir
        const containerTmp = `/tmp/ef-pw-ci-${Date.now()}`;
        const mkdirResult = spawnSync("docker", ["exec", container, "mkdir", "-p", containerTmp], {
            encoding: "utf8",
            stdio: ["ignore", "pipe", "pipe"],
        });
        if (mkdirResult.status !== 0) {
            return { ok: false, output: `mkdir failed: ${mkdirResult.stderr}` };
        }

        for (const [hostFile, containerName] of [
            [specPath, "quest.spec.ts"],
            [configPath, "playwright.config.ts"],
            [pkgPath, "package.json"],
        ]) {
            const cpResult = spawnSync("docker", ["cp", hostFile, `${container}:${containerTmp}/${containerName}`], {
                encoding: "utf8",
                stdio: ["ignore", "pipe", "pipe"],
            });
            if (cpResult.status !== 0) {
                return { ok: false, output: `docker cp failed: ${cpResult.stderr}` };
            }
        }

        // 3. Run inside container: npm install + playwright test
        // PLAYWRIGHT_BROWSERS_PATH=0 skips browser download; we use system Chromium
        const bashCmd = [
            `cd ${containerTmp}`,
            "PLAYWRIGHT_BROWSERS_PATH=0 npm install --prefer-offline --silent 2>&1 | tail -1",
            `PLAYWRIGHT_BROWSERS_PATH=0 npx playwright test quest.spec.ts --reporter=list`,
        ].join(" && ");

        const runResult = spawnSync("docker", ["exec", container, "bash", "-c", bashCmd], {
            encoding: "utf8",
            stdio: ["ignore", "pipe", "pipe"],
            timeout: 120000,
        });

        const combined = (runResult.stdout || "") + (runResult.stderr || "");

        // 4. Cleanup container tmp dir
        spawnSync("docker", ["exec", container, "rm", "-rf", containerTmp], {
            stdio: "ignore"
        });

        return { ok: runResult.status === 0, output: combined };

    } finally {
        // Cleanup host tmp dir
        try { fs.rmSync(tmpHost, { recursive: true, force: true }); } catch {}
    }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
    const questpackPath = arg("--questpack");
    if (!questpackPath) usage();

    const mode = arg("--mode") || "student";
    const onlySlug = arg("--only-slug");

    const root = process.cwd();
    const qpAbs = path.resolve(root, questpackPath);
    if (!fs.existsSync(qpAbs)) {
        console.error(`Questpack not found: ${qpAbs}`);
        process.exit(2);
    }

    const pack = JSON.parse(fs.readFileSync(qpAbs, "utf8"));
    let slugs = extractSlugs(pack);
    if (onlySlug) slugs = slugs.filter(s => s === onlySlug);

    const container = findBackendContainer();
    if (!container) {
        console.error("EF_PW_ERROR: Cannot find running backend container. Start Docker stack first.");
        process.exit(2);
    }
    console.log(`=== Playwright CI runner: ${slugs.length} quests | mode=${mode} | container=${container} ===`);

    let passed = 0;
    let failed = 0;
    const errors = [];
    const slugResults = [];

    for (const slug of slugs) {
        // Boss quests are excluded from smoke tests (too complex to auto-run)
        const isBoss = slug.includes("boss");
        if (isBoss) {
            console.log(`⏭  SKIP (boss): ${slug}`);
            continue;
        }

        let specContent = null;
        const questDir = path.join(root, "data", "quests", slug);

        if (mode === "solution") {
            const solFile = path.join(questDir, "grading", "solutions", "solution.spec.ts");
            if (fs.existsSync(solFile)) {
                specContent = fs.readFileSync(solFile, "utf8");
            } else {
                // Fallback: look for solution.spec.ts in solution/
                const altFile = path.join(questDir, "solution", "solution.spec.ts");
                if (fs.existsSync(altFile)) {
                    specContent = fs.readFileSync(altFile, "utf8");
                }
            }
        } else {
            // student mode: use workspace/main.spec.ts
            const wsFile = path.join(questDir, "workspace", "main.spec.ts");
            if (fs.existsSync(wsFile)) {
                specContent = fs.readFileSync(wsFile, "utf8");
            }
        }

        if (!specContent) {
            const msg = `No spec file found for ${slug} in mode=${mode}`;
            console.error(`EF_PW_MISSING: ${msg}`);
            failed++;
            errors.push(msg);
            slugResults.push({ slug, status: "failed", error: msg });
            continue;
        }

        process.stdout.write(`  Running ${slug} [${mode}]... `);
        const result = runSpecInContainer(container, specContent, mode);

        if (result.ok) {
            console.log("PASS");
            passed++;
            slugResults.push({ slug, status: "passed" });
        } else {
            console.log("FAIL");
            if (result.output) {
                // Print last 10 lines of output for debugging
                const lines = result.output.split("\n").filter(l => l.trim());
                lines.slice(-10).forEach(l => console.error(`    ${l}`));
            }
            failed++;
            errors.push(`${slug}: test failed`);
            slugResults.push({ slug, status: "failed", error: result.output?.slice(-500) || "unknown" });
        }
    }

    const total = passed + failed;
    console.log(`\n${passed}/${total} playwright quests passed.`);

    const resultJson = {
        total,
        passed,
        failed,
        errors,
        slugs: slugResults,
    };
    console.log(`EF_RUNNER_RESULT_JSON=${JSON.stringify(resultJson)}`);
    process.exit(failed === 0 ? 0 : 1);
}

main().catch(err => {
    console.error("EF_PW_FATAL:", err?.stack || err);
    process.exit(1);
});
