// TS Control
// Classify HTTP-like status codes using typed control flow.

export type StatusClass =
    | "success"
    | "redirect"
    | "client_error"
    | "server_error"
    | "invalid";

export function classifyStatus(code: unknown): StatusClass {
    // TODO: implement rules per README
    return "invalid";
}
