import fs from "node:fs";
import path from "node:path";

function fail(msg) {
    console.error(msg);
    process.exit(1);
}

const cwd = process.cwd();
const lockPath = path.join(cwd, "package-lock.json");
const pkgPath = path.join(cwd, "package.json");

if (!fs.existsSync(lockPath)) {
    fail("Missing package-lock.json");
}

let lock;
try {
    lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));
} catch {
    fail("Invalid JSON in package-lock.json");
}

const version = lock?.lockfileVersion;
if (typeof version !== "number" || version < 2) {
    fail("lockfileVersion must be >= 2");
}

let pkg;
try {
    pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
} catch {
    fail("Invalid JSON in package.json");
}

const pkgName = pkg?.name;
const lockName = lock?.name;

// Only enforce name match if lockfile has a name field.
if (typeof lockName === "string") {
    if (typeof pkgName !== "string" || pkgName.trim() === "") {
        fail("package.json name is missing");
    }
    if (lockName !== pkgName) {
        fail(`Lockfile name mismatch: expected ${pkgName}`);
    }
}

console.log("Lockfile OK");
process.exit(0);
