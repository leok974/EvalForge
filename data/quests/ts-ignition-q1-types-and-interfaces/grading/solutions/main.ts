export interface Item {
    name: string;
    weight: number;
}

export function createItem(name: string, weight: number): Item {
    return { name, weight };
}