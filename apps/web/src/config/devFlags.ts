/**
 * Centralized dev feature flags
 * 
 * This module consolidates all "unlock all" / "god mode" environment variables
 * into a single source of truth. Tests can override these easily by mocking
 * import.meta.env in setupTests.ts.
 */

/**
 * Check if god mode (unlock all features) is enabled via environment variables.
 * 
 * God mode can be enabled by any of these env vars being set to '1' or 'true':
 * - VITE_DEV_UNLOCK_ALL
 * - VITE_UNLOCK_ALL
 * - VITE_LAYOUT_UNLOCK_ALL
 * 
 * @returns true if any god mode flag is set, false otherwise
 */
export function isGodModeEnabledFromEnv(): boolean {
    const env = import.meta.env;

    const devUnlock =
        env.VITE_DEV_UNLOCK_ALL === '1' || env.VITE_DEV_UNLOCK_ALL === 'true';
    const unlockAll =
        env.VITE_UNLOCK_ALL === '1' || env.VITE_UNLOCK_ALL === 'true';
    const layoutUnlock =
        env.VITE_LAYOUT_UNLOCK_ALL === '1' ||
        env.VITE_LAYOUT_UNLOCK_ALL === 'true';

    return devUnlock || unlockAll || layoutUnlock;
}
