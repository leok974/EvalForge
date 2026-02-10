import React from 'react';

export function CardBody() {
    return React.createElement('div', { 'data-testid': 'card-body' }, 'I am the body');
}

export function Card() {
    return React.createElement('div', { 'data-testid': 'card' },
        React.createElement(CardBody)
    );
}
