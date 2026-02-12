import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function workspaceDirFromTestFile(metaUrl) {
    // Runner override (enables temp, isolated workspaces)
    const override = process.env.EF_WORKSPACE_OVERRIDE;
    if (override && override.trim()) return override;

    // Default behavior: locate sibling workspace/starter relative to grading/public test file
    const testFile = fileURLToPath(new URL(metaUrl));
    const questDir = path.resolve(path.dirname(testFile), "..", ".."); // grading/public -> quest root

    const ws = path.join(questDir, "workspace");
    if (fs.existsSync(ws)) return ws;

    const starter = path.join(questDir, "starter");
    if (fs.existsSync(starter)) return starter;

    // Last resort: old layouts
    return questDir;
}

export function readTextTrim(ws, relPath) {
    const abs = path.join(ws, relPath);
    const txt = fs.readFileSync(abs, "utf8");
    return txt.replace(/\r\n/g, "\n").trimEnd();
}

export function readText(ws, relPath) {
    return fs.readFileSync(path.join(ws, relPath), "utf8").replace(/\r\n/g, "\n");
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

// IMPORTANT: do NOT throw on non-zero exit — return { status, stdout, stderr }
export async function runSh({ ws, args = [], env = {} } = {}) {
    const cleanEnv = { ...process.env };

    // Allow callers to *unset* env vars by passing undefined/null
    for (const [k, v] of Object.entries(env || {})) {
        if (v === undefined || v === null) delete cleanEnv[k];
        else cleanEnv[k] = String(v);
    }

    // Windows-friendly sh resolution
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";

    const argv = [sh, "task.sh", ...args];

    return await new Promise((resolve, reject) => {
        const child = spawn(argv[0], argv.slice(1), {
            cwd: ws,
            env: cleanEnv,
            shell: false,
            stdio: ["ignore", "pipe", "pipe"],
        });

        let stdout = "";
        let stderr = "";

        child.stdout.on("data", (d) => (stdout += d.toString("utf8")));
        child.stderr.on("data", (d) => (stderr += d.toString("utf8")));

        child.on("error", reject);
        child.on("close", (code) => {
            resolve({
                status: code ?? 0,
                stdout,
                stderr,
            });
        });
    });
}
