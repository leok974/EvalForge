import React from 'react';

export function UserList({ users }) {
    return React.createElement('ul', { 'data-testid': 'user-list' },
        users.map(u => React.createElement('li', { key: u.id }, u.name))
    );
}
