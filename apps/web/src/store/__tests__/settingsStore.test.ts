import { describe, it, expect, beforeEach } from 'vitest';
import { useSettingsStore } from '../settingsStore';

describe('Settings Store', () => {
    beforeEach(() => {
        useSettingsStore.setState({
            masterVolume: 0.5,
            sfxVolume: 0.8,
            uiVolume: 0.3,
            muted: false,
            crtMode: false,
            screenShake: true,
            particles: true
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

        store.toggleVisual('crtMode');
        expect(useSettingsStore.getState().crtMode).toBe(true); // Toggled On

        store.toggleVisual('screenShake');
        expect(useSettingsStore.getState().screenShake).toBe(false); // Toggled Off
    });
});
