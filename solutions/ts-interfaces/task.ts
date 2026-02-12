// TS Interfaces
// Implement a deterministic formatter using interfaces and type guards.

export interface BaseEvent {
    readonly id: string;
    readonly ts: number;
    type: string;
}

export interface UserEvent extends BaseEvent {
    type: "user.login" | "user.logout";
    userId: string;
    ip?: string;
}

function isUserEvent(e: BaseEvent): e is UserEvent {
    return e.type === "user.login" || e.type === "user.logout";
}

export function formatEvent(e: BaseEvent): string {
    let out = `${e.type} id=${e.id} ts=${e.ts}`;

    if (isUserEvent(e)) {
        out += ` user=${e.userId}`;
        if (e.ip) {
            out += ` ip=${e.ip}`;
        }
    }
    return out;
}
