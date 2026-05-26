// Sprint 22: crtMode removed from settingsStore — Cyberdeck layout deleted.
import { describe, it, expect, beforeEach } from 'vitest';
import { useSettingsStore } from '../settingsStore';

describe('Settings Store', () => {
    beforeEach(() => {
        useSettingsStore.setState({
            masterVolume: 0.5,
            sfxVolume: 0.8,
            uiVolume: 0.3,
            muted: false,
            screenShake: true,
            particles: true,
            worldViewMode: 'grid',
        });
    });

    it('updates volume levels', () => {
        const store = useSettingsStore.getState();
        store.setVolume('master', 1.0);
        expect(useSettingsStore.getState().masterVolume).toBe(1.0);

        store.setVolume('ui', 0.0);
        expect(useSettingsStore.getState().uiVolume).toBe(0.0);
    });

    it('toggles mute', () => {
        const store = useSettingsStore.getState();
        expect(store.muted).toBe(false);

        store.toggleMute();
        expect(useSettingsStore.getState().muted).toBe(true);
    });

    it('toggles visual effects', () => {
        const store = useSettingsStore.getState();

        store.toggleVisual('screenShake');
        expect(useSettingsStore.getState().screenShake).toBe(false); // Toggled Off

        store.toggleVisual('particles');
        expect(useSettingsStore.getState().particles).toBe(false); // Toggled Off
    });

    it('sets worldViewMode', () => {
        const store = useSettingsStore.getState();
        store.setWorldViewMode('map');
        expect(useSettingsStore.getState().worldViewMode).toBe('map');

        store.setWorldViewMode('grid');
        expect(useSettingsStore.getState().worldViewMode).toBe('grid');
    });
});
