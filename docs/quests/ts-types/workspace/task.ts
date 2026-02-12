// TS Types
// Build a tiny runtime-safe parser using TypeScript types + type guards.

export type Role = "admin" | "user" | "guest";

export type User = {
    id: number;
    name: string;
    role: Role;
};

export function isUser(value: unknown): value is User {
    // TODO: implement a runtime shape check
    // Requirements:
    // - value must be a non-null object
    // - id must be a number
    // - name must be a string
    // - role must be one of "admin" | "user" | "guest"
    return false;
}

export function parseUser(json: string): User {
    // TODO: parse JSON and validate using isUser
    // Throw Error("EF_TS_TYPES_INVALID") on any failure.
    throw new Error("EF_TS_TYPES_INVALID");
}
