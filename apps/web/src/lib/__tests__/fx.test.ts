import { describe, it, expect, vi } from 'vitest';
import { FX } from '../fx';

describe('FXBus', () => {
    it('notifies subscribers when an event is emitted', () => {
        const handler = vi.fn();

        const unsubscribe = FX.subscribe(handler);

        FX.emit('confetti', { count: 42, x: 0.3, y: 0.7 });

        expect(handler).toHaveBeenCalledTimes(1);
        expect(handler).toHaveBeenCalledWith(
            'confetti',
            expect.objectContaining({ count: 42, x: 0.3, y: 0.7 })
        );

        // cleanup
        unsubscribe();
    });

    it('stops notifying after unsubscribe', () => {
        const handler = vi.fn();

        const unsubscribe = FX.subscribe(handler);

        FX.emit('confetti', { count: 10 });
        unsubscribe();
        FX.emit('confetti', { count: 99 });

        // Only first emit should be seen
        expect(handler).toHaveBeenCalledTimes(1);
        expect(handler).toHaveBeenCalledWith(
            'confetti',
            expect.objectContaining({ count: 10 })
        );
    });
});
