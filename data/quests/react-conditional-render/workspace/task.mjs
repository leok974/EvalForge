import React from 'react';

export function ToggleSection({ title, isVisible }) {
    return React.createElement('div', null,
        React.createElement('h2', null, title)
        // TODO: conditional p tag
    );
}
