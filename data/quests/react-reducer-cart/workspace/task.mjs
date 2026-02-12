import React, { useReducer } from "react";

/**
 * TODO:
 * Export ShoppingCart() using useReducer.
 * State: { total: 0 }
 * Actions:
 * - { type: "ADD", amount: 10 } -> total += amount
 * - { type: "RESET" } -> total = 0
 *
 * UI:
 * - div data-testid="total" showing total as string
 * - button data-testid="add-10" dispatches ADD 10
 * - button data-testid="reset" dispatches RESET
 * No JSX.
 */
function reducer(state, action) {
    // TODO: implement pure reducer
    return state;
}

export function ShoppingCart() {
    const [state, dispatch] = useReducer(reducer, { total: 0 });

    const onAdd10 = () => dispatch({ type: "ADD", amount: 10 });
    const onReset = () => dispatch({ type: "RESET" });

    return React.createElement(
        "div",
        { "data-testid": "cart" },
        React.createElement("div", { "data-testid": "total" }, String(state.total)),
        React.createElement("button", { "data-testid": "add-10", onClick: onAdd10 }, "Add 10"),
        React.createElement("button", { "data-testid": "reset", onClick: onReset }, "Reset")
    );
}
