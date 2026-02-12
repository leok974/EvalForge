// TS Functions
// Compute an order total from line items safely.

export type LineItem = {
    sku: string;
    priceCents: number;
    qty: number;
};

function isPlainObject(value: unknown): value is Record<string, unknown> {
    if (!value || typeof value !== "object") return false;
    const proto = Object.getPrototypeOf(value);
    return proto === Object.prototype || proto === null;
}

function isValidLineItem(value: unknown): value is LineItem {
    // TODO: implement validation per README
    return false;
}

export function totalCents(input: unknown): number {
    // TODO: implement rules per README
    return 0;
}
