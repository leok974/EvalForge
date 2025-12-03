import { useCurriculumStore } from "../store/curriculumStore";

export function useCurriculumState() {
    const {
        activeWorldId,
        setActiveWorldId,
        activeTrackId,
        setActiveTrackById,
        tracks
    } = useCurriculumStore();

    const activeTrack = tracks.find(t => t.id === activeTrackId) || null;

    return {
        activeWorldId,
        setActiveWorldId,
        activeTrack,
        setActiveTrackById,
        tracks
    };
}
