// TS Control
// Classify HTTP-like status codes using typed control flow.

export type StatusClass =
    | "success"
    | "redirect"
    | "client_error"
    | "server_error"
    | "invalid";

export function classifyStatus(code: unknown): StatusClass {
    if (typeof code !== "number") return "invalid";
    if (!Number.isInteger(code)) return "invalid";

    if (code >= 200 && code <= 299) return "success";
    if (code >= 300 && code <= 399) return "redirect";
    if (code >= 400 && code <= 499) return "client_error";
    if (code >= 500 && code <= 599) return "server_error";

    return "invalid";
}
