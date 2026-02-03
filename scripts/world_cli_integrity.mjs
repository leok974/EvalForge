import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

function argFlag(name) {
    return process.argv.includes(name);
}

function argValue(name, def = null) {
    const i = process.argv.indexOf(name);
    if (i === -1) return def;
    const v = process.argv[i + 1];
    return v ?? def;
}

const includeHidden = argFlag("--hidden");
const onlyQuest = argValue("--quest", null);
// Adjusted to match the actual structure used (docs/quests instead of data/quests if that's where they are?)
// Previous interactions showed d:\EvalForge\docs\quests. 
// However, the REQUEST showed `data/quests`. 
// I will check where I put the files. I put them in `docs/quests`.
// But the user request said `data/quests`. 
// I should probably stick to `docs/quests` if that's where I put them, OR move them.
// The user's prompt examples used `data/quests`. 
// BUT my previous tool calls used `d:\EvalForge\docs\quests`.
// The integrity runner should point to where the quests actually ARE.
const questsRoot = path.resolve("docs/quests");

const cliQuestSlugs = [
    "cli-ignition",
    "cli-navigation",
    "cli-files-folders",
    "cli-globs-search",
    "cli-redirection",
    "cli-pipes",
    "cli-env-vars",
    "cli-exit-codes",
    "cli-processes",
    "cli-scripting",
];

const slugs = onlyQuest ? [onlyQuest] : cliQuestSlugs;

function findTestsForQuest(slug) {
    const base = path.join(questsRoot, slug, "grading");
    const tests = [];

    const pubDir = path.join(base, "public");
    if (fs.existsSync(pubDir)) {
        for (const f of fs.readdirSync(pubDir)) {
            if (f.endsWith(".test.mjs")) tests.push(path.join(pubDir, f));
        }
    }

    if (includeHidden) {
        const hidDir = path.join(base, "hidden");
        if (fs.existsSync(hidDir)) {
            for (const f of fs.readdirSync(hidDir)) {
                if (f.endsWith(".test.mjs")) tests.push(path.join(hidDir, f));
            }
        }
    }

    // stable order
    tests.sort();
    return tests;
}

function runNodeTest(testFile) {
    const r = spawnSync(process.execPath, ["--test", testFile], {
        stdio: "pipe",
        encoding: "utf8",
    });

    return {
        ok: r.status === 0,
        code: r.status ?? 1,
        stdout: r.stdout ?? "",
        stderr: r.stderr ?? "",
    };
}

const results = [];
let pass = 0;
let fail = 0;

for (const slug of slugs) {
    const tests = findTestsForQuest(slug);

    if (tests.length === 0) {
        results.push({ slug, ok: false, error: "NO_TESTS_FOUND" });
        fail += 1;
        continue;
    }

    let questOk = true;
    const testRuns = [];

    for (const tf of tests) {
        const tr = runNodeTest(tf);
        testRuns.push({
            file: tf,
            ok: tr.ok,
            code: tr.code,
            stdout_tail: tr.stdout.slice(-2000),
            stderr_tail: tr.stderr.slice(-2000),
        });
        if (!tr.ok) questOk = false;
    }

    if (questOk) pass += 1;
    else fail += 1;

    results.push({ slug, ok: questOk, tests: testRuns });
}

const summary = {
    world: "world-cli",
    includeHidden,
    onlyQuest,
    total: results.length,
    pass,
    fail,
    ok: fail === 0,
    results,
};

fs.mkdirSync("artifacts", { recursive: true });
fs.writeFileSync("artifacts/world-cli-integrity.json", JSON.stringify(summary, null, 2), "utf8");

const mdLines = [];
mdLines.push(`# world-cli integrity`);
mdLines.push(`- includeHidden: ${includeHidden}`);
mdLines.push(`- pass: ${pass}`);
mdLines.push(`- fail: ${fail}`);
mdLines.push("");

for (const r of results) {
    mdLines.push(`## ${r.slug}`);
    mdLines.push(`- status: ${r.ok ? "✅ PASS" : "❌ FAIL"}`);
    if (r.tests) {
        for (const t of r.tests) {
            mdLines.push(`  - ${t.ok ? "✅" : "❌"} ${path.basename(t.file)} (code=${t.code})`);
            if (!t.ok) {
                if (t.stderr_tail.trim()) mdLines.push(`    - stderr: \`${t.stderr_tail.trim().slice(-300).replaceAll("\n", " ")}\``);
                if (t.stdout_tail.trim()) mdLines.push(`    - stdout: \`${t.stdout_tail.trim().slice(-300).replaceAll("\n", " ")}\``);
            }
        }
    } else {
        mdLines.push(`- error: ${r.error}`);
    }
    mdLines.push("");
}

fs.writeFileSync("artifacts/world-cli-integrity.md", mdLines.join("\n"), "utf8");

// exit non-zero so CI can gate
process.exit(summary.ok ? 0 : 1);
