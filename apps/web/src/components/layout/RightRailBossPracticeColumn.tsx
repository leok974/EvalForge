import React from "react";
import { PracticeGauntletCard } from "../practice/PracticeGauntletCard";

/**
 * Reusable right-rail column with Boss + Practice + Codex pattern.
 * 
 * This ensures Workshop, Orion, and Cyberdeck all have the same
 * practice-oriented sidebar without duplicating layout code.
 */
export const RightRailBossPracticeColumn: React.FC<{
    /** Optional mode hint for Practice Gauntlet filtering */
    mode?: "default" | "boss" | "world";
    /** Optional: include boss HUD */
    showBossHud?: boolean;
    /** Optional: include codex shelf */
    showCodex?: boolean;
}> = ({
    mode = "default",
    showBossHud = true,
    showCodex = true,
}) => {
        return (
            <section className="flex flex-col gap-4">
                {/* Boss HUD placeholder - to be wired up when BossHudCard exists */}
                {showBossHud && (
                    <div
                        className="rounded-2xl border border-red-500/60 bg-slate-950/90 p-4"
                        data-testid="boss-hud-placeholder"
                    >
                        <div className="text-xs font-semibold uppercase tracking-wide text-red-200">
                            Boss HUD
                        </div>
                        <p className="mt-1 text-xs text-slate-400">
                            Boss HP, Integrity, Combat Status
                        </p>
                    </div>
                )}

                {/* Practice Gauntlet */}
                <PracticeGauntletCard />

                {/* Codex Shelf placeholder - to be wired up when CodexShelfCard exists */}
                {showCodex && (
                    <div
                        className="rounded-2xl border border-indigo-500/60 bg-slate-950/90 p-4"
                        data-testid="codex-shelf-placeholder"
                    >
                        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-200">
                            Codex Shelf
                        </div>
                        <p className="mt-1 text-xs text-slate-400">
                            Boss Guides • Project Docs
                        </p>
                    </div>
                )}
            </section>
        );
    };
