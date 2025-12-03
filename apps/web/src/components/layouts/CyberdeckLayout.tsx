import React from "react";
import { CyberdeckTopHud } from "./CyberdeckTopHud";
import { useArcadeHudState } from "@/hooks/useArcadeHudState";
import { NetworkPanel } from "@/components/hud/NetworkPanel";
import { EventLog as EventFeed } from "@/components/hud/EventLog";
import { ProjectPayloadPanel } from "@/components/hud/ProjectPayloadPanel";
import { CodexStrip } from "@/components/hud/CodexStrip";
import { RepoStatusPanel } from "@/components/hud/RepoStatusPanel";
import { TerminalFrame } from "./TerminalFrame";

export function CyberdeckLayout({ children }: { children: React.ReactNode }) {
    const hud = useArcadeHudState();

    return (
        <div className="flex h-screen flex-col bg-[#020617] text-slate-50 font-sans overflow-hidden">
            <CyberdeckTopHud
                level={hud.level}
                xp={hud.xp}
                xpToNext={hud.xpToNext}
                systemIntegrity={hud.systemIntegrity}
                activeQuest={hud.activeQuestTitle || ""}
                worldLabel={hud.worldLabel}
                latencyMs={hud.latencyMs}
                secure={hud.secure}
                online={hud.online}
            />

            {/* Main Grid Layout */}
            <div className="flex-1 grid grid-cols-[minmax(220px,260px)_minmax(0,1fr)_minmax(240px,280px)] gap-4 p-4 overflow-hidden">

                {/* LEFT COLUMN */}
                <div className="flex flex-col gap-4 overflow-y-auto">
                    <NetworkPanel />
                    <EventFeed />
                </div>

                {/* CENTER COLUMN (Terminal) */}
                <div className="relative flex flex-col">
                    <TerminalFrame>
                        {children}
                    </TerminalFrame>
                </div>

                {/* RIGHT COLUMN */}
                <div className="flex flex-col gap-4 overflow-y-auto">
                    <ProjectPayloadPanel />
                    <CodexStrip />
                    <RepoStatusPanel />
                </div>

            </div>
        </div>
    );
}
