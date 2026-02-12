// TS Interfaces
// Define interfaces and implement a deterministic formatter.

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
    // TODO: implement rules from README
    return `${e.type} id=${e.id} ts=${e.ts}`;
}
