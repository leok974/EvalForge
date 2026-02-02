// Crystal Forge: Generics + Result<T,E>
// Implement Result + helpers + parseIntStrict + mapResult.

export type Result<T, E> =
    | { ok: true; value: T }
    | { ok: false; error: E };

export function ok<T>(value: T): Result<T, never> {
    // TODO
    return { ok: true, value };
}

export function err<E>(error: E): Result<never, E> {
    // TODO
    return { ok: false, error };
}

export function parseIntStrict(input: string): Result<number, string> {
    // TODO: trim, parse base 10 int, return ok(n) or err("invalid integer")
    return err("invalid integer");
}

export function mapResult<T, U, E>(
    res: Result<T, E>,
    fn: (value: T) => U
): Result<U, E> {
    // TODO: transform ok values; preserve errors
    return res.ok ? ok(fn(res.value)) : res;
}

// Demo
const r1 = parseIntStrict(" 42 ");
console.log(r1.ok ? r1.value : r1.error);

const r2 = mapResult(parseIntStrict("7"), (n) => n * 2);
console.log(r2.ok ? r2.value : r2.error);

const r3 = parseIntStrict("nope");
console.log(r3.ok ? r3.value : r3.error);
