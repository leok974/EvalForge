import { loadUser } from "./db.js";

export async function getUserName(id) {
    try {
        const user = await loadUser(id);
        return user.name;
    } catch (err) {
        return "Guest";
    }
}
