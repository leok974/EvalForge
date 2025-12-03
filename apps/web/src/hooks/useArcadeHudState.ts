import { useGameStore } from "@/store/gameStore";
import { useBossStore } from "@/store/bossStore";
// import { useProjectsStore } from "@/store/projectsStore"; // If we had one, or use a query

export function useArcadeHudState() {
    const gameState = useGameStore();
    const bossState = useBossStore();

    // Calculate XP to next level (simple formula from gameStore: level * 1000)
    const xpToNext = gameState.level * 1000;

    return {
        level: gameState.level,
        xp: gameState.xp,
        xpToNext,
        systemIntegrity: gameState.integrity,
        activeQuestTitle: gameState.activeQuestId ? `QUEST: ${gameState.activeQuestId}` : null,
        worldLabel: "PYTHON WORLD – APPLYLENS BACKEND", // Placeholder until we have real world state
        latencyMs: 45, // Placeholder
        secure: true, // Placeholder
        online: true, // Placeholder

        // Boss state for alerts
        bossActive: bossState.status === 'active',
        bossName: bossState.bossName,
    };
}
