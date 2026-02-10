import React, { useReducer } from 'react';

const initialState = { total: 0 };

function reducer(state, action) {
    switch (action.type) {
        case 'ADD':
            return { total: state.total + action.amount };
        case 'RESET':
            return initialState;
        default:
            return state;
    }
}

export function ShoppingCart() {
    const [state, dispatch] = useReducer(reducer, initialState);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'total' }, String(state.total)),
        React.createElement('button', {
            'data-testid': 'add-10',
            onClick: () => dispatch({ type: 'ADD', amount: 10 })
        }, '+10'),
        React.createElement('button', {
            'data-testid': 'reset',
            onClick: () => dispatch({ type: 'RESET' })
        }, 'Reset')
    );
}
