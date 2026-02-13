import json
import os
import shutil
from pathlib import Path

# Prism TS Quests
PRISM_TS_SPECS = [
    {
        "slug": "quest-ts-hello-console",
        "title": "Hello Console",
        "student_task_summary": "Print 'Hello, Prism' to the console.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";

// Execute the main.ts file and check output
test("Output is correct", () => {
    // We assume running from repo root or utilizing test runner env
    // But here we need to run the TS file. 
    // Best is to use 'tsx' to run workspace/main.ts
    // We can rely on relative path from this test file: ../../workspace/main.ts
    
    const wsMain = path.resolve(import.meta.dirname, "../../workspace/main.ts");
    
    // We use 'process.execPath' (node) with --import tsx? Or just 'npx tsx'?
    // Let's assume 'npx tsx' is available or use node loader.
    // Simpler: assume the runner handles environment, preventing network access etc is not our job here.
    
    const res = spawnSync("npx", ["tsx", wsMain], { encoding: "utf8", shell: true });
    
    assert.equal(res.status, 0, "Script should exit 0");
    assert.match(res.stdout, /Hello, Prism/);
});
""",
        "solution_ts": """
console.log("Hello, Prism");
"""
    },
    {
        "slug": "quest-ts-hello-variable",
        "title": "Hello Variable",
        "student_task_summary": "Export variable `energy` (number) set to 100.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.ts";

test("energy variable", () => {
    assert.equal(typeof mod.energy, "number");
    assert.equal(mod.energy, 100);
});
""",
        "solution_ts": """
export let energy: number = 100;
"""
    },
    {
        "slug": "quest-ts-loop-countdown",
        "title": "Loop Countdown",
        "student_task_summary": "Export function `countdown(start: number): number[]` returning [start, start-1, ..., 0].",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { countdown } from "../../workspace/main.ts";

test("countdown logic", () => {
    assert.deepEqual(countdown(3), [3, 2, 1, 0]);
    assert.deepEqual(countdown(0), [0]);
});
""",
        "solution_ts": """
export function countdown(start: number): number[] {
    const res: number[] = [];
    for (let i = start; i >= 0; i--) {
        res.push(i);
    }
    return res;
}
"""
    },
    {
        "slug": "ts-ignition-q1-types-and-interfaces",
        "title": "Types and Interfaces",
        "student_task_summary": "Define interface `Item` { name: string; weight: number } and export `createItem(n: string, w: number): Item`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { createItem } from "../../workspace/main.ts";

test("createItem", () => {
    const i = createItem("Rock", 5);
    assert.equal(i.name, "Rock");
    assert.equal(i.weight, 5);
});
""",
        "solution_ts": """
export interface Item {
    name: string;
    weight: number;
}

export function createItem(name: string, weight: number): Item {
    return { name, weight };
}
"""
    },
    {
        "slug": "ts-narrowing-q2-unions-and-guards",
        "title": "Unions and Guards",
        "student_task_summary": "Export `format(val: string | number): string`. If number, return 'Value: N', if string, return uppercase.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { format } from "../../workspace/main.ts";

test("format logic", () => {
    assert.equal(format(10), "Value: 10");
    assert.equal(format("hello"), "HELLO");
});
""",
        "solution_ts": """
export function format(val: string | number): string {
    if (typeof val === "number") {
        return `Value: ${val}`;
    }
    return val.toUpperCase();
}
"""
    },
    {
        "slug": "ts-generics-q2-result-type",
        "title": "Result Type",
        "student_task_summary": "Implement generic `Result<T>` type and `success<T>(data: T): Result<T>` helper (tagged union with discriminated union).",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { success } from "../../workspace/main.ts";

test("success helper", () => {
    const res = success(42);
    assert.equal(res.status, "success");
    if (res.status === "success") {
        assert.equal(res.data, 42); 
    }
});
""",
        "solution_ts": """
export type Result<T> = 
    | { status: "success"; data: T }
    | { status: "error"; error: string };

export function success<T>(data: T): Result<T> {
    return { status: "success", data };
}
"""
    }
]

def main():
    root = Path.cwd()
    quests_dir = root / "data" / "quests"
    
    # We only scaffold Prism TS, because Prism JS reuses existing JS Core quests (already scaffolded)
    for q in PRISM_TS_SPECS:
        slug = q["slug"]
        print(f"Scaffolding {slug}...")
        q_dir = quests_dir / slug
        
        # Paths
        ws_dir = q_dir / "workspace"
        grading_dir = q_dir / "grading"
        
        # Clean
        if ws_dir.exists(): shutil.rmtree(ws_dir)
        if grading_dir.exists(): shutil.rmtree(grading_dir)
        
        ws_dir.mkdir(parents=True, exist_ok=True)
        pub_dir = grading_dir / "public"
        sol_dir = grading_dir / "solutions"
        pub_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)
        
        # README
        readme_txt = f"# {q['title']}\n\n{q['student_task_summary']}\n"
        (ws_dir / "README.md").write_bytes(readme_txt.encode("utf-8"))
        
        # Starter main.ts
        starter_ts = "// TODO: Implement\nexport const task = {};\n"
        # Special case for console log quest which might not export anything
        if "console" in slug:
             starter_ts = "// TODO: Print 'Hello, Prism'\n"
        (ws_dir / "main.ts").write_bytes(starter_ts.encode("utf-8"))
        
        # package.json (ESM for TS execution context via tsx if needed, though tsx handles imports usually)
        # But node:test running .mjs needs package.json type:module if we import relative
        pkg_json = '{\n  "type": "module"\n}\n'
        (ws_dir / "package.json").write_bytes(pkg_json.encode("utf-8"))
        
        # Tests
        test_txt = q["test_code"].replace("\r\n", "\n").strip()
        (pub_dir / f"{slug}.public.test.mjs").write_bytes(test_txt.encode("utf-8"))
        
        # Solution
        sol_txt = q["solution_ts"].replace("\r\n", "\n").strip()
        (sol_dir / "main.ts").write_bytes(sol_txt.encode("utf-8"))
    
    print("Done.")

if __name__ == "__main__":
    main()
