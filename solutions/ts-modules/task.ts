// TS Modules - main task
import { sum, toCents } from "./math.ts";

export function formatInvoiceTotal(lineTotalsDollars: number[]): string {
    const centsArr = lineTotalsDollars.map((d) => toCents(d));
    const total = sum(centsArr);
    return `Total: ${total} cents`;
}
