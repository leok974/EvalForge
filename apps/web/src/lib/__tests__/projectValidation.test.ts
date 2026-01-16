import { describe, it, expect } from 'vitest';
import { resolveSelectedProject, MinimalTrack, MinimalUniverse } from '../projectValidation';

describe('resolveSelectedProject logic', () => {
    it('returns null if no active track', () => {
        const universe = { worlds: [] };
        expect(resolveSelectedProject(null, universe)).toBeNull();
    });

    it('returns valid track if found in universe', () => {
        const track = { worldSlug: 'world-python', trackSlug: 'foundry-io' };
        const universe: MinimalUniverse = {
            worlds: [
                {
                    slug: 'world-python',
                    tracks: [{ id: 'foundry-io' }]
                }
            ]
        };
        expect(resolveSelectedProject(track, universe)).toEqual(track);
    });

    it('returns null (clears) if world not found', () => {
        const track = { worldSlug: 'world-java', trackSlug: 'reactor' };
        const universe: MinimalUniverse = {
            worlds: [
                {
                    slug: 'world-python',
                    tracks: [{ id: 'foundry-io' }]
                }
            ]
        };
        expect(resolveSelectedProject(track, universe)).toBeNull();
    });

    it('returns null (clears) if track not found in world', () => {
        const track = { worldSlug: 'world-python', trackSlug: 'missing-track' };
        const universe: MinimalUniverse = {
            worlds: [
                {
                    slug: 'world-python',
                    tracks: [{ id: 'foundry-io' }]
                }
            ]
        };
        expect(resolveSelectedProject(track, universe)).toBeNull();
    });
});
