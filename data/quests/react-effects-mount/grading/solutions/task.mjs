import React, { useEffect } from 'react';

export function LifecycleLogger({ onMount, onUnmount }) {
    useEffect(() => {
        onMount();
        return () => onUnmount();
    }, []); // Empty dependency array for mount/unmount only
    return null;
}
