import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, readFixture, textContent } from "../../../_shared/react_test_helpers.mjs";
import { UserList } from "../../workspace/task.mjs";

test("Renders ul with 3 li items from fixtures/users.json", () => {
    const users = readFixture(import.meta.url, "fixtures/users.json");

    const { root } = runComponent(UserList, { users });
    const ul = findByTestId(root, "user-list");

    const lis = ul.findAllByType("li");
    assert.equal(lis.length, 3);

    assert.equal(textContent(lis[0]), "Alice");
    assert.equal(textContent(lis[1]), "Bob");
    assert.equal(textContent(lis[2]), "Charlie");
});
