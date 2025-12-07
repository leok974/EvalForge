import { vi } from 'vitest';

/**
 * Stubs the global fetch API with a neutral implementation.
 * Use inside beforeEach().
 */
export function stubGlobalFetch() {
    const fetchMock = vi.fn((url: string | Request | URL) => {
        return Promise.resolve({
            ok: true,
            json: async () => ({}),
            text: async () => "",
        } as Response);
    });
    vi.stubGlobal('fetch', fetchMock);
    return fetchMock;
}

/**
 * Mocks the game socket to simulate an idle connected state.
 * Useful for component tests that don't need real socket interactions.
 */
export function mockGameSocketIdle() {
    vi.mock('../../hooks/useGameSocket', () => ({
        useGameSocket: () => ({ status: 'idle', send: vi.fn(), lastMessage: null }),
    }));
}

/**
 * Mocks the game store with specific partial state.
 * This preserves the store structure while allowing overrides.
 */
export function mockGameStoreState(partial: Record<string, any>) {
    vi.mock('../../store/gameStore', () => {
        // We can't use importActual easily inside factory, so we rely on a simplified mock
        // or a manual partial implementation if needed.
        // For now, we return a factory that produces a state with overrides.
        return {
            useGameStore: (selector: any) => {
                const defaultState = {
                    layout: 'workshop',
                    activeTrack: null,
                    bossesUnlocked: [],
                    xp: 0,
                    level: 1,
                    integrity: 100,
                    setLayout: vi.fn(),
                    addXp: vi.fn(),
                };
                const state = { ...defaultState, ...partial };
                return selector ? selector(state) : state;
            }
        };
    });
}
