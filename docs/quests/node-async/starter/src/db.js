import { setTimeout } from "node:timers/promises";

export async function loadUser(id) {
    await setTimeout(50); // Simulate DB delay
    if (id < 0) throw new Error("Invalid ID");
    return { id, name: "User" + id };
}
