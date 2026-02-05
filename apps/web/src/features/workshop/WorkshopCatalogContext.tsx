import React, { createContext, useContext, useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";

export type NameMode = "lore" | "real";

export interface CatalogWorld {
    world_id: string;
    real_name: string;
    lore_name: string;
    display_name: string; // Original display name (usually mix)
    icon: string;
    quest_count: number;
    order: number;
}

export interface CatalogTrack {
    track_id: string;
    world_id: string;
    real_name: string;
    lore_name: string;
    quest_count: number;
    order_index: number;
}

interface WorkshopCatalogContextType {
    worlds: CatalogWorld[];
    tracks: CatalogTrack[];
    aliases: Record<string, string>; // NEW: Mappings like "fundamentals" -> "python-fundamentals"
    loading: boolean;
    nameMode: NameMode;
    setNameMode: (mode: NameMode) => void;
    toggleNameMode: () => void;

    // Helpers
    resolveWorldName: (w: CatalogWorld | undefined) => string;
    resolveTrackName: (t: CatalogTrack | undefined) => string;
    getTracksForWorld: (worldId: string) => CatalogTrack[];
    resolveCanonicalTrackId: (rawId: string) => string;
}

const WorkshopCatalogContext = createContext<WorkshopCatalogContextType | null>(null);

export const WorkshopCatalogProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { user } = useAuth();

    const [worlds, setWorlds] = useState<CatalogWorld[]>([]);
    const [tracks, setTracks] = useState<CatalogTrack[]>([]);
    const [aliases, setAliases] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(true);

    const [nameMode, setNameModeState] = useState<NameMode>(() => {
        return (window.localStorage.getItem("ef:name_mode") as NameMode) || "lore";
    });

    const setNameMode = (mode: NameMode) => {
        setNameModeState(mode);
        window.localStorage.setItem("ef:name_mode", mode);
    };

    const toggleNameMode = () => setNameMode(nameMode === "lore" ? "real" : "lore");

    useEffect(() => {
        if (!user) {
            setLoading(false);
            return;
        }

        setLoading(true);
        fetch('/api/workshop/catalog')
            .then(res => {
                if (!res.ok) throw new Error("Failed to fetch catalog");
                return res.json();
            })
            .then(data => {
                setWorlds(data.worlds || []);
                setTracks(data.tracks || []);
                setAliases(data.aliases || {});
            })
            .catch(err => console.error("Catalog fetch error:", err))
            .finally(() => setLoading(false));
    }, [user]);

    const resolveWorldName = (w: CatalogWorld | undefined) => {
        if (!w) return "Unknown World";
        return nameMode === "lore" ? w.lore_name : w.real_name;
    };

    const resolveTrackName = (t: CatalogTrack | undefined) => {
        if (!t) return "Unknown Track";
        return nameMode === "lore" ? t.lore_name : t.real_name;
    };

    const getTracksForWorld = (worldId: string) => {
        return tracks.filter(t => t.world_id === worldId).sort((a, b) => a.order_index - b.order_index);
    };

    const resolveCanonicalTrackId = (rawId: string) => {
        return aliases[rawId] || rawId;
    };

    return (
        <WorkshopCatalogContext.Provider value={{
            worlds,
            tracks,
            aliases,
            loading,
            nameMode,
            setNameMode,
            toggleNameMode,
            resolveWorldName,
            resolveTrackName,
            getTracksForWorld,
            resolveCanonicalTrackId
        }}>
            {children}
        </WorkshopCatalogContext.Provider>
    );
};

export const useWorkshopCatalog = () => {
    const ctx = useContext(WorkshopCatalogContext);
    if (!ctx) throw new Error("useWorkshopCatalog must be used within WorkshopCatalogProvider");
    return ctx;
};
