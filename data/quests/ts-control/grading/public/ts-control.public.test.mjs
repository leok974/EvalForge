import test from "node:test";
import assert from "node:assert/strict";
import { fizzBuzz } from "../../workspace/main.ts";

test("fizzBuzz logic", () => {
    assert.equal(fizzBuzz(3), "Fizz");
    assert.equal(fizzBuzz(5), "Buzz");
    assert.equal(fizzBuzz(15), "FizzBuzz");
    assert.equal(fizzBuzz(2), "2");
});