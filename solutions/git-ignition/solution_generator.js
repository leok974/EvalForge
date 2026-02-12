import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

// Get the mapped workspace path from environment
const workspace = process.env.EF_WORKSPACE_OVERRIDE;
if (!workspace) {
    console.error("EF_WORKSPACE_OVERRIDE not set");
    process.exit(1);
}

console.log(`Generating solution for git-ignition in ${workspace}`);

// Run git init
const res = spawnSync("git", ["init"], { cwd: workspace, stdio: "inherit" });
if (res.status !== 0) {
    console.error("Failed to run git init");
    process.exit(1);
}

// Create a commit so it's a valid repo with HEAD (optional for this quest, but good practice)
spawnSync("git", ["add", "."], { cwd: workspace });
spawnSync("git", ["commit", "-m", "Initial commit"], { cwd: workspace });
