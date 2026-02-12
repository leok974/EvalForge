import test from "node:test";
import assert from "node:assert/strict";

import { cleanScores } from "../../workspace/task.ts";

test("returns [] for non-array input", () => {
    assert.deepEqual(cleanScores(null), [], "EF_TS_ARRAYS_NONARRAY_NULL");
    assert.deepEqual(cleanScores("x"), [], "EF_TS_ARRAYS_NONARRAY_STR");
    assert.deepEqual(cleanScores({}), [], "EF_TS_ARRAYS_NONARRAY_OBJ");
});

test("filters to finite numbers, rounds, bounds 0..100, uniques, sorts", () => {
    const out = cleanScores([
        99.6,     // -> 100
        100.4,    // -> 100 (duplicate)
        -1,       // drop
        0,        // keep
        50.2,     // -> 50
        50.8,     // -> 51
        NaN,      // drop
        Infinity, // drop
        101,      // drop
        1,        // keep
        1.49,     // -> 1 (duplicate)
        2.5       // -> 3
    ]);

    assert.deepEqual(out, [0, 1, 3, 50, 51, 100], "EF_TS_ARRAYS_CLEAN");
});

test("handles already-clean arrays deterministically", () => {
    assert.deepEqual(cleanScores([3, 2, 1, 2, 3]), [1, 2, 3], "EF_TS_ARRAYS_UNIQUE_SORT");
});
