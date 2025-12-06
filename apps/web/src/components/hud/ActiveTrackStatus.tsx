import { useGameStore } from '@/store/gameStore';

export function ActiveTrackStatus() {
    const activeTrack = useGameStore((s) => s.activeTrack);

    const label = activeTrack?.label ?? 'NONE';

    return (
        <div className="text-[10px] uppercase tracking-[0.24em] text-cyan-300/80">
            Active Track: <span className="text-cyan-100">{label}</span>
        </div>
    );
}
