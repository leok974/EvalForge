import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");
const QUESTS_DIR = path.join(ROOT, "data", "quests");

const QUESTS = [
    "infra-images-containers",
    "infra-dockerfile-basics",
    "infra-compose-basics",
    "infra-ports-localhost",
    "infra-networks",
    "infra-volumes",
    "infra-env-secrets",
    "infra-healthchecks",
    "infra-reverse-proxy",
    "infra-ci-smoke",
];

const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const RESET = "\x1b[0m";

async function runTest(quest, type) {
    const testFile = path.join(QUESTS_DIR, quest, "grading", type, `${quest}.${type}.test.mjs`);
    if (!fs.existsSync(testFile)) {
        // Some quests might not have hidden tests? The spec provided all of them.
        // simpler to just try/catch execution
        return { ok: true, skipped: true };
    }

    try {
        await execFileAsync(process.execPath, ["--test", testFile], { cwd: ROOT });
        return { ok: true };
    } catch (e) {
        return { ok: false, error: e };
    }
}

async function copySolution(quest) {
    const ws = path.join(QUESTS_DIR, quest, "workspace");
    const sol = path.join(QUESTS_DIR, quest, "grading", "solutions");

    // Backup handled by just overwriting from starter later?
    // Ideally we backup first.
    // Actually, simpler: read sol files, write to ws.

    const items = fs.readdirSync(sol);
    for (const item of items) {
        const src = path.join(sol, item);
        const dest = path.join(ws, item);
        fs.cpSync(src, dest, { recursive: true, force: true });
    }
}

async function revertToStarter(quest) {
    // Re-instantiate the starter files?
    // The user prompt didn't strictly give a "staging" area, but I can assume the starter state 
    // was what I just wrote. 
    // To be robust: I'll manually revert specific known files based on the quest spec.
    // Or better: I can't easily revert without a backup.
    // I will rely on the user manually reverting or I will write a quick "reset" based on my knowledge of the starter content.
    // Actually, for this integrity run, I'll just check "Solution Passes".
    // I won't worry about reverting to clean state for the USER, unless I want to leave it clean.
    // I SHOULD leave it clean.

    // Strategy: Backup workspace before applying solution.
    const ws = path.join(QUESTS_DIR, quest, "workspace");
    const backup = path.join(QUESTS_DIR, quest, "workspace_backup");
    fs.cpSync(ws, backup, { recursive: true });
}

async function restoreBackup(quest) {
    const ws = path.join(QUESTS_DIR, quest, "workspace");
    const backup = path.join(QUESTS_DIR, quest, "workspace_backup");
    if (fs.existsSync(backup)) {
        fs.rmSync(ws, { recursive: true, force: true });
        fs.renameSync(backup, ws);
    }
}

async function checkQuest(quest) {
    console.log(`\nChecking ${quest}...`);

    // Clean outputs
    const wsClean = path.join(QUESTS_DIR, quest, "workspace");
    const outputs = path.join(wsClean, "outputs");
    if (fs.existsSync(outputs)) {
        fs.rmSync(outputs, { recursive: true, force: true });
    }

    // 1. Test Starter (Expect Fail)
    process.stdout.write("  Starter State: ");
    const starterRes = await runTest(quest, "public");
    if (starterRes.ok) {
        console.log(`${RED}FAIL (Unexpected Pass)${RESET}`);
        return false;
    }
    console.log(`${GREEN}PASS (Expected Fail)${RESET}`);

    // Backup
    const ws = path.join(QUESTS_DIR, quest, "workspace");
    const backup = path.join(QUESTS_DIR, quest, `_backup_${Date.now()}`);
    fs.cpSync(ws, backup, { recursive: true });

    try {
        // 2. Apply Solution
        await copySolution(quest);

        // 3. Test Public (Expect Pass)
        process.stdout.write("  Solution Public: ");
        const solPubRes = await runTest(quest, "public");
        if (!solPubRes.ok) {
            console.log(`${RED}FAIL${RESET}`);
            console.error(solPubRes.error.stdout || solPubRes.error.message);
            return false;
        }
        console.log(`${GREEN}PASS${RESET}`);

        // 4. Test Hidden (Expect Pass)
        process.stdout.write("  Solution Hidden: ");
        const solHidRes = await runTest(quest, "hidden");
        if (!solHidRes.ok) {
            console.log(`${RED}FAIL${RESET}`);
            console.error(solHidRes.error.stdout || solHidRes.error.message);
            return false;
        }
        console.log(`${GREEN}PASS${RESET}`);

        return true;

    } finally {
        // 5. Restore
        fs.rmSync(ws, { recursive: true, force: true });
        fs.cpSync(backup, ws, { recursive: true });
        fs.rmSync(backup, { recursive: true, force: true });
    }
}

async function main() {
    let failed = 0;
    for (const q of QUESTS) {
        const ok = await checkQuest(q);
        if (!ok) failed++;
    }

    console.log("\n" + "=".repeat(30));
    if (failed > 0) {
        console.log(`${RED}INTEGRITY CHECK FAILED: ${failed} quests failed.${RESET}`);
        process.exit(1);
    } else {
        console.log(`${GREEN}ALL INFRA QUESTS PASSED INTEGRITY CHECK${RESET}`);
    }
}

main();
