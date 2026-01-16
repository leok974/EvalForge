import { useState, useEffect } from 'react';

export type Track = {
    id: string;
    title: string;
    order_index: number;
};

export type World = {
    slug: string;
    label: string;
    tracks: Track[];
    bosses: any[];
};

export type UniverseData = {
    worlds: World[];
};

export function useUniverse() {
    const [universe, setUniverse] = useState<UniverseData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/universe')
            .then(res => res.json())
            .then(data => {
                setUniverse(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load universe", err);
                setLoading(false);
            });
    }, []);

    return { universe, loading };
}
