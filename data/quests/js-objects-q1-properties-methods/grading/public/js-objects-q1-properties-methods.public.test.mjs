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