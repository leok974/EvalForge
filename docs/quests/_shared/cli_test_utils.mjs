import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);

/**
 * From a test file at:
 *   data/quests/<slug>/grading/{public|hidden}/x.test.mjs
 * returns the workspace directory:
 *   data/quests/<slug>/workspace
 * 
 * Note: checks for 'workspace' or 'starter' to support local dev structure.
 */
export function workspaceDirFromTestFile(importMetaUrl) {
    const testFile = fileURLToPath(importMetaUrl);
    const testDir = path.dirname(testFile);

    // Try standard ../../workspace first (for production structure)
    let check = path.resolve(testDir, "../../workspace");
    if (fs.existsSync(check)) return check;

    // Fallback to ../../starter (for local dev structure we've been using)
    check = path.resolve(testDir, "../../starter");
    if (fs.existsSync(check)) return check;

    // Default to workspace even if missing, to allow failure elsewhere
    return path.resolve(testDir, "../../workspace");
}

export async function runSh({
    ws,
    args = ["task.sh"],
    env = {},
    timeoutMs = 5000,
} = {}) {
    if (!ws) throw new Error("runSh requires { ws }");

    // Windows-friendly sh resolution
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";

    return execFileAsync(sh, args, {
        cwd: ws,
        timeout: timeoutMs,
        env: { ...process.env, ...env },
    });
}

export function readText(ws, relPath) {
    // Normalize CRLF to LF for consistent testing on Windows
    return fs.readFileSync(path.join(ws, relPath), "utf8").replace(/\r\n/g, "\n");
}

export function readTextTrim(ws, relPath) {
    return readText(ws, relPath).trimEnd();
}

export function writeText(ws, relPath, content) {
    fs.mkdirSync(path.dirname(path.join(ws, relPath)), { recursive: true });
    fs.writeFileSync(path.join(ws, relPath), content, "utf8");
}

export function exists(ws, relPath) {
    return fs.existsSync(path.join(ws, relPath));
}

/**
 * Temporarily overwrite a workspace file and restore it after the callback.
 */
export async function withRestoredFile(ws, relPath, fn) {
    const abs = path.join(ws, relPath);
    const had = fs.existsSync(abs);
    const orig = had ? fs.readFileSync(abs, "utf8") : null;

    try {
        return await fn(abs);
    } finally {
        if (had) fs.writeFileSync(abs, orig, "utf8");
        else if (fs.existsSync(abs)) fs.unlinkSync(abs);
    }
}
