import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/react';
import { ConfettiManager } from '../ConfettiManager';
import { FX } from '../../../lib/fx';

// Mock for canvas-confetti and settings store using vi.hoisted
const { confettiMock, useSettingsStoreMock } = vi.hoisted(() => {
    return {
        confettiMock: vi.fn(),
        useSettingsStoreMock: vi.fn(),
    };
});

vi.mock('canvas-confetti', () => ({
    __esModule: true,
    default: confettiMock,
}));

vi.mock('../../../store/settingsStore', () => ({
    useSettingsStore: () => useSettingsStoreMock(),
}));

describe('ConfettiManager', () => {
    beforeEach(() => {
        confettiMock.mockReset();
        useSettingsStoreMock.mockReset();
    });

    it('fires confetti when FX emits and particles are enabled', () => {
        // Particles ON
        useSettingsStoreMock.mockReturnValue({ particles: true });

        render(<ConfettiManager />);

        // Emit an FX event
        FX.emit('confetti', { count: 123, x: 0.1, y: 0.9 });

        expect(confettiMock).toHaveBeenCalledTimes(1);
        expect(confettiMock).toHaveBeenCalledWith(
            expect.objectContaining({
                particleCount: 123,
                origin: { x: 0.1, y: 0.9 },
            })
        );
    });

    it('does not fire confetti when particles are disabled', () => {
        // Particles OFF
        useSettingsStoreMock.mockReturnValue({ particles: false });

        render(<ConfettiManager />);

        FX.emit('confetti', { count: 50 });

        expect(confettiMock).not.toHaveBeenCalled();
    });
});
