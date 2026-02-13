export type User = {
    id: number;
    username: string;
};

export function getUser(id: number, username: string): User {
    return { id, username };
}