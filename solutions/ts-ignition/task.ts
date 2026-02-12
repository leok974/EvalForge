// TS Ignition
// Implement a typed handshake payload with literal types.

export type Handshake = {
    message: "System Online";
    code: 42;
    ok: true;
};

export function handshake(): Handshake {
    // TODO: return the exact payload that matches Handshake
    return {
        message: "System Online",
        code: 42,
        ok: true,
    };
}
