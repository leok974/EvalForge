import React, { useReducer } from 'react';

const initialState = { total: 0 };

function reducer(state, action) {
    // TODO: implement reducer logic
    return state;
}

export function ShoppingCart() {
    const [state, dispatch] = useReducer(reducer, initialState);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'total' }, state.total),
        React.createElement('button', { 'data-testid': 'add-10' }, '+10'),
        React.createElement('button', { 'data-testid': 'reset' }, 'Reset')
    );
}
