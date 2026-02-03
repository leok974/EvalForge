import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function fail(msg) {
    console.error(msg);
    process.exit(2);
}

const root = process.cwd();
const pkgPath = path.join(root, "package.json");
const lockPath = path.join(root, "package-lock.json");

if (!fs.existsSync(lockPath)) fail("EF_NODE_NPM_LOCKFILE_MISSING: package-lock.json is required");

let pkg;
let lock;
try {
    pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
} catch {
    fail("EF_NODE_NPM_PKG_JSON_INVALID: package.json must be valid JSON");
}

try {
    lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));
} catch {
    fail("EF_NODE_NPM_LOCK_JSON_INVALID: package-lock.json must be valid JSON");
}

if (typeof lock.lockfileVersion !== "number" || lock.lockfileVersion < 2) {
    fail("EF_NODE_NPM_LOCK_VERSION: lockfileVersion must be >= 2");
}

if (pkg?.name && lock?.name && pkg.name !== lock.name) {
    fail(`EF_NODE_NPM_LOCK_NAME: lockfile name '${lock.name}' must match package.json name '${pkg.name}'`);
}

console.log("Lockfile OK");
process.exit(0);
