import { CyberdeckTopHud } from "../components/layouts/CyberdeckTopHud";
import { OrionMap } from "./OrionMap";
import { useArcadeHudState } from "@/hooks/useArcadeHudState";
import { useCurriculumState } from "@/hooks/useCurriculumState";
import { useGameStore } from "@/store/gameStore";

export function OrionLayout() {
    const hud = useArcadeHudState();
    const {
        activeWorldId,
        setActiveWorldId,
        activeTrack,
        setActiveTrackById,
    } = useCurriculumState();
    const { setLayout } = useGameStore();

    return (
        <div className="flex h-screen flex-col bg-[#020617] text-slate-50">
            <CyberdeckTopHud
                level={hud.level ?? 1}
                xp={hud.xp ?? 0}
                xpToNext={hud.xpToNext ?? 100}
                systemIntegrity={hud.systemIntegrity ?? 98}
                activeQuest={activeTrack?.title ?? ""}
                worldLabel={activeWorldId.replace("world-", "").toUpperCase()}
                latencyMs={hud.latencyMs ?? null}
                secure={hud.secure ?? true}
                online={hud.online ?? true}
            />

            <div className="flex flex-1 flex-col">
                <div className="relative flex-1 overflow-hidden">
                    <OrionMap
                        activeWorldId={activeWorldId ?? "world-python"}
                        onWorldChange={setActiveWorldId}
                        onTrackSelected={(id) => setActiveTrackById(id)}
                    />
                </div>

                {/* Bridge console bar (reuse existing console, collapsed) */}
                <div className="border-t border-cyan-400/30 bg-slate-950/95 px-4 py-2 flex items-center justify-between">
                    <div className="text-[10px] font-mono text-slate-400 tracking-wider">
                        ACTIVE TRACK: <span className="text-cyan-300">{activeTrack?.title || "NONE"}</span>
                        {activeTrack && ` – progress ${activeTrack.progress}%`}
                    </div>
                    {activeTrack && (
                        <button
                            onClick={() => setLayout("cyberdeck")}
                            className="text-[10px] text-cyan-400 hover:text-cyan-200 tracking-widest border border-cyan-900 px-2 py-1 rounded bg-cyan-950/30"
                        >
                            [OPEN IN CYBERDECK]
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
