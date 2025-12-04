import { test, expect } from '@playwright/test';

test.describe('Practice Gauntlet API (Daily Practice Rounds)', () => {
    test('returns a valid DailyPracticePlan shape', async ({ request }) => {
        const response = await request.get('/api/practice_rounds/today');

        // If you expect auth in non-mock mode, you can temporarily
        // log this to debug:
        // console.log('Status:', response.status(), await response.text());

        expect(response.ok()).toBeTruthy();

        const body = await response.json();

        // Basic top-level shape
        expect(typeof body).toBe('object');
        expect(typeof body.date).toBe('string');
        expect(typeof body.label).toBe('string');
        expect(Array.isArray(body.items)).toBe(true);

        // Optional fields
        if (body.completed_count !== undefined) {
            expect(typeof body.completed_count).toBe('number');
        }
        if (body.total_count !== undefined) {
            expect(typeof body.total_count).toBe('number');
        }
        if (body.streak_days !== undefined && body.streak_days !== null) {
            expect(typeof body.streak_days).toBe('number');
        }

        // Validate at least the first item shape if any exist
        if (body.items.length > 0) {
            const item = body.items[0];

            expect(typeof item.id).toBe('string');
            expect(['quest_review', 'boss_review', 'project_maintenance']).toContain(
                item.item_type
            );
            expect(typeof item.label).toBe('string');
            expect(typeof item.description).toBe('string');

            if (item.world_slug !== null && item.world_slug !== undefined) {
                expect(typeof item.world_slug).toBe('string');
            }
            if (item.project_slug !== null && item.project_slug !== undefined) {
                expect(typeof item.project_slug).toBe('string');
            }

            expect(['easy', 'medium', 'hard']).toContain(item.difficulty);
            expect(typeof item.rationale).toBe('string');
            expect(typeof item.struggle_score).toBe('number');
        }
    });

    test('is deterministic for the same user and date', async ({ request }) => {
        // First call
        const res1 = await request.get('/api/practice_rounds/today');
        expect(res1.ok()).toBeTruthy();
        const body1 = await res1.json();

        // Second call
        const res2 = await request.get('/api/practice_rounds/today');
        expect(res2.ok()).toBeTruthy();
        const body2 = await res2.json();

        // Same date
        expect(body1.date).toBe(body2.date);

        // Same item IDs and order (deterministic for profile+date)
        const ids1 = body1.items.map((i: any) => i.id);
        const ids2 = body2.items.map((i: any) => i.id);

        expect(ids1).toEqual(ids2);
    });
});
