import React, { useReducer } from "react";

function reducer(state, action) {
    switch (action.type) {
        case "ADD":
            return { total: state.total + Number(action.amount ?? 0) };
        case "RESET":
            return { total: 0 };
        default:
            return state;
    }
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
