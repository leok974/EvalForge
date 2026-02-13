import json
import os
import shutil
from pathlib import Path

# User Specs mapped to existing slugs
QUESTS_SPECS = [
    {
        "slug": "js-ignition-q1-console-and-functions",
        "title": "Ignition: Console & Functions",
        "student_task_summary": "Export a function `hello()` that returns 'Hello World'.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { hello } from "../../workspace/main.js";

test("hello() returns correct string", () => {
    assert.equal(hello(), "Hello World");
});
""",
        "solution_js": """
export function hello() {
    return "Hello World";
}
"""
    },
    {
        "slug": "js-vars-q1-let-const-var",
        "title": "Variables: Let, Const, Var",
        "student_task_summary": "Export `age` (let), `NAME` (const), and `isStudent` (var).",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.js"; // Import namespace to check exports

test("Exports exist and are correct types", () => {
    assert.equal(typeof mod.age, "number");
    assert.equal(typeof mod.NAME, "string");
    assert.equal(typeof mod.isStudent, "boolean");
});

test("NAME is constant convention", () => {
    assert.equal(mod.NAME, "EvalForge");
});
""",
        "solution_js": """
export let age = 25;
export const NAME = "EvalForge";
export var isStudent = true;
"""
    },
    {
        "slug": "js-control-q1-if-else-loops",
        "title": "Control Flow",
        "student_task_summary": "Implement `checkNumber(n)` returning 'positive'/'negative'/'zero'. Implement `sumTo(n)`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { checkNumber, sumTo } from "../../workspace/main.js";

test("checkNumber", () => {
    assert.equal(checkNumber(10), "positive");
    assert.equal(checkNumber(-5), "negative");
    assert.equal(checkNumber(0), "zero");
});

test("sumTo", () => {
    assert.equal(sumTo(5), 15); // 1+2+3+4+5
    assert.equal(sumTo(1), 1);
    assert.equal(sumTo(0), 0);
});
""",
        "solution_js": """
export function checkNumber(n) {
    if (n > 0) return "positive";
    if (n < 0) return "negative";
    return "zero";
}

export function sumTo(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) sum += i;
    return sum;
}
"""
    },
    {
        "slug": "js-arrays-q1-basics",
        "title": "Arrays Basics",
        "student_task_summary": "Implement `getFirst(arr)`, `getLast(arr)`, and `addEnd(arr, item)`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { getFirst, getLast, addEnd } from "../../workspace/main.js";

test("Array Access", () => {
    const arr = [10, 20, 30];
    assert.equal(getFirst(arr), 10);
    assert.equal(getLast(arr), 30);
});

test("Array Mutation", () => {
    const arr = [1, 2];
    const newArr = addEnd(arr, 3);
    assert.deepEqual(newArr, [1, 2, 3]);
    // Allow mutation or new array, usually mutation is standard for 'push'
    // But safely return result
});
""",
        "solution_js": """
export function getFirst(arr) {
    return arr[0];
}
export function getLast(arr) {
    return arr[arr.length - 1];
}
export function addEnd(arr, item) {
    arr.push(item);
    return arr;
}
"""
    },
    {
        "slug": "js-arrays-q2-map-filter-reduce",
        "title": "Array Methods",
        "student_task_summary": "Implement `doubleAll(arr)`, `getEvens(arr)`, `sumAll(arr)`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { doubleAll, getEvens, sumAll } from "../../workspace/main.js";

test("doubleAll", () => {
    assert.deepEqual(doubleAll([1, 2]), [2, 4]);
});

test("getEvens", () => {
    assert.deepEqual(getEvens([1, 2, 3, 4]), [2, 4]);
});

test("sumAll", () => {
    assert.equal(sumAll([1, 2, 3]), 6);
});
""",
        "solution_js": """
export function doubleAll(arr) {
    return arr.map(x => x * 2);
}
export function getEvens(arr) {
    return arr.filter(x => x % 2 === 0);
}
export function sumAll(arr) {
    return arr.reduce((acc, x) => acc + x, 0);
}
"""
    },
    {
        "slug": "js-objects-q1-properties-methods",
        "title": "Objects",
        "student_task_summary": "Export `person` object with `firstName`, `lastName`, and `fullName()` method.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { person } from "../../workspace/main.js";

test("person object structure", () => {
    assert.equal(person.firstName, "John");
    assert.equal(person.lastName, "Doe");
});

test("fullName method", () => {
    assert.equal(person.fullName(), "John Doe");
});
""",
        "solution_js": """
export const person = {
    firstName: "John",
    lastName: "Doe",
    fullName() {
        return `${this.firstName} ${this.lastName}`;
    }
};
"""
    },
    {
        "slug": "js-functions-q1-arrow-vs-regular",
        "title": "Functions: Arrow",
        "student_task_summary": "Export `add(a,b)` (regular) and `multiply(a,b)` (arrow) functions.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { add, multiply } from "../../workspace/main.js";

test("add function", () => {
    assert.equal(add(2, 3), 5);
});

test("multiply arrow function", () => {
    assert.equal(multiply(3, 4), 12);
});
""",
        "solution_js": """
export function add(a, b) {
    return a + b;
}

export const multiply = (a, b) => a * b;
"""
    },
    {
        "slug": "js-async-q1-promises-basics",
        "title": "Async Promises",
        "student_task_summary": "Implement `waitAndReturn(ms, val)` that returns a Promise resolving to val after ms.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { waitAndReturn } from "../../workspace/main.js";

test("waitAndReturn returns correct value", async () => {
    const start = Date.now();
    const val = await waitAndReturn(50, "foo");
    const diff = Date.now() - start;
    
    assert.equal(val, "foo");
    assert.ok(diff >= 40, "Should wait approx timeout");
});
""",
        "solution_js": """
export function waitAndReturn(ms, val) {
    return new Promise(resolve => setTimeout(() => resolve(val), ms));
}
"""
    },
    {
        "slug": "js-errors-q1-try-catch",
        "title": "Errors",
        "student_task_summary": "Implement `parseJson(str)` that returns parsed object or null on error.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import { parseJson } from "../../workspace/main.js";

test("parseJson valid", () => {
    assert.deepEqual(parseJson('{"a":1}'), {a: 1});
});

test("parseJson invalid returns null", () => {
    assert.equal(parseJson('{bad:'), null);
});
""",
        "solution_js": """
export function parseJson(str) {
    try {
        return JSON.parse(str);
    } catch (e) {
        return null;
    }
}
"""
    },
    {
        "slug": "js-modules-q1-import-export",
        "title": "Modules",
        "student_task_summary": "Export constants `PI`, `E` and default export function `circleArea(r)`.",
        "test_code": """
import test from "node:test";
import assert from "node:assert/strict";
import circleArea, { PI, E } from "../../workspace/main.js";

test("Named exports", () => {
    assert.equal(PI, 3.14159);
    assert.equal(E, 2.718);
});

test("Default export circleArea", () => {
    assert.ok(Math.abs(circleArea(1) - 3.14159) < 0.0001);
});
""",
        "solution_js": """
export const PI = 3.14159;
export const E = 2.718;

export default function circleArea(r) {
    return PI * r * r;
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
        
        # Starter main.js
        starter_js = "// TODO: Implement\nexport function task() {}\n"
        (ws_dir / "main.js").write_bytes(starter_js.encode("utf-8"))
        
        # package.json (ESM)
        pkg_json = '{\n  "type": "module",\n  "main": "main.js"\n}\n'
        (ws_dir / "package.json").write_bytes(pkg_json.encode("utf-8"))
        
        # Tests
        test_txt = q["test_code"].replace("\r\n", "\n").strip()
        (pub_dir / f"{slug}.public.test.mjs").write_bytes(test_txt.encode("utf-8"))
        
        # Solution
        sol_txt = q["solution_js"].replace("\r\n", "\n").strip()
        (sol_dir / "main.js").write_bytes(sol_txt.encode("utf-8"))
    
    print("Done.")

if __name__ == "__main__":
    main()
