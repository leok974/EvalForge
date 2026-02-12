import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, textContent } from "../../../_shared/react_test_helpers.mjs";
import { Card } from "../../workspace/task.mjs";

test("Card renders CardBody nested inside", () => {
    const { root } = runComponent(Card);

    const card = findByTestId(root, "card");
    assert.equal(card.type, "div");

    const body = findByTestId(card, "card-body");
    assert.equal(body.type, "div");
    assert.equal(textContent(body), "I am the body");
});
