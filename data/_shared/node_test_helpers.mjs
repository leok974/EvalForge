
import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export const DEFAULT_TIMEOUT_MS = 5000;

export function readText(wsDir, rel) {
    return fs.readFileSync(path.join(wsDir, rel), "utf8").trimEnd();
}

export function writeText(wsDir, rel, txt) {
    fs.mkdirSync(path.dirname(path.join(wsDir, rel)), { recursive: true });
    fs.writeFileSync(path.join(wsDir, rel), txt, "utf8");
}

export async function runSh(wsDir, scriptRel = "task.sh", args = [], env = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
    const merged = { ...process.env };

    // Allow callers to unset env vars by passing null/undefined
    const envKeysToShare = [];
    for (const [k, v] of Object.entries(env || {})) {
        if (v === undefined || v === null) {
            delete merged[k];
        } else {
            merged[k] = String(v);
            envKeysToShare.push(k);
        }
    }

    // On Windows, if using WSL, we need to explicitly list env vars in WSLENV to share them
    if (process.platform === "win32" && envKeysToShare.length > 0) {
        const currentWslEnv = merged.WSLENV ? merged.WSLENV + ":" : "";
        merged.WSLENV = currentWslEnv + envKeysToShare.join(":");
    }

    // Use bash on Windows/WSL environments if sh is missing, or default to sh
    const shell = process.platform === "win32" ? "bash" : "sh";
    return execFileAsync(shell, [scriptRel, ...args], {
        cwd: wsDir,
        timeout: timeoutMs,
        env: merged,
    });
}

export async function runNode(wsDir, scriptRel, args = [], env = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
    const merged = { ...process.env, NODE_DISABLE_COLORS: "1", FORCE_COLOR: "0" };
    // Unset via null/undefined
    for (const [k, v] of Object.entries(env || {})) {
        if (v === undefined || v === null) delete merged[k];
        else merged[k] = String(v);
    }

    return execFileAsync(process.execPath, [scriptRel, ...args], {
        cwd: wsDir,
        timeout: timeoutMs,
        env: merged,
    });
}

export function listFiles(dir, suffix) {
    if (!fs.existsSync(dir)) return [];
    return fs.readdirSync(dir).filter((f) => f.endsWith(suffix)).map((f) => path.join(dir, f));
}

export async function withRestoredFile(wsDir, relPath, fn) {
    const absPath = path.join(wsDir, relPath);
    let original = null;
    const exists = fs.existsSync(absPath);
    if (exists) {
        original = fs.readFileSync(absPath, "utf8");
    }

    try {
        await fn();
    } finally {
        if (exists) {
            fs.writeFileSync(absPath, original, "utf8");
        } else {
            if (fs.existsSync(absPath)) fs.unlinkSync(absPath);
        }
    }
}
