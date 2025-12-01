import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useSound } from '../useSound';
import { useSettingsStore } from '../../store/settingsStore';
import { useGameStore } from '../../store/gameStore';

// Mock Howler class
const mockPlay = vi.fn();
const mockVolume = vi.fn();
const mockUnload = vi.fn();

vi.mock('howler', () => {
    return {
        Howl: class {
            play = mockPlay;
            volume = mockVolume;
            unload = mockUnload;
            constructor() {
                // Constructor logic if needed
            }
        }
    };
});

describe('useSound Hook', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useSettingsStore.setState({
            masterVolume: 0.5,
            uiVolume: 0.5,
            sfxVolume: 1.0,
            muted: false
        });
        useGameStore.setState({
            layout: 'cyberdeck'
        });
    });

    it('plays sound with calculated volume', () => {
        const { result } = renderHook(() => useSound());

        // Play UI sound
        result.current.play('click');

        // Verify play called
        expect(mockPlay).toHaveBeenCalled();

        // Verify Volume Math: Master(0.5) * UI(0.5) = 0.25
        expect(mockVolume).toHaveBeenCalledWith(0.25);
    });

    it('does not play when muted', () => {
        useSettingsStore.setState({ muted: true });

        const { result } = renderHook(() => useSound());
        result.current.play('click');

        expect(mockPlay).not.toHaveBeenCalled();
    });

    it('calculates SFX volume correctly', () => {
        const { result } = renderHook(() => useSound());

        // Play SFX sound
        result.current.play('boss');

        // Verify Volume Math: Master(0.5) * SFX(1.0) = 0.5
        expect(mockVolume).toHaveBeenCalledWith(0.5);
    });
});
