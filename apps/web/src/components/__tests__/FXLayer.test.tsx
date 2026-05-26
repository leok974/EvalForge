// Sprint 22: crtMode and layout mock removed — Cyberdeck deleted, Workshop is the only layout.
// CRT aberration test removed — CRT overlay is gone.
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import { FXLayer } from '../FXLayer';
import { FX } from '../../lib/fx';

// --- Mocks ---

// Use vi.hoisted for the confetti mock to avoid hoisting issues
const { confettiMock } = vi.hoisted(() => ({
    confettiMock: vi.fn(),
}));

// 1) Mock settings store (screenShake only — crtMode removed Sprint 22)
vi.mock('../../store/settingsStore', () => ({
    useSettingsStore: () => ({
        screenShake: false,
        particles: true,
    }),
}));

// 2) Mock game socket so FXLayer sees a sync_complete event via lastEvent
vi.mock('../../hooks/useGameSocket', () => ({
    useGameSocket: () => ({ lastEvent: { type: 'sync_complete' } }),
}));

// 3) Mock sound hook to avoid loading audio
vi.mock('../../hooks/useSound', () => ({
    useSound: () => ({ play: vi.fn() }),
}));

// 4) Mock canvas-confetti
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

    it('renders children inside the Workshop layout container', () => {
        const { getByTestId } = render(
            <FXLayer>
                <div data-testid="content">Hello</div>
            </FXLayer>
        );
        expect(getByTestId('content')).toBeDefined();
    });
});
