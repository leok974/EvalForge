import json
import os
import shutil
from pathlib import Path

# User Specs mapped to existing slugs
QUESTS_SPECS = [
    {
        "slug": "ts-ignition",
        "title": "TypeScript Ignition",
        "student_task_summary": "Export a function `hello(name: string): string` that returns 'Hello, {name}!'.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { hello } from "../../workspace/main.ts";

test("hello returns greeting", () => {
    assert.equal(hello("World"), "Hello, World!");
    assert.equal(hello("EvalForge"), "Hello, EvalForge!");
});
""",
        "solution_ts": """
export function hello(name: string): string {
    return `Hello, ${name}!`;
}
"""
    },
    {
        "slug": "ts-vars",
        "title": "Basic Types",
        "student_task_summary": "Export variables `age` (number), `name` (string), `isActive` (boolean).",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.ts";

test("Types are correct", () => {
    assert.equal(typeof mod.age, "number");
    assert.equal(typeof mod.name, "string");
    assert.equal(typeof mod.isActive, "boolean");
});
""",
        "solution_ts": """
export let age: number = 25;
export let name: string = "Alice";
export let isActive: boolean = true;
"""
    },
    {
        "slug": "ts-types",
        "title": "Type Annotations",
        "student_task_summary": "Implement `add(a: number, b: number): number`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { add } from "../../workspace/main.ts";

test("add function", () => {
    assert.equal(add(10, 5), 15);
});
""",
        "solution_ts": """
export function add(a: number, b: number): number {
    return a + b;
}
"""
    },
    {
        "slug": "ts-control",
        "title": "Control Flow",
        "student_task_summary": "Implement `fizzBuzz(n: number): string`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { fizzBuzz } from "../../workspace/main.ts";

test("fizzBuzz logic", () => {
    assert.equal(fizzBuzz(3), "Fizz");
    assert.equal(fizzBuzz(5), "Buzz");
    assert.equal(fizzBuzz(15), "FizzBuzz");
    assert.equal(fizzBuzz(2), "2");
});
""",
        "solution_ts": """
export function fizzBuzz(n: number): string {
    if (n % 15 === 0) return "FizzBuzz";
    if (n % 3 === 0) return "Fizz";
    if (n % 5 === 0) return "Buzz";
    return n.toString();
}
"""
    },
    {
        "slug": "ts-arrays",
        "title": "Typed Arrays",
        "student_task_summary": "Implement `sumArray(nums: number[]): number`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { sumArray } from "../../workspace/main.ts";

test("sumArray", () => {
    assert.equal(sumArray([1, 2, 3]), 6);
    assert.equal(sumArray([]), 0);
});
""",
        "solution_ts": """
export function sumArray(nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}
"""
    },
    {
        "slug": "ts-objects",
        "title": "Object Types",
        "student_task_summary": "Define type `User` { id: number, username: string } and export `getUser(id: number, username: string): User`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { getUser } from "../../workspace/main.ts";

test("getUser returns typed object", () => {
    const u = getUser(1, "alice");
    assert.equal(u.id, 1);
    assert.equal(u.username, "alice");
});
""",
        "solution_ts": """
export type User = {
    id: number;
    username: string;
};

export function getUser(id: number, username: string): User {
    return { id, username };
}
"""
    },
    {
        "slug": "ts-functions",
        "title": "Optional Parameters",
        "student_task_summary": "Implement `greet(name: string, title?: string): string`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { greet } from "../../workspace/main.ts";

test("greet logic", () => {
    assert.equal(greet("Alice"), "Hello, Alice");
    assert.equal(greet("Bob", "Dr."), "Hello, Dr. Bob");
});
""",
        "solution_ts": """
export function greet(name: string, title?: string): string {
    if (title) return `Hello, ${title} ${name}`;
    return `Hello, ${name}`;
}
"""
    },
    {
        "slug": "ts-interfaces",
        "title": "Interfaces",
        "student_task_summary": "Define interface `Shape` { area(): number } and class `Circle` implementing it.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { Circle } from "../../workspace/main.ts";

test("Circle implements Shape", () => {
    const c = new Circle(10);
    // Area = pi * r^2 ~= 314.159
    assert.ok(Math.abs(c.area() - 314.159) < 0.01);
});
""",
        "solution_ts": """
export interface Shape {
    area(): number;
}

export class Circle implements Shape {
    constructor(private radius: number) {}
    
    area(): number {
        return Math.PI * this.radius * this.radius;
    }
}
"""
    },
    {
        "slug": "ts-generics",
        "title": "Generics",
        "student_task_summary": "Implement `wrap<T>(val: T): { value: T }`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { wrap } from "../../workspace/main.ts";

test("wrap generic", () => {
    const n = wrap(10);
    assert.equal(n.value, 10);
    
    const s = wrap("foo");
    assert.equal(s.value, "foo");
});
""",
        "solution_ts": """
export function wrap<T>(val: T): { value: T } {
    return { value: val };
}
"""
    },
    {
        "slug": "ts-modules",
        "title": "Modules & Export",
        "student_task_summary": "Export `CONFIG` object and default function `run()`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import run, { CONFIG } from "../../workspace/main.ts";

test("Exports check", () => {
    assert.equal(CONFIG.env, "dev");
    assert.equal(run(), "Running in dev");
});
""",
        "solution_ts": """
export const CONFIG = { env: "dev" };

export default function run(): string {
    return `Running in ${CONFIG.env}`;
}
"""
    }
]

def main():
    root = Path.cwd()
    quests_dir = root / "data" / "quests"
    
    for q in QUESTS_SPECS:
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
        (ws_dir / "main.ts").write_bytes(starter_ts.encode("utf-8"))
        
        # package.json (ESM)
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
