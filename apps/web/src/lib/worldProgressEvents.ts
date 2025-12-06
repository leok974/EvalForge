// Simple pub/sub for world progress updates

export type WorldProgressEvent = {
    type: 'world-progress-updated';
    trackSlug?: string;
};

type Listener = (event: WorldProgressEvent) => void;

const listeners = new Set<Listener>();

export function subscribeWorldProgress(
    listener: Listener
): () => void {
    listeners.add(listener);
    return () => {
        listeners.delete(listener);
    };
}

export function emitWorldProgressUpdated(event: WorldProgressEvent) {
    for (const listener of listeners) {
        listener(event);
    }
}
