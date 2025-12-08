import { renderWithRouter } from '@/test/testUtils';
import { WorkshopLayout } from '../WorkshopLayout';
import { screen, waitFor } from '@testing-library/react';
import { vi, test, expect } from 'vitest';
import * as useGameStoreModule from '@/hooks/useGameStore';

// Mock API
vi.stubGlobal('fetch', vi.fn((url: string) => {
    if (url.includes('/api/universe')) {
        return Promise.resolve({
            ok: true,
            json: () => Promise.resolve({
                worlds: [{
                    slug: 'world-java',
                    tracks: [{
                        id: 'reactor-core-circuit',
                        slug: 'core-circuit',
                        title: 'T1: Core Circuit',
                        quests: [{
                            id: 'java-core-q1-first-spark',
                            slug: 'first-spark',
                            title: 'Q1 – First Spark'
                        }]
                    }]
                }]
            })
        });
    }
    return Promise.resolve({ ok: false });
}));

test('renders Java Quest in Workshop', async () => {
    // Setup Store Mock
    const setActiveWorldSlug = vi.fn();
    const setActiveTrackId = vi.fn();

    // @ts-ignore
    vi.spyOn(useGameStoreModule, 'useGameStore').mockReturnValue({
        activeWorldSlug: 'world-java',
        activeTrackId: 'reactor-core-circuit',
        setActiveWorldSlug,
        setActiveTrackId,
        activeBossSlug: null,
        layout: { rightPanelExpanded: false }
    });

    renderWithRouter(
        <WorkshopLayout />,
        { route: '/worlds/world-java/quests/java-core-q1-first-spark' }
    );

    await waitFor(() => {
        expect(screen.getByText('Q1 – First Spark')).toBeInTheDocument();
    });
});
