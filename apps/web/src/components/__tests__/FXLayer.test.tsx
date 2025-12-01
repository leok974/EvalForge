import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { FXLayer } from '../FXLayer';
import { FX } from '../../lib/fx';

// --- Mocks ---

// Use vi.hoisted for the confetti mock to avoid hoisting issues
const { confettiMock } = vi.hoisted(() => ({
    confettiMock: vi.fn(),
}));

// 1) Mock settings store (crtMode + screenShake etc.)
vi.mock('../../store/settingsStore', () => ({
    useSettingsStore: () => ({
        crtMode: true,
        screenShake: false,
        particles: true,
    }),
}));

// 2) Mock game store (layout theme)
vi.mock('../../store/gameStore', () => ({
    useGameStore: (selector: any) =>
        selector({
            layout: 'cyberdeck', // default for our tests
        }),
}));

// 3) Mock game socket so FXLayer sees a sync_complete event
vi.mock('../../hooks/useGameSocket', () => ({
    useGameSocket: () => ({ type: 'sync_complete' }),
}));

// 4) Mock sound hook to avoid loading audio
vi.mock('../../hooks/useSound', () => ({
    useSound: () => ({ play: vi.fn() }),
}));

// 5) Mock canvas-confetti
vi.mock('canvas-confetti', () => ({
    __esModule: true,
    default: confettiMock,
}));

describe('FXLayer', () => {
    beforeEach(() => {
        confettiMock.mockReset();
    });

    it('emits a confetti FX event when a sync_complete game event arrives', async () => {
        const emitSpy = vi.spyOn(FX, 'emit');

        render(
            <FXLayer>
                <div data-testid="content">Hello</div>
            </FXLayer>
        );

        // The bridge effect runs after mount; wait for FX.emit to be called
        await waitFor(() => {
            expect(emitSpy).toHaveBeenCalledWith(
                'confetti',
                expect.objectContaining({ count: 150 })
            );
        });

        emitSpy.mockRestore();
    });

    it('applies CRT aberration class in cyberdeck layout when crtMode is enabled', () => {
        const { container } = render(
            <FXLayer>
                <div data-testid="content">Hello</div>
            </FXLayer>
        );

        // The root element should have the class
        expect((container.firstChild as HTMLElement).className).toContain('crt-aberration');
    });
});
