export type FXType = 'confetti' | 'glitch' | 'shockwave';

export type FXPayload = {
    confetti: { x?: number; y?: number; count?: number };
    glitch: { intensity: 'low' | 'high' };
    shockwave: { x: number; y: number };
};

type FXCallback = <T extends FXType>(type: T, payload: FXPayload[T]) => void;

class FXBus {
    private listeners = new Set<FXCallback>();

    subscribe(callback: FXCallback) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    emit<T extends FXType>(type: T, payload: FXPayload[T]) {
        this.listeners.forEach((cb) => cb(type, payload));
    }
}

export const FX = new FXBus();
