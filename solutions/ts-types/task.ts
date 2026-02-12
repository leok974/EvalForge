// TS Types
// Build a tiny runtime-safe parser using TypeScript types + type guards.

export type Role = "admin" | "user" | "guest";

export type User = {
    id: number;
    name: string;
    role: Role;
};

export function isUser(value: unknown): value is User {
    if (!value || typeof value !== "object") return false;
    const u = value as any;
    return (
        typeof u.id === "number" &&
        typeof u.name === "string" &&
        ["admin", "user", "guest"].includes(u.role)
    );
}

export function parseUser(json: string): User {
    try {
        const parsed = JSON.parse(json);
        if (!isUser(parsed)) {
            throw new Error("Invalid shape");
        }
        return parsed;
    } catch {
        throw new Error("EF_TS_TYPES_INVALID");
    }
}
