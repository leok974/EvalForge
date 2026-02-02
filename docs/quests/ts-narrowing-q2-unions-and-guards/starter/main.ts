// Crystal Lens: Unions + Type Guards
// Implement the functions without using unsafe casts as a shortcut.

export type Contact =
    | { kind: "email"; email: string }
    | { kind: "phone"; phone: string };

export function normalizeId(id: string | number): number | null {
    // TODO: if number -> return it
    // TODO: if string -> trim + parse int base 10
    // TODO: if NaN -> return null
    return null;
}

export function isContact(value: unknown): value is Contact {
    // TODO: implement as a type guard (return value is Contact)
    return false;
}

export function formatContact(contact: Contact): string {
    // TODO: use switch on contact.kind
    return "";
}

// Demo
console.log(normalizeId(" 42 "));
console.log(isContact({ kind: "email", email: "a@b.com" }));
console.log(formatContact({ kind: "phone", phone: "555-1234" }));
