import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { CardBody } from "../../workspace/task.mjs";

test("CardBody works independently", () => {
    const { root } = runComponent(CardBody);
    const body = findByTestId(root, "card-body");
    assert.ok(body, "EF_REACT_COMP_INDEPENDENT");
});
