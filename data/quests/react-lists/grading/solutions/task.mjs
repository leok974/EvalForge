import React from "react";

export function UserList({ users }) {
    const items = (users ?? []).map((u) =>
        React.createElement(
            "li",
            { key: u.id, "data-testid": `user-${u.id}` },
            u.name
        )
    );

    return React.createElement("ul", { "data-testid": "user-list" }, ...items);
}
