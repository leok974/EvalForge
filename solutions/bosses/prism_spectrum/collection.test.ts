import { describe, it, expect } from 'vitest';
import {
    pluck,
    indexBy,
    groupBy,
    mergeById,
    ensureUnique,
} from './collection';

type User = {
    id: string;
    email: string;
    role: 'user' | 'admin';
};

type Job = {
    id: number;
    title: string;
    status: 'open' | 'closed';
};

describe('Curator of the Generic Arsenal – collection toolkit', () => {
    const users: User[] = [
        { id: 'u1', email: 'a@example.com', role: 'user' },
        { id: 'u2', email: 'b@example.com', role: 'admin' },
    ];

    const jobs: Job[] = [
        { id: 1, title: 'TS Engineer', status: 'open' },
        { id: 2, title: 'Python Engineer', status: 'closed' },
    ];

    it('pluck returns typed property arrays', () => {
        const emails = pluck(users, 'email');
        // Type-level: emails: string[]
        expect(emails).toEqual(['a@example.com', 'b@example.com']);
    });

    it('indexBy creates a typed lookup map', () => {
        const byId = indexBy(users, 'id');
        expect(byId.u1.email).toBe('a@example.com');
        expect(byId.u2.role).toBe('admin');
    });

    it('groupBy groups by a key', () => {
        const grouped = groupBy(jobs, 'status');
        expect(grouped.open).toHaveLength(1);
        expect(grouped.open[0].title).toBe('TS Engineer');
    });

    it('mergeById merges collections by id, preferring incoming items', () => {
        const updated: Job[] = [
            { id: 2, title: 'Senior Python Engineer', status: 'open' },
            { id: 3, title: 'Go Engineer', status: 'open' },
        ];

        const merged = mergeById(jobs, updated, 'id');
        // Note: order might vary depending on impl (Object.values), but for small sets usually insertion order in JS engines
        // Let's sort to be safe if checking array equality, or just check contents
        const byId = indexBy(merged, 'id');

        expect(Object.keys(byId).sort()).toEqual(['1', '2', '3']);
        expect(byId[2].title).toBe('Senior Python Engineer');
        expect(byId[2].status).toBe('open');
    });

    it('ensureUnique drops duplicates by key, keeping last occurrence', () => {
        const noisy: User[] = [
            { id: 'u1', email: 'old@example.com', role: 'user' },
            { id: 'u1', email: 'new@example.com', role: 'admin' },
        ];

        const unique = ensureUnique(noisy, 'id');
        expect(unique).toHaveLength(1);
        expect(unique[0].email).toBe('new@example.com');
        expect(unique[0].role).toBe('admin');
    });
});
