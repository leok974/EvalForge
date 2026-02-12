// TS Functions
// Implement a safe totalCents function that ignores invalid items.

export type LineItem = {
    sku: string;
    priceCents: number;
    qty: number;
};

export function totalCents(items: unknown): number {
    if (!Array.isArray(items)) return 0;

    let total = 0;
    for (const item of items) {
        if (!item || typeof item !== "object") continue;

        // validate sku
        if (typeof item.sku !== "string") continue;
        const sku = item.sku.trim();
        if (sku.length === 0) continue;

        // validate priceCents
        if (typeof item.priceCents !== "number" || !Number.isInteger(item.priceCents)) continue;
        if (item.priceCents < 0) continue; // New check per README

        // validate qty
        if (typeof item.qty !== "number" || !Number.isInteger(item.qty)) continue;
        if (item.qty < 1 || item.qty > 99) continue;

        total += item.priceCents * item.qty;
    }

    return total;
}
