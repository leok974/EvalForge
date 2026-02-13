export type Result<T> = 
    | { status: "success"; data: T }
    | { status: "error"; error: string };

export function success<T>(data: T): Result<T> {
    return { status: "success", data };
}