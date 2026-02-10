import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { UserList } from "../../workspace/task.mjs";

test("dynamic list updates", () => {
    const users = [{ id: 10, name: "X" }, { id: 11, name: "Y" }];
    const { root } = runComponent(UserList, { users });

    const ul = findByTestId(root, "user-list");
    const lis = ul.findAllByType("li");

    assert.equal(lis.length, 2, "EF_REACT_LIST_DYNAMIC_COUNT");
    assert.equal(lis[1].children[0], "Y", "EF_REACT_LIST_DYNAMIC_TEXT");
});
