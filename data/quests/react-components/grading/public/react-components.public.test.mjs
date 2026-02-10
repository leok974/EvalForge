import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { Card, CardBody } from "../../workspace/task.mjs";

test("Card renders CardBody", () => {
    const { root } = runComponent(Card);

    const card = findByTestId(root, "card");
    const body = findByTestId(card, "card-body"); // Search *inside* card

    assert.ok(body, "EF_REACT_COMP_NESTING: CardBody must be inside Card");
    assert.equal(body.children[0], "I am the body", "EF_REACT_COMP_TEXT");
});
